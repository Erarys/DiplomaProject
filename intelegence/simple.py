from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()


def generate_answer(message: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": message,
        }],
        model="gpt-4o-mini",
    )
    text = response.choices[0].message.content
    return text


if __name__ == "__main__":
    result = generate_answer("Привет, как дела?:")
    print(result)
