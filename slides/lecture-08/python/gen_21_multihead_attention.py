#!/usr/bin/env python3
"""
Generate slide 21: Multi-Head Attention as parallel graphs.

Three side-by-side 6x6 heatmaps showing different attention heads
for "The cat sat on the mat":
  Head 1 "Position": Strong diagonal band (neighbor attention)
  Head 2 "Syntax":   Articles attend to nouns
  Head 3 "Semantics": Verb-object pattern

Output: ../images/21-multihead-attention.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '21-multihead-attention.png')

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
# Data
# ---------------------------------------------------------------------------
WORDS = ['The', 'cat', 'sat', 'on', 'the', 'mat']
N = len(WORDS)


def head_position():
    """Head 1: Strong diagonal band -- each word attends to neighbors."""
    mat = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            dist = abs(i - j)
            if dist == 0:
                mat[i, j] = 1.0
            elif dist == 1:
                mat[i, j] = 0.7
            elif dist == 2:
                mat[i, j] = 0.25
            else:
                mat[i, j] = 0.05
    return mat


def head_syntax():
    """Head 2: Articles attend to nouns (The->cat, the->mat)."""
    mat = np.full((N, N), 0.05)
    np.fill_diagonal(mat, 0.3)
    # The(0)->cat(1), the(4)->mat(5)  articles to their nouns
    mat[0, 1] = 0.95
    mat[1, 0] = 0.50
    mat[4, 5] = 0.90
    mat[5, 4] = 0.50
    # Weaker article-noun cross-links
    mat[0, 5] = 0.30
    mat[4, 1] = 0.25
    # Nouns to each other
    mat[1, 5] = 0.40
    mat[5, 1] = 0.40
    return mat


def head_semantics():
    """Head 3: Verb->object pattern (sat->mat, sat->on)."""
    mat = np.full((N, N), 0.05)
    np.fill_diagonal(mat, 0.3)
    # sat(2)->mat(5) strongest
    mat[2, 5] = 0.90
    mat[5, 2] = 0.60
    # sat(2)->on(3) moderate
    mat[2, 3] = 0.70
    mat[3, 2] = 0.45
    # on(3)->mat(5)
    mat[3, 5] = 0.75
    mat[5, 3] = 0.55
    # cat(1)->sat(2) subject-verb
    mat[1, 2] = 0.65
    mat[2, 1] = 0.40
    return mat


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, axes = plt.subplots(1, 3, figsize=(19.2, 10.8), facecolor=BG)

    cmap = LinearSegmentedColormap.from_list(
        'attention', [BG, '#1a3a5c', BLUE, ORANGE, YELLOW], N=256
    )

    heads = [
        ('Head 1: Position', head_position(), YELLOW),
        ('Head 2: Syntax', head_syntax(), TEAL),
        ('Head 3: Semantics', head_semantics(), RED),
    ]

    for ax, (title, mat, accent) in zip(axes, heads):
        ax.set_facecolor(BG)
        im = ax.imshow(mat, cmap=cmap, vmin=0, vmax=1, aspect='equal')

        ax.set_xticks(range(N))
        ax.set_xticklabels(WORDS, fontsize=23, fontweight='bold', color=TEXT)
        ax.set_yticks(range(N))
        ax.set_yticklabels(WORDS, fontsize=23, fontweight='bold', color=TEXT)
        ax.tick_params(axis='both', length=0, pad=6)

        ax.set_title(title, fontsize=24, fontweight='bold', color=accent, pad=14)

        # Annotate cells
        for i in range(N):
            for j in range(N):
                val = mat[i, j]
                txt_color = BG if val > 0.6 else TEXT
                ax.text(j, i, f'{val:.1f}', ha='center', va='center',
                        fontsize=23, fontweight='bold', color=txt_color)

    fig.suptitle('Multi-Head Attention: H Heads = H Parallel Graphs',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)

    fig.text(0.5, 0.02,
             'Each head learns a different relationship pattern over the same tokens',
             ha='center', fontsize=23, color=MUTED)

    plt.tight_layout(rect=[0, 0.05, 1, 0.92])

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
