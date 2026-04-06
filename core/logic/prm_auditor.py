from typing import List, Dict

# The "PRM Auditor" (Process Reward Model)
# Task: Checks every step of the reasoning path.
# A +1.0 reward is only granted if the whole path is consistent.

class PRMAuditor:
    def __init__(self):
        self.history = []
        
    def evaluate_step(self, step_id: int, logic: str, result: int, expected: int) -> float:
        """
        Evaluates a single step.
        Returns: +1.0 for success, -0.5 for gap, -2.0 for violation.
        """
        if result == expected:
            reward = 1.0
            status = "PASSED"
        elif result % 5 == expected % 5: # Mirrored logic
            reward = 0.5
            status = "MIRROR-GAP"
        else:
            reward = -2.0
            status = "VIOLATION"
            
        self.history.append({"step": step_id, "logic": logic, "status": status, "reward": reward})
        return reward

    def compile_total_reward(self) -> float:
        """
        Compiles the total reward for the thinking path.
        """
        if not self.history: return 0.0
        return sum([s['reward'] for s in self.history]) / len(self.history)

    def print_path_audit(self):
        print("\n--- [PRM AUDIT: THINKING PATH] ---")
        for s in self.history:
            print(f"  Step {s['step']}: {s['logic']} -> {s['status']} ({s['reward']})")
        print(f"Final Path Reward: {self.compile_total_reward():.2f}")

if __name__ == "__main__":
    prm = PRMAuditor()
    # Step 1: Root 2
    prm.evaluate_step(1, "Root Derivation", 2, 2)
    # Step 2: Lord 2
    prm.evaluate_step(2, "Lord Derivation", 2, 2)
    # Step 3: Result 2
    prm.evaluate_step(3, "Triple-Resonance", 2, 2)
    
    prm.print_path_audit()
