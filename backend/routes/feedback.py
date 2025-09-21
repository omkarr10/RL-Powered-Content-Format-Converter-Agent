from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from agent.rl_agent import get_shared_agent


router = APIRouter()


def _get_history_path() -> Path:
    # backend/routes -> parents[1] == backend
    return Path(__file__).resolve().parents[1] / "logs" / "rl_history.json"


@router.get("/feedback", response_model=List[Dict[str, Any]])
def get_feedback(limit: int = Query(default=100, ge=1, le=1000)):
    """Return the latest RL feedback records from rl_history.json (newline-delimited JSON)."""
    history_path = _get_history_path()
    if not history_path.exists():
        return []

    try:
        with open(history_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # take last N lines (newest at end), then reverse to newest first
        selected = lines[-limit:][::-1]
        records: List[Dict[str, Any]] = []
        for idx, line in enumerate(selected):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                obj["id"] = idx  # transient id for UI rendering
                records.append(obj)
            except Exception:
                # skip malformed line
                continue
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read feedback: {e}")


@router.post("/feedback")
def post_feedback(payload: Dict[str, Any]):
    """Accept user correctness/score and update the RL agent.

    Payload supports two shapes:
    1) { rl: { state, action }, correct: bool } or { reward: number }
    2) { state, action, correct|reward }
    """
    agent = get_shared_agent()

    rl: Optional[Dict[str, Any]] = payload.get("rl")
    state = payload.get("state") or (rl.get("state") if rl else None)
    action = payload.get("action") or (rl.get("action") if rl else None)
    if not state or not action:
        raise HTTPException(status_code=400, detail="Missing rl state/action")

    if "reward" in payload and isinstance(payload["reward"], (int, float)):
        reward = float(payload["reward"])
    else:
        correct = payload.get("correct")
        if correct is None:
            raise HTTPException(status_code=400, detail="Provide reward or correct")
        reward = 10.0 if bool(correct) else -5.0

    agent.update(state, action, reward)

    return {
        "ok": True,
        "applied_reward": reward,
    }


