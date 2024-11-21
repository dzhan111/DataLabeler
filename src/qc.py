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

class QualityControl:
   
    def __init__(self, image_path, keywords, threshold = MINIMUM_WORDS, kw_threshold = KW_THRESHOLD):
        self.image_path = image_path
        self.threshold = threshold
        self.kw_threshold = kw_threshold

        self.keywords = keywords
        if not self.keywords:
            self.extract_keywords_from_image()

    def extract_keywords_from_image(self):
        """Retrieves keywords from an image using GPT.

        Args:
            None
        Returns:
            The keywords found in the transcription.
        """
        with open(self.image_path, "rb") as image_file:
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
        keywords = response.choices[0].message.content.split(', ')[:10] # enforce 10
        
        self.keywords = keywords

    def count_keywords_in_transcription(self, transcription):
        """Counts the number of keywords present in a transcription.

        Args:
            transcription: The text of the transcription.

        Returns:
            The number of keywords found in the transcription.
        """

        keyword_count = 0
        for keyword in self.keywords:
            if keyword.lower() in transcription.lower(): keyword_count += 1
        return keyword_count
    
    def fits_quality_control(self, transcription):
        """Checks if the transcription qualifies for the respective image.

        Args:
            transcription: The text of the transcription.

        Returns:
            True if it qualifies and False if it doesn't.
        """
        if len(transcription.split(' ')) < self.threshold:
            return False
        if self.count_keywords_in_transcription(transcription) < self.kw_threshold:
            return False
        return True
