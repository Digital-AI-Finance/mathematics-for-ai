"""
gen_02_konigsberg_graph.py
Abstract graph version of Konigsberg using NetworkX MultiGraph.
4 nodes (A, B, C, D) with 7 edges matching the historical bridges.
Multiple edges between same node pairs drawn with different curvatures.

Historical: A-C:2, D-C:2, B-C:1, A-B:1, D-B:1
Degrees: A=3, B=3, C=5, D=3 (all odd)

Output: ../images/02-konigsberg-graph.png (3840x2160, 4K)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import networkx as nx
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '02-konigsberg-graph.png')
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

# ---------------------------------------------------------------------------
# Build the multigraph
# ---------------------------------------------------------------------------
G = nx.MultiGraph()
G.add_nodes_from(['A', 'B', 'C', 'D'])

# 7 edges matching historical Konigsberg:
# A-C: 2, D-C: 2, B-C: 1, A-B: 1, D-B: 1
edges = [
    ('A', 'C'), ('A', 'C'),  # 2 bridges north-island
    ('D', 'C'), ('D', 'C'),  # 2 bridges south-island
    ('B', 'C'),              # 1 bridge east-island
    ('A', 'B'),              # 1 bridge north-east
    ('D', 'B'),              # 1 bridge south-east
]
for e in edges:
    G.add_edge(*e)

# Positions mirroring geographical layout:
# A=north, D=south, C=island(center), B=east
pos = {
    'A': (0.0, 1.0),
    'B': (2.0, 0.0),
    'C': (0.8, 0.0),
    'D': (0.0, -1.0),
}

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(3840/200, 2160/200), dpi=200)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_aspect('equal')
ax.axis('off')

# ---------------------------------------------------------------------------
# Draw edges with curvature to distinguish multi-edges
# ---------------------------------------------------------------------------
edge_count = {}
EDGE_COLORS = [ORANGE, YELLOW, GREEN, TEAL, BLUE, RED, PURPLE]

for idx, (u, v) in enumerate(edges):
    pair = tuple(sorted([u, v]))
    edge_count[pair] = edge_count.get(pair, 0)
    count = edge_count[pair]

    # Curvature: first edge slightly curved, second edge curved opposite
    if count == 0:
        rad = 0.15
    else:
        rad = -0.25

    edge_count[pair] += 1

    x1, y1 = pos[u]
    x2, y2 = pos[v]
    color = EDGE_COLORS[idx % len(EDGE_COLORS)]

    ax.annotate('',
                xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='-',
                    color=color,
                    linewidth=4.5,
                    connectionstyle=f'arc3,rad={rad}',
                    shrinkA=30, shrinkB=30,
                ),
                zorder=2)

# ---------------------------------------------------------------------------
# Draw nodes
# ---------------------------------------------------------------------------
for node, (x, y) in pos.items():
    circle = plt.Circle((x, y), 0.14, facecolor=BLUE, edgecolor=TEXT,
                         linewidth=2.5, zorder=4)
    ax.add_patch(circle)
    ax.text(x, y, node, fontsize=28, fontweight='bold', color=TEXT,
            ha='center', va='center', zorder=5)

# ---------------------------------------------------------------------------
# Degree annotations
# ---------------------------------------------------------------------------
for node in G.nodes():
    deg = G.degree(node)
    x, y = pos[node]
    offsets = {'A': (-0.28, 0.12), 'B': (0.28, 0.12),
               'C': (-0.08, 0.22), 'D': (-0.28, -0.12)}
    ox, oy = offsets[node]
    ax.text(x + ox, y + oy, f'deg={deg}', fontsize=14, color=MUTED,
            ha='center', va='center', zorder=5,
            bbox=dict(boxstyle='round,pad=0.15', facecolor=BG,
                      edgecolor=MUTED, alpha=0.8, linewidth=1))

# ---------------------------------------------------------------------------
# Edge legend
# ---------------------------------------------------------------------------
legend_items = []
pair_labels = ['A-C (1)', 'A-C (2)', 'D-C (1)', 'D-C (2)',
               'B-C', 'A-B', 'D-B']
for i, label in enumerate(pair_labels):
    legend_items.append(
        mpatches.Patch(color=EDGE_COLORS[i], label=label))

legend = ax.legend(handles=legend_items, loc='lower left',
                   fontsize=12, framealpha=0.8,
                   facecolor=CARD_BG, edgecolor=MUTED, labelcolor=TEXT,
                   title='7 Bridges', title_fontsize=13)
legend.get_title().set_color(TEXT)

# ---------------------------------------------------------------------------
# Title and subtitle
# ---------------------------------------------------------------------------
ax.set_title('The Graph Abstraction',
             fontsize=34, fontweight='bold', color=TEXT, pad=25)

ax.text(1.0, -1.6,
        'Landmasses become nodes. Bridges become edges.\n'
        'Every node has odd degree, so no Eulerian circuit exists.',
        fontsize=16, color=MUTED, ha='center', va='center',
        style='italic', linespacing=1.6)

# Adjust limits
ax.set_xlim(-0.8, 2.8)
ax.set_ylim(-1.9, 1.8)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.close()
print(f'Saved: {OUTPUT_PATH}')
