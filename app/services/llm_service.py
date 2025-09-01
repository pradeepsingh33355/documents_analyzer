import os
from openai import OpenAI

client = OpenAI()


async def correct_text_with_llm(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Correct grammar and typos."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content
