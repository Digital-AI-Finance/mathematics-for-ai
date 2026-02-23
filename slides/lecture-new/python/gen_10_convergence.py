#!/usr/bin/env python3
"""
gen_10_convergence.py
Simplified transformer block diagram with five colored pillar annotations.
Vertical stack: Input -> Embedding -> Attention -> FeedForward -> Softmax -> Loss
Left bracket for Backprop (Calculus) + Adam (Numerical Opt.).
Output: ../images/10-convergence.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '10-convergence.png')

BG = '#1b2631'; BLUE = '#3498db'; YELLOW = '#f1c40f'; GREEN = '#2ecc71'; TEAL = '#1abc9c'
ORANGE = '#e67e22'; RED = '#e74c3c'; TEXT = '#ecf0f1'; MUTED = '#95a5a6'


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    # Layer definitions (bottom to top)
    # (label, color, pillar_annotation, annotation_color)
    layers = [
        ('Input Tokens',        MUTED,  None,                         None),
        ('Embedding',           BLUE,   'Linear Algebra',             BLUE),
        ('Multi-Head\nAttention', YELLOW, 'Linear Algebra\n+ Probability', YELLOW),
        ('Feed-Forward',        TEAL,   'Linear Algebra',             TEAL),
        ('Softmax Output',      GREEN,  'Probability',                GREEN),
        ('Loss:\nCross-Entropy', RED,   'Information Theory',         RED),
    ]

    n = len(layers)
    box_w = 6.5
    box_h = 1.15
    gap = 0.50
    x_center = 7.5
    y_start = 0.8

    layer_positions = []  # (cx, cy)

    for i, (label, color, annotation, ann_color) in enumerate(layers):
        cx = x_center
        cy = y_start + i * (box_h + gap)
        layer_positions.append((cx, cy))

        # Main box
        box = FancyBboxPatch(
            (cx - box_w / 2, cy - box_h / 2), box_w, box_h,
            boxstyle='round,pad=0.18',
            facecolor=color, edgecolor='white',
            linewidth=2.0, alpha=0.88, zorder=3)
        ax.add_patch(box)

        # Layer label inside box
        txt_c = BG if color in (YELLOW, TEAL, GREEN, ORANGE, RED) else TEXT
        ax.text(cx, cy, label, fontsize=17, fontweight='bold',
                color=txt_c, ha='center', va='center', zorder=4,
                linespacing=1.0)

        # Right-side pillar annotation
        if annotation:
            ann_x = cx + box_w / 2 + 0.6
            ax.annotate(
                annotation,
                xy=(cx + box_w / 2, cy),
                xytext=(ann_x + 2.0, cy),
                fontsize=15, fontweight='bold', color=ann_color,
                ha='left', va='center',
                arrowprops=dict(arrowstyle='->', color=ann_color,
                                lw=2.0, shrinkA=0, shrinkB=5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                          edgecolor=ann_color, alpha=0.7, linewidth=1.5),
                zorder=5)

    # Upward arrows between layers
    for i in range(n - 1):
        _, y_bot = layer_positions[i]
        _, y_top = layer_positions[i + 1]
        arrow = FancyArrowPatch(
            (x_center, y_bot + box_h / 2 + 0.06),
            (x_center, y_top - box_h / 2 - 0.06),
            arrowstyle='->', color=TEXT, lw=2.5,
            mutation_scale=18, zorder=2)
        ax.add_patch(arrow)

    # Left side bracket for training components
    bracket_x = x_center - box_w / 2 - 0.8
    bracket_top = layer_positions[-1][1] + box_h / 2 + 0.15
    bracket_bot = layer_positions[0][1] - box_h / 2 - 0.15

    # Vertical bracket line
    ax.plot([bracket_x, bracket_x], [bracket_bot, bracket_top],
            color=ORANGE, lw=3.0, zorder=2)
    # Tick marks
    for yy in [bracket_bot, bracket_top]:
        ax.plot([bracket_x, bracket_x + 0.3], [yy, yy],
                color=ORANGE, lw=3.0, zorder=2)

    # Training annotation labels
    mid_y = (bracket_top + bracket_bot) / 2
    label_x = bracket_x - 2.8

    ax.text(label_x, mid_y + 0.9, 'Backpropagation',
            fontsize=17, fontweight='bold', color=ORANGE,
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor=BG,
                      edgecolor=ORANGE, alpha=0.8, linewidth=1.5),
            zorder=5)
    ax.text(label_x, mid_y + 0.1, '(Calculus)', fontsize=14,
            color=ORANGE, ha='center', va='center', style='italic',
            zorder=5)

    ax.text(label_x, mid_y - 1.4, 'Adam Optimizer',
            fontsize=17, fontweight='bold', color=YELLOW,
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor=BG,
                      edgecolor=YELLOW, alpha=0.8, linewidth=1.5),
            zorder=5)
    ax.text(label_x, mid_y - 2.2, '(Numerical Opt.)', fontsize=14,
            color=YELLOW, ha='center', va='center', style='italic',
            zorder=5)

    # Connecting lines from labels to bracket
    for y_label in [mid_y + 0.9, mid_y - 1.4]:
        ax.plot([label_x + 1.6, bracket_x], [y_label, y_label],
                ls='--', color=MUTED, lw=1.2, alpha=0.5, zorder=1)

    # Title
    fig.suptitle('Where All Five Pillars Meet',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)
    fig.text(0.5, 0.91,
             'Inside a single transformer layer',
             ha='center', fontsize=22, color=MUTED, style='italic')

    # Axis limits
    ax.set_xlim(-1.5, 16.5)
    ax.set_ylim(-0.5, y_start + n * (box_h + gap) + 0.5)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
