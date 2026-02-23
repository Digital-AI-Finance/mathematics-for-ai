#!/usr/bin/env python3
"""
gen_19_radar_pillars.py
Five-spoke radar/pentagon chart comparing Modern LLM vs Classical Math pre-1950
across the five mathematical pillars.
Output: ../images/19-radar-pillars.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '19-radar-pillars.png')

BG      = '#1b2631'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
TEAL    = '#1abc9c'
ORANGE  = '#e67e22'
RED     = '#e74c3c'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')

    fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG)
    ax = plt.subplot(111, projection='polar')
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)

    # Spoke definitions
    labels = [
        'Linear Algebra',
        'Probability',
        'Calculus',
        'Information Theory',
        'Optimization',
    ]
    spoke_colors = [BLUE, GREEN, ORANGE, TEAL, YELLOW]
    N = len(labels)

    # Compute spoke angles (evenly spaced, starting at top)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    # Close polygon by repeating first angle
    angles_closed = angles + [angles[0]]

    # Data values (0..1 scale)
    llm_vals     = [0.95, 0.90, 0.92, 0.85, 0.88]
    classic_vals = [0.70, 0.50, 0.80, 0.30, 0.20]

    llm_closed     = llm_vals     + [llm_vals[0]]
    classic_closed = classic_vals + [classic_vals[0]]

    # --- Grid circles ---
    for r in [0.25, 0.50, 0.75, 1.00]:
        ax.plot(angles_closed, [r] * (N + 1),
                color='white', alpha=0.12, linewidth=0.8, linestyle='--', zorder=1)

    # --- Grid spokes ---
    for angle in angles:
        ax.plot([angle, angle], [0, 1],
                color='white', alpha=0.12, linewidth=0.8, zorder=1)

    # --- Area 2: Classical Math pre-1950 (back layer) ---
    ax.fill(angles_closed, classic_closed,
            color=ORANGE, alpha=0.25, zorder=2)
    ax.plot(angles_closed, classic_closed,
            color=ORANGE, linewidth=2.5, linestyle='--', zorder=3,
            label='Classical Math pre-1950')

    # --- Area 1: Modern LLM (front layer) ---
    ax.fill(angles_closed, llm_closed,
            color=TEAL, alpha=0.40, zorder=4)
    ax.plot(angles_closed, llm_closed,
            color=TEAL, linewidth=3.0, zorder=5,
            label='Modern LLM')

    # --- Data point markers ---
    ax.scatter(angles, llm_vals,
               color=TEAL, s=80, zorder=6)
    ax.scatter(angles, classic_vals,
               color=ORANGE, s=80, zorder=6)

    # --- Spoke labels with individual colors ---
    ax.set_xticks(angles)
    ax.set_xticklabels([])  # disable default, draw manually

    for angle, label, color in zip(angles, labels, spoke_colors):
        # Nudge labels outward
        r_label = 1.16
        x = r_label * np.cos(np.pi / 2 - angle)
        y = r_label * np.sin(np.pi / 2 - angle)
        ha = 'center'
        va = 'center'
        ax.annotate(
            label,
            xy=(angle, r_label),
            xycoords='data',
            ha=ha, va=va,
            fontsize=22, fontweight='bold',
            color=color,
            annotation_clip=False,
        )

    # --- Radial tick labels (percentage) ---
    ax.set_yticks([0.25, 0.50, 0.75, 1.00])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'],
                       fontsize=13, color=MUTED)
    ax.yaxis.set_tick_params(pad=6)

    # Hide default polar frame lines
    ax.spines['polar'].set_visible(False)
    ax.grid(False)

    # --- Legend ---
    legend = ax.legend(
        loc='upper right',
        bbox_to_anchor=(1.38, 1.18),
        fontsize=22,
        framealpha=0.25,
        facecolor='#2c3e50',
        edgecolor=MUTED,
        labelcolor=TEXT,
    )

    # --- Title ---
    fig.text(
        0.5, 0.97,
        'Five Mathematical Pillars — LLM vs Classical Math',
        ha='center', va='top',
        fontsize=30, fontweight='bold',
        color=TEXT,
    )
    fig.text(
        0.5, 0.925,
        'How much does each pillar matter for modern AI vs. classical work before 1950?',
        ha='center', va='top',
        fontsize=18, fontstyle='italic',
        color=MUTED,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.92])

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
