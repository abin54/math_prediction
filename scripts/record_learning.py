import json
import os
from datetime import date

TRICKS_PATH = "core/learned_tricks.json"

def record_trick(trick_name, pattern, lesson):
    os.makedirs("core", exist_ok=True)
    
    if os.path.exists(TRICKS_PATH):
        with open(TRICKS_PATH, 'r') as f:
            tricks = json.load(f)
    else:
        tricks = []
        
    new_trick = {
        "date": str(date.today()),
        "name": trick_name,
        "pattern": pattern,
        "lesson": lesson
    }
    
    tricks.append(new_trick)
    
    with open(TRICKS_PATH, 'w') as f:
        json.dump(tricks, f, indent=4)
        
    print(f"Successfully learned new trick: {trick_name}")

if __name__ == "__main__":
    # Specific learning from May 6, 2026 (Result 9)
    record_trick(
        trick_name="Lord-Date Convergence",
        pattern="Result = (Root + Lord - 2) % 10",
        lesson="On Wednesday (Lord 5), the Root (6) combined to produce 9. Prioritize local Lord-Date sums over long-term drift."
    )
