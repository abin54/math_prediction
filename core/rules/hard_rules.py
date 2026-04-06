# Static-Metadata: The Immutable Causal Foundation
# Tamil Numerology (Enn Kanietham) & Lo Shu Square Constants

import numpy as np

class HardRules:
    """
    Enforces 'Static-Metadata' constraints on the 52-year dataset (1972-2026).
    These rules are immutable and govern the 'Wavefunction' of numerical sequences.
    """
    
    # Tamil Numerology: Planetary Alignment (1-9)
    PLANETARY_MAP = {
        1: "Sun (Suriyan)",
        2: "Moon (Chandran)",
        3: "Jupiter (Guru)",
        4: "Rahu",
        5: "Mercury (Budhan)",
        6: "Venus (Sukki)",
        7: "Ketu",
        8: "Saturn (Sani)",
        9: "Mars (Sevvai)"
    }
    
    # Lo Shu Square Constants (Sum = 15)
    LO_SHU_SQUARE = np.array([
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ])
    
    # Chaldean Hora Order (Saturn -> Moon)
    HORA_ORDER = [8, 3, 9, 1, 6, 5, 2] 
    
    @staticmethod
    def get_numerological_value(date_str) -> int:
        """Calculate the Root Number (Destiny) of any date (Reverse-Derivation Base)."""
        # Example: 1972-04-03 -> 1+9+7+2+4+3 = 26 -> 2+6 = 8
        if not isinstance(date_str, str):
            date_str = str(date_str)
        digits = [int(d) for d in date_str if d.isdigit()]
        total = sum(digits)
        while total > 9:
            total = sum(int(d) for d in str(total))
        return total

    @staticmethod
    def get_day_lord(day_name: str) -> int:
        """Map Day of Week to its Planetary Lord."""
        mapping = {
            "Sunday": 1, "Monday": 2, "Tuesday": 9, 
            "Wednesday": 5, "Thursday": 3, "Friday": 6, "Saturday": 8
        }
        return mapping.get(day_name.capitalize(), 0)

    @staticmethod
    def verify_causal_node(prev_result: int, current_date: str, prediction: int) -> bool:
        """
        Verify if a prediction aligns with the Static-Metadata of the current node.
        Includes Yama-Gandom 'Mirror-Flipping' detection for Fridays.
        """
        from datetime import datetime
        dt = datetime.strptime(current_date, '%Y-%m-%d')
        root_num = HardRules.get_numerological_value(current_date)
        day_lord = HardRules.get_day_lord(dt.strftime('%A'))
        
        # Friday Yama-Gandam Filter (3:00 PM - 4:30 PM)
        # This window often forces a 'Cut' or 'Mirror' result.
        if dt.strftime('%A') == "Friday":
            # If the current prediction is a CUT of the root, it survives the conflict.
            is_cut = (abs(prediction - root_num) == 5)
            is_mirror = ((prediction + root_num) % 10 == 0)
            return is_cut or is_mirror or (prediction == root_num)
            
        return (prediction % 10 == root_num) or (prediction % 10 == day_lord)
