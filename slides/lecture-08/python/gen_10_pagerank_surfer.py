#!/usr/bin/env python3
"""
Generate slide 10: The Random Surfer Model.

Same web graph as gen_09, but now a "surfer" is shown on one node with a
glowing halo. A dotted trail of recently visited pages fades in green,
and one teleportation jump is drawn as a dashed orange arc.

Output: ../images/10-pagerank-surfer.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as FancyArrowPatch
import networkx as nx

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '10-pagerank-surfer.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG        = '#1b2631'
CARD_BG   = '#1e3044'
BLUE      = '#3498db'
YELLOW    = '#f1c40f'
GREEN     = '#2ecc71'
ORANGE    = '#e67e22'
TEXT      = '#ecf0f1'
MUTED     = '#95a5a6'
EDGE_CLR  = '#4a5568'

# ---------------------------------------------------------------------------
# Web-graph (same as gen_09)
# ---------------------------------------------------------------------------
PAGES = ['Home', 'Blog', 'News', 'Shop', 'About', 'FAQ', 'Wiki', 'Forum']

EDGES = [
    ('Home', 'Blog'), ('Home', 'News'), ('Home', 'Shop'),
    ('Home', 'About'), ('Home', 'Wiki'),
    ('Blog', 'News'), ('Blog', 'Home'), ('Blog', 'Forum'),
    ('News', 'Home'), ('News', 'Blog'), ('News', 'Wiki'),
    ('Shop', 'Home'), ('Shop', 'FAQ'),
    ('About', 'Home'), ('About', 'FAQ'),
    ('FAQ', 'Home'), ('FAQ', 'Forum'),
    ('Wiki', 'Home'), ('Wiki', 'News'),
    ('Forum', 'Blog'), ('Forum', 'Wiki'), ('Forum', 'News'),
    ('Shop', 'Wiki'), ('About', 'Wiki'), ('FAQ', 'Wiki'),
]

SEED = 42

# Surfer trail: sequence of pages the surfer recently visited
# The last entry is the surfer's *current* position.
TRAIL = ['Blog', 'News', 'Wiki', 'Home', 'Shop', 'FAQ']
SURFER_NODE = TRAIL[-1]           # current position

# Teleportation: surfer jumps from FAQ to Forum (no direct link FAQ->Forum
# exists, but FAQ->Forum IS in edges -- so let's use a pair with no edge)
TELEPORT_FROM = 'FAQ'
TELEPORT_TO   = 'News'           # distant jump


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    G = nx.DiGraph()
    G.add_nodes_from(PAGES)
    G.add_edges_from(EDGES)

    # Use SAME layout seed as gen_09 for visual consistency
    pos = nx.spring_layout(G, seed=SEED, k=1.8)

    # -----------------------------------------------------------------------
    # Plot
    # -----------------------------------------------------------------------
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    fig.suptitle('The Random Surfer Model',
                 fontsize=36, fontweight='bold', color=TEXT, y=0.95)

    # --- background edges ---------------------------------------------------
    nx.draw_networkx_edges(
        G, pos, ax=ax, edge_color=EDGE_CLR, width=1.2, alpha=0.35,
        arrows=True, arrowstyle='-|>', arrowsize=16,
        connectionstyle='arc3,rad=0.12',
        min_source_margin=20, min_target_margin=20)

    # --- trail edges (dotted green, decreasing alpha) -----------------------
    trail_edges = list(zip(TRAIL[:-1], TRAIL[1:]))
    n_trail = len(trail_edges)
    for i, (u, v) in enumerate(trail_edges):
        alpha = 0.25 + 0.65 * (i / max(n_trail - 1, 1))
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v)], ax=ax,
            edge_color=GREEN, width=3.5, alpha=alpha,
            arrows=True, arrowstyle='-|>', arrowsize=20,
            connectionstyle='arc3,rad=0.10',
            style='dotted',
            min_source_margin=20, min_target_margin=20)

    # --- teleportation arc (dashed orange) ----------------------------------
    tp_from_pos = np.array(pos[TELEPORT_FROM])
    tp_to_pos   = np.array(pos[TELEPORT_TO])
    ax.annotate(
        '', xy=tp_to_pos, xytext=tp_from_pos,
        arrowprops=dict(
            arrowstyle='-|>', color=ORANGE, lw=3,
            linestyle='dashed',
            connectionstyle='arc3,rad=-0.4'))

    # --- draw all nodes (base layer) ----------------------------------------
    regular_nodes = [n for n in PAGES if n != SURFER_NODE]
    nx.draw_networkx_nodes(
        G, pos, nodelist=regular_nodes, ax=ax,
        node_size=1400, node_color=BLUE,
        edgecolors='white', linewidths=1.2)

    # --- surfer node with glow halo -----------------------------------------
    sx, sy = pos[SURFER_NODE]
    # Outer glow rings
    for radius, alpha in [(0.095, 0.08), (0.070, 0.14), (0.050, 0.22)]:
        glow = plt.Circle((sx, sy), radius, color=YELLOW,
                           alpha=alpha, transform=ax.transData)
        ax.add_patch(glow)

    # Surfer node itself
    nx.draw_networkx_nodes(
        G, pos, nodelist=[SURFER_NODE], ax=ax,
        node_size=2200, node_color=YELLOW,
        edgecolors='white', linewidths=2.5)

    # --- node labels --------------------------------------------------------
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=12, font_weight='bold',
        font_color='#1b2631')

    # --- trail node markers (small green ring on visited nodes) -------------
    visited = TRAIL[:-1]  # exclude current
    nx.draw_networkx_nodes(
        G, pos, nodelist=visited, ax=ax,
        node_size=1400, node_color='none',
        edgecolors=GREEN, linewidths=2.5)

    # --- annotations --------------------------------------------------------
    # "85% follow links" near a regular trail edge
    mid_edge_u, mid_edge_v = TRAIL[2], TRAIL[3]  # Wiki -> Home
    mx = (pos[mid_edge_u][0] + pos[mid_edge_v][0]) / 2
    my = (pos[mid_edge_u][1] + pos[mid_edge_v][1]) / 2
    ax.text(mx + 0.06, my + 0.08, '85% follow links',
            fontsize=18, fontweight='bold', color=GREEN,
            ha='left', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG,
                      edgecolor=GREEN, alpha=0.85))

    # "15% teleport" near the dashed arc
    tmx = (tp_from_pos[0] + tp_to_pos[0]) / 2
    tmy = (tp_from_pos[1] + tp_to_pos[1]) / 2
    ax.text(tmx - 0.04, tmy - 0.12, '15% teleport',
            fontsize=18, fontweight='bold', color=ORANGE,
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG,
                      edgecolor=ORANGE, alpha=0.85))

    # Subtitle
    ax.text(0.5, -0.04,
            'Green trail = recent browsing history   |   '
            'Orange arc = random teleportation   |   '
            'Yellow glow = current position',
            transform=ax.transAxes, fontsize=16, color=MUTED,
            ha='center', va='top')

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
