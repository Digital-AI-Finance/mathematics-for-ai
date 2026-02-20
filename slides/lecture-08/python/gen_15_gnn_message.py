#!/usr/bin/env python3
"""
gen_15_gnn_message.py
GNN message passing visualized over 3 rounds.

Three panels: Round 0 (Initial), Round 1 (Aggregate), Round 2 (Update).
5-node pentagon graph. Each round, node colors blend toward neighbors'
average, demonstrating the aggregate-update cycle.

Output: ../images/15-gnn-message.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import networkx as nx

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '15-gnn-message.png')

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
EDGE_C  = '#4a5568'

# Initial node colors (RGB tuples, 0-1 range)
INIT_COLORS_HEX = [BLUE, GREEN, YELLOW, ORANGE, PURPLE]


def hex_to_rgb(h):
    """Convert hex color to (r, g, b) float tuple."""
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """Convert (r, g, b) float tuple to hex string."""
    return '#{:02x}{:02x}{:02x}'.format(
        int(np.clip(rgb[0], 0, 1) * 255),
        int(np.clip(rgb[1], 0, 1) * 255),
        int(np.clip(rgb[2], 0, 1) * 255),
    )


def pentagon_layout(n=5, radius=1.0):
    """Return positions for n nodes in a regular pentagon, node 0 at top."""
    pos = {}
    for i in range(n):
        angle = 2 * np.pi * i / n - np.pi / 2
        pos[i] = (radius * np.cos(angle), radius * np.sin(angle))
    return pos


def message_pass(colors_rgb, adjacency):
    """One round: each node's new color = average of self + neighbors."""
    n = len(colors_rgb)
    new_colors = []
    for i in range(n):
        neighbors = [j for j in range(n) if adjacency[i][j]]
        all_nodes = [i] + neighbors
        avg = np.mean([colors_rgb[j] for j in all_nodes], axis=0)
        new_colors.append(tuple(avg))
    return new_colors


def draw_message_arrows(ax, G, pos, target_node, color=YELLOW):
    """Draw small arrows from neighbors to target_node."""
    neighbors = list(G.neighbors(target_node))
    for nb in neighbors:
        x0, y0 = pos[nb]
        x1, y1 = pos[target_node]
        dx = x1 - x0
        dy = y1 - y0
        length = np.sqrt(dx**2 + dy**2)
        if length == 0:
            continue
        # Shorten arrow to not overlap node circles
        shrink = 0.18
        sx = x0 + dx * shrink
        sy = y0 + dy * shrink
        ex = x1 - dx * shrink
        ey = y1 - dy * shrink
        ax.annotate(
            '', xy=(ex, ey), xytext=(sx, sy),
            arrowprops=dict(
                arrowstyle='->', color=color, lw=1.8,
                mutation_scale=14, alpha=0.8,
            ),
            zorder=6,
        )


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Build pentagon graph
    G = nx.cycle_graph(5)
    pos = pentagon_layout(5, radius=1.0)

    # Adjacency matrix
    adj = nx.to_numpy_array(G).astype(int)

    # Compute color evolution
    init_rgb = [hex_to_rgb(c) for c in INIT_COLORS_HEX]
    round_colors = [init_rgb]
    current = init_rgb
    for _ in range(2):
        current = message_pass(current, adj)
        round_colors.append(current)

    panel_titles = ['Round 0  (Initial)', 'Round 1  (Aggregate)', 'Round 2  (Update)']

    plt.style.use('dark_background')
    fig, axes = plt.subplots(1, 3, figsize=(3840 / 200, 2160 / 200), dpi=200,
                             facecolor=BG)
    fig.subplots_adjust(wspace=0.25, top=0.82, bottom=0.10)

    fig.suptitle(
        'Graph Neural Networks: Message Passing',
        fontsize=32, fontweight='bold', color=TEXT, y=0.93,
    )

    for idx, (ax, title, colors_rgb) in enumerate(
            zip(axes, panel_titles, round_colors)):
        ax.set_facecolor(BG)
        ax.set_aspect('equal')
        ax.axis('off')

        # Draw edges
        for u, v in G.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            ax.plot([x0, x1], [y0, y1], color=EDGE_C, linewidth=2.0,
                    alpha=0.7, zorder=1)

        # Round 1: message arrows toward node 0
        if idx == 1:
            draw_message_arrows(ax, G, pos, target_node=0, color=YELLOW)

            # "AGGREGATE" label near node 0
            nx0, ny0 = pos[0]
            ax.text(nx0 + 0.05, ny0 + 0.32, 'AGGREGATE',
                    fontsize=10, fontweight='bold', color=YELLOW,
                    ha='center', va='bottom', zorder=10,
                    bbox=dict(boxstyle='round,pad=0.15', facecolor=BG,
                              edgecolor=YELLOW, linewidth=1.0, alpha=0.9))

        # Round 2: update annotation
        if idx == 2:
            # Show AGGREGATE arrows into node 2 (bottom-right)
            draw_message_arrows(ax, G, pos, target_node=2, color=YELLOW)
            nx2, ny2 = pos[2]
            ax.text(nx2, ny2 + 0.32, 'AGGREGATE',
                    fontsize=9, fontweight='bold', color=YELLOW,
                    ha='center', va='bottom', zorder=10,
                    bbox=dict(boxstyle='round,pad=0.12', facecolor=BG,
                              edgecolor=YELLOW, linewidth=1.0, alpha=0.9))

            # "UPDATE" arrow pointing outward from node 2
            ax.annotate(
                'UPDATE', xy=(nx2 + 0.45, ny2 - 0.25),
                xytext=(nx2 + 0.85, ny2 - 0.55),
                fontsize=10, fontweight='bold', color=GREEN,
                ha='center', va='top', zorder=10,
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.0),
                bbox=dict(boxstyle='round,pad=0.12', facecolor=BG,
                          edgecolor=GREEN, linewidth=1.0, alpha=0.9),
            )

        # Draw nodes
        node_hex = [rgb_to_hex(c) for c in colors_rgb]
        for i in range(5):
            nx_i, ny_i = pos[i]
            circle = plt.Circle(
                (nx_i, ny_i), 0.16, facecolor=node_hex[i],
                edgecolor='white', linewidth=2.0, zorder=8,
            )
            ax.add_patch(circle)
            ax.text(nx_i, ny_i, str(i), fontsize=11, fontweight='bold',
                    color='white', ha='center', va='center', zorder=9,
                    path_effects=[pe.withStroke(linewidth=2, foreground='#00000088')])

        ax.set_title(title, fontsize=22, fontweight='bold', color=TEXT, pad=14)

        # Set limits
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

    # Legend at bottom
    fig.text(
        0.5, 0.04,
        'Each round: nodes collect messages from neighbors (AGGREGATE) '
        'then update their own features (UPDATE)',
        fontsize=14, color=MUTED, ha='center', va='center', style='italic',
    )

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
