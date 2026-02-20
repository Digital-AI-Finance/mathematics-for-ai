#!/usr/bin/env python3
"""
gen_17_timeline.py
300-year timeline from Euler (1736) to GNNs (2020s).

Horizontal bezier curve with 8 milestone dots, colored by type.
Names above the line, years below. Dots sized by recency/impact.
Subtle gradient glow behind the curve.

Output: ../images/17-timeline-chain.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '17-timeline-chain.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG      = '#1b2631'
CARD_BG = '#1e3044'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
TEAL    = '#1abc9c'
ORANGE  = '#e67e22'
RED     = '#e74c3c'
PURPLE  = '#9b59b6'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'

# ---------------------------------------------------------------------------
# Milestones
# ---------------------------------------------------------------------------
# (x_position, display_year, name, color, size_factor)
# Using explicit x-positions to ensure even visual spacing across the slide.
MILESTONES = [
    (1.5,  '1736',           'Euler\nK\u00f6nigsberg Bridges',       ORANGE, 1.0),
    (3.8,  '1857',           'Cayley\nTree Enumeration',             GREEN,  1.0),
    (6.1,  '1959',           'Erd\u0151s-R\u00e9nyi\nRandom Graphs', YELLOW, 1.2),
    (8.2,  '1998',           'Watts-Strogatz\nSmall Worlds',         GREEN,  1.3),
    (10.3, '1998',           'Brin & Page\nPageRank',                BLUE,   1.5),
    (12.4, '2012\u20132017', 'NN Architectures\nCNN/RNN/Transformer', BLUE,  1.6),
    (14.5, '2012\u20132024', 'Knowledge\nGraphs',                    BLUE,   1.5),
    (16.8, '2020\u20132024', 'Graph Neural\nNetworks',               BLUE,   1.8),
]


def cubic_bezier(p0, p1, p2, p3, t):
    """Evaluate cubic bezier at parameter t (array)."""
    t = np.asarray(t)
    return ((1 - t)**3 * np.array(p0)[:, None]
            + 3 * (1 - t)**2 * t * np.array(p1)[:, None]
            + 3 * (1 - t) * t**2 * np.array(p2)[:, None]
            + t**3 * np.array(p3)[:, None])


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(3840 / 200, 2160 / 200), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.5, 19.0)
    ax.set_ylim(-2.5, 6.5)
    ax.axis('off')

    # x positions come directly from the milestone definitions
    xs = [m[0] for m in MILESTONES]
    y_line = 2.0  # vertical position of the timeline

    # Draw the flowing bezier curve through the timeline
    # Control points for a gentle S-curve
    p0 = (xs[0] - 1.5, y_line)
    p1 = (xs[2], y_line + 0.6)
    p2 = (xs[5], y_line - 0.6)
    p3 = (xs[-1] + 1.5, y_line)

    t_vals = np.linspace(0, 1, 500)
    curve = cubic_bezier(p0, p1, p2, p3, t_vals)

    # Glow effect: multiple passes with decreasing alpha and increasing width
    glow_widths = [28, 20, 14, 8, 4]
    glow_alphas = [0.03, 0.06, 0.10, 0.18, 0.35]
    glow_color = BLUE
    for w, a in zip(glow_widths, glow_alphas):
        ax.plot(curve[0], curve[1], color=glow_color, linewidth=w,
                alpha=a, solid_capstyle='round', zorder=1)

    # Main curve line
    ax.plot(curve[0], curve[1], color=TEXT, linewidth=2.5,
            alpha=0.5, solid_capstyle='round', zorder=2)

    # Function to get y on bezier at a given x (approximate)
    def bezier_y_at_x(target_x):
        dists = np.abs(curve[0] - target_x)
        idx = np.argmin(dists)
        return curve[1][idx]

    # Draw milestones
    for i, (x_pos, year_label, name, color, size_fac) in enumerate(MILESTONES):
        x = xs[i]
        y_base = bezier_y_at_x(x)

        dot_size = 140 * size_fac

        # Glow behind dot
        ax.plot(x, y_base, 'o', color=color, markersize=np.sqrt(dot_size) * 1.6,
                alpha=0.15, zorder=3)
        ax.plot(x, y_base, 'o', color=color, markersize=np.sqrt(dot_size) * 1.2,
                alpha=0.25, zorder=3)

        # Dot
        ax.plot(x, y_base, 'o', color=color, markersize=np.sqrt(dot_size),
                markeredgecolor='white', markeredgewidth=1.5, zorder=5)

        # Vertical stem
        stem_top = y_base + 0.3
        stem_bot = y_base - 0.3
        ax.plot([x, x], [stem_top, stem_top + 0.15], color=MUTED,
                linewidth=1.0, alpha=0.5, zorder=4)
        ax.plot([x, x], [stem_bot, stem_bot - 0.15], color=MUTED,
                linewidth=1.0, alpha=0.5, zorder=4)

        # Name ABOVE the line
        ax.text(
            x, y_base + 0.85, name,
            fontsize=11, fontweight='bold', color=TEXT,
            ha='center', va='bottom', zorder=6,
            linespacing=1.3,
            path_effects=[pe.withStroke(linewidth=3, foreground=BG)],
        )

        # Year BELOW the line
        ax.text(
            x, y_base - 0.75, year_label,
            fontsize=11, color=color, fontweight='bold',
            ha='center', va='top', zorder=6,
            path_effects=[pe.withStroke(linewidth=3, foreground=BG)],
        )

    # Color legend
    legend_items = [
        (ORANGE, 'Origin'),
        (GREEN,  'Discovery'),
        (YELLOW, 'Breakthrough'),
        (BLUE,   'AI Connection'),
    ]
    lx_start = 2.0
    ly = -1.5
    for i, (col, label) in enumerate(legend_items):
        lx = lx_start + i * 3.5
        ax.plot(lx, ly, 'o', color=col, markersize=10, zorder=8)
        ax.text(lx + 0.35, ly, label, fontsize=12, color=TEXT,
                va='center', zorder=8)

    # Title
    ax.set_title(
        '300 Years of Connection Mathematics',
        fontsize=32, fontweight='bold', color=TEXT, pad=28,
    )

    # Subtitle
    ax.text(
        9.25, -2.1,
        'From Euler\'s bridges to modern Graph Neural Networks',
        fontsize=15, color=MUTED, ha='center', va='center', style='italic',
    )

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
