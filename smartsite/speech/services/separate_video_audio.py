import ffmpeg
import io

def extract_audio_from_video(video_path):
    out, _ = (
        ffmpeg.input(video_path)
        .output('pipe:', format='wav', acodec='pcm_s16le', ac=1, ar='16000')
        .run(capture_stdout=True, capture_stderr=True)
    )
    return io.BytesIO(out)
