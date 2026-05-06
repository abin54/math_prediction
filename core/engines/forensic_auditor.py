import requests
from typing import Dict, Any
from core.utils.logger import sovereign_logger as logger
from core.utils.config_manager import ConfigManager

class ForensicAuditor:
    """
    Handles adversarial logic auditing using Ollama LLMs.
    """
    
    def __init__(self):
        self.url = ConfigManager.get("models.ollama.url")
        self.model = ConfigManager.get("models.ollama.model_name")
        
    def query(self, prompt: str, system_context: str = "You are a Lead Forensic Auditor.") -> str:
        """Sends a query to the Ollama endpoint."""
        payload = {
            "model": self.model,
            "prompt": f"{system_context}\n\nSTRESS-TEST THIS PROOF:\n{prompt}",
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_gpu": 1
            }
        }
        
        logger.debug(f"Querying Ollama model {self.model}")
        try:
            response = requests.post(self.url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "No response.")
        except Exception as e:
            logger.error(f"Ollama connection error: {e}")
            return f"Audit Error: {str(e)}"

    def audit_win_probability(self, batting_team: str, win_prob: float, match_state: Dict[str, Any]) -> str:
        """
        Performs a forensic audit of a predicted win probability.
        """
        prompt = (
            f"YOU ARE THE IPL FORENSIC EXECUTIONER. Prove why {batting_team} is structurally favored to win "
            f"with a {win_prob*100:.1f}% probability despite chasing {match_state.get('chasing_target')}. "
            f"Current Score: {match_state.get('total_runs')}/{match_state.get('wickets_fallen')} in {match_state.get('over')} overs."
        )
        
        logger.info(f"Commencing forensic audit for {batting_team}")
        return self.query(prompt)
