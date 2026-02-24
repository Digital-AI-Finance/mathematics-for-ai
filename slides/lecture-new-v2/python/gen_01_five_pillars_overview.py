#!/usr/bin/env python3
"""
gen_01_five_pillars_overview.py
Five architectural pillars supporting the beam of AI/LLMs.
Output: ../images/01-five-pillars-overview.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '01-five-pillars-overview.png')

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
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.set_aspect('equal')
    ax.axis('off')

    # Pillar definitions
    pillars = [
        ('Linear\nAlgebra',       'The Skeleton',  BLUE),
        ('Probability\n& Statistics', 'The Output', GREEN),
        ('Calculus &\nOptimization',  'The Teacher', ORANGE),
        ('Information\nTheory',    'The Objective',  TEAL),
        ('Numerical\nOptimization', 'The Scale',    YELLOW),
    ]

    n = len(pillars)
    pillar_w = 10
    pillar_h = 28
    gap = (86 - n * pillar_w) / (n - 1)
    x_start = 7
    floor_y = 5
    pillar_bot = floor_y + 3.5
    beam_y = pillar_bot + pillar_h
    beam_h = 3.5

    # Foundation / floor
    floor = FancyBboxPatch(
        (3, floor_y - 1), 94, 4.5,
        boxstyle='round,pad=0.4', facecolor='#2c3e50', edgecolor=MUTED,
        linewidth=1.5, zorder=1,
    )
    ax.add_patch(floor)
    ax.text(50, floor_y + 1.2, 'Mathematics',
            ha='center', va='center', fontsize=18, fontweight='bold',
            color=TEXT, family='sans-serif', zorder=2)

    # Draw each pillar
    for i, (label, subtitle, color) in enumerate(pillars):
        cx = x_start + i * (pillar_w + gap) + pillar_w / 2
        px = cx - pillar_w / 2

        # Pillar body
        pillar = FancyBboxPatch(
            (px, pillar_bot), pillar_w, pillar_h,
            boxstyle='round,pad=0.6', facecolor=color, edgecolor='white',
            linewidth=1.2, alpha=0.85, zorder=3,
        )
        ax.add_patch(pillar)

        # Capital (top decorative band)
        cap = FancyBboxPatch(
            (px - 0.6, beam_y - 2), pillar_w + 1.2, 2.5,
            boxstyle='round,pad=0.3', facecolor=color, edgecolor='white',
            linewidth=1.0, alpha=0.95, zorder=4,
        )
        ax.add_patch(cap)

        # Base (bottom decorative band)
        base = FancyBboxPatch(
            (px - 0.4, pillar_bot - 0.3), pillar_w + 0.8, 2.2,
            boxstyle='round,pad=0.3', facecolor=color, edgecolor='white',
            linewidth=1.0, alpha=0.95, zorder=4,
        )
        ax.add_patch(base)

        # Pillar label
        ax.text(cx, pillar_bot + pillar_h / 2 + 1, label,
                ha='center', va='center', fontsize=13, fontweight='bold',
                color='white', family='sans-serif', zorder=5,
                linespacing=1.3)

        # Subtitle below pillar label
        ax.text(cx, pillar_bot + pillar_h / 2 - 4.5,
                f'"{subtitle}"',
                ha='center', va='center', fontsize=10, fontstyle='italic',
                color='#ffffffcc', family='sans-serif', zorder=5)

    # Beam / entablature
    beam = FancyBboxPatch(
        (2, beam_y + 0.5), 96, beam_h,
        boxstyle='round,pad=0.5', facecolor='#34495e', edgecolor=TEXT,
        linewidth=2, zorder=6,
    )
    ax.add_patch(beam)
    ax.text(50, beam_y + beam_h / 2 + 0.5, 'LLMs  /  Artificial Intelligence',
            ha='center', va='center', fontsize=22, fontweight='bold',
            color=YELLOW, family='sans-serif', zorder=7)

    # Pediment / triangle on top
    tri_bot = beam_y + beam_h + 0.5
    tri_top = tri_bot + 6
    triangle_x = [5, 50, 95]
    triangle_y = [tri_bot, tri_top, tri_bot]
    ax.fill(triangle_x, triangle_y, color='#2c3e50', edgecolor=TEXT,
            linewidth=1.5, zorder=6)

    # Title inside pediment
    ax.text(50, tri_bot + 2.8, 'The Five Mathematical Pillars of AI',
            ha='center', va='center', fontsize=20, fontweight='bold',
            color=TEXT, family='sans-serif', zorder=7)

    # Subtitle at very bottom
    ax.text(50, 1.5,
            'Each pillar was developed by brilliant minds who had no idea their work would power AI',
            ha='center', va='center', fontsize=12, fontstyle='italic',
            color=MUTED, family='sans-serif', zorder=2)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
