from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()


def check_msg(submission: str) :
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)
    with open("ai/system_prompt", "r", encoding="utf-8") as file:
        content = file.read()
    system_prompt = content

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": submission},
        ],
        temperature=0.0,
        max_tokens=400,
    )

    raw_text = resp.choices[0].message.content.strip()
    return raw_text

