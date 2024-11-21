import syspathhack
from clients import SUPABASE_CLIENT, MEGA_CLIENT
import os
import uuid

# add 43 new rows to db
image_files = []
keywords = []
for f in os.listdir('data/dataset/'):
    file = 'data/dataset/' + f
    if file.endswith('.jpeg'):
        image_files.append(file)
        with open(file[:-4] + 'txt', 'r') as kw_file:
            keywords.append(",".join([i[:-1] for i in kw_file.readlines()]))

for im_file, kw in zip(image_files, keywords):

    row = {
        'id': str(uuid.uuid4()),
        'num_captions': 0,
        'final_caption': None,
        'keywords': kw
    }

    SUPABASE_CLIENT.table('images').upsert(row).execute()

    MEGA_CLIENT.upload(im_file, dest=None, dest_filename=(row['id'] + '.jpeg'))