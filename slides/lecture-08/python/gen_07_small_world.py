#!/usr/bin/env python3
"""
Generate slide 07: Watts-Strogatz Small-World Networks.

Three panels showing the rewiring spectrum from regular lattice (p=0)
through small-world (p=0.2) to random graph (p=1.0). Rewired edges
are detected by comparison with the p=0 baseline and colored yellow.
Clustering coefficient (C) and average path length (L) shown below each.

Output: ../images/07-small-world.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '07-small-world.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG        = '#1b2631'
CARD_BG   = '#1e3044'
BLUE      = '#3498db'
YELLOW    = '#f1c40f'
TEXT      = '#ecf0f1'
MUTED     = '#95a5a6'

# ---------------------------------------------------------------------------
# Graph parameters
# ---------------------------------------------------------------------------
N = 20          # number of nodes
K = 4           # each node connected to K nearest neighbours (even)
SEED = 42       # reproducibility
PROBABILITIES = [0.0, 0.2, 1.0]
TITLES = ['Regular  ($p=0$)', 'Small World  ($p=0.2$)', 'Random  ($p=1.0$)']


def circular_layout(G):
    """Return positions on a circle, node 0 at the top."""
    n = len(G)
    pos = {}
    for i in G.nodes():
        angle = 2 * np.pi * i / n - np.pi / 2  # start at top
        pos[i] = (np.cos(angle), np.sin(angle))
    return pos


def detect_rewired_edges(G_regular, G_rewired):
    """Return sets of (kept, rewired) edges in G_rewired."""
    regular_set = set(frozenset(e) for e in G_regular.edges())
    kept = []
    rewired = []
    for e in G_rewired.edges():
        if frozenset(e) in regular_set:
            kept.append(e)
        else:
            rewired.append(e)
    return kept, rewired


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')

    fig, axes = plt.subplots(1, 3, figsize=(19.2, 10.8), facecolor=BG)
    fig.subplots_adjust(wspace=0.28, top=0.82, bottom=0.12)

    fig.suptitle('Watts-Strogatz Small-World Model',
                 fontsize=36, fontweight='bold', color=TEXT, y=0.93)

    # Build the regular (p=0) graph as baseline for rewired-edge detection
    G_regular = nx.watts_strogatz_graph(N, K, 0.0, seed=SEED)

    for idx, (p, title) in enumerate(zip(PROBABILITIES, TITLES)):
        ax = axes[idx]
        ax.set_facecolor(BG)
        ax.set_aspect('equal')
        ax.axis('off')

        # Generate graph
        G = nx.watts_strogatz_graph(N, K, p, seed=SEED)

        # Layout: circular for regular/small-world, spring for random
        if p < 1.0:
            pos = circular_layout(G)
        else:
            pos = nx.spring_layout(G, seed=SEED, k=0.35)

        # Detect rewired edges
        kept, rewired = detect_rewired_edges(G_regular, G)

        # Draw kept edges
        nx.draw_networkx_edges(G, pos, edgelist=kept, ax=ax,
                               edge_color=BLUE, width=1.4, alpha=0.7)
        # Draw rewired edges
        if rewired:
            nx.draw_networkx_edges(G, pos, edgelist=rewired, ax=ax,
                                   edge_color=YELLOW, width=2.0, alpha=0.9)

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=180,
                               node_color=BLUE, edgecolors='white',
                               linewidths=0.8)

        # Panel title
        ax.set_title(title, fontsize=24, fontweight='bold',
                     color=TEXT, pad=16)

        # Compute metrics
        C = nx.average_clustering(G)
        if nx.is_connected(G):
            L = nx.average_shortest_path_length(G)
        else:
            # For disconnected graphs, use largest component
            largest_cc = max(nx.connected_components(G), key=len)
            L = nx.average_shortest_path_length(G.subgraph(largest_cc))

        # Metric annotation below panel
        metric_text = f'$C = {C:.3f}$      $L = {L:.2f}$'
        ax.text(0.5, -0.08, metric_text, transform=ax.transAxes,
                fontsize=20, color=MUTED, ha='center', va='top')

    # Legend
    blue_patch = mpatches.Patch(color=BLUE, label='Original edges')
    yellow_patch = mpatches.Patch(color=YELLOW, label='Rewired edges')
    fig.legend(handles=[blue_patch, yellow_patch], loc='lower center',
               ncol=2, fontsize=18, frameon=False,
               labelcolor=TEXT, handlelength=2.5,
               bbox_to_anchor=(0.5, 0.01))

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
