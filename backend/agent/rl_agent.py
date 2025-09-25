import json
import os
from pathlib import Path
from typing import Dict, Tuple, List, Union
import random


# Global variable for shared agent instance
_shared_agent: Union[None, 'RLAgent'] = None


class RLAgent:
    """Production-ready Q-learning agent with persistence and adaptive learning.

    State is discretized from input features. Actions are string labels.
    Stores Q-table in-memory and appends transitions to logs/rl_history.json.
    Loads previous Q-table state on initialization for persistence.
    """

    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9, exploration_epsilon: float = 0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_epsilon = exploration_epsilon
        self.q_table: Dict[Tuple[str, str], float] = {}
        base_dir = Path(__file__).parent.parent
        self.log_dir = base_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history_path = self.log_dir / "rl_history.json"
        self.q_table_path = self.log_dir / "q_table.json"
        
        # Load previous Q-table state if exists
        self._load_q_table()
        
        # Track performance metrics for adaptive learning
        self.performance_history = []
        self._load_performance_history()

    def _discretize_state(self, state: Dict) -> str:
        content_type = state.get("content_type", "unknown")
        length = state.get("length", 0)
        quality = state.get("quality", 0.0)

        length_bucket = (
            "short" if length < 1_000_000 else "medium" if length < 10_000_000 else "long"
        )
        quality_bucket = "low" if quality < 0.33 else "mid" if quality < 0.66 else "high"
        return f"{content_type}|{length_bucket}|{quality_bucket}"

    def _q(self, state_key: str, action: str) -> float:
        return self.q_table.get((state_key, action), 0.0)

    def select_action(self, state: Dict, candidate_actions):
        """Epsilon-greedy policy over provided candidate action labels."""
        if not candidate_actions:
            return None

        state_key = self._discretize_state(state)

        if random.random() < self.exploration_epsilon:
            return random.choice(candidate_actions)

        # exploit
        best_action = None
        best_q = float("-inf")
        for action in candidate_actions:
            q_val = self._q(state_key, action)
            if q_val > best_q:
                best_q = q_val
                best_action = action
        return best_action or candidate_actions[0]

    def update(self, state: Dict, action: str, reward: float, next_state: Dict = None, next_actions=None):
        state_key = self._discretize_state(state)
        next_key = self._discretize_state(next_state) if next_state else None

        current_q = self._q(state_key, action)
        if next_state and next_actions:
            next_qs = [self._q(next_key, a) for a in next_actions] if next_actions else [0.0]
            max_next_q = max(next_qs) if next_qs else 0.0
        else:
            max_next_q = 0.0

        target = reward + self.discount_factor * max_next_q
        updated_q = current_q + self.learning_rate * (target - current_q)
        self.q_table[(state_key, action)] = updated_q

        # Track performance for adaptive learning
        self.performance_history.append(reward)
        
        # Adapt parameters based on recent performance
        self._adapt_parameters()
        
        # Save Q-table periodically (every 10 updates)
        if len(self.performance_history) % 10 == 0:
            self._save_q_table()

        self._append_history({
            "state": state,
            "action": action,
            "reward": reward,
            "next_state": next_state,
            "updated_q": updated_q,
            "exploration_epsilon": self.exploration_epsilon,
            "learning_rate": self.learning_rate,
        })

    def _load_q_table(self):
        """Load Q-table from previous session if exists."""
        try:
            if self.q_table_path.exists():
                with open(self.q_table_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Convert string keys back to tuples
                    for key_str, value in data.items():
                        state, action = key_str.split("|", 1)
                        self.q_table[(state, action)] = value
        except Exception:
            # If loading fails, start with empty Q-table
            pass

    def _save_q_table(self):
        """Save current Q-table state to disk."""
        try:
            # Convert tuple keys to strings for JSON serialization
            data = {f"{state}|{action}": value for (state, action), value in self.q_table.items()}
            with open(self.q_table_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            # best-effort saving; avoid crashing core flow
            pass

    def _load_performance_history(self):
        """Load performance history for adaptive learning."""
        try:
            if self.history_path.exists():
                with open(self.history_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            record = json.loads(line.strip())
                            if "reward" in record:
                                self.performance_history.append(record["reward"])
        except Exception:
            pass

    def _adapt_parameters(self):
        """Adapt learning parameters based on recent performance."""
        if len(self.performance_history) < 10:
            return
        
        recent_rewards = self.performance_history[-10:]
        avg_recent = sum(recent_rewards) / len(recent_rewards)
        
        # If performance is improving, reduce exploration
        if avg_recent > 7.0:
            self.exploration_epsilon = max(0.05, self.exploration_epsilon * 0.95)
        # If performance is poor, increase exploration
        elif avg_recent < 3.0:
            self.exploration_epsilon = min(0.3, self.exploration_epsilon * 1.05)

    def _append_history(self, record: Dict[str, any]):
        try:
            with open(self.history_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            # best-effort logging; avoid crashing core flow
            pass


# Shared singleton accessor so routes and converters use the same agent instance
def get_shared_agent() -> RLAgent:
    global _shared_agent
    if _shared_agent is None:
        _shared_agent = RLAgent()
    return _shared_agent
