import io
import wave
import numpy as np
import pyaudio


def record_audio():
    activity = []

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    THRESHOLD = 500
    SILENCE_DURATION = 2  # Количество секунд тишины перед завершением записи

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    silence_counter = 0  # Счётчик длительности тишины

    print("Recording...")

    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        frames.append(data)

        if  np.max(np.abs(audio_data)) > THRESHOLD:
            activity.append(np.max(np.abs(audio_data)))


        # Проверяем, превышает ли амплитуда порог
        if np.max(np.abs(audio_data)) > THRESHOLD:
            silence_counter = 0  # Если речь, сбрасываем счётчик тишины
        else:
            silence_counter += 1

        print("activity ----", len(activity))
        print("second", silence_counter)
        if len(activity) > (RATE / CHUNK) * SILENCE_DURATION:
            if silence_counter > (RATE / CHUNK) * SILENCE_DURATION:
                break


    stream.stop_stream()
    stream.close()
    p.terminate()

    # Сохраняем аудио в формате WAV
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    wav_buffer.seek(0)

    with wave.open("file.wav", 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    wav_buffer.seek(0)

    # Назначаем имя файла
    wav_buffer.name = "speech.wav"

    return wav_buffer
