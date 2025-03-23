import torchaudio
import torch
from transformers import HubertForSequenceClassification, Wav2Vec2FeatureExtractor


def voice_emotion_recognition(audio_bytes):
    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/hubert-large-ls960-ft")
    model = HubertForSequenceClassification.from_pretrained("xbgoose/hubert-speech-emotion-recognition-russian-dusha-finetuned")
    num2emotion = {0: 'neutral', 1: 'angry', 2: 'positive', 3: 'sad', 4: 'other'}

    audio_bytes.seek(0)
    audio_bytes.name = "speech.wav"

    # Загружаем аудиофайл с помощью torchaudio
    waveform, sample_rate = torchaudio.load(audio_bytes)

    # Нормализация вручную
    waveform = waveform / waveform.abs().max()

    # Преобразование sample rate
    transform = torchaudio.transforms.Resample(sample_rate, 16000)
    waveform = transform(waveform)

    # Подготовка входных данных для модели
    inputs = feature_extractor(
            waveform,
            sampling_rate=feature_extractor.sampling_rate,
            return_tensors="pt",
            padding=True,
            max_length=16000 * 10,
            truncation=True
        )

    # Прогноз
    logits = model(inputs['input_values'][0]).logits
    predictions = torch.argmax(logits, dim=-1)
    predicted_emotion = num2emotion[predictions.item()]

    return predicted_emotion


