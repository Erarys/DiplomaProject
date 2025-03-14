from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

message_ls = []


def generate_answer(message: str) -> str:
    client = OpenAI()
    message_ls.append({
        "role": "user",
        "content": message,
    })
    response = client.chat.completions.create(
        messages=message_ls,
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=150,
    )
    text = response.choices[0].message.content
    return text


if __name__ == "__main__":
    result = generate_answer("Привет, как дела?:")
    print(result)
