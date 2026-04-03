"""
Triple-Layer Oracle Loss Blueprint v25.0 — Custom Loss
======================================================
1. Loss = MSE(y_hat, y) + alpha(1 - Bindu) + beta(Delta_Arc) + gamma(Dist_Saham).
2. alpha (Vedic): Penalize confidence in low-strength (Bindu < 20) signs.
3. beta (Western): Penalize predictions outside of Solar Arc windows.
4. gamma (Arabic): Penalize numbers far from the calculated Saham degree.
"""

import torch
import torch.nn as nn

class TripleLayerLoss(nn.Module):
    def __init__(self, alpha=0.5, beta=0.3, gamma=0.2):
        super(TripleLayerLoss, self).__init__()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.mse = nn.MSELoss()

    def forward(self, y_pred, y_true, bindu_score, delta_arc, dist_saham):
        # Loss components
        mse_loss = self.mse(y_pred, y_true)
        # alpha component: Penalize low SAV Bindu score
        vedic_loss = self.alpha * (1.0 - (bindu_score / 56.0))
        # beta component: Penalize out-of-arc window
        western_loss = self.beta * delta_arc
        # gamma component: Penalize distance from Saham target
        arabic_loss = self.gamma * dist_saham
        
        return mse_loss + vedic_loss + western_loss + arabic_loss

print("Triple-Layer Oracle Loss Blueprint v25.0 Initialized.")
