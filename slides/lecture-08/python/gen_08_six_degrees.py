#!/usr/bin/env python3
"""
Generate slide 08: Six Degrees of Separation.

Social network with 4 colour-coded communities built via a stochastic
block model. Bridge nodes (connecting communities) are highlighted in
yellow. One shortest path between distant communities is drawn in bold
yellow with its length annotated.

Output: ../images/08-six-degrees.png (3840x2160, 4K)
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
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '08-six-degrees.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG        = '#1b2631'
CARD_BG   = '#1e3044'
BLUE      = '#3498db'
GREEN     = '#2ecc71'
ORANGE    = '#e67e22'
PURPLE    = '#9b59b6'
YELLOW    = '#f1c40f'
TEXT      = '#ecf0f1'
MUTED     = '#95a5a6'
EDGE_CLR  = '#4a5568'

COMMUNITY_COLORS = [BLUE, GREEN, ORANGE, PURPLE]

# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------
SIZES = [8, 8, 7, 7]                   # 30 nodes total
P_INTRA = 0.60
P_INTER = 0.05
SEED = 42


def build_social_network():
    """Create a stochastic block model graph with 4 communities."""
    n_communities = len(SIZES)
    probs = [[P_INTRA if i == j else P_INTER
              for j in range(n_communities)]
             for i in range(n_communities)]

    np.random.seed(SEED)
    G = nx.stochastic_block_model(SIZES, probs, seed=SEED)

    # Assign community labels
    community_map = {}
    offset = 0
    for c_idx, size in enumerate(SIZES):
        for node in range(offset, offset + size):
            community_map[node] = c_idx
        offset += size
    nx.set_node_attributes(G, community_map, 'community')
    return G, community_map


def find_bridge_nodes(G, community_map):
    """Nodes with edges to at least two different communities."""
    bridges = set()
    for node in G.nodes():
        neighbour_communities = set()
        for nbr in G.neighbors(node):
            neighbour_communities.add(community_map[nbr])
        if len(neighbour_communities) >= 2:
            bridges.add(node)
    return bridges


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    G, community_map = build_social_network()
    bridge_nodes = find_bridge_nodes(G, community_map)

    # Pick two distant nodes: one from community 0, one from community 3
    comm0_nodes = [n for n, c in community_map.items() if c == 0]
    comm3_nodes = [n for n, c in community_map.items() if c == 3]

    # Find the pair with the longest shortest path
    best_pair = None
    best_length = 0
    for s in comm0_nodes:
        for t in comm3_nodes:
            if nx.has_path(G, s, t):
                length = nx.shortest_path_length(G, s, t)
                if length > best_length:
                    best_length = length
                    best_pair = (s, t)

    if best_pair is None:
        # Fallback: just pick first nodes
        best_pair = (comm0_nodes[0], comm3_nodes[0])

    shortest_path = nx.shortest_path(G, best_pair[0], best_pair[1])
    path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
    path_length = len(path_edges)

    # Layout
    pos = nx.kamada_kawai_layout(G)

    # -----------------------------------------------------------------------
    # Plot
    # -----------------------------------------------------------------------
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    fig.suptitle('Social Network: Six Degrees of Separation',
                 fontsize=36, fontweight='bold', color=TEXT, y=0.95)

    # Node colours and sizes
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node in bridge_nodes:
            node_colors.append(YELLOW)
            node_sizes.append(500)
        else:
            node_colors.append(COMMUNITY_COLORS[community_map[node]])
            node_sizes.append(300)

    # Draw all edges (background)
    non_path_edges = [e for e in G.edges() if e not in path_edges
                      and (e[1], e[0]) not in path_edges]
    nx.draw_networkx_edges(G, pos, edgelist=non_path_edges, ax=ax,
                           edge_color=EDGE_CLR, width=1.0, alpha=0.4)

    # Draw shortest-path edges (foreground)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax,
                           edge_color=YELLOW, width=4.0, alpha=0.95,
                           style='solid')

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=node_sizes,
                           node_color=node_colors, edgecolors='white',
                           linewidths=1.2)

    # Labels on path nodes
    path_labels = {n: str(i) for i, n in enumerate(shortest_path)}
    nx.draw_networkx_labels(G, pos, labels=path_labels, ax=ax,
                            font_size=11, font_color='#1b2631',
                            font_weight='bold')

    # Path length annotation
    mid_idx = len(shortest_path) // 2
    mid_node = shortest_path[mid_idx]
    mx, my = pos[mid_node]
    ax.annotate(f'Shortest path length = {path_length}',
                xy=(mx, my), xytext=(mx + 0.15, my + 0.20),
                fontsize=20, fontweight='bold', color=YELLOW,
                arrowprops=dict(arrowstyle='->', color=YELLOW, lw=2),
                bbox=dict(boxstyle='round,pad=0.4', facecolor=CARD_BG,
                          edgecolor=YELLOW, alpha=0.9))

    # Legend
    handles = [mpatches.Patch(color=c, label=f'Community {i+1}')
               for i, c in enumerate(COMMUNITY_COLORS)]
    handles.append(mpatches.Patch(color=YELLOW, label='Bridge nodes'))
    fig.legend(handles=handles, loc='lower center', ncol=5,
               fontsize=16, frameon=False, labelcolor=TEXT,
               handlelength=2.0, bbox_to_anchor=(0.5, 0.02))

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
