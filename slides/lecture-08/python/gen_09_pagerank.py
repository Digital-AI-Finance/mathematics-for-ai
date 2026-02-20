#!/usr/bin/env python3
"""
Generate slide 09: PageRank Web Graph.

Directed web graph of 8 pages with realistic link structure.
Node sizes are proportional to their computed PageRank. The highest-ranked
node is coloured yellow; others are shaded blue (darker = lower rank).
PageRank percentages are labelled beside each node.

Output: ../images/09-pagerank-web.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '09-pagerank-web.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG        = '#1b2631'
CARD_BG   = '#1e3044'
BLUE      = '#3498db'
YELLOW    = '#f1c40f'
TEXT      = '#ecf0f1'
MUTED     = '#95a5a6'
EDGE_CLR  = '#4a5568'

# Blue gradient for non-leader nodes: low rank -> dark, high rank -> bright
BLUE_DARK  = '#1a5276'
BLUE_LIGHT = '#5dade2'

# ---------------------------------------------------------------------------
# Web-graph construction
# ---------------------------------------------------------------------------
PAGES = ['Home', 'Blog', 'News', 'Shop', 'About', 'FAQ', 'Wiki', 'Forum']

EDGES = [
    # Home links out broadly
    ('Home', 'Blog'), ('Home', 'News'), ('Home', 'Shop'),
    ('Home', 'About'), ('Home', 'Wiki'),
    # Blog
    ('Blog', 'News'), ('Blog', 'Home'), ('Blog', 'Forum'),
    # News
    ('News', 'Home'), ('News', 'Blog'), ('News', 'Wiki'),
    # Shop
    ('Shop', 'Home'), ('Shop', 'FAQ'),
    # About
    ('About', 'Home'), ('About', 'FAQ'),
    # FAQ
    ('FAQ', 'Home'), ('FAQ', 'Forum'),
    # Wiki -- many incoming links make it authoritative
    ('Wiki', 'Home'), ('Wiki', 'News'),
    # Forum
    ('Forum', 'Blog'), ('Forum', 'Wiki'), ('Forum', 'News'),
    # Extra links pointing INTO Wiki to boost its rank
    ('Shop', 'Wiki'), ('About', 'Wiki'), ('FAQ', 'Wiki'),
]

SEED = 42


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    G = nx.DiGraph()
    G.add_nodes_from(PAGES)
    G.add_edges_from(EDGES)

    # Compute PageRank
    pr = nx.pagerank(G, alpha=0.85)

    # Layout
    pos = nx.spring_layout(G, seed=SEED, k=1.8)

    # Determine leader (highest PR)
    leader = max(pr, key=pr.get)

    # Build colour map: gradient for non-leaders, yellow for leader
    pr_values = np.array([pr[n] for n in PAGES])
    pr_min, pr_max = pr_values.min(), pr_values.max()
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'blue_grad', [BLUE_DARK, BLUE_LIGHT])

    node_colors = []
    for n in PAGES:
        if n == leader:
            node_colors.append(YELLOW)
        else:
            # Normalise to [0,1] for gradient
            normed = (pr[n] - pr_min) / (pr_max - pr_min + 1e-9)
            node_colors.append(cmap(normed))

    # Node sizes proportional to PageRank
    SIZE_MIN, SIZE_MAX = 1200, 5500
    node_sizes = [SIZE_MIN + (SIZE_MAX - SIZE_MIN) *
                  ((pr[n] - pr_min) / (pr_max - pr_min + 1e-9))
                  for n in PAGES]

    # -----------------------------------------------------------------------
    # Plot
    # -----------------------------------------------------------------------
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    fig.suptitle('The Web as a Graph: PageRank Scores',
                 fontsize=36, fontweight='bold', color=TEXT, y=0.95)

    # Edges with arrows
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color=EDGE_CLR, width=1.5, alpha=0.6,
        arrows=True, arrowstyle='-|>', arrowsize=20,
        connectionstyle='arc3,rad=0.12',
        min_source_margin=22, min_target_margin=22)

    # Nodes
    nx.draw_networkx_nodes(
        G, pos, nodelist=PAGES, ax=ax,
        node_size=node_sizes, node_color=node_colors,
        edgecolors='white', linewidths=1.5)

    # Node name labels (inside)
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=13, font_weight='bold',
        font_color='#1b2631')

    # PageRank percentage labels (offset above)
    for node in PAGES:
        x, y = pos[node]
        pct = pr[node] * 100
        # Offset direction: upward
        label_y = y + 0.10
        ax.text(x, label_y, f'{pct:.1f}%',
                fontsize=16, fontweight='bold',
                color=YELLOW if node == leader else TEXT,
                ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=CARD_BG,
                          edgecolor='none', alpha=0.7))

    # Subtitle
    ax.text(0.5, -0.04,
            'Node size $\\propto$ PageRank   |   '
            'Highest-ranked page highlighted in yellow',
            transform=ax.transAxes, fontsize=17, color=MUTED,
            ha='center', va='top')

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
