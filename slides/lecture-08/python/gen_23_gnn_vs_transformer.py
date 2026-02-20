#!/usr/bin/env python3
"""
Generate slide 23: GNN Message Passing vs Transformer Attention.

Two panels side by side using networkx:
  Left:  GNN with sparse graph, message passing to node C
  Right: Transformer with complete graph, varying edge widths

Output: ../images/23-gnn-vs-transformer.png (3840x2160, 4K)
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
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '23-gnn-vs-transformer.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG      = '#1b2631'
YELLOW  = '#f1c40f'
BLUE    = '#3498db'
TEAL    = '#2ecc71'
RED     = '#e74c3c'
ORANGE  = '#e67e22'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'

NODES = ['A', 'B', 'C', 'D', 'E']


def draw_gnn_panel(ax):
    """Left panel: GNN with sparse graph, message arrows to C."""
    G = nx.Graph()
    G.add_edges_from([
        ('A', 'B'), ('A', 'C'), ('B', 'C'),
        ('C', 'D'), ('D', 'E'), ('B', 'E'), ('C', 'E')
    ])

    # Fixed layout for consistency
    pos = {
        'A': (-1.0,  0.8),
        'B': (-0.6, -0.5),
        'C': ( 0.0,  0.2),
        'D': ( 0.7, -0.4),
        'E': ( 1.0,  0.7),
    }

    # Draw all edges first (muted)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=MUTED, width=2.0,
                           alpha=0.4)

    # Highlight edges TO node C with colored arrows
    c_neighbors = list(G.neighbors('C'))  # A, B, D, E
    highlight_colors = [YELLOW, TEAL, ORANGE, RED]
    for nbr, clr in zip(c_neighbors, highlight_colors):
        ax.annotate('', xy=pos['C'], xytext=pos[nbr],
                    arrowprops=dict(arrowstyle='->', color=clr,
                                   lw=3.5, shrinkA=18, shrinkB=18))

    # Draw nodes
    node_colors = [BLUE if n != 'C' else YELLOW for n in NODES]
    node_sizes = [900 if n != 'C' else 1300 for n in NODES]
    nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=NODES,
                           node_color=node_colors, node_size=node_sizes,
                           edgecolors='white', linewidths=2.5)

    # Labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=23, font_weight='bold',
                            font_color=BG)

    ax.set_title('GNN: Message Passing', fontsize=26, fontweight='bold',
                 color=TEAL, pad=18)

    # Formula below graph
    ax.text(0.5, -0.08,
            r'$h_v^{(l+1)} = \sigma\!\left(\sum_{u \in N(v)} W\, h_u^{(l)}\right)$',
            transform=ax.transAxes, fontsize=23, color=TEXT,
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e3044',
                      edgecolor=TEAL, alpha=0.9))

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.0, 1.3)
    ax.axis('off')


def draw_transformer_panel(ax):
    """Right panel: Transformer with complete graph, varying edge widths."""
    G = nx.complete_graph(5)
    mapping = {i: n for i, n in enumerate(NODES)}
    G = nx.relabel_nodes(G, mapping)

    pos = {
        'A': (-1.0,  0.8),
        'B': (-0.6, -0.5),
        'C': ( 0.0,  0.2),
        'D': ( 0.7, -0.4),
        'E': ( 1.0,  0.7),
    }

    # Assign random-looking but fixed attention weights to edges
    np.random.seed(42)
    edge_weights = {}
    for u, v in G.edges():
        edge_weights[(u, v)] = 0.2 + 0.8 * np.random.random()

    # Draw edges with varying width and alpha
    for (u, v), w in edge_weights.items():
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                color=YELLOW, lw=1.0 + w * 4.0, alpha=0.15 + w * 0.6,
                solid_capstyle='round', zorder=1)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=NODES,
                           node_color=[BLUE] * 5, node_size=900,
                           edgecolors='white', linewidths=2.5)

    nx.draw_networkx_labels(G, pos, ax=ax, font_size=23, font_weight='bold',
                            font_color=BG)

    ax.set_title('Transformer: Attention', fontsize=26, fontweight='bold',
                 color=YELLOW, pad=18)

    # Formula
    ax.text(0.5, -0.08,
            r'$\mathrm{Attn}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)\!V$',
            transform=ax.transAxes, fontsize=23, color=TEXT,
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e3044',
                      edgecolor=YELLOW, alpha=0.9))

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.0, 1.3)
    ax.axis('off')


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19.2, 10.8), facecolor=BG)
    ax1.set_facecolor(BG)
    ax2.set_facecolor(BG)

    draw_gnn_panel(ax1)
    draw_transformer_panel(ax2)

    fig.suptitle('Transformer Attention IS GNN Message Passing',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)

    fig.text(0.5, 0.02,
             'Sparse neighbors (GNN) vs. full attention (Transformer) \u2014 same update rule, different graphs',
             ha='center', fontsize=23, color=MUTED)

    plt.tight_layout(rect=[0, 0.05, 1, 0.92])

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
