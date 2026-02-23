#!/usr/bin/env python3
"""
Generate slide 27: LLM Architecture Cross-Section.

Vertical stack of architectural layers (bottom-to-top), each labelled with
the mathematical domain it relies on.  Side annotation for training maths.

Output: ../images/27-llm-cross-section.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '27-llm-cross-section.png')

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
# Layer definitions (bottom to top)
# ---------------------------------------------------------------------------
LAYERS = [
    # (label,              math_label,                         colour)
    ('Input Tokens',       '',                                 MUTED),
    ('Embedding Layer',    'Linear Algebra',                   BLUE),
    ('Attention \u00d7 N', 'Graph Theory + Linear Algebra',    YELLOW),
    ('Feed-Forward \u00d7 N', 'Function Approximation',        TEAL),
    ('Layer Norm',         'Statistics',                        MUTED),
    ('Output Probabilities', 'Probability (softmax)',           RED),
]


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    n_layers = len(LAYERS)
    box_w = 6.0
    box_h = 1.05
    gap = 0.35
    x_centre = 5.0
    y_start = 0.5  # bottom of first layer

    layer_centres = []  # store (cx, cy) for arrows

    for i, (label, math_label, colour) in enumerate(LAYERS):
        y = y_start + i * (box_h + gap)
        x = x_centre - box_w / 2

        # Main box
        box = FancyBboxPatch(
            (x, y), box_w, box_h,
            boxstyle='round,pad=0.15',
            facecolor=colour, edgecolor='white',
            linewidth=1.5, alpha=0.85, zorder=3)
        ax.add_patch(box)

        # Layer label (inside box)
        cx = x_centre
        cy = y + box_h / 2
        layer_centres.append((cx, cy))

        # Choose text colour for readability
        txt_c = BG if colour in (YELLOW, TEAL, RED, ORANGE) else TEXT
        ax.text(cx, cy, label, fontsize=20, fontweight='bold',
                color=txt_c, ha='center', va='center', zorder=4)

        # Math label (right side)
        if math_label:
            ax.text(x + box_w + 0.4, cy, math_label,
                    fontsize=16, color=colour, ha='left', va='center',
                    style='italic', zorder=4,
                    bbox=dict(boxstyle='round,pad=0.25', facecolor=BG,
                              edgecolor=colour, alpha=0.6, linewidth=1.0))

    # Arrows between layers
    for i in range(n_layers - 1):
        _, y_bot = layer_centres[i]
        _, y_top = layer_centres[i + 1]
        y_arrow_start = y_bot + box_h / 2 + 0.04
        y_arrow_end = y_top - box_h / 2 - 0.04

        ax.annotate('', xy=(x_centre, y_arrow_end),
                    xytext=(x_centre, y_arrow_start),
                    arrowprops=dict(arrowstyle='->', color=TEXT,
                                    lw=2.0, shrinkA=0, shrinkB=0),
                    zorder=2)

    # Side annotation: Training maths
    side_x = x_centre - box_w / 2 - 0.5
    mid_y = y_start + (n_layers - 1) * (box_h + gap) / 2 + box_h / 2

    # Vertical brace approximation: a long bracket on the left
    brace_top = y_start + (n_layers - 1) * (box_h + gap) + box_h + 0.1
    brace_bot = y_start - 0.1

    ax.annotate('',
                xy=(side_x - 0.3, brace_top),
                xytext=(side_x - 0.3, brace_bot),
                arrowprops=dict(arrowstyle='-', color=ORANGE, lw=2.5),
                zorder=2)
    # Tick marks at top and bottom
    for yy in [brace_top, brace_bot]:
        ax.plot([side_x - 0.3, side_x - 0.05], [yy, yy],
                color=ORANGE, lw=2.5, zorder=2)

    ax.text(side_x - 1.8, mid_y,
            'Training:\nCalculus ($\\nabla$)\n+\nInformation\nTheory ($H$)',
            fontsize=16, color=ORANGE, ha='center', va='center',
            fontweight='bold', linespacing=1.4,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=BG,
                      edgecolor=ORANGE, alpha=0.7, linewidth=1.5))

    # Titles
    fig.suptitle('LLM Architecture: A Cross-Section',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)
    fig.text(0.5, 0.02,
             'Every layer is powered by a different branch of mathematics',
             ha='center', fontsize=23, color=MUTED)

    # Axis limits
    ax.set_xlim(-1.5, 13.0)
    ax.set_ylim(-0.5, y_start + n_layers * (box_h + gap) + 0.8)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
