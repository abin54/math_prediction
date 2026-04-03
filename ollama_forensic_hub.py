import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

class OllamaForensicHub:
    def __init__(self, model=MODEL_NAME):
        self.model = model

    def query_auditor(self, prompt, context="You are the Lead Forensic Prosecutor and Socratic Auditor."):
        payload = {
            "model": self.model,
            "prompt": f"{context}\n\nSTRESS-TEST THIS PROOF:\n{prompt}",
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_gpu": 1,  # Force NVIDIA GPU
                "num_thread": 4 # Limit CPU usage
            }
        }
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("response", "No audit response.")
            else:
                return f"Error: Ollama returned status {response.status_code}"
        except Exception as e:
            return f"Ollama Connection Error: {str(e)}"

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
