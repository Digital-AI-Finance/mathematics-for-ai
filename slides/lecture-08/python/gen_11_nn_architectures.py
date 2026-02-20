#!/usr/bin/env python3
"""
Generate slide 11: Neural Network Architectures as Graph Diagrams.

2x2 grid showing four architectures:
  1. Feedforward (3-4-2)
  2. Deep / VGG-style (3-4-4-4-4-2)
  3. Branching / Inception-style (parallel paths that split and merge)
  4. Skip / ResNet-style (forward + skip connections over 2 layers)

Each architecture is drawn as a directed graph with nodes arranged in
layer columns.

Output: ../images/11-nn-architectures.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import networkx as nx

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '11-nn-architectures.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG        = '#1b2631'
CARD_BG   = '#1e3044'
BLUE      = '#3498db'
TEAL      = '#1abc9c'
GREEN     = '#2ecc71'
YELLOW    = '#f1c40f'
TEXT      = '#ecf0f1'
MUTED     = '#95a5a6'
EDGE_CLR  = '#4a5568'


def layer_positions(layers, x_spacing=1.6, y_spacing=0.9):
    """
    Assign (x, y) positions for nodes arranged in vertical layer columns.

    Parameters
    ----------
    layers : list[int]
        Number of nodes in each layer.
    x_spacing : float
        Horizontal distance between layers.
    y_spacing : float
        Vertical distance between nodes within a layer.

    Returns
    -------
    pos : dict[str, tuple]
        Node id -> (x, y).
    node_list : list[list[str]]
        Grouped by layer for convenient edge-drawing.
    """
    pos = {}
    node_list = []
    for layer_idx, n_nodes in enumerate(layers):
        x = layer_idx * x_spacing
        y_offset = -(n_nodes - 1) * y_spacing / 2
        layer_nodes = []
        for node_idx in range(n_nodes):
            nid = f'L{layer_idx}_N{node_idx}'
            pos[nid] = (x, y_offset + node_idx * y_spacing)
            layer_nodes.append(nid)
        node_list.append(layer_nodes)
    return pos, node_list


def draw_nn(ax, layers, color, title, skip_layers=None):
    """
    Draw a neural-network graph on the given axes.

    Parameters
    ----------
    ax : matplotlib Axes
    layers : list[int]
    color : str
        Main colour for nodes and edges.
    title : str
    skip_layers : list[tuple(int,int)] or None
        Pairs (from_layer, to_layer) for skip connections.
    """
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_title(title, fontsize=22, fontweight='bold', color=TEXT, pad=14)

    pos, node_list = layer_positions(layers)

    G = nx.DiGraph()

    # Fully-connected forward edges
    for l_idx in range(len(node_list) - 1):
        for src in node_list[l_idx]:
            for dst in node_list[l_idx + 1]:
                G.add_edge(src, dst, kind='forward')

    # Draw forward edges
    forward_edges = [(u, v) for u, v, d in G.edges(data=True)
                     if d['kind'] == 'forward']
    nx.draw_networkx_edges(
        G, pos, edgelist=forward_edges, ax=ax,
        edge_color=color, width=1.2, alpha=0.5,
        arrows=True, arrowstyle='-|>', arrowsize=10,
        min_source_margin=12, min_target_margin=12)

    # Skip connections
    if skip_layers:
        for (l_from, l_to) in skip_layers:
            for src in node_list[l_from]:
                # Connect to node at same vertical position if possible
                src_y = pos[src][1]
                # Find closest node in target layer
                best = min(node_list[l_to],
                           key=lambda n: abs(pos[n][1] - src_y))
                G.add_edge(src, best, kind='skip')

        skip_edges = [(u, v) for u, v, d in G.edges(data=True)
                      if d['kind'] == 'skip']
        nx.draw_networkx_edges(
            G, pos, edgelist=skip_edges, ax=ax,
            edge_color=YELLOW, width=2.8, alpha=0.85,
            arrows=True, arrowstyle='-|>', arrowsize=14,
            connectionstyle='arc3,rad=-0.3',
            min_source_margin=12, min_target_margin=12)

    # Nodes
    all_nodes = list(pos.keys())
    nx.draw_networkx_nodes(
        G, pos, nodelist=all_nodes, ax=ax,
        node_size=500, node_color=color,
        edgecolors='white', linewidths=1.0)

    # Centre the view
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    margin = 0.8
    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)


def draw_inception(ax):
    """
    Branching / Inception-style architecture with parallel paths.

    Input(3) -> split into two branches of width 2 each -> merge(4) -> output(2)
    """
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_title('Branching (Inception)', fontsize=22,
                 fontweight='bold', color=TEXT, pad=14)

    # Manual layout
    x_sp = 1.6
    y_sp = 0.9

    # Layer 0: input (3 nodes)
    input_nodes = [f'I{i}' for i in range(3)]
    # Layer 1a: branch A (2 nodes, upper)
    branchA = [f'A{i}' for i in range(2)]
    # Layer 1b: branch B (2 nodes, lower)
    branchB = [f'B{i}' for i in range(2)]
    # Layer 2: merge (4 nodes)
    merge_nodes = [f'M{i}' for i in range(4)]
    # Layer 3: output (2 nodes)
    output_nodes = [f'O{i}' for i in range(2)]

    pos = {}
    # Input
    for i, n in enumerate(input_nodes):
        pos[n] = (0, -(i - 1) * y_sp)
    # Branch A (shifted up)
    for i, n in enumerate(branchA):
        pos[n] = (x_sp, 1.2 + -(i - 0.5) * y_sp)
    # Branch B (shifted down)
    for i, n in enumerate(branchB):
        pos[n] = (x_sp, -1.2 + -(i - 0.5) * y_sp)
    # Merge
    for i, n in enumerate(merge_nodes):
        pos[n] = (2 * x_sp, -(i - 1.5) * y_sp)
    # Output
    for i, n in enumerate(output_nodes):
        pos[n] = (3 * x_sp, -(i - 0.5) * y_sp)

    G = nx.DiGraph()
    # Input -> branches
    for src in input_nodes:
        for dst in branchA + branchB:
            G.add_edge(src, dst)
    # Branches -> merge
    for src in branchA + branchB:
        for dst in merge_nodes:
            G.add_edge(src, dst)
    # Merge -> output
    for src in merge_nodes:
        for dst in output_nodes:
            G.add_edge(src, dst)

    nx.draw_networkx_edges(
        G, pos, ax=ax, edge_color=GREEN, width=1.2, alpha=0.5,
        arrows=True, arrowstyle='-|>', arrowsize=10,
        min_source_margin=12, min_target_margin=12)

    all_nodes = list(pos.keys())
    # Colour branches differently
    node_colors = []
    for n in all_nodes:
        if n.startswith('A'):
            node_colors.append('#27ae60')  # darker green
        elif n.startswith('B'):
            node_colors.append('#58d68d')  # lighter green
        else:
            node_colors.append(GREEN)

    nx.draw_networkx_nodes(
        G, pos, nodelist=all_nodes, ax=ax,
        node_size=500, node_color=node_colors,
        edgecolors='white', linewidths=1.0)

    # Branch labels
    ax.text(pos['A0'][0], pos['A0'][1] + 0.7, 'Branch A',
            fontsize=13, color=MUTED, ha='center', fontweight='bold')
    ax.text(pos['B0'][0], pos['B1'][1] - 0.7, 'Branch B',
            fontsize=13, color=MUTED, ha='center', fontweight='bold')

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    margin = 0.8
    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(19.2, 10.8), facecolor=BG)
    fig.subplots_adjust(hspace=0.32, wspace=0.22, top=0.88, bottom=0.06)

    fig.suptitle('Neural Network Architectures as Graphs',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.96)

    # 1. Feedforward
    draw_nn(axes[0, 0], layers=[3, 4, 2], color=BLUE,
            title='Feedforward')

    # 2. Deep (VGG)
    draw_nn(axes[0, 1], layers=[3, 4, 4, 4, 4, 2], color=TEAL,
            title='Deep (VGG)')

    # 3. Branching (Inception) -- custom function
    draw_inception(axes[1, 0])

    # 4. Skip (ResNet) -- 5 layers with skip connections
    draw_nn(axes[1, 1], layers=[3, 4, 4, 4, 2], color=BLUE,
            title='Skip (ResNet)',
            skip_layers=[(0, 2), (1, 3), (2, 4)])

    # Legend for skip connections
    blue_patch = mpatches.Patch(color=BLUE, label='Regular connections')
    yellow_patch = mpatches.Patch(color=YELLOW, label='Skip connections')
    fig.legend(handles=[blue_patch, yellow_patch], loc='lower right',
               fontsize=14, frameon=False, labelcolor=TEXT,
               bbox_to_anchor=(0.98, 0.01))

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
