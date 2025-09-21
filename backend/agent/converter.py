
import os
import logging
from agent.models.whisper_stt import transcribe_audio
from agent.models.tts import synthesize_speech
from agent.utils import extract_audio_from_video, convert_audio_to_wav, score_clarity, get_metadata
from agent.rl_agent import get_shared_agent
from pathlib import Path

rl_agent = get_shared_agent()
BASE_DIR = Path(__file__).parent.parent
LOG_PATH = BASE_DIR / "logs" / "conversions.log"

def log_conversion(log_data):
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{log_data}\n")

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
        elif input_type == "video" and output_type == "text":
            if not file_path:
                return {"error": "No video file provided"}
            audio_path = extract_audio_from_video(file_path)
            stt_result = transcribe_audio(audio_path)
            transcript = stt_result.get("text", "")
            result_path = None
            action = "video2text"
        elif input_type == "audio" and output_type == "text":
            if not file_path:
                return {"error": "No audio file provided"}
            # Normalize to wav 16k mono for whisper if input is mp3/m4a etc.
            wav_path = convert_audio_to_wav(file_path)
            stt_result = transcribe_audio(wav_path)
            transcript = stt_result.get("text", "")
            result_path = None
            action = "audio2text"
        elif input_type == "text" and output_type == "audio":
            if not input_text or input_text.strip() == "":
                return {"error": "No text provided"}
            # Let RL choose TTS variant (placeholder actions)
            tts_action = rl_agent.select_action(state, ["tortoise_fast", "gtts"])
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
    # enrich metadata for audio->text with whisper fields
    if input_type == "audio" and output_type == "text":
        if 'duration_sec' not in metadata or metadata['duration_sec'] is None:
            metadata['duration_sec'] = stt_result.get('duration_sec')
        metadata['language'] = stt_result.get('language')
        metadata['method_used'] = stt_result.get('method_used')
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

    # Align with Ashmit's backend schema
    result = {
        "converted_content": content,
        "metadata": {
            "duration": metadata.get("duration_sec", 0),
            "clarity_score": clarity,
            "language": metadata.get("language", "unknown"),
            "method_used": metadata.get("method_used", "unknown"),
            "content_type": input_type,
            "output_type": output_type,
            "file_size": metadata.get("file_size", 0),
            "quality_metrics": {
                "clarity": clarity,
                "confidence": metadata.get("confidence", 0.0)
            }
        },
        "transcript": transcript if output_type == "text" else None,
        "generated_audio": result_path if output_type == "audio" else None,
        "generated_video": result_path if output_type == "video" else None,
        "feedback": {
            "clarity_score": clarity,
            "reward": reward,
            "user_rating": None,  # To be filled by feedback endpoint
            "improvement_suggestions": []
        },
        "rl": {
            "state": state,
            "action": action,
            "exploration_epsilon": rl_agent.exploration_epsilon,
            "learning_rate": rl_agent.learning_rate
        }
    }
    
    return result
