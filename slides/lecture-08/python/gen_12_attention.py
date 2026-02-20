#!/usr/bin/env python3
"""
Generate slide 12: Transformer Self-Attention as a Complete Graph.

Six words arranged horizontally with curved arcs above connecting every
pair (15 arcs total for a complete graph). Arc thickness and opacity
encode pre-set attention weights -- strong relationships are bright
yellow, moderate ones blue, and weak ones muted grey.

Output: ../images/12-attention-complete.png (3840x2160, 4K)
"""

import os
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '12-attention-complete.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG        = '#1b2631'
CARD_BG   = '#1e3044'
YELLOW    = '#f1c40f'
BLUE      = '#3498db'
WEAK_CLR  = '#4a5568'
TEXT      = '#ecf0f1'
MUTED     = '#95a5a6'

# ---------------------------------------------------------------------------
# Words and attention weights
# ---------------------------------------------------------------------------
WORDS = ['The', 'cat', 'sat', 'on', 'the', 'mat']
N = len(WORDS)

# Pre-set attention weights (symmetric for visual clarity).
# Key is frozenset of indices.
ATTENTION = {
    frozenset({1, 2}): 0.90,  # cat-sat (strongest)
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


def arc_color(weight):
    """Return colour string based on attention weight."""
    if weight >= 0.5:
        return YELLOW
    elif weight >= 0.3:
        return BLUE
    else:
        return WEAK_CLR


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    fig.suptitle('Self-Attention: Every Word Attends to Every Other',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.93)

    # Word positions along a horizontal line
    x_margin = 1.5
    x_positions = np.linspace(x_margin, 10 - x_margin, N)
    word_y = 1.5  # baseline for words

    # Draw arcs ABOVE the word line
    # Sort pairs by weight so strong arcs are drawn on top
    from matplotlib.path import Path

    pairs = sorted(ATTENTION.items(), key=lambda kv: kv[1])

    for pair_set, weight in pairs:
        i, j = sorted(pair_set)
        x1, x2 = x_positions[i], x_positions[j]

        # Arc height proportional to distance + weight
        # Quadratic Bezier control-point is ~2x the visual apex,
        # so use aggressive scaling to fill vertical space.
        span = abs(x2 - x1)
        height = 1.2 + span * 1.0 + weight * 2.5

        color = arc_color(weight)
        lw = 1.0 + weight * 7.0       # linewidth 1..8
        alpha = 0.15 + weight * 0.75   # alpha 0.15..0.90

        # Draw a quadratic Bezier arc
        mid_x = (x1 + x2) / 2
        arc_top = word_y + height

        verts = [
            (x1, word_y + 0.3),      # start (just above word)
            (mid_x, arc_top),         # control point (peak)
            (x2, word_y + 0.3),       # end
        ]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path = Path(verts, codes)

        patch = mpatches.PathPatch(
            path, facecolor='none', edgecolor=color,
            lw=lw, alpha=alpha, capstyle='round')
        ax.add_patch(patch)

    # Draw word nodes as scatter points (always circular in display space)
    ax.scatter(x_positions, [word_y] * N, s=900, c=BLUE,
               edgecolors='white', linewidths=2.5, zorder=5)

    # Word labels below
    for x, word in zip(x_positions, WORDS):
        ax.text(x, word_y - 0.8, word, fontsize=28, fontweight='bold',
                color=TEXT, ha='center', va='top', zorder=6)

    # Weight legend
    legend_items = [
        mpatches.Patch(color=YELLOW, label='Strong ($w \\geq 0.5$)'),
        mpatches.Patch(color=BLUE, label='Medium ($0.3 \\leq w < 0.5$)'),
        mpatches.Patch(color=WEAK_CLR, label='Weak ($w < 0.3$)'),
    ]
    fig.legend(handles=legend_items, loc='lower center', ncol=3,
               fontsize=17, frameon=False, labelcolor=TEXT,
               handlelength=2.5, bbox_to_anchor=(0.5, 0.04))

    # Compute arc-height function (same formula as drawing code) for annotations
    def _arc_h(i, j, w):
        span = abs(x_positions[j] - x_positions[i])
        return 1.2 + span * 1.0 + w * 2.5

    # Highlighted pair annotations
    # "cat" - "sat" strongest
    cat_sat_mid_x = (x_positions[1] + x_positions[2]) / 2
    cat_sat_h = _arc_h(1, 2, 0.9)
    ax.annotate('Strongest: "cat"-"sat"  $w=0.9$',
                xy=(cat_sat_mid_x, word_y + cat_sat_h * 0.5),
                xytext=(cat_sat_mid_x + 2.0, word_y + cat_sat_h + 1.5),
                fontsize=17, color=YELLOW, ha='center',
                fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=YELLOW, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG,
                          edgecolor=YELLOW, alpha=0.85))

    # "on"-"mat" annotation
    on_mat_mid_x = (x_positions[3] + x_positions[5]) / 2
    on_mat_h = _arc_h(3, 5, 0.7)
    ax.annotate('"on"-"mat"  $w=0.7$',
                xy=(on_mat_mid_x, word_y + on_mat_h * 0.5),
                xytext=(on_mat_mid_x + 1.5, word_y + on_mat_h + 2.0),
                fontsize=15, color=YELLOW, ha='center',
                arrowprops=dict(arrowstyle='->', color=YELLOW, lw=1.2),
                bbox=dict(boxstyle='round,pad=0.25', facecolor=CARD_BG,
                          edgecolor=YELLOW, alpha=0.8))

    # Set axis limits -- remove equal aspect to use full canvas
    max_arc_h = _arc_h(0, 5, 0.15)  # The-mat (widest span)
    ax.set_xlim(-0.3, 10.3)
    ax.set_ylim(-0.2, word_y + max_arc_h + 2.5)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
