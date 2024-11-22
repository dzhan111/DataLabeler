from fastapi import FastAPI, File, Response, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import os
import uuid
import random
import httpx, asyncio
from contextlib import asynccontextmanager

from src.agg import aggregate
from src.image_utils import convert_to_jpeg
from src.clients import LEMONFOX_CLIENT, SUPABASE_CLIENT, MEGA_CLIENT
from src.qc import passes_quality_check, get_keywords

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Setup background tasks"""
    asyncio.create_task(keep_alive())
    yield

async def keep_alive():
    """Keep the server alive"""
    while True:
        try:
            async with httpx.AsyncClient() as client:
                await client.get("https://datalabeler.onrender.com/")
        except Exception as e:
            print(e)
        await asyncio.sleep(600)

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "https://data-labeler-ten.vercel.app"
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/')
async def read_root():
    return JSONResponse(content={
        "message": "Welcome to the DataLabeler API",
        "version": "1.0",
        "documentation": "https://datalabeler.onrender.com/docs"
    })

@app.get("/get_image_task")
async def get_image_task(mturkid: str):
    """Selects a random image without a finished caption and less than 3 transcriptions"""

    already_completed = (SUPABASE_CLIENT
        .table('captions')
        .select('image_id')
        .eq('mturkid', mturkid)
    ).execute().data

    results = (SUPABASE_CLIENT
        .table('images')
        .select('id')
        .not_.in_('id', already_completed)
        .is_('final_caption', None)
        .lt('num_captions', 3)
        .order('id')
        .limit(5)
    ).execute()

    if not results.data:
        raise HTTPException(status_code=204, detail="No tasks available at this time.")
    
    return JSONResponse(content={
        'image_id': random.choice(results.data)['id']
    })
    

@app.get("/get_image/{image_id}")
async def get_image(image_id: str):
    """Endpoint to serve an image file by image_id"""
    file = image_id + '.jpeg'
    file_object = MEGA_CLIENT.find(file)

    if not file_object:
        raise HTTPException(status_code=404, detail="Image not found")
    
    MEGA_CLIENT.download(file_object, dest_path='./', dest_filename=file)
    with open(file, 'rb') as f:
        file_data = f.read()

    os.remove(file)

    return Response(file_data, media_type="image/jpeg")

@app.post("/process_audio/{image_id}")
async def process_audio(image_id: str, mturkid: str, audio_file: UploadFile = File(...)):
    """Accepts an audio caption from an MTurk requester"""
    # transcribe audio
    temp_audio_path = f"./temp_{audio_file.filename}.webm"
    with open(temp_audio_path, "wb") as f:
        f.write(await audio_file.read())
    try:
        caption = LEMONFOX_CLIENT.transcribe(temp_audio_path)
    finally:
        os.remove(temp_audio_path)

    # check quality
    passed, reason = passes_quality_check(caption, image_id)
    if not passed:
        return JSONResponse(content = {
            'accepted': False,
            'payload': reason
        })
    
    # add to captions table (check dupes)
    past_responses = (SUPABASE_CLIENT.table('captions')
                      .select('mturkid', 'image_id')
                      .eq('mturkid', mturkid)
                      .eq('image_id', image_id)).execute().data
    if past_responses:
        return JSONResponse(content = {
            'accepted': False,
            'payload': 'You already completed this task.'
        })

    SUPABASE_CLIENT.table('captions').insert({
        'image_id': image_id,
        'caption': caption,
        'mturkid': mturkid
    }).execute()

    # increment counter in images, check if >= 3 and caption is null, if so, aggregate

    old_count = (SUPABASE_CLIENT.table('images')
                 .select('num_captions')
                 .eq('id', image_id)).execute().data[0]['num_captions']
    response = SUPABASE_CLIENT.table('images').update({
        "num_captions": old_count + 1
    }).eq('id', image_id).execute()

    if response.data[0]['final_caption']:
        return JSONResponse(content = {
            'accepted': False,
            'payload': 'Captions no longer needed for this image.'
        })

    # accept caption, generate code
    confirmation_code = str(uuid.uuid4())
    SUPABASE_CLIENT.table('verification').insert({
        'code': confirmation_code,
        'mturkid': mturkid
    }).execute()

    if response.data[0]['num_captions'] < 3:
        return JSONResponse(content = {
            'accepted': True,
            'payload': confirmation_code
        })

    captions = (SUPABASE_CLIENT
                .table('captions')
                .select('caption')
                .eq('image_id', image_id)).execute().data
    captions = [i['caption'] for i in captions]
    final_caption = aggregate(captions)
    SUPABASE_CLIENT.table('images').update({
        "final_caption": final_caption
    }).eq('id', image_id).execute()

    return JSONResponse(content = {
        'accepted': True,
        'payload': confirmation_code
    })

@app.get("/get_captioned_images")
async def get_captioned_images():
    """Returns a list of paired image_ids and captions"""
    results = (SUPABASE_CLIENT
               .table('images')
               .select('id', 'final_caption')
               .not_.is_('final_caption', None)).execute().data
    return JSONResponse(content = results)

@app.put("/add_image", status_code=200)
async def add_image(admin_key: str, new_image: UploadFile = File(...)):
    """Accepts a new image provided a valid admin key"""

    if not admin_key == os.environ.get('ADMIN_IMAGE_KEY'):
        raise HTTPException(403, detail = 'Insufficient permissions to submit files')

    if not new_image.content_type in ['image/jpeg', 'image/png', 'image/jpg']:
        raise HTTPException(400, detail = 'Unsupported image data provided')
    
    extension = '.png' if new_image.content_type == 'image/png' else '.jpeg'

    temp_path = f"./temp_{new_image.filename}{extension}"
    with open(temp_path, "wb") as f:
        f.write(await new_image.read())

    if extension == '.png':
        temp_path = convert_to_jpeg(temp_path)

    keywords = get_keywords(temp_path)
    
    row = {
        'id': str(uuid.uuid4()),
        'num_captions': 0,
        'final_caption': None,
        'keywords': keywords
    }

    SUPABASE_CLIENT.table('images').upsert(row).execute()

    MEGA_CLIENT.upload(temp_path, dest=None, dest_filename=(row['id'] + '.jpeg'))

    try:
        os.remove(temp_path)
    except OSError as e:
        print(e)

    return row['id']