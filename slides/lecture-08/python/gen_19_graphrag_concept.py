#!/usr/bin/env python3
"""
gen_19_graphrag_concept.py
GraphRAG pipeline diagram (Microsoft, 2024).

Left-to-right flow of four stages:
  1. Documents          — blue
  2. Knowledge Graph    — green (small embedded network)
  3. Communities        — yellow (clustered subgraph with boundary)
  4. LLM Synthesis      — red (single output node with glow)

Thick arrows connect stages; each stage has an icon drawn with
matplotlib patches so no external images are required.

Output: ../images/19-graphrag-concept.png (3840x2160, 4K)
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
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '19-graphrag-concept.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG      = '#1b2631'
CARD_BG = '#1e3044'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
RED     = '#e74c3c'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'

# ---------------------------------------------------------------------------
# Stage definitions  (label, color, x_center, sublabel)
# ---------------------------------------------------------------------------
STAGE_Y   = 4.8   # vertical centre of stage boxes
BOX_W     = 2.8
BOX_H     = 3.2
ARROW_H   = STAGE_Y  # arrows at same height as box centres

STAGES = [
    ('Documents',        BLUE,   1.80, 'Raw text corpus'),
    ('Knowledge\nGraph', GREEN,  6.20, 'Entities & relations'),
    ('Communities',      YELLOW, 10.60, 'Clusters + summaries'),
    ('LLM\nSynthesis',   RED,   15.00, 'Final answer'),
]


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_stage_box(ax, xc, yc, w, h, color, label, sublabel):
    """Draw a rounded rectangle with title label and sublabel."""
    x = xc - w / 2
    y = yc - h / 2
    box = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=mpatches.BoxStyle.Round(pad=0.25, rounding_size=0.3),
        facecolor=CARD_BG, edgecolor=color,
        linewidth=3.5, alpha=0.95, zorder=3,
    )
    ax.add_patch(box)

    # Coloured top stripe
    stripe_h = 0.55
    stripe = mpatches.FancyBboxPatch(
        (x, yc + h / 2 - stripe_h), w, stripe_h,
        boxstyle=mpatches.BoxStyle.Round(pad=0.12, rounding_size=0.15),
        facecolor=color, edgecolor='none', alpha=0.85, zorder=4,
    )
    ax.add_patch(stripe)

    # Stage title at top
    ax.text(
        xc, yc + h / 2 - stripe_h / 2, label,
        fontsize=16, fontweight='bold', color=BG if color == YELLOW else 'white',
        ha='center', va='center', zorder=6,
        path_effects=[pe.withStroke(linewidth=2, foreground=color)],
    )

    # Sub-label at bottom
    ax.text(
        xc, yc - h / 2 + 0.40, sublabel,
        fontsize=12, color=MUTED,
        ha='center', va='center', style='italic', zorder=5,
    )


def draw_arrow(ax, x1, x2, y, color=TEXT, lw=4.0):
    """Fat right-pointing arrow between two x positions."""
    ax.annotate(
        '', xy=(x2, y), xytext=(x1, y),
        arrowprops=dict(
            arrowstyle='-|>', color=color, lw=lw,
            mutation_scale=32, shrinkA=6, shrinkB=6,
        ),
        zorder=4,
    )


# ---------------------------------------------------------------------------
# Icon drawing — one per stage, centred in the box
# ---------------------------------------------------------------------------

def draw_documents_icon(ax, xc, yc, color):
    """Stack of three overlapping page rectangles."""
    offsets = [(0.10, -0.10), (0.05, -0.05), (0.0, 0.0)]
    for dx, dy in offsets:
        page = mpatches.FancyBboxPatch(
            (xc - 0.52 + dx, yc - 0.60 + dy), 1.04, 1.32,
            boxstyle='square,pad=0.04',
            facecolor=CARD_BG, edgecolor=color,
            linewidth=2.0, alpha=0.80, zorder=5,
        )
        ax.add_patch(page)
    # Lined text lines
    for k in range(4):
        ly = yc - 0.38 + k * 0.22
        ax.plot([xc - 0.34, xc + 0.34], [ly, ly],
                color=color, linewidth=1.3, alpha=0.55, zorder=6)


def draw_knowledge_graph_icon(ax, xc, yc, color):
    """Small 6-node connected graph."""
    r = 0.62
    angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    node_pos = [(xc + r * np.cos(a), yc + r * np.sin(a)) for a in angles]
    # Edges
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),
             (0, 3), (1, 4), (2, 5)]
    for i, j in edges:
        ax.plot(
            [node_pos[i][0], node_pos[j][0]],
            [node_pos[i][1], node_pos[j][1]],
            color=color, linewidth=1.8, alpha=0.50, zorder=5,
        )
    # Nodes
    for (nx_, ny_) in node_pos:
        ax.plot(nx_, ny_, 'o', color=color,
                markersize=9, alpha=0.90, zorder=6,
                markeredgecolor='white', markeredgewidth=1.2)


def draw_communities_icon(ax, xc, yc, color):
    """Two clusters with elliptical halos."""
    clusters = [
        {'centre': (xc - 0.42, yc + 0.28), 'nodes': [(-0.22, 0.20), (0.22, 0.25),
                                                       (-0.10, -0.18), (0.15, -0.12)],
         'color': BLUE},
        {'centre': (xc + 0.42, yc - 0.28), 'nodes': [(-0.20, 0.18), (0.20, 0.12),
                                                       (-0.05, -0.22), (0.18, -0.18)],
         'color': GREEN},
    ]
    for cl in clusters:
        cx_, cy_ = cl['centre']
        # Halo ellipse
        halo = mpatches.Ellipse(
            (cx_, cy_), 0.78, 0.68,
            facecolor=cl['color'], edgecolor=cl['color'],
            linewidth=2.0, alpha=0.20, zorder=5,
        )
        ax.add_patch(halo)
        halo_edge = mpatches.Ellipse(
            (cx_, cy_), 0.78, 0.68,
            facecolor='none', edgecolor=cl['color'],
            linewidth=2.0, linestyle='--', alpha=0.70, zorder=5,
        )
        ax.add_patch(halo_edge)
        # Inner nodes
        npos = [(cx_ + dx, cy_ + dy) for dx, dy in cl['nodes']]
        for (nx_, ny_) in npos:
            ax.plot(nx_, ny_, 'o', color=cl['color'],
                    markersize=7, alpha=0.95, zorder=6,
                    markeredgecolor='white', markeredgewidth=1.0)
        for k in range(len(npos)):
            for l in range(k + 1, len(npos)):
                ax.plot([npos[k][0], npos[l][0]],
                        [npos[k][1], npos[l][1]],
                        color=cl['color'], linewidth=1.2,
                        alpha=0.40, zorder=5)
    # Inter-cluster bridge
    ax.plot(
        [clusters[0]['centre'][0] + 0.32,
         clusters[1]['centre'][0] - 0.32],
        [clusters[0]['centre'][1] - 0.05,
         clusters[1]['centre'][1] + 0.05],
        color=color, linewidth=2.0, linestyle=':', alpha=0.60, zorder=5,
    )


def draw_llm_icon(ax, xc, yc, color):
    """Single glowing output node with radiating lines."""
    R = 0.55
    # Glow halos
    for r, alpha in [(R + 0.32, 0.10), (R + 0.20, 0.18), (R + 0.08, 0.30)]:
        glow = plt.Circle((xc, yc), r, color=color, alpha=alpha, zorder=4)
        ax.add_patch(glow)
    # Core circle
    core = plt.Circle((xc, yc), R, color=color,
                       ec='white', linewidth=2.5, zorder=5)
    ax.add_patch(core)
    # Radiating spokes
    for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        dx = np.cos(angle)
        dy = np.sin(angle)
        ax.plot(
            [xc + (R + 0.08) * dx, xc + (R + 0.42) * dx],
            [yc + (R + 0.08) * dy, yc + (R + 0.42) * dy],
            color=color, linewidth=1.8, alpha=0.45, zorder=4,
        )
    # "LLM" text inside
    ax.text(
        xc, yc, 'AI', fontsize=17, fontweight='bold',
        color='white', ha='center', va='center', zorder=6,
        path_effects=[pe.withStroke(linewidth=2, foreground=color)],
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(3840 / 200, 2160 / 200), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.5, 17.5)
    ax.set_ylim(0.0, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # -----------------------------------------------------------------------
    # Stage boxes
    # -----------------------------------------------------------------------
    for label, color, xc, sublabel in STAGES:
        draw_stage_box(ax, xc, STAGE_Y, BOX_W, BOX_H, color, label, sublabel)

    # -----------------------------------------------------------------------
    # Icons inside each stage box (centred, slightly above mid)
    # -----------------------------------------------------------------------
    icon_y = STAGE_Y + 0.30
    draw_documents_icon(ax,       STAGES[0][2], icon_y, STAGES[0][1])
    draw_knowledge_graph_icon(ax, STAGES[1][2], icon_y, STAGES[1][1])
    draw_communities_icon(ax,     STAGES[2][2], icon_y, STAGES[2][1])
    draw_llm_icon(ax,             STAGES[3][2], icon_y, STAGES[3][1])

    # -----------------------------------------------------------------------
    # Arrows between stages
    # -----------------------------------------------------------------------
    for i in range(len(STAGES) - 1):
        x1 = STAGES[i][2]  + BOX_W / 2 + 0.10
        x2 = STAGES[i + 1][2] - BOX_W / 2 - 0.10
        clr = STAGES[i][1]
        draw_arrow(ax, x1, x2, STAGE_Y, color=clr)

    # -----------------------------------------------------------------------
    # Step labels above arrows
    # -----------------------------------------------------------------------
    step_labels = ['1. Extract', '2. Cluster', '3. Query']
    for i, slabel in enumerate(step_labels):
        mx = (STAGES[i][2] + STAGES[i + 1][2]) / 2
        ax.text(mx, STAGE_Y + BOX_H / 2 + 0.45, slabel,
                fontsize=13, color=MUTED, ha='center', va='center',
                style='italic',
                path_effects=[pe.withStroke(linewidth=2, foreground=BG)])

    # -----------------------------------------------------------------------
    # Annotation: "Global context" at Community→LLM edge
    # -----------------------------------------------------------------------
    ann_x = (STAGES[2][2] + STAGES[3][2]) / 2
    ann_y_box = STAGE_Y - BOX_H / 2 - 1.0
    ax.annotate(
        'Global context\n(not just chunks)',
        xy=(ann_x, STAGE_Y - BOX_H / 2 - 0.12),
        xytext=(ann_x, ann_y_box),
        fontsize=14, fontweight='bold', color=YELLOW, ha='center',
        arrowprops=dict(
            arrowstyle='->', color=YELLOW, lw=2.2,
            connectionstyle='arc3,rad=0.0',
        ),
        zorder=8,
        bbox=dict(boxstyle='round,pad=0.35', facecolor=BG,
                  edgecolor=YELLOW, linewidth=1.5),
    )

    # -----------------------------------------------------------------------
    # Bottom subtitle
    # -----------------------------------------------------------------------
    ax.text(
        8.50, 1.05,
        'GraphRAG (Microsoft, 2024): builds a knowledge graph + community summaries '
        'to enable global reasoning over large corpora.',
        fontsize=13, color=MUTED, ha='center', va='center',
        style='italic',
        path_effects=[pe.withStroke(linewidth=2, foreground=BG)],
    )

    # -----------------------------------------------------------------------
    # Title
    # -----------------------------------------------------------------------
    ax.set_title(
        'GraphRAG — Graph-Enhanced Retrieval-Augmented Generation (Microsoft 2024)',
        fontsize=28, fontweight='bold', color=TEXT, pad=22,
    )

    # -----------------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------------
    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
