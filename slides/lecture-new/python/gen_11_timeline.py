#!/usr/bin/env python3
"""
gen_11_timeline.py
2000 Years of Mathematics → AI: horizontal timeline from ~100 BCE to 2024.
Output: ../images/11-timeline.png
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '11-timeline.png')

BG     = '#1b2631'
BLUE   = '#3498db'
YELLOW = '#f1c40f'
GREEN  = '#2ecc71'
TEAL   = '#1abc9c'
ORANGE = '#e67e22'
RED    = '#e74c3c'
TEXT   = '#ecf0f1'
MUTED  = '#95a5a6'

# Each milestone: (year, label_line1, label_line2, color)
# Colors map to pillar: Linear Algebra=BLUE, Probability=GREEN,
#   Calculus/Optim=ORANGE, Info Theory=TEAL, Numerical Optim=YELLOW
MILESTONES = [
    (-100, 'Fangcheng',             'Chinese Linear Algebra',     BLUE),
    (1654, 'Pascal & Fermat',       'Probability letters',        GREEN),
    (1666, "Newton's Calculus",     'Fluxions (unpublished)',     ORANGE),
    (1684, 'Leibniz Calculus',      'Nova Methodus published',    ORANGE),
    (1736, 'Euler Bridges',         'Graph / topology born',      TEAL),
    (1763, "Bayes' Theorem",        'Published posthumously',     GREEN),
    (1844, 'Grassmann',             'Extension Theory (vectors)', BLUE),
    (1847, 'Cauchy',                'Gradient descent method',    YELLOW),
    (1858, 'Cayley',                'Matrix algebra paper',       BLUE),
    (1933, 'Kolmogorov',            'Probability axioms',         GREEN),
    (1948, 'Shannon',               'Information Theory paper',   TEAL),
    (1951, 'Robbins-Monro',         'Stochastic gradient desc.',  YELLOW),
    (1986, 'Backpropagation',       'Hinton et al.',              ORANGE),
    (2014, 'Adam Optimizer',        'Kingma & Ba',                YELLOW),
    (2017, 'Attention Is All',      'Transformer paper',          TEAL),
    (2020, 'Scaling Laws',          'Kaplan et al.',              ORANGE),
    (2022, 'ChatGPT',               'OpenAI launches',            RED),
    (2024, 'Hinton Nobel Prize',    'Physics Prize for DL',       RED),
]


def year_to_x(year, x_min, x_max, y_min=-100, y_max=2024):
    """Map a year to an x-coordinate using a piecewise scale.
    BCE to 1600 is compressed; 1600-2024 is expanded.
    """
    pivot = 1600
    pivot_frac = 0.18   # 18% of the width goes to the long ancient period
    if year <= pivot:
        t = (year - y_min) / (pivot - y_min)
        return x_min + t * (x_max - x_min) * pivot_frac
    else:
        t = (year - pivot) / (y_max - pivot)
        return x_min + pivot_frac * (x_max - x_min) + t * (x_max - x_min) * (1 - pivot_frac)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # --- Title ---
    ax.text(50, 94, '2000 Years of Mathematics  →  AI',
            ha='center', va='center', fontsize=26, fontweight='bold',
            color=TEXT, family='sans-serif')
    ax.text(50, 89.5,
            'Key milestones that built the mathematical foundation of modern AI',
            ha='center', va='center', fontsize=14, color=MUTED,
            family='sans-serif', fontstyle='italic')

    # --- Timeline baseline ---
    tl_y   = 48          # vertical centre of the timeline track
    x_left = 4
    x_right = 97

    ax.plot([x_left, x_right], [tl_y, tl_y],
            color=MUTED, linewidth=2.5, zorder=2, solid_capstyle='round')

    # Arrow head at right end
    ax.annotate('', xy=(x_right + 0.5, tl_y),
                xytext=(x_right - 0.1, tl_y),
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=2.0))

    # --- Axis tick labels (century marks) ---
    century_years = [1, 500, 1000, 1500, 1600, 1700, 1800, 1900, 1950, 2000, 2024]
    century_labels = ['1 CE', '500', '1000', '1500', '1600', '1700', '1800', '1900', '1950', '2000', '2024']
    for yr, lbl in zip(century_years, century_labels):
        cx = year_to_x(yr, x_left, x_right)
        ax.plot([cx, cx], [tl_y - 1.0, tl_y + 1.0],
                color=MUTED, linewidth=0.8, zorder=2)
        ax.text(cx, tl_y - 2.5, lbl,
                ha='center', va='top', fontsize=7, color=MUTED,
                family='monospace')

    # Label far left
    ax.text(year_to_x(-100, x_left, x_right) - 0.5, tl_y - 2.5,
            '~100 BCE', ha='center', va='top', fontsize=7,
            color=MUTED, family='monospace')

    # --- Plot milestones ---
    # Alternate labels above (odd index) and below (even index)
    above_y_base = tl_y + 6
    below_y_base = tl_y - 6
    stem_above   = 5.0
    stem_below   = 5.0
    label_spacing_above = 6.5
    label_spacing_below = 6.5

    for idx, (year, line1, line2, color) in enumerate(MILESTONES):
        x = year_to_x(year, x_left, x_right)
        above = (idx % 2 == 0)

        # Dot on timeline
        ax.plot(x, tl_y, 'o', markersize=9, color=color,
                markeredgecolor='white', markeredgewidth=0.8, zorder=5)

        if above:
            stem_end = tl_y + stem_above
            label_y  = above_y_base + (idx // 2) * label_spacing_above
            # clamp to figure top
            label_y  = min(label_y, 85)
            connector_y = label_y - 2.8
            ax.annotate('',
                        xy=(x, stem_end),
                        xytext=(x, tl_y + 1.5),
                        arrowprops=dict(arrowstyle='-', color=color,
                                        lw=1.2, linestyle='dotted'))
            ax.plot([x, x], [stem_end, connector_y],
                    color=color, linewidth=1.0, linestyle=':', zorder=3)
        else:
            stem_end = tl_y - stem_below
            label_y  = below_y_base - (idx // 2) * label_spacing_below
            label_y  = max(label_y, 5)
            connector_y = label_y + 4.0
            ax.plot([x, x], [tl_y - 1.5, connector_y],
                    color=color, linewidth=1.0, linestyle=':', zorder=3)

        # Year badge
        ax.text(x, label_y + 3.2,
                f'{abs(year)}{"" if year > 0 else " BCE"}',
                ha='center', va='bottom', fontsize=8.5,
                color=color, fontweight='bold', family='sans-serif')
        # Line 1
        ax.text(x, label_y + 1.2, line1,
                ha='center', va='bottom', fontsize=9.5,
                color=TEXT, fontweight='bold', family='sans-serif')
        # Line 2
        ax.text(x, label_y - 0.5, line2,
                ha='center', va='bottom', fontsize=8,
                color=MUTED, family='sans-serif')

    # --- Legend (pillar color key) ---
    legend_items = [
        mpatches.Patch(color=BLUE,   label='Linear Algebra'),
        mpatches.Patch(color=GREEN,  label='Probability & Statistics'),
        mpatches.Patch(color=ORANGE, label='Calculus & Optimization'),
        mpatches.Patch(color=TEAL,   label='Information Theory'),
        mpatches.Patch(color=YELLOW, label='Numerical Optimization'),
        mpatches.Patch(color=RED,    label='AI Milestone'),
    ]
    leg = ax.legend(handles=legend_items, loc='lower center',
                    ncol=6, fontsize=10,
                    facecolor='#2c3e50', edgecolor=MUTED,
                    labelcolor=TEXT, framealpha=0.9,
                    bbox_to_anchor=(0.5, -0.01))

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
