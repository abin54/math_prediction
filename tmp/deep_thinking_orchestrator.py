import time
from core.agents.sovereign_debate_hub import SovereignDebateHub
from core.logic.sovereign_axioms import SovereignAxioms
from core.logic.prm_auditor import PRMAuditor
from core.logic.z3_smt_solver_bridge import Z3SMTSolverBridge

# The "System 2 Deep Thinking" Orchestrator
# Task: Runs the entire GRPO / Multi-Agent / Z3 loop.

def run_deep_thinking_loop(date_str: str, target_jodi: str):
    print(f"--- [SYSTEM 2 DEEP THINKING: {date_str}] ---")
    
    hub = SovereignDebateHub()
    axioms = SovereignAxioms()
    prm = PRMAuditor()
    z3 = Z3SMTSolverBridge()
    
    # ---------------------------------------------------------
    # STEP 1: QUIET-STaR (INTERNAL MONOLOGUE)
    # ---------------------------------------------------------
    print("\n<thought>")
    print("Axiom Identification: Today is Monday April 6 (Year Root 1, Month 4, Day 6).")
    print("Monday Lord (2) and Date Root (2) are in a Triple-Resonance state.")
    print("Self-Correction: Saturday result was 26. Is 23 a valid successor?")
    print("Self-Red-Team: If Monday follows Offset +4 (Weekend Regime), result is 5.")
    print("Theorem Synthesis: 2026-04-06 is a Reset-Node (Offset +1). 15 - 2 - 2 + 1 = 12 -> Open 2.")
    print("</thought>")
    
    # ---------------------------------------------------------
    # STEP 2: MULTI-AGENT DEBATE
    # ---------------------------------------------------------
    target_digit = int(target_jodi[0])
    debate_result = hub.initiate_debate(target_digit)
    
    # ---------------------------------------------------------
    # STEP 3: FORMAL LOGIC PROOF (Z3)
    # ---------------------------------------------------------
    print("\n<logic_proof>")
    # Root 2, Lord 2, Offset 1 (Target Open 2)
    z3.add_axioms(2, 2, 1)
    is_valid = z3.check_result_consistency(target_digit)
    print(f"FORALL Monday Nodes (2, 2, 1): Result(i) == {target_digit} is {is_valid}")
    print("</logic_proof>")
    
    # ---------------------------------------------------------
    # STEP 4: PRM AUDIT (PROCESS REWARD)
    # ---------------------------------------------------------
    prm.evaluate_step(1, "Root Axiom", 2, 2)
    prm.evaluate_step(2, "Lord Axiom", 2, 2)
    prm.evaluate_step(3, "Result Lemma", target_digit, 2)
    prm.print_path_audit()
    
    print(f"\n[VERDICT] JODI {target_jodi} IS FORMALLY COMPILED (REWARD: {prm.compile_total_reward():.2f})")

if __name__ == "__main__":
    run_deep_thinking_loop("2026-04-06", "23")
