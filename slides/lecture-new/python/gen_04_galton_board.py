#!/usr/bin/env python3
"""
gen_04_galton_board.py
Galton board (quincunx) with pegs, falling balls, histogram, and bell curve.
Output: ../images/04-galton-board.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '04-galton-board.png')

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
    ax.set_xlim(-12, 12)
    ax.set_ylim(-10, 14)
    ax.set_aspect('equal')
    ax.axis('off')

    # --- Peg array ---
    n_rows = 11
    peg_radius = 0.18
    row_spacing_y = 1.3
    peg_top_y = 12.0

    peg_positions = []
    for row in range(n_rows):
        n_pegs = row + 1
        y = peg_top_y - row * row_spacing_y
        for col in range(n_pegs):
            x = (col - row / 2.0) * 1.4
            peg_positions.append((x, y))
            peg = Circle((x, y), peg_radius, facecolor='#5d6d7e',
                         edgecolor='#85929e', linewidth=0.6, zorder=3)
            ax.add_patch(peg)

    # --- Simulate falling balls for the histogram ---
    rng = np.random.RandomState(123)
    n_balls = 3000
    final_positions = []
    for _ in range(n_balls):
        x = 0.0
        for row in range(n_rows):
            x += rng.choice([-0.7, 0.7])
        final_positions.append(x)
    final_positions = np.array(final_positions)

    # Histogram bins
    n_bins = n_rows + 1
    bin_edges = np.linspace(-0.7 * n_rows - 0.7, 0.7 * n_rows + 0.7, n_bins + 1)
    counts, _ = np.histogram(final_positions, bins=bin_edges)
    max_count = counts.max()

    # Draw histogram as stacked circles (like real Galton board)
    hist_base_y = -9.5
    ball_r = 0.32
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    for i, (cx, count) in enumerate(zip(bin_centers, counts)):
        n_show = int(count / max_count * 18)  # scale to fit
        for j in range(n_show):
            by = hist_base_y + j * (ball_r * 2.05)
            # Color gradient from blue at bottom to teal at top
            t = j / max(n_show - 1, 1)
            r_c = int(52 + t * (26 - 52))
            g_c = int(152 + t * (188 - 152))
            b_c = int(219 + t * (156 - 219))
            color = f'#{r_c:02x}{g_c:02x}{b_c:02x}'
            ball = Circle((cx, by), ball_r, facecolor=color,
                          edgecolor='white', linewidth=0.3, alpha=0.8, zorder=4)
            ax.add_patch(ball)

    # --- Bell curve overlay ---
    mu = np.mean(final_positions)
    sigma = np.std(final_positions)
    x_curve = np.linspace(-10, 10, 300)
    y_curve = np.exp(-0.5 * ((x_curve - mu) / sigma) ** 2)
    # Scale to match histogram height
    y_curve = y_curve / y_curve.max() * 18 * ball_r * 2.05
    y_curve += hist_base_y
    ax.plot(x_curve, y_curve, color=YELLOW, linewidth=2.5, alpha=0.9,
            zorder=6, linestyle='--')

    # --- A few balls mid-fall ---
    mid_balls = [
        (0.0, 13.0),     # at the very top (entry)
        (-0.3, 10.5),    # between rows 1-2
        (0.7, 8.8),      # between rows 2-3
        (-1.4, 6.5),     # mid-board
        (1.0, 4.2),      # lower-mid
        (-0.5, 2.0),     # near bottom of pegs
        (2.1, 0.5),      # just exited pegs
    ]
    for bx, by in mid_balls:
        ball = Circle((bx, by), 0.28, facecolor=ORANGE,
                      edgecolor='white', linewidth=1.2, alpha=0.95, zorder=7)
        ax.add_patch(ball)

    # --- Funnel at top ---
    funnel_x = [-2, -0.4, 0.4, 2]
    funnel_y = [14.2, 13.0, 13.0, 14.2]
    ax.fill(funnel_x, funnel_y, color='#2c3e50', edgecolor=MUTED,
            linewidth=1.5, zorder=2)

    # --- Board outline (triangular) ---
    board_left = -0.7 * n_rows - 1.5
    board_right = 0.7 * n_rows + 1.5
    board_top = peg_top_y + 1.0
    board_bottom_y = peg_top_y - (n_rows - 1) * row_spacing_y - 1.0
    # Side walls
    ax.plot([board_left, -0.5], [board_bottom_y, board_top],
            color=MUTED, linewidth=1.5, alpha=0.5, zorder=2)
    ax.plot([board_right, 0.5], [board_bottom_y, board_top],
            color=MUTED, linewidth=1.5, alpha=0.5, zorder=2)
    # Bottom separator
    ax.plot([board_left, board_right], [board_bottom_y, board_bottom_y],
            color=MUTED, linewidth=1.0, alpha=0.4, zorder=2)

    # --- Bin dividers ---
    for edge in bin_edges:
        ax.plot([edge, edge], [hist_base_y - 0.5, board_bottom_y],
                color=MUTED, linewidth=0.5, alpha=0.3, zorder=1)

    # --- Labels ---
    ax.text(0, 14.8, 'The Galton Board: Randomness Creates Order',
            ha='center', va='center', fontsize=22, fontweight='bold',
            color=TEXT, family='sans-serif', zorder=8)

    ax.text(0, -10.2,
            'Individual events are random, but the aggregate is predictable',
            ha='center', va='center', fontsize=13, fontstyle='italic',
            color=MUTED, family='sans-serif', zorder=8)

    # Bell curve label
    ax.text(7.5, hist_base_y + 10,
            'Normal\nDistribution', ha='center', va='center',
            fontsize=12, fontweight='bold', color=YELLOW,
            family='sans-serif', zorder=8,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#2c3e50',
                      edgecolor=YELLOW, alpha=0.8))

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
