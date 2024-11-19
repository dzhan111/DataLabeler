from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
import os

load_dotenv('.env')

client = Cerebras(
    # This is the default and can be omitted
    api_key = os.environ.get('CEREBRAS_API_KEY'),
)

transcriptions = [
    "And this image we can see why the street in what seems like to be a major city. There are about two inches of snow. We can see in the foreground a person wearing a scarf and walking two dogs, one of which is a bulletproof fever and a slug is in the other dog which is black and gay. There are two pigeons in the background and there seem to be two people for the living background. There are a lot of buildings in the photo, one of which is, has green color to it and the rest of the buildings seem to be beige and brown. There are a lot of trees but none of them have leaves. The weather seems to be overcast in that photo. There seems to be two flash bins and a bunch of benches with snow on them. There are two street lights that seem to be of all style in the photo.",
    "A man is walking down a snowy path in a city. He is walking his two dogs. One of them is small and has a black coat, and the other one is larger and has a golden coat. It may be some sort of golden retriever. There is a pigeon also in the middle of the path, and there is another pigeon on the side near the benches. Along the path are a lot of benches that are all covered with snow. In the background there are trees and buildings, and two other people, along with some trash cans and lamp posts. The person is wearing a scarf, a hat, and a coat, and their feet are covered with snow. There are tall buildings in the background.",
    "There is a man walking two dogs in a city park and it appears to be the middle of winter. One of the dogs is a small and black. The other one is a golden retriever. The person is wearing a grey hat and a scarf around. There knows a black coat, gloves and what appears to be snow pants. The city in the background is very consists of 10 buildings and there are park benches on the right side of the walkway. The ground is covered in snow and there is a pigeon standing in the middle of the walkway. The trees, there are trees in the background which all don't have leaves."
]
joined = "\n".join([f"Caption {i + 1}: {x}\n" for i, x in enumerate(transcriptions)])
message_prompt = f"""Your job is to combine the following 3 image captions into 1 unified description capturing all of the information in each.
Please do your best to keep as many of the details as possible while maintaining consistency of the scene.
Remove phrases and words that do not make sense in the context provided by the responses. Please do not report anything else. Only return the description.
{joined}
Please provide the resulting description in your following message:"""
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": message_prompt
        },
    ],
    model="llama3.1-8b",
    max_tokens=8192,
)
result = chat_completion.choices[0].message.content
print(result)