#!/usr/bin/env python3
"""
gen_07_shannon_diagram.py
Two parallel flow diagrams: Shannon 1948 vs LLM 2024.
Boxes connected by arrows, dashed lines linking corresponding stages.
Output: ../images/07-shannon-diagram.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '07-shannon-diagram.png')

BG = '#1b2631'; BLUE = '#3498db'; YELLOW = '#f1c40f'; GREEN = '#2ecc71'; TEAL = '#1abc9c'
ORANGE = '#e67e22'; RED = '#e74c3c'; TEXT = '#ecf0f1'; MUTED = '#95a5a6'


def draw_flow_row(ax, boxes, y_center, color, row_label):
    """Draw a horizontal row of boxes with arrows between them."""
    n = len(boxes)
    box_w = 2.4
    box_h = 1.4
    gap = 1.0
    total_w = n * box_w + (n - 1) * gap
    x_start = (16 - total_w) / 2

    centers = []
    for i, label in enumerate(boxes):
        cx = x_start + i * (box_w + gap) + box_w / 2
        cy = y_center
        centers.append((cx, cy))

        box = FancyBboxPatch(
            (cx - box_w / 2, cy - box_h / 2), box_w, box_h,
            boxstyle='round,pad=0.2',
            facecolor=color, edgecolor='white',
            linewidth=2.0, alpha=0.88, zorder=3)
        ax.add_patch(box)

        # Text color: dark for bright backgrounds
        txt_c = BG if color in (YELLOW, TEAL, GREEN, ORANGE) else TEXT
        ax.text(cx, cy, label, fontsize=13, fontweight='bold',
                color=txt_c, ha='center', va='center', zorder=4,
                linespacing=1.1)

    # Arrows between consecutive boxes
    for i in range(n - 1):
        x1 = centers[i][0] + box_w / 2 + 0.08
        x2 = centers[i + 1][0] - box_w / 2 - 0.08
        arrow = FancyArrowPatch(
            (x1, y_center), (x2, y_center),
            arrowstyle='->', color=TEXT, lw=2.5,
            mutation_scale=18, zorder=5)
        ax.add_patch(arrow)

    # Row year label above the first box
    first_cx = centers[0][0]
    ax.text(first_cx, y_center + box_h / 2 + 0.35, row_label,
            fontsize=20, fontweight='bold',
            color=color, ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                      edgecolor=color, alpha=0.85, linewidth=2),
            zorder=6)

    return centers, box_w, box_h


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    # Shannon row (top)
    shannon_boxes = ['Information\nSource', 'Transmitter', 'Channel',
                     'Receiver', 'Destination']
    y_top = 6.5
    top_centers, bw, bh = draw_flow_row(
        ax, shannon_boxes, y_top, TEAL, '1948')

    # Noise source pointing into Channel (box index 2)
    noise_x = top_centers[2][0]
    noise_y = y_top + bh / 2 + 1.8
    noise_box = FancyBboxPatch(
        (noise_x - 1.2, noise_y - 0.5), 2.4, 1.0,
        boxstyle='round,pad=0.15',
        facecolor=RED, edgecolor='white',
        linewidth=1.5, alpha=0.85, zorder=3)
    ax.add_patch(noise_box)
    ax.text(noise_x, noise_y, 'Noise\nSource', fontsize=12, fontweight='bold',
            color=TEXT, ha='center', va='center', zorder=4)
    # Arrow from noise down into channel
    noise_arrow = FancyArrowPatch(
        (noise_x, noise_y - 0.5), (noise_x, y_top + bh / 2 + 0.08),
        arrowstyle='->', color=RED, lw=2.5,
        mutation_scale=16, zorder=5)
    ax.add_patch(noise_arrow)

    # LLM row (bottom)
    llm_boxes = ['Your\nPrompt', 'Tokenizer', 'Transformer', 'Detokenizer',
                 'Response']
    y_bot = 2.2
    bot_centers, _, _ = draw_flow_row(
        ax, llm_boxes, y_bot, YELLOW, '2024')

    # Dashed lines connecting corresponding boxes
    for i in range(len(top_centers)):
        tc = top_centers[i]
        bc = bot_centers[i]
        ax.plot([tc[0], bc[0]], [tc[1] - bh / 2, bc[1] + bh / 2],
                ls='--', color=MUTED, lw=1.5, alpha=0.5, zorder=1)

    # Title
    fig.suptitle("Shannon's Model  \u2192  The LLM Pipeline",
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)
    fig.text(0.5, 0.91,
             'The same architecture, 75 years apart',
             ha='center', fontsize=22, color=MUTED, style='italic')

    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(0, 10)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
