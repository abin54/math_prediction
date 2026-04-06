
import subprocess
import json
import re
import time

def get_live_score_via_eyes():
    print("  [Vision] Querying agent-eyes for Chrome UI tree...")
    try:
        # Run agent-eyes to get the focused Chrome window tree
        result = subprocess.run(
            ["uvx", "agent-eyes", "eyes_get_tree", "--app", "Google Chrome"],
            capture_output=True, text=True, timeout=60
        )
        
        tree_text = result.stdout
        
        # Look for MI Score pattern: e.g., "MI 25/2 (3.4)" or similar
        # Cricbuzz typically has score in a very specific format
        # Let's search for "MI" or "Mumbai Indians" followed by digits
        
        score_patterns = [
            r"(MI|Mumbai Indians)\s+(\d+/\d+)\s+\((\d+\.\d+)\)", # MI 25/2 (3.5)
            r"(MI|Mumbai Indians)\s+(\d+/\d+)", # MI 25/2
            r"(\d+-\d+)\s+overs\s+(\d+/\d+)", # overs 3.5 25/2
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, tree_text, re.IGNORECASE)
            if match:
                print(f"  [Found] Live Score Match: {match.group(0)}")
                return match.group(0)
        
        # Fallback: Look for any "Runs/Wickets" pattern
        generic_match = re.search(r"(\d+/\d+)\s+\((\d+\.\d+)\)", tree_text)
        if generic_match:
            print(f"  [Found] Generic Score Match: {generic_match.group(0)}")
            return generic_match.group(0)
            
        print("  [Warning] No score pattern found in the current UI tree.")
        return None
        
    except Exception as e:
        print(f"  [Error] Vision Engine failed: {e}")
        return None

if __name__ == "__main__":
    score = get_live_score_via_eyes()
    if score:
        print(f"\nFinal Extracted Score: {score}")
    else:
        print("\nForensic Vision failed to extract live data.")
