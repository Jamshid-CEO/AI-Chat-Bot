import openai

openai.api_key = "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"

def ask_gpt(user_text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_text}
        ]
    )
    return response['choices'][0]['message']['content']
