import base64

from src.clients import OPENAI_CLIENT, SUPABASE_CLIENT

MINIMUM_WORDS = 80
KW_THRESHOLD = 2

def passes_quality_check(caption: str, image_id: str) -> tuple[bool, str]:

    chunked_caption = [i.strip(' .,!?').lower() for i in caption.split(' ')]

    if len(chunked_caption) < MINIMUM_WORDS:
        return False, "Caption is too short."
    
    chunked_caption = set(chunked_caption)

    wrapped_kws = (SUPABASE_CLIENT
     .table('images')
     .select('keywords')
     .eq('id', image_id)).execute().data
    
    if not wrapped_kws: # no such image
        return False, "Image does not exist."

    keywords = [i.lower() for i in wrapped_kws[0]['keywords'].split(',')]
    
    if len(chunked_caption.intersection(keywords)) < KW_THRESHOLD:
        return False, "Caption is not sufficiently relevant."

    return True, ''

def get_keywords(image_path: str):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

        response = OPENAI_CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": """
                    What’s in this image? Output 10 keywords and only the keywords, nothing else. Comma and space seperated (i.e. hi, x, y...)
                    Each keyword is only one word. Use only concrete nouns (no abstract nouns)
                    """},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"
                    },
                    },
                ],
                }
            ],
            max_tokens=300,
        )

        # Parse the response to get keywords
        return ",".join(response.choices[0].message.content.split(', ')[:10])
