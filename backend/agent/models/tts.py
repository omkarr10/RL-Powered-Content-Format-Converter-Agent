# TTS wrapper

from gtts import gTTS
import os

def synthesize_speech(text, lang='en'):
    if not text or text.strip() == "":
        raise ValueError("No text provided for speech synthesis")
    
    try:
        tts = gTTS(text=text.strip(), lang=lang)
        output_path = "temp/tts_output.mp3"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        tts.save(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Text-to-speech failed: {str(e)}")
