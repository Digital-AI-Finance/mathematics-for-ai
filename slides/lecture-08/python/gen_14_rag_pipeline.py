#!/usr/bin/env python3
"""
gen_14_rag_pipeline.py
RAG (Retrieval-Augmented Generation) architecture flow diagram.

Left-to-right: User Question -> Query Engine -> Knowledge Graph ->
               Retrieved Facts -> LLM -> Answer
Each stage is a rounded box; thick arrows connect them.
The Knowledge Graph box contains a small embedded node cluster.

Output: ../images/14-rag-pipeline.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '14-rag-pipeline.png')

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

# Stage definitions: (label, color, x_center)
STAGES = [
    ('User\nQuestion',    PURPLE, 1.2),
    ('Query\nEngine',     ORANGE, 4.0),
    ('Knowledge\nGraph',  TEAL,   6.8),
    ('Retrieved\nFacts',  GREEN,  9.6),
    ('LLM',              BLUE,   12.4),
    ('Answer',           YELLOW, 15.2),
]

BOX_W = 2.2
BOX_H = 2.0
BOX_Y = 4.0  # vertical center of boxes


def draw_rounded_box(ax, x_center, y_center, w, h, color, label):
    """Draw a rounded rectangle with centered label."""
    x = x_center - w / 2
    y = y_center - h / 2
    box = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=mpatches.BoxStyle.Round(pad=0.25, rounding_size=0.3),
        facecolor=color, edgecolor='white', linewidth=2.0, alpha=0.88,
        zorder=3,
    )
    ax.add_patch(box)
    ax.text(
        x_center, y_center, label,
        fontsize=16, fontweight='bold', color='white',
        ha='center', va='center', zorder=5,
        path_effects=[pe.withStroke(linewidth=2, foreground='#00000066')],
    )
    return x, y


def draw_arrow(ax, x1, y, x2, color=TEXT, lw=3.5):
    """Draw a thick arrow between two x positions at fixed y."""
    ax.annotate(
        '', xy=(x2, y), xytext=(x1, y),
        arrowprops=dict(
            arrowstyle='-|>', color=color, lw=lw,
            mutation_scale=22, shrinkA=4, shrinkB=4,
        ),
        zorder=4,
    )


def draw_mini_graph(ax, cx, cy, color):
    """Draw a small cluster of 6 connected dots inside the KG box."""
    np.random.seed(7)
    # Fixed positions for a small 6-node graph
    nodes = [
        (cx - 0.55, cy + 0.35),
        (cx + 0.55, cy + 0.35),
        (cx - 0.35, cy - 0.30),
        (cx + 0.35, cy - 0.30),
        (cx,        cy + 0.55),
        (cx,        cy - 0.55),
    ]
    edges = [
        (0, 1), (0, 2), (1, 3), (2, 3), (0, 4), (1, 4),
        (2, 5), (3, 5), (4, 1), (5, 0),
    ]
    for i, j in edges:
        ax.plot(
            [nodes[i][0], nodes[j][0]],
            [nodes[i][1], nodes[j][1]],
            color='white', alpha=0.3, linewidth=1.0, zorder=6,
        )
    for nx_, ny_ in nodes:
        ax.plot(nx_, ny_, 'o', color='white', markersize=5,
                alpha=0.7, zorder=7)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(3840 / 200, 2160 / 200), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.5, 17.0)
    ax.set_ylim(0.0, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw boxes
    for label, color, xc in STAGES:
        draw_rounded_box(ax, xc, BOX_Y, BOX_W, BOX_H, color, label)

    # Mini graph inside Knowledge Graph box
    kg_x = STAGES[2][2]
    draw_mini_graph(ax, kg_x, BOX_Y, TEAL)

    # Draw arrows between consecutive boxes
    for i in range(len(STAGES) - 1):
        x1 = STAGES[i][2] + BOX_W / 2 + 0.1
        x2 = STAGES[i + 1][2] - BOX_W / 2 - 0.1
        draw_arrow(ax, x1, BOX_Y, x2)

    # Annotation: "Less hallucination!" pointing to KG->Facts connection
    mid_x = (STAGES[2][2] + STAGES[3][2]) / 2
    ann_y = BOX_Y - BOX_H / 2 - 1.2
    ax.annotate(
        'Less hallucination!',
        xy=(mid_x, BOX_Y - BOX_H / 2 - 0.15),
        xytext=(mid_x, ann_y),
        fontsize=16, fontweight='bold', color=YELLOW, ha='center',
        arrowprops=dict(
            arrowstyle='->', color=YELLOW, lw=2.5,
            connectionstyle='arc3,rad=0.0',
        ),
        zorder=8,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                  edgecolor=YELLOW, linewidth=1.5),
    )

    # Subtitle below the flow
    ax.text(
        8.25, 1.0,
        'Ground the LLM in real facts retrieved from a structured knowledge graph',
        fontsize=14, color=MUTED, ha='center', va='center', style='italic',
    )

    # Title
    ax.set_title(
        'Retrieval-Augmented Generation (RAG)',
        fontsize=30, fontweight='bold', color=TEXT, pad=24,
    )

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
