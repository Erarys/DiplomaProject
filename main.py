from intelegence.simple import generate_answer
from voice_ai.audio_rec import record_audio
from voice_ai.recognize import recognize_audio
from voice_ai.speach import generate_speach


if __name__ == '__main__':
    audio = record_audio()
    message = recognize_audio(audio)
    print(message)

    answer = generate_answer(message)
    generate_speach(answer)
