
import os
import logging
from agent.models.whisper_stt import transcribe_audio
from agent.models.tts import synthesize_speech
from agent.utils import extract_audio_from_video, score_clarity, get_metadata
from agent.rl_agent import RLAgent

rl_agent = RLAgent()
LOG_PATH = "c:/Users/admin/Ins/INTERN/backend/logs/conversions.log"
def log_conversion(data):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(str(data) + "\n")

def extract_tags_metadata(content):
    # Sanika's stub: returns dummy tags
    return {"tags": ["ai", "conversion"], "metadata": {"length": len(str(content))}}

async def convert_content(input_file, input_text, input_type, output_type):
    # Save input file if present
    file_path = None
    transcript = None
    result_path = None
    if input_file:
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{input_file.filename}"
        with open(file_path, "wb") as f:
            f.write(await input_file.read())

    # RL state: content type, length, dummy quality
    state = {
        "content_type": input_type,
        "length": os.path.getsize(file_path) if file_path else len(input_text or ""),
        "quality": 0.5
    }

    # Conversion logic
    try:
        if input_type == "video" and output_type == "audio":
            if not file_path:
                return {"error": "No video file provided"}
            audio_path = extract_audio_from_video(file_path)
            result_path = audio_path
            action = "video2audio"
        elif input_type == "audio" and output_type == "text":
            if not file_path:
                return {"error": "No audio file provided"}
            transcript = transcribe_audio(file_path)
            result_path = None
            action = "audio2text"
        elif input_type == "text" and output_type == "audio":
            if not input_text or input_text.strip() == "":
                return {"error": "No text provided"}
            audio_path = synthesize_speech(input_text.strip())
            result_path = audio_path
            action = "text2audio"
        elif input_type == "text" and output_type == "video":
            if not input_text or input_text.strip() == "":
                return {"error": "No text provided"}
            # Placeholder for text-to-video summary
            transcript = f"[Video summary stub for: {input_text[:100]}...]"
            result_path = None
            action = "text2video"
        else:
            return {"error": "Unsupported conversion"}
    except Exception as e:
        return {"error": str(e)}

    # Metadata and scoring
    content = result_path if result_path else transcript
    metadata = get_metadata(content)
    clarity = score_clarity(content)
    tags_metadata = extract_tags_metadata(content)

    # RL reward: simulated
    reward = clarity * 10
    rl_agent.update(state, action, reward)

    # Logging
    log_data = {
        "input_type": input_type,
        "output_type": output_type,
        "action": action,
        "metadata": metadata,
        "clarity": clarity,
        "reward": reward,
        "tags_metadata": tags_metadata
    }
    log_conversion(log_data)

    return {
        "converted_content": content,
        "metadata": metadata,
        "clarity_score": clarity,
        "reward": reward,
        "tags_metadata": tags_metadata
    }
