"""
gen_06_random_graph.py
2x2 subplot grid showing Erdos-Renyi random graph phase transition.
n=50 nodes, p in {0.01, 0.02, 0.04, 0.08}.
Largest connected component highlighted in yellow; rest in muted gray.
Spring layout computed once on a dense graph, reused across all panels.

Output: ../images/06-random-graph-phases.png (3840x2160, 4K)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '06-random-graph-phases.png')
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG        = '#1b2631'
CARD_BG   = '#1e3044'
BLUE      = '#3498db'
YELLOW    = '#f1c40f'
GREEN     = '#2ecc71'
TEAL      = '#1abc9c'
ORANGE    = '#e67e22'
RED       = '#e74c3c'
PURPLE    = '#9b59b6'
TEXT      = '#ecf0f1'
MUTED     = '#95a5a6'
DIM_GRAY  = '#4a5568'

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
N = 50
P_VALUES = [0.01, 0.02, 0.04, 0.08]
SEED = 42

# ---------------------------------------------------------------------------
# Compute a stable layout from a moderately dense reference graph
# ---------------------------------------------------------------------------
np.random.seed(SEED)
G_ref = nx.erdos_renyi_graph(N, 0.15, seed=SEED)
pos = nx.spring_layout(G_ref, seed=SEED, k=1.8, iterations=80)

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.style.use('dark_background')
fig, axes = plt.subplots(2, 2, figsize=(3840/200, 2160/200), dpi=200)
fig.patch.set_facecolor(BG)

fig.suptitle('Erd\u0151s\u2013R\u00e9nyi Random Graph Phase Transition  '
             r'$G(n, p)$  with  $n = 50$',
             fontsize=28, fontweight='bold', color=TEXT, y=0.97)

for idx, (p, ax) in enumerate(zip(P_VALUES, axes.flat)):
    ax.set_facecolor(BG)
    ax.set_aspect('equal')
    ax.axis('off')

    # Generate random graph with this p
    G = nx.erdos_renyi_graph(N, p, seed=SEED + idx)

    # Find connected components
    components = sorted(nx.connected_components(G), key=len, reverse=True)
    giant = components[0] if components else set()
    giant_frac = len(giant) / N

    # Classify nodes
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node in giant:
            node_colors.append(YELLOW)
            node_sizes.append(60)
        else:
            node_colors.append(DIM_GRAY)
            node_sizes.append(30)

    # Draw edges
    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if u in giant and v in giant:
            edge_colors.append(YELLOW)
            edge_widths.append(1.0)
        else:
            edge_colors.append(DIM_GRAY)
            edge_widths.append(0.5)

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                           width=edge_widths, alpha=0.5)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=node_sizes, edgecolors='none', alpha=0.85)

    # Panel label
    num_edges = G.number_of_edges()
    num_components = len(components)
    label = f'p = {p}'
    ax.set_title(label, fontsize=20, color=TEXT, fontweight='bold', pad=10)

    # Stats box
    stats = (f'Edges: {num_edges}\n'
             f'Components: {num_components}\n'
             f'Giant component: {giant_frac:.0%} of nodes')
    ax.text(0.02, 0.02, stats, transform=ax.transAxes,
            fontsize=11, color=TEXT, va='bottom', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG,
                      edgecolor=MUTED, linewidth=1, alpha=0.85),
            linespacing=1.5)

    # Phase label in top-right
    if giant_frac < 0.3:
        phase = 'Subcritical'
        phase_color = DIM_GRAY
    elif giant_frac < 0.7:
        phase = 'Near critical'
        phase_color = ORANGE
    else:
        phase = 'Supercritical'
        phase_color = GREEN

    ax.text(0.98, 0.98, phase, transform=ax.transAxes,
            fontsize=13, color=phase_color, va='top', ha='right',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=BG,
                      edgecolor=phase_color, linewidth=1.5, alpha=0.9))

# ---------------------------------------------------------------------------
# Bottom annotation
# ---------------------------------------------------------------------------
fig.text(0.5, 0.02,
         'Phase transition at $p = 1/n$: below this threshold the graph '
         'is fragmented; above it a "giant component" emerges connecting '
         'most nodes.',
         fontsize=14, color=MUTED, ha='center', va='center', style='italic',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=CARD_BG,
                   edgecolor=MUTED, linewidth=1, alpha=0.7))

# Legend
legend_elements = [
    mpatches.Patch(facecolor=YELLOW, edgecolor='none', label='Largest component'),
    mpatches.Patch(facecolor=DIM_GRAY, edgecolor='none', label='Other components'),
]
fig.legend(handles=legend_elements, loc='lower right',
           fontsize=12, framealpha=0.8, facecolor=CARD_BG,
           edgecolor=MUTED, labelcolor=TEXT,
           bbox_to_anchor=(0.97, 0.02))

plt.subplots_adjust(hspace=0.22, wspace=0.08, top=0.90, bottom=0.09)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.close()
print(f'Saved: {OUTPUT_PATH}')
