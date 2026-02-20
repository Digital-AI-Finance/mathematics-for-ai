#!/usr/bin/env python3
"""
Generate slide 22: Sparse vs Dense Attention patterns.

Three side-by-side 16x16 binary matrices:
  Left:   Full Attention (complete graph)
  Middle: Sliding Window (w=3)
  Right:  Longformer (window + global tokens)

Output: ../images/22-sparse-dense-attention.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '22-sparse-dense-attention.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG      = '#1b2631'
YELLOW  = '#f1c40f'
BLUE    = '#3498db'
TEAL    = '#2ecc71'
RED     = '#e74c3c'
ORANGE  = '#e67e22'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'

N = 16  # matrix dimension


def full_attention():
    """Complete graph: every token attends to every token."""
    return np.ones((N, N))


def sliding_window(w=3):
    """Diagonal band of width w."""
    mat = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if abs(i - j) <= w // 2:
                mat[i, j] = 1.0
    return mat


def longformer(w=3):
    """Sliding window + global tokens (first and last)."""
    mat = sliding_window(w)
    # First token is global: attends to all and all attend to it
    mat[0, :] = 1.0
    mat[:, 0] = 1.0
    # Last token is global
    mat[N - 1, :] = 1.0
    mat[:, N - 1] = 1.0
    return mat


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, axes = plt.subplots(1, 3, figsize=(19.2, 10.8), facecolor=BG)

    # Binary colormap: dark bg for 0, blue for 1
    cmap = LinearSegmentedColormap.from_list('binary_blue', [BG, BLUE], N=2)

    panels = [
        ('Full Attention', full_attention(), YELLOW),
        ('Sliding Window (w=3)', sliding_window(3), TEAL),
        ('Longformer', longformer(3), ORANGE),
    ]

    for ax, (title, mat, accent) in zip(axes, panels):
        ax.set_facecolor(BG)
        ax.imshow(mat, cmap=cmap, vmin=0, vmax=1, aspect='equal',
                  interpolation='nearest')

        edges = int(mat.sum())
        total = N * N
        pct = edges / total * 100

        ax.set_title(title, fontsize=22, fontweight='bold', color=accent, pad=14)
        ax.set_xlabel(f'{edges} edges ({pct:.0f}%)', fontsize=16,
                      color=TEXT, labelpad=10)

        # Tick styling
        ax.set_xticks(range(0, N, 4))
        ax.set_yticks(range(0, N, 4))
        ax.tick_params(axis='both', colors=MUTED, labelsize=11, length=0)

        # Subtle grid
        for k in range(N + 1):
            ax.axhline(k - 0.5, color=MUTED, lw=0.3, alpha=0.3)
            ax.axvline(k - 0.5, color=MUTED, lw=0.3, alpha=0.3)

    fig.suptitle('Sparse Attention = Sparse Graph',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)

    fig.text(0.5, 0.02,
             'Reducing edges from O(n\u00b2) to O(n) cuts compute while preserving key connections',
             ha='center', fontsize=18, color=MUTED)

    plt.tight_layout(rect=[0, 0.05, 1, 0.92])

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
