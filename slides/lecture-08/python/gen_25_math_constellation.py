#!/usr/bin/env python3
"""
Generate slide 25: The Mathematical Universe of AI.

Constellation / network diagram showing 6 mathematical branches feeding into
"Large Language Models" at the centre.  Graph Theory is visually dominant
(larger node, thicker edge, brighter colour).

Output: ../images/25-math-constellation.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '25-math-constellation.png')

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
# Branch definitions
# ---------------------------------------------------------------------------
BRANCHES = [
    # (label, subtitle, colour, radius_scale, edge_width, edge_style)
    ('Graph Theory',             'structure, attention, GNNs',   TEAL,   1.0,  5.0, '-'),
    ('Linear Algebra',           'embeddings, attention',        BLUE,   0.7,  2.5, '-'),
    ('Probability\n& Statistics','distributions, Bayes',         ORANGE, 0.7,  2.5, '-'),
    ('Calculus',                 'gradients, backprop',           RED,    0.7,  2.5, '-'),
    ('Information\nTheory',      'entropy, cross-entropy',       GREEN,  0.7,  2.5, '-'),
    ('Topology',                 'manifolds, latent spaces',     MUTED,  0.5,  1.5, '--'),
]

N_BRANCHES = len(BRANCHES)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    # -- Central node --
    cx, cy = 0.0, 0.0
    central_radius = 0.38

    # Draw glow behind central node
    for r, alpha in [(0.55, 0.04), (0.48, 0.07), (0.42, 0.12)]:
        glow = plt.Circle((cx, cy), r, color=YELLOW, alpha=alpha,
                           transform=ax.transData, zorder=1)
        ax.add_patch(glow)

    central_circle = plt.Circle((cx, cy), central_radius, color=YELLOW,
                                 ec='white', linewidth=2.5, zorder=5)
    ax.add_patch(central_circle)
    ax.text(cx, cy + 0.04, 'Large\nLanguage\nModels', fontsize=20,
            fontweight='bold', color=BG, ha='center', va='center', zorder=6)

    # -- Branch nodes arranged in a circle --
    orbit_r = 1.6
    start_angle = 90  # degrees, top of circle
    angles = [start_angle - i * (360 / N_BRANCHES) for i in range(N_BRANCHES)]

    for i, (label, subtitle, colour, r_scale, ew, estyle) in enumerate(BRANCHES):
        angle_rad = np.radians(angles[i])
        bx = cx + orbit_r * np.cos(angle_rad)
        by = cy + orbit_r * np.sin(angle_rad)

        node_r = 0.22 * r_scale + 0.08

        # Glow for Graph Theory (index 0)
        if i == 0:
            for gr, ga in [(node_r + 0.15, 0.06), (node_r + 0.10, 0.10),
                           (node_r + 0.05, 0.15)]:
                glow = plt.Circle((bx, by), gr, color=colour, alpha=ga,
                                   transform=ax.transData, zorder=1)
                ax.add_patch(glow)

        # Edge connecting branch to centre
        # Compute start/end points on circle borders
        dx, dy = cx - bx, cy - by
        dist = np.hypot(dx, dy)
        ux, uy = dx / dist, dy / dist

        x_start = bx + ux * node_r
        y_start = by + uy * node_r
        x_end = cx - ux * central_radius
        y_end = cy - uy * central_radius

        ax.plot([x_start, x_end], [y_start, y_end],
                color=colour, lw=ew, ls=estyle,
                alpha=0.9 if i == 0 else 0.55, zorder=2)

        # Branch node
        node_circle = plt.Circle((bx, by), node_r, color=colour,
                                  ec='white', linewidth=1.8, zorder=5)
        ax.add_patch(node_circle)

        # Label inside node
        fs = 14 if i == 0 else 11
        ax.text(bx, by, label, fontsize=fs, fontweight='bold',
                color=BG if colour != MUTED else TEXT,
                ha='center', va='center', zorder=6,
                linespacing=0.9)

        # Subtitle outside node
        sub_offset = node_r + 0.18
        sx = bx + ux * (-sub_offset * 1.8)
        sy = by + uy * (-sub_offset * 1.8)
        ax.text(sx, sy, subtitle, fontsize=11, color=MUTED,
                ha='center', va='center', style='italic', zorder=4)

    # -- Decorative stars (small dots) --
    rng = np.random.default_rng(42)
    n_stars = 80
    star_x = rng.uniform(-3.0, 3.0, n_stars)
    star_y = rng.uniform(-2.2, 2.2, n_stars)
    star_s = rng.uniform(0.5, 3.0, n_stars)
    ax.scatter(star_x, star_y, s=star_s, c='white', alpha=0.25, zorder=0)

    # -- Titles --
    fig.suptitle('The Mathematical Universe of AI',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.96)
    fig.text(0.5, 0.03, 'Graph Theory is today\'s thread',
             ha='center', fontsize=23, color=TEAL, fontweight='bold')

    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-2.3, 2.3)
    ax.set_aspect('equal')

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
