#!/usr/bin/env python3
"""
Generate slide 26: Attention Step by Step.

Six panels showing a concrete 4-token, 3-dimensional attention computation:
  1. Input X           2. Q, K, V projections
  3. Score matrix S    4. After scaling by sqrt(d_k)
  5. After softmax     6. Output = Attention(Q,K,V)

Output: ../images/26-attention-derivation.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '26-attention-derivation.png')

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

# Custom colourmap: dark bg -> blue -> yellow
CMAP = LinearSegmentedColormap.from_list(
    'attn', [BG, '#1a3a5c', BLUE, ORANGE, YELLOW], N=256)

TOKENS = ['The', 'cat', 'sat', '.']

# ---------------------------------------------------------------------------
# Concrete numeric data (small integers for pedagogy)
# ---------------------------------------------------------------------------
X = np.array([
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 0],
    [0, 0, 1],
], dtype=float)

# Projection weights (3x3 for simplicity -- d_k = 3)
W_Q = np.array([[1, 0, 1],
                [0, 1, 0],
                [1, 0, 0]], dtype=float)
W_K = np.array([[0, 1, 0],
                [1, 0, 1],
                [0, 1, 1]], dtype=float)
W_V = np.array([[1, 1, 0],
                [0, 1, 1],
                [1, 0, 1]], dtype=float)


def softmax_rows(m):
    """Row-wise softmax."""
    e = np.exp(m - m.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def draw_matrix(ax, mat, title, formula, row_labels=None, col_labels=None,
                fmt='.1f', cmap=CMAP, vmin=None, vmax=None, annotate=True):
    """Draw a heatmap matrix in *ax* with title and formula."""
    ax.set_facecolor(BG)

    if vmin is None:
        vmin = mat.min()
    if vmax is None:
        vmax = mat.max()

    im = ax.imshow(mat, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto')

    rows, cols = mat.shape

    # Cell annotations
    if annotate:
        for i in range(rows):
            for j in range(cols):
                val = mat[i, j]
                brightness = (val - vmin) / (vmax - vmin + 1e-9)
                tc = BG if brightness > 0.65 else TEXT
                ax.text(j, i, f'{val:{fmt}}', ha='center', va='center',
                        fontsize=14, fontweight='bold', color=tc)

    # Labels
    if row_labels:
        ax.set_yticks(range(rows))
        ax.set_yticklabels(row_labels, fontsize=12, color=TEXT)
    else:
        ax.set_yticks([])

    if col_labels:
        ax.set_xticks(range(cols))
        ax.set_xticklabels(col_labels, fontsize=12, color=TEXT)
    else:
        ax.set_xticks([])

    ax.tick_params(length=0)

    # Title + formula
    ax.set_title(title, fontsize=16, fontweight='bold', color=YELLOW, pad=10)
    ax.set_xlabel(formula, fontsize=13, color=MUTED, labelpad=8)

    return im


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Compute all intermediate matrices
    Q = X @ W_Q
    K = X @ W_K
    V = X @ W_V

    d_k = K.shape[1]
    S = Q @ K.T                        # raw scores (4x4)
    S_scaled = S / np.sqrt(d_k)        # scaled scores
    A = softmax_rows(S_scaled)          # attention weights
    Out = A @ V                         # final output

    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 3, figsize=(19.2, 10.8), facecolor=BG)
    fig.subplots_adjust(hspace=0.55, wspace=0.35, top=0.86, bottom=0.06,
                        left=0.06, right=0.96)

    dim_labels = ['d1', 'd2', 'd3']

    # Panel 1: Input X (4x3)
    draw_matrix(axes[0, 0], X,
                title='1. Input X',
                formula='$X \\in \\mathbb{R}^{4 \\times 3}$',
                row_labels=TOKENS, col_labels=dim_labels,
                fmt='.0f')

    # Panel 2: Q projection (show Q; mention K, V)
    draw_matrix(axes[0, 1], Q,
                title='2. Q = X W_Q',
                formula='$Q, K, V = X W_Q,\\; X W_K,\\; X W_V$',
                row_labels=TOKENS, col_labels=dim_labels,
                fmt='.0f')

    # Panel 3: Score matrix S = QK^T (4x4)
    draw_matrix(axes[0, 2], S,
                title='3. Scores  S = QK$^T$',
                formula='$S_{ij} = q_i \\cdot k_j$',
                row_labels=TOKENS, col_labels=TOKENS,
                fmt='.0f')

    # Panel 4: After scaling
    draw_matrix(axes[1, 0], S_scaled,
                title=f'4. Scale by $\\sqrt{{d_k}}={np.sqrt(d_k):.2f}$',
                formula='$S / \\sqrt{d_k}$',
                row_labels=TOKENS, col_labels=TOKENS,
                fmt='.1f')

    # Panel 5: After softmax (probabilities)
    draw_matrix(axes[1, 1], A,
                title='5. Softmax (row-wise)',
                formula='$A = \\mathrm{softmax}(S / \\sqrt{d_k})$',
                row_labels=TOKENS, col_labels=TOKENS,
                fmt='.2f', vmin=0, vmax=1)

    # Panel 6: Output
    draw_matrix(axes[1, 2], Out,
                title='6. Output = A V',
                formula='$\\mathrm{Attention}(Q,K,V) = A \\, V$',
                row_labels=TOKENS, col_labels=dim_labels,
                fmt='.1f')

    # Suptitle
    fig.suptitle('Attention: Step by Step',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)

    # Flow arrows between panels (figure-level text)
    for col in range(2):
        x = 0.06 + (col + 1) * (0.90 / 3) + 0.01
        for row in range(2):
            y = 0.86 - row * 0.44 - 0.04
            fig.text(x, y, '\u2192', fontsize=28, color=YELLOW,
                     ha='center', va='center', fontweight='bold')

    # Arrow from row 0 col 2 down to row 1 col 0
    fig.text(0.50, 0.46, '\u2193', fontsize=28, color=YELLOW,
             ha='center', va='center', fontweight='bold')

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
