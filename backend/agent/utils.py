# Utility functions

import ffmpeg
import os

def convert_audio_to_wav(audio_path):
    wav_path = "temp/converted_audio.wav"
    os.makedirs(os.path.dirname(wav_path), exist_ok=True)
    (
        ffmpeg
        .input(audio_path)
        .output(wav_path, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
        .run(overwrite_output=True)
    )
    return wav_path

def extract_audio_from_video(video_path):
    audio_path = "temp/extracted_audio.wav"
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    (
        ffmpeg
        .input(video_path)
        .output(audio_path, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
        .run(overwrite_output=True)
    )
    return audio_path

def score_clarity(content):
    # Placeholder: always returns 0.95
    return 0.95

def get_metadata(content):
    # Placeholder: returns static metadata
    return {"duration": "00:01:00", "language": "en"}
