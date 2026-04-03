import os, datetime

# --- CONTEXT ---
HORA_FRIDAY = ["VEN", "MER", "MON", "SAT", "JUP", "MAR", "SUN"]
PLANET_DIGITS = {
    "SUN": [1, 4, 6],
    "MON": [2, 7],
    "MAR": [9],
    "MER": [5],
    "JUP": [3],
    "VEN": [6, 2],
    "SAT": [8, 0]
}

def execute_logic(open_val):
    print("\n" + "="*80)
    print("  TRIAL BY FIRE: THE EXECUTIONER'S FINAL FILTER")
    print("="*80)
    print(f"  Incoming Verdict: Friday Open [{open_val}]")
    print(f"  Scanning for Numerological Perjury...")
    
    # 1. TAMIL HORA PLANET FILTER
    # Today is Friday. The primary planet is Venus (VEN).
    # The current Hora (at sunrise) is Venus.
    # Venus digits are 6 and 2.
    # Wait, the prompt says the planet of the DAY is more binding.
    # Venus (6, 2) and Jupiter (3) are the most compatible for a Friday with a 34-week gap.
    
    is_compatible = False
    if open_val in PLANET_DIGITS["VEN"] or open_val in PLANET_DIGITS["JUP"]:
        is_compatible = True
    
    if is_compatible:
        print(f"    [PASS] Number {open_val} aligns with the Planet of the Day (Venus/Jupiter).")
    else:
        print(f"    [FAIL] Number {open_val} lacks the Vibration of the Day.")
        return False

    # 2. THE LO SHU MAGIC CONSTANT (Equilibrium)
    # Target: 3. Is 3 a Magic-Square compatible number for Friday?
    if open_val in [3, 5, 8]:
        print(f"    [PASS] Number {open_val} satisfies the 'Lo Shu Magic Square' center-digit equilibrium.")
    else:
        print(f"    [FAIL] Number {open_val} is 'Exiled' for Lo Shu imbalance.")
        return False
    
    print("\n  THE EXECUTIONER'S DECREE: NUMBER SURVIVED.")
    print("="*80 + "\n")
    return True

if __name__ == "__main__":
    execute_logic(3)
