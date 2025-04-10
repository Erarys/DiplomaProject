from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_tone_instruction(face_emotion, voice_emotion):
    if face_emotion in ['angry', 'sad'] or voice_emotion in ['angry', 'sad']:
        return f"{face_emotion} эмоция в голосе: {voice_emotion}"
    elif face_emotion in ['positive', 'other', 'neutral'] or voice_emotion in ['positive', 'other', 'neutral']:
        return f"{face_emotion} эмоция в голосе: {voice_emotion}"
    else:
        return f"{face_emotion} эмоция в голосе: {voice_emotion}"

message_ls = [
    {
        "role": "system",
        "content": "Ты должен помочь человек в контроле эмоций и актерского мастерства, если он этого попросит и оцений его старание, если человек выразил похожую на то что нужно эмоцию похвали, если нет то дай совета. Если человек попросил помочь с изуением языка тоже помоги. Ответь на том языке на котором написан текст сообщения (текст)"
    }
]

def generate_answer(message: str, face_emotion: str, voice_emotion: str) -> str:
    client = OpenAI()

    tone_instruction = get_tone_instruction(face_emotion, voice_emotion)

    full_message = (
        f"Текст сообщения: ({message})\n"
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
