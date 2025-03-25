from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

def get_tone_instruction(face_emotion, voice_emotion):
    if face_emotion in ['angry', 'sad'] or voice_emotion in ['angry', 'sad']:
        return "Отвечай мягко и поддерживающе."
    elif face_emotion in ['positive', 'other', 'neutral'] or voice_emotion in ['positive', 'other', 'neutral']:
        return "Отвечай радостно и позитивно."
    else:
        return "Отвечай спокойно и дружелюбно."

message_ls = [
    {
        "role": "system",
        "content": "Ты — умный и заботливый собеседник."
    }
]

def generate_answer(message: str, face_emotion: str, voice_emotion: str) -> str:
    client = OpenAI()

    tone_instruction = get_tone_instruction(face_emotion, voice_emotion)

    full_message = (
        f"Текст сообщения: {message}\n"
        f"Эмоция лица: {face_emotion}\n"
        f"Эмоция голоса: {voice_emotion}\n"
        f"{tone_instruction}"
    )

    message_ls.append({
        "role": "user",
        "content": full_message,
    })

    response = client.chat.completions.create(
        messages=message_ls,
        model="gpt-4o",
        temperature=0.5,
        max_tokens=150,
    )
    text = response.choices[0].message.content
    return text
