import requests
import json
from core.utils.forensic_logger import ForensicLogger

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

class OllamaForensicHub:
    def __init__(self, logger=None, model=MODEL_NAME):
        self.logger = logger if logger else ForensicLogger()
        self.model = model

    def query_auditor(self, prompt, context="You are the Lead Forensic Prosecutor and Socratic Auditor."):
        payload = {
            "model": self.model,
            "prompt": f"{context}\n\nSTRESS-TEST THIS PROOF:\n{prompt}",
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_gpu": 1,
                "num_thread": 4
            }
        }
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json().get("response", "No audit response.")
            else:
                return f"Error: Ollama returned status {response.status_code}"
        except Exception as e:
            return f"Ollama Connection Error: {str(e)}"

    def conduct_adversarial_debate(self, jodi, proof_context):
        """Phase Gamma: Adversarial Stress-Test (Dual-Persona logic state)."""
        self.logger.log_phase("Gamma", "Commencing Adversarial Debate (Dual-Persona)...")
        
        # Step 1: The Architect's Proposition
        architect_prompt = (
            f"YOU ARE THE ARCHITECT. Propose a final mathematical proof for Jodi {jodi} "
            f"based on the 52-year causal chain and the context: {proof_context}. "
            "Use Lo Shu Square constants and Time-Series convergence."
        )
        architect_res = self.query_auditor(architect_prompt, context="You are The Architect.")
        self.logger.info("[The Architect]: Validating Node Resonance...")
        
        # Step 2: The Auditor's Deconstruction
        auditor_prompt = (
            f"YOU ARE THE AUDITOR. Perform a Forensic Deconstruction of the Architect's proof: {architect_res}. "
            "Attempt to prove that the 1970s and 1980s data contradicts this conclusion. "
            "Expose any 'probabilistic guessing' or data-drift bias."
        )
        auditor_res = self.query_auditor(auditor_prompt, context="You are The Auditor.")
        self.logger.info("[The Auditor]: Identifying Logic Conflicts...")
        
        # Step 3: Survival Conclusion
        survival_prompt = (
            f"Based on the debate above, provide the Surviving Conclusion. "
            f"Architect: {architect_res}\nAuditor: {auditor_res}\n"
            "Only if the proof survives the attack is it 'Perfect'. "
            "Discard weak weights and output the Final Periodic Singularity."
        )
        final_res = self.query_auditor(survival_prompt, context="You are the Supreme Judge.")
        self.logger.info(f"[Decision]: Survived Audit Status: {final_res[:50].strip()}...")
        
        return {
            "transcript": f"Architect: {architect_res}\n\nAuditor: {auditor_res}",
            "verdict": final_res
        }

def test_ollama_connection():
    hub = OllamaForensicHub()
    print("\n" + "="*80)
    print("  OLLAMA FORENSIC HUB: INITIALIZING GPU REASONING")
    print("="*80)
    
    # Simple Socratic test
    test_prompt = "Prove why the number 3 is mathematically superior to the number 8 in a 52-year historical context."
    print(f"\n  [Investigation] Querying llama3.2:3b (GPU Accelerated)...")
    res = hub.query_auditor(test_prompt)
    print(f"\n  [Audit Response]:\n{res}")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    test_ollama_connection()
