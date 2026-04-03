"""
SBC Vedha Nakshatra Blueprint v23.0 — 28-Nakshatra Filtering
============================================================
1. Mapping the 28 Nakshatras (incl. Abhijit) to a 9x9 coordinate system.
2. Calculating Front, Left, and Right Vedhas from Malefics (Mars, Saturn, Rahu).
3. If a 'Vedha' occurs on the vowel/consonant, apply negative weight (0.8).
"""

import numpy as np

class SBC_NakshatraGrid:
    def __init__(self, size=9):
        # 9x9 Sarvatobhadra Chakra grid
        self.grid = np.zeros((size, size))
        # Mapping 28 Nakshatras to specific (x, y) coordinates
        self.nakshatra_map = {i: (i // 7, i % 7) for i in range(28)}

    def calculate_vedha(self, mars_pos, saturn_pos, rahu_pos, janma_nakshatra):
        # Front, Left, and Right Vedhas (Hits)
        target_coord = self.nakshatra_map[janma_nakshatra]
        malefics = [mars_pos, saturn_pos, rahu_pos]
        veda_hit = False
        
        for m in malefics:
            m_coord = self.nakshatra_map[m]
            # Simplifying: A Vedha hit occurs if in the same row or column (SBC logic)
            if m_coord[0] == target_coord[0] or m_coord[1] == target_coord[1]:
                veda_hit = True
                break
                
        # If a Vedha occurs, apply a negative weight of 0.8
        return 0.8 if veda_hit else 1.0

print("SBC Vedha Nakshatra Blueprint v23.0 Initialized.")
