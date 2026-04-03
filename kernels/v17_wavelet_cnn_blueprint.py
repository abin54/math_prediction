"""
Wavelet CNN Blueprint v17.0 — Multi-Scale Sequence Analysis
===========================================================
1. Localizing the 52-year frequency patterns (Daily vs Decadal).
2. Architecture: Multi-Scale 1D-CNN with Atrous (Dilated) branch.
"""

import torch
import torch.nn as nn
import pywt

class WaveletCNN(nn.Module):
    def __init__(self, input_len=16000, hidden_dim=64):
        super(WaveletCNN, self).__init__()
        
        # Branch 1: High-Frequency (Detail)
        self.conv_detail = nn.Sequential(
            nn.Conv1d(1, hidden_dim, kernel_size=3, padding=1),
            nn.LeakyReLU(),
            nn.Conv1d(hidden_dim, hidden_dim * 2, kernel_size=5, padding=2),
            nn.LeakyReLU()
        )
        
        # Branch 2: Low-Frequency (Approximation) - DILATED
        self.conv_approx = nn.Sequential(
            nn.Conv1d(1, hidden_dim, kernel_size=3, padding=10, dilation=10),
            nn.LeakyReLU(),
            nn.Conv1d(hidden_dim, hidden_dim * 2, kernel_size=5, padding=20, dilation=20),
            nn.LeakyReLU()
        )
        
        self.fc_fusion = nn.Linear(hidden_dim * 4, 1)

    def forward(self, x):
        # x: Input Jodi sequence (1D)
        # Decompose using Discrete Wavelet Transform (DWT)
        # cA, cD = pywt.dwt(x, 'db1') 
        
        feat_detail = self.conv_detail(x)
        feat_approx = self.conv_approx(x)
        
        # Fuse Approximations (Trends) and Details (Noise)
        fusion = torch.cat([feat_detail, feat_approx], dim=1)
        return self.fc_fusion(fusion)

print("Wavelet CNN Blueprint v17.0 Initialized.")
