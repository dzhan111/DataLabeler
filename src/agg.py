from src.clients import CEREBRAS_CLIENT

def aggregate(captions: list[str]) -> str:
    n = len(captions)
    joined = "\n".join([f"Caption {i + 1}: {x}\n" for i, x in enumerate(captions)])
    message_prompt = f"""Your job is to combine the following {n} image captions into 1 unified description capturing all of the information in each.
    Please do your best to keep as many of the details as possible while maintaining consistency of the scene.
    Remove phrases and words that do not make sense in the context provided by the responses. Please do not report anything else. Only return the description.
    {joined}
    Please provide the resulting description in your following message:"""
    chat_completion = CEREBRAS_CLIENT.chat.completions.create(
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
    return result