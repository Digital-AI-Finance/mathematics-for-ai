#!/usr/bin/env python3
"""
Generate slide 29: The Five Pillars of AI Mathematics.

Five classical pillars supporting a horizontal beam labelled "AI / LLMs".
Graph Theory pillar is taller and brighter to mark today's focus.

Output: ../images/29-five-pillars.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '29-five-pillars.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG      = '#1b2631'
YELLOW  = '#f1c40f'
BLUE    = '#3498db'
TEAL    = '#2ecc71'
RED     = '#e74c3c'
ORANGE  = '#e67e22'
GREEN   = '#2ecc71'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'

# ---------------------------------------------------------------------------
# Pillar definitions
# ---------------------------------------------------------------------------
PILLARS = [
    # (name,              one_word,        colour, is_highlighted)
    ('Graph\nTheory',     'Structure',     TEAL,   True),
    ('Linear\nAlgebra',   'Transformation', BLUE,   False),
    ('Probability',       'Uncertainty',    ORANGE, False),
    ('Calculus',          'Optimisation',   RED,    False),
    ('Information\nTheory', 'Communication', GREEN,  False),
]


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    n = len(PILLARS)
    pillar_w = 1.6
    spacing = 2.6
    total_w = (n - 1) * spacing + pillar_w
    x_start = (10 - total_w) / 2  # centre the group in a 0-10 x range

    base_y = 1.0         # bottom of pillars
    normal_h = 4.5        # normal pillar height
    highlight_h = 5.2     # highlighted (Graph Theory) pillar height
    cap_h = 0.35          # capital (rounded top) height
    beam_h = 0.6          # horizontal beam thickness

    # Determine beam y (top of tallest pillar + cap)
    beam_y = base_y + highlight_h + cap_h

    # -- Foundation / floor --
    floor = FancyBboxPatch(
        (x_start - 0.5, base_y - 0.35), total_w + 1.0, 0.3,
        boxstyle='round,pad=0.05',
        facecolor='#2c3e50', edgecolor=MUTED, linewidth=1.5,
        alpha=0.7, zorder=2)
    ax.add_patch(floor)
    ax.text(x_start + total_w / 2, base_y - 0.55, 'Mathematics',
            fontsize=20, color=MUTED, ha='center', va='top',
            fontweight='bold', style='italic')

    # -- Draw each pillar --
    for i, (name, one_word, colour, highlight) in enumerate(PILLARS):
        cx = x_start + i * spacing + pillar_w / 2
        px = x_start + i * spacing
        ph = highlight_h if highlight else normal_h

        # Glow behind highlighted pillar
        if highlight:
            for gw, ga in [(0.25, 0.04), (0.15, 0.07), (0.08, 0.12)]:
                glow = FancyBboxPatch(
                    (px - gw, base_y - gw), pillar_w + 2 * gw, ph + cap_h + 2 * gw,
                    boxstyle='round,pad=0.1',
                    facecolor=colour, edgecolor='none',
                    alpha=ga, zorder=1)
                ax.add_patch(glow)

        # Pillar shaft
        shaft = FancyBboxPatch(
            (px, base_y), pillar_w, ph,
            boxstyle='round,pad=0.05',
            facecolor=colour, edgecolor='white',
            linewidth=1.5 if not highlight else 2.5,
            alpha=0.85 if not highlight else 1.0,
            zorder=3)
        ax.add_patch(shaft)

        # Capital (rounded top piece)
        cap = FancyBboxPatch(
            (px - 0.15, base_y + ph), pillar_w + 0.3, cap_h,
            boxstyle='round,pad=0.08',
            facecolor=colour, edgecolor='white',
            linewidth=1.2, alpha=0.9, zorder=3)
        ax.add_patch(cap)

        # Pillar name (inside, vertical centre)
        txt_c = BG if colour in (YELLOW, TEAL, GREEN, ORANGE) else TEXT
        fs = 17 if highlight else 15
        ax.text(cx, base_y + ph / 2, name, fontsize=fs,
                fontweight='bold', color=txt_c,
                ha='center', va='center', zorder=4,
                linespacing=0.9)

        # One-word description below pillar
        ax.text(cx, base_y - 0.75, one_word, fontsize=14,
                color=colour, ha='center', va='top',
                fontweight='bold')

        # Star marker for highlighted pillar
        if highlight:
            ax.text(cx, base_y + ph + cap_h + 0.15, '\u2605',
                    fontsize=22, color=YELLOW, ha='center', va='bottom',
                    zorder=5)

    # -- Horizontal beam --
    beam = FancyBboxPatch(
        (x_start - 0.6, beam_y), total_w + 1.2, beam_h,
        boxstyle='round,pad=0.1',
        facecolor=YELLOW, edgecolor='white',
        linewidth=2.0, alpha=0.95, zorder=4)
    ax.add_patch(beam)

    ax.text(x_start + total_w / 2, beam_y + beam_h / 2,
            'AI  /  LLMs', fontsize=24, fontweight='bold',
            color=BG, ha='center', va='center', zorder=5)

    # -- Titles --
    fig.suptitle('The Five Pillars of AI Mathematics',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)
    fig.text(0.5, 0.02,
             'Graph Theory was today\'s focus \u2014 '
             'but every pillar is essential',
             ha='center', fontsize=23, color=TEAL, fontweight='bold')

    # Axis limits
    ax.set_xlim(-1.0, 11.0)
    ax.set_ylim(-1.0, beam_y + beam_h + 1.5)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
