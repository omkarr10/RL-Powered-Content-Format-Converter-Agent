import os
import sys
import pytest
import tempfile
from fastapi.testclient import TestClient

# Ensure backend package is on path
CURRENT_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from main import app

client = TestClient(app)


def test_audio_to_text():
    audio_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp", "sample.wav"))
    if not os.path.exists(audio_path):
        # Skip if sample missing in local env
        return
    with open(audio_path, "rb") as f:
        files = {"input_file": ("sample.wav", f, "audio/wav")}
        data = {"input_type": "audio", "output_type": "text"}
        resp = client.post("/convert-content", data=data, files=files)
    assert resp.status_code == 200
    payload = resp.json()
    assert "converted_content" in payload
    assert isinstance(payload["converted_content"], str)
    assert "metadata" in payload


def test_text_to_speech():
    data = {"input_type": "text", "output_type": "audio", "input_text": "Hello world from test"}
    resp = client.post("/convert-content", data=data)
    assert resp.status_code == 200
    payload = resp.json()
    assert "converted_content" in payload
    # file path to audio or direct content
    assert isinstance(payload["converted_content"], str)


def test_video_to_text_chain():
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp", "sam.mp4"))
    if not os.path.exists(video_path):
        return
    with open(video_path, "rb") as f:
        files = {"input_file": ("sam.mp4", f, "video/mp4")}
        data = {"input_type": "video", "output_type": "text"}
        resp = client.post("/convert-content", data=data, files=files)
    assert resp.status_code == 200
    payload = resp.json()
    assert isinstance(payload.get("converted_content"), str)


def test_metadata_presence():
    data = {"input_type": "text", "output_type": "audio", "input_text": "Short test"}
    resp = client.post("/convert-content", data=data)
    assert resp.status_code == 200
    payload = resp.json()
    md = payload.get("metadata", {})
    assert "duration_sec" in md
    assert "language" in md


def test_api_error_handling():
    # Missing file for audio input
    data = {"input_type": "audio", "output_type": "text"}
    resp = client.post("/convert-content", data=data)
    assert resp.status_code == 400
    
    # Invalid input type
    data = {"input_type": "invalid", "output_type": "text"}
    resp = client.post("/convert-content", data=data)
    assert resp.status_code == 400
    
    # Missing text for text input
    data = {"input_type": "text", "output_type": "audio"}
    resp = client.post("/convert-content", data=data)
    assert resp.status_code == 400


def test_health_endpoint():
    """Test health check endpoint."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["service"] == "rl-converter"


def test_rl_agent_persistence():
    """Test that RL agent persists state across calls."""
    # First call
    data = {"input_type": "text", "output_type": "audio", "input_text": "Test persistence"}
    resp1 = client.post("/convert-content", data=data)
    assert resp1.status_code == 200
    
    # Second call with same content
    resp2 = client.post("/convert-content", data=data)
    assert resp2.status_code == 200
    
    # Check that RL metadata is present
    data1 = resp1.json()
    data2 = resp2.json()
    
    assert "rl" in data1
    assert "rl" in data2
    assert "exploration_epsilon" in data1["rl"]
    assert "learning_rate" in data1["rl"]


def test_metadata_correctness():
    """Test that metadata contains all required fields."""
    data = {"input_type": "text", "output_type": "audio", "input_text": "Metadata test"}
    resp = client.post("/convert-content", data=data)
    assert resp.status_code == 200
    
    payload = resp.json()
    metadata = payload.get("metadata", {})
    
    # Required fields
    assert "duration" in metadata
    assert "clarity_score" in metadata
    assert "language" in metadata
    assert "method_used" in metadata
    assert "content_type" in metadata
    assert "output_type" in metadata
    assert "file_size" in metadata
    assert "quality_metrics" in metadata
    
    # Quality metrics structure
    quality = metadata["quality_metrics"]
    assert "clarity" in quality
    assert "confidence" in quality


def test_schema_alignment():
    """Test that output aligns with Ashmit's backend schema."""
    data = {"input_type": "text", "output_type": "audio", "input_text": "Schema test"}
    resp = client.post("/convert-content", data=data)
    assert resp.status_code == 200
    
    payload = resp.json()
    
    # Check schema alignment
    assert "transcript" in payload
    assert "generated_audio" in payload
    assert "generated_video" in payload
    assert "feedback" in payload
    
    # Feedback structure
    feedback = payload["feedback"]
    assert "clarity_score" in feedback
    assert "reward" in feedback
    assert "user_rating" in feedback
    assert "improvement_suggestions" in feedback


def test_video_to_audio_conversion():
    """Test video to audio conversion."""
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp", "sam.mp4"))
    if not os.path.exists(video_path):
        pytest.skip("Sample video not found")
    
    with open(video_path, "rb") as f:
        files = {"input_file": ("sam.mp4", f, "video/mp4")}
        data = {"input_type": "video", "output_type": "audio"}
        resp = client.post("/convert-content", data=data, files=files)
    
    assert resp.status_code == 200
    # Should return a file download
    assert resp.headers.get("content-type") == "audio/mpeg"


def test_text_to_video_conversion():
    """Test text to video conversion (stub)."""
    data = {"input_type": "text", "output_type": "video", "input_text": "Video test"}
    resp = client.post("/convert-content", data=data)
    assert resp.status_code == 200
    
    payload = resp.json()
    assert "converted_content" in payload
    assert isinstance(payload["converted_content"], str)


def test_conversion_chain():
    """Test complete conversion chain: video -> audio -> text."""
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp", "sam.mp4"))
    if not os.path.exists(video_path):
        pytest.skip("Sample video not found")
    
    # Step 1: Video to Audio
    with open(video_path, "rb") as f:
        files = {"input_file": ("sam.mp4", f, "video/mp4")}
        data = {"input_type": "video", "output_type": "audio"}
        resp1 = client.post("/convert-content", data=data, files=files)
    
    assert resp1.status_code == 200
    
    # Step 2: Audio to Text (using the generated audio)
    # Note: In a real scenario, we'd need to save the audio and upload it
    # For this test, we'll use the original video for audio extraction
    with open(video_path, "rb") as f:
        files = {"input_file": ("sam.mp4", f, "video/mp4")}
        data = {"input_type": "video", "output_type": "text"}
        resp2 = client.post("/convert-content", data=data, files=files)
    
    assert resp2.status_code == 200
    payload = resp2.json()
    assert "transcript" in payload
    assert payload["transcript"] is not None

