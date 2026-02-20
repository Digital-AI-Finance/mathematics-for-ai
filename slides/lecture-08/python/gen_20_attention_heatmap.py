#!/usr/bin/env python3
"""
Generate slide 20: Attention Weights as an Adjacency Matrix (heatmap).

6x6 heatmap of attention weights for "The cat sat on the mat".
Symmetric matrix with self-attention (diagonal = 1.0).

Output: ../images/20-attention-heatmap.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '20-attention-heatmap.png')

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

# ---------------------------------------------------------------------------
# Words and attention weights (reused from gen_12_attention.py)
# ---------------------------------------------------------------------------
WORDS = ['The', 'cat', 'sat', 'on', 'the', 'mat']
N = len(WORDS)

ATTENTION = {
    frozenset({1, 2}): 0.90,  # cat-sat
    frozenset({3, 5}): 0.70,  # on-mat
    frozenset({0, 1}): 0.60,  # The-cat
    frozenset({2, 3}): 0.50,  # sat-on
    frozenset({4, 5}): 0.45,  # the-mat
    frozenset({1, 5}): 0.35,  # cat-mat
    frozenset({0, 2}): 0.25,  # The-sat
    frozenset({2, 5}): 0.20,  # sat-mat
    frozenset({1, 3}): 0.20,  # cat-on
    frozenset({3, 4}): 0.18,  # on-the
    frozenset({0, 5}): 0.15,  # The-mat
    frozenset({0, 4}): 0.12,  # The-the
    frozenset({0, 3}): 0.10,  # The-on
    frozenset({1, 4}): 0.10,  # cat-the
    frozenset({2, 4}): 0.10,  # sat-the
}


def build_matrix():
    """Convert frozenset attention weights to a 6x6 symmetric numpy array."""
    mat = np.zeros((N, N))
    for pair, weight in ATTENTION.items():
        i, j = sorted(pair)
        mat[i, j] = weight
        mat[j, i] = weight
    np.fill_diagonal(mat, 1.0)  # self-attention
    return mat


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)

    mat = build_matrix()

    # Custom colormap: dark bg -> blue -> yellow
    cmap = LinearSegmentedColormap.from_list(
        'attention', [BG, '#1a3a5c', BLUE, ORANGE, YELLOW], N=256
    )

    im = ax.imshow(mat, cmap=cmap, vmin=0, vmax=1, aspect='equal')

    # Axis labels
    ax.set_xticks(range(N))
    ax.set_xticklabels(WORDS, fontsize=24, fontweight='bold', color=TEXT)
    ax.set_yticks(range(N))
    ax.set_yticklabels(WORDS, fontsize=24, fontweight='bold', color=TEXT)
    ax.tick_params(axis='both', length=0, pad=10)

    # Move x-axis labels to top as well
    ax.xaxis.set_ticks_position('both')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', top=True, bottom=True, labeltop=True, labelbottom=True)

    # Annotate cell values
    for i in range(N):
        for j in range(N):
            val = mat[i, j]
            txt_color = BG if val > 0.6 else TEXT
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=23, fontweight='bold', color=txt_color)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Attention Weight', fontsize=23, color=TEXT, labelpad=12)
    cbar.ax.tick_params(labelsize=23, colors=TEXT)

    # Title
    fig.suptitle('Attention Weights = Adjacency Matrix',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.95)

    # Subtitle
    ax.set_xlabel('"The cat sat on the mat" \u2014 each cell is an edge weight',
                  fontsize=23, color=MUTED, labelpad=15)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
