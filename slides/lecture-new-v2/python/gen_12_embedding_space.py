#!/usr/bin/env python3
"""
gen_12_embedding_space.py
2D scatter plot simulating word embeddings projected to 2D with cluster groups.
Output: ../images/12-embedding-space.png
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '12-embedding-space.png')

BG     = '#1b2631'
BLUE   = '#3498db'
YELLOW = '#f1c40f'
GREEN  = '#2ecc71'
TEAL   = '#1abc9c'
ORANGE = '#e67e22'
RED    = '#e74c3c'
TEXT   = '#ecf0f1'
MUTED  = '#95a5a6'


# Cluster definitions: (name, center_x, center_y, spread_x, spread_y, color, words)
CLUSTERS = [
    ('Animals',   -3.5,  2.5, 0.9, 0.7, GREEN, [
        'cat', 'dog', 'lion', 'whale', 'eagle', 'fox', 'wolf', 'bear']),
    ('Countries',  3.0,  3.2, 0.8, 0.6, BLUE, [
        'France', 'Japan', 'Brazil', 'Canada', 'Egypt', 'India', 'Spain', 'Peru']),
    ('Emotions',  -3.0, -2.8, 0.8, 0.7, RED, [
        'happy', 'sad', 'angry', 'fear', 'joy', 'grief', 'calm', 'love']),
    ('Food',       3.2, -2.6, 0.9, 0.7, ORANGE, [
        'pizza', 'sushi', 'bread', 'salad', 'pasta', 'curry', 'tacos', 'soup']),
    ('Science',    0.0,  0.1, 0.85, 0.65, TEAL, [
        'physics', 'algebra', 'entropy', 'vector', 'matrix', 'gradient',
        'neuron', 'photon']),
]


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    rng = np.random.default_rng(42)
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)

    # Thin grid
    ax.grid(True, color='#2c3e50', linewidth=0.5, alpha=0.6, zorder=0)
    ax.set_axisbelow(True)

    # Axis styling
    for spine in ax.spines.values():
        spine.set_edgecolor('#2c3e50')
        spine.set_linewidth(1)

    ax.tick_params(colors=MUTED, labelsize=9)
    ax.set_xlabel('Dimension 1  (t-SNE / PCA projection)',
                  fontsize=12, color=MUTED, labelpad=8)
    ax.set_ylabel('Dimension 2  (t-SNE / PCA projection)',
                  fontsize=12, color=MUTED, labelpad=8)

    legend_handles = []

    for name, cx, cy, sx, sy, color, words in CLUSTERS:
        n = len(words)
        xs = rng.normal(cx, sx, n)
        ys = rng.normal(cy, sy, n)

        # Subtle ellipse outline for the cluster
        ellipse = Ellipse(
            (cx, cy),
            width=sx * 5.5, height=sy * 5.5,
            angle=rng.uniform(-20, 20),
            facecolor=color, alpha=0.08,
            edgecolor=color, linewidth=1.5,
            linestyle='--', zorder=1
        )
        ax.add_patch(ellipse)

        # Scatter dots
        ax.scatter(xs, ys, s=90, color=color, alpha=0.85,
                   edgecolors='white', linewidths=0.5, zorder=3)

        # Word labels — offset slightly to avoid overlap with dot
        for i, (x, y, word) in enumerate(zip(xs, ys, words)):
            # Alternate label placement: right/above
            dx = 0.12 if i % 2 == 0 else -0.12
            dy = 0.18 if i % 3 != 1 else -0.22
            ax.text(x + dx, y + dy, word,
                    fontsize=9.5, color=TEXT, alpha=0.92,
                    va='center', ha='left' if dx > 0 else 'right',
                    family='sans-serif', zorder=4)

        # Cluster label (centroid)
        ax.text(cx, cy + sy * 3.2, name,
                ha='center', va='bottom', fontsize=13, fontweight='bold',
                color=color, alpha=0.95, family='sans-serif', zorder=5)

        legend_handles.append(
            mpatches.Patch(color=color, label=name, alpha=0.8))

    # "King - Man + Woman = Queen" style analogy arrow
    # France  →  Paris  analogy hint
    france_x = CLUSTERS[1][1] + 0.3   # index 1 = cx
    france_y = CLUSTERS[1][2] - 0.15  # index 2 = cy
    king_x, king_y = -0.7, 0.35   # in Science cluster zone

    ax.annotate('',
                xy=(king_x, king_y),
                xytext=(france_x, france_y - 0.5),
                arrowprops=dict(
                    arrowstyle='->', color=YELLOW,
                    lw=1.4, connectionstyle='arc3,rad=0.3'))
    ax.text((france_x + king_x) / 2 + 0.4,
            (france_y + king_y) / 2 - 0.1,
            'vector\nanalogy',
            ha='center', va='center', fontsize=9,
            color=YELLOW, fontstyle='italic', alpha=0.8)

    # Axis limits
    ax.set_xlim(-5.8, 5.8)
    ax.set_ylim(-5.2, 5.4)

    # Legend
    leg = ax.legend(handles=legend_handles, loc='lower right',
                    fontsize=11, facecolor='#2c3e50',
                    edgecolor=MUTED, labelcolor=TEXT,
                    framealpha=0.9, title='Word Categories',
                    title_fontsize=11)
    leg.get_title().set_color(TEXT)

    # Titles
    ax.set_title(
        'Word Embedding Space  (2D Projection)\n'
        r'$\it{Similar\ words\ cluster\ together\ in\ high{-}dimensional\ space}$',
        fontsize=18, fontweight='bold', color=TEXT,
        family='sans-serif', pad=18, linespacing=1.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
