from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
from pathlib import Path

router = APIRouter()

class FeedbackRequest(BaseModel):
    conversion_id: str
    user_rating: float
    feedback_text: Optional[str] = None

@router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback for conversion quality (for RL learning)."""
    
    # Validate user rating
    if not 1.0 <= feedback.user_rating <= 10.0:
        raise HTTPException(status_code=400, detail="User rating must be between 1.0 and 10.0")
    
    # Store feedback for RL learning
    feedback_data = {
        "conversion_id": feedback.conversion_id,
        "user_rating": feedback.user_rating,
        "feedback_text": feedback.feedback_text,
        "timestamp": str(Path(__file__).parent.parent / "logs" / "feedback.json")
    }
    
    # Log feedback to file
    try:
        log_path = Path(__file__).parent.parent / "logs" / "feedback.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback_data) + "\n")
    except Exception as e:
        print(f"Failed to log feedback: {e}")
    
    return {
        "status": "success",
        "message": "Feedback submitted successfully",
        "conversion_id": feedback.conversion_id
    }