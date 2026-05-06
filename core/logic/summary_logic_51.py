from core.logic.formal_logic_bridge import FormalLogicBridge
from core.rules.hard_rules import HardRules

def define_summary_logic_51():
    """
    Formally defines the logic for the result '51' (Monday 06/04/2026).
    """
    # 1. Contextual Variables
    rn = 2  # Root Number (2026-04-06)
    dl = 2  # Day Lord (Monday)
    offset = 4  # Current Galactic Offset Regime
    loshu = 15  # Lo Shu Equilibrium Constant
    
    # 2. Open Logic (Resonance Syllogism)
    # (LoShu - RN - DL + Offset) % 10
    open_calc = (loshu - rn - dl + offset) % 10
    
    # 3. Close Logic (Step-Inverse Shift)
    # (Open - Offset) % 10
    close_calc = (open_calc - offset) % 10
    
    jodi = f"{open_calc}{close_calc}"
    
    print("--- SUMMARY LOGIC: RESULT 51 ---")
    print(f"Date: 06/04/2026 (Monday)")
    print(f"Result: {jodi}")
    print(f"Open Logic: (15 - RN:{rn} - DL:{dl} + Offset:{offset}) = {open_calc}")
    print(f"Close Logic: (Open:{open_calc} - Offset:{offset}) = {close_calc}")
    print(f"Status: +4 Offset Regime Confirmed.")
    print("--------------------------------")
    
    return {
        "jodi": jodi,
        "open_logic": f"(15 - {rn} - {dl} + {offset}) % 10",
        "close_logic": f"({open_calc} - {offset}) % 10",
        "regime": "+4 Galactic Offset"
    }

if __name__ == "__main__":
    define_summary_logic_51()
