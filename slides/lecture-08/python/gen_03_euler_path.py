"""
gen_03_euler_path.py
Two side-by-side subplots demonstrating Euler's theorem on Eulerian paths.
LEFT:  Konigsberg graph with all odd-degree nodes highlighted -- NO Euler path.
RIGHT: A simple graph with exactly 2 odd-degree nodes -- Euler path EXISTS, traced.

Output: ../images/03-euler-path-rule.png (3840x2160, 4K)
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
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '03-euler-path-rule.png')
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
# Figure
# ---------------------------------------------------------------------------
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(3840/200, 2160/200), dpi=200)
fig.patch.set_facecolor(BG)
for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    ax.set_aspect('equal')
    ax.axis('off')

fig.suptitle("Euler's Theorem on Eulerian Paths",
             fontsize=32, fontweight='bold', color=TEXT, y=0.97)

# ===================================================================
# LEFT PANEL: Konigsberg graph -- all nodes odd degree, NO Euler path
# ===================================================================
G1 = nx.MultiGraph()
G1.add_nodes_from(['A', 'B', 'C', 'D'])
# Historical: A-C:2, D-C:2, B-C:1, A-B:1, D-B:1
k_edges = [('A','C'), ('A','C'), ('D','C'), ('D','C'),
           ('B','C'), ('A','B'), ('D','B')]
for e in k_edges:
    G1.add_edge(*e)

pos1 = {'A': (0, 1), 'B': (2, 0), 'C': (0.8, 0), 'D': (0, -1)}

# Draw edges with curvature for multi-edges
edge_counter = {}
for u, v in k_edges:
    pair = tuple(sorted([u, v]))
    edge_counter[pair] = edge_counter.get(pair, 0)
    cnt = edge_counter[pair]
    rad = 0.2 if cnt == 0 else (-0.3 if cnt == 1 else 0.4)
    edge_counter[pair] += 1

    x1, y1 = pos1[u]
    x2, y2 = pos1[v]
    ax1.annotate('', xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle='-', color=MUTED, linewidth=3,
                                 connectionstyle=f'arc3,rad={rad}',
                                 shrinkA=22, shrinkB=22),
                 zorder=2)

# Draw nodes -- all odd degree, circle in red
for node, (x, y) in pos1.items():
    deg = G1.degree(node)
    # Outer warning ring (all are odd)
    ring = plt.Circle((x, y), 0.16, facecolor='none', edgecolor=RED,
                       linewidth=3, linestyle='--', zorder=3)
    ax1.add_patch(ring)
    # Node circle
    circle = plt.Circle((x, y), 0.10, facecolor=RED, edgecolor=TEXT,
                         linewidth=2, zorder=4, alpha=0.9)
    ax1.add_patch(circle)
    # Label
    ax1.text(x, y, node, fontsize=20, fontweight='bold', color=TEXT,
             ha='center', va='center', zorder=5)
    # Degree annotation
    offset_map = {'A': (-0.28, 0.12), 'B': (0.28, 0.12),
                  'C': (-0.08, 0.22), 'D': (-0.28, -0.12)}
    ox, oy = offset_map[node]
    ax1.text(x + ox, y + oy, f'deg {deg}\n(odd)',
             fontsize=11, color=RED, ha='center', va='center',
             fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.15', facecolor=BG,
                       edgecolor=RED, alpha=0.85, linewidth=1))

# Big X mark
ax1.text(1.0, -1.5, '\u2717  NO Eulerian Path', fontsize=20, fontweight='bold',
         color=RED, ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG,
                   edgecolor=RED, linewidth=2))

ax1.text(1.0, -1.85, 'All 4 nodes have odd degree', fontsize=13,
         color=MUTED, ha='center', va='center', style='italic')

ax1.set_title('K\u00f6nigsberg Bridge Graph', fontsize=20, color=TEXT, pad=12)
ax1.set_xlim(-0.7, 2.7)
ax1.set_ylim(-2.0, 1.8)

# ===================================================================
# RIGHT PANEL: A graph with exactly 2 odd-degree nodes, Euler path shown
# ===================================================================
# Graph: "house" shape -- a square with one diagonal
# Nodes: 1--2--3--4--1, plus diagonal 1--3
# Degrees: 1:3(odd), 2:2(even), 3:3(odd), 4:2(even) -- exactly 2 odd nodes
G2 = nx.Graph()
G2.add_edges_from([(1,2), (2,3), (3,4), (4,1), (1,3)])

pos2 = {1: (0, 0), 2: (1.2, 0), 3: (1.2, 1.2), 4: (0, 1.2)}

# Draw all edges in muted first
for u, v in G2.edges():
    x1, y1 = pos2[u]
    x2, y2 = pos2[v]
    ax2.plot([x1, x2], [y1, y2], color=MUTED, linewidth=2.5,
             solid_capstyle='round', zorder=2, alpha=0.4)

# Euler path: 1 -> 2 -> 3 -> 1 -> 4 -> 3
# (starts and ends at the two odd-degree nodes: 1 and 3)
euler_path = [1, 2, 3, 1, 4, 3]

# Draw the Euler path with arrows in green
for i in range(len(euler_path) - 1):
    u, v = euler_path[i], euler_path[i+1]
    x1, y1 = pos2[u]
    x2, y2 = pos2[v]

    # Slight offset for overlapping edges (1->3 drawn twice in different directions)
    dx, dy = x2 - x1, y2 - y1
    perp_x, perp_y = -dy, dx
    norm = (perp_x**2 + perp_y**2)**0.5
    if norm > 0:
        perp_x, perp_y = perp_x / norm * 0.04, perp_y / norm * 0.04
    offset = i * 0.015  # slight cumulative offset

    ax2.annotate('',
                 xy=(x2 + perp_x * i * 0.5, y2 + perp_y * i * 0.5),
                 xytext=(x1 + perp_x * i * 0.5, y1 + perp_y * i * 0.5),
                 arrowprops=dict(
                     arrowstyle='->,head_width=0.25,head_length=0.15',
                     color=GREEN, linewidth=3.5,
                     shrinkA=18, shrinkB=18,
                     connectionstyle=f'arc3,rad={0.05 * (i - 2)}',
                 ),
                 zorder=3)

    # Step number
    mx = (x1 + x2) / 2 + perp_x * (i * 0.5 + 2)
    my = (y1 + y2) / 2 + perp_y * (i * 0.5 + 2)
    ax2.text(mx, my, str(i + 1), fontsize=11, fontweight='bold',
             color=GREEN, ha='center', va='center',
             bbox=dict(boxstyle='circle,pad=0.15', facecolor=BG,
                       edgecolor=GREEN, linewidth=1, alpha=0.9),
             zorder=6)

# Draw nodes
for node, (x, y) in pos2.items():
    deg = G2.degree(node)
    is_odd = deg % 2 == 1
    node_color = ORANGE if is_odd else BLUE

    if is_odd:
        ring = plt.Circle((x, y), 0.14, facecolor='none', edgecolor=ORANGE,
                           linewidth=2.5, linestyle='--', zorder=3)
        ax2.add_patch(ring)

    circle = plt.Circle((x, y), 0.09, facecolor=node_color, edgecolor=TEXT,
                         linewidth=2, zorder=4)
    ax2.add_patch(circle)
    ax2.text(x, y, str(node), fontsize=18, fontweight='bold', color=TEXT,
             ha='center', va='center', zorder=5)

    # Degree label
    side = 1 if x > 0.6 else -1
    vert = 1 if y > 0.6 else -1
    ax2.text(x + side * 0.22, y + vert * 0.08,
             f'deg {deg}\n({"odd" if is_odd else "even"})',
             fontsize=10, color=node_color, ha='center', va='center',
             fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.12', facecolor=BG,
                       edgecolor=node_color, alpha=0.85, linewidth=1))

# Check mark
ax2.text(0.6, -0.55, '\u2713  Eulerian Path EXISTS', fontsize=20,
         fontweight='bold', color=GREEN, ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG,
                   edgecolor=GREEN, linewidth=2))

ax2.text(0.6, -0.9, 'Exactly 2 nodes have odd degree (nodes 1 & 3)',
         fontsize=13, color=MUTED, ha='center', va='center', style='italic')

ax2.set_title('Graph with Eulerian Path', fontsize=20, color=TEXT, pad=12)
ax2.set_xlim(-0.6, 1.8)
ax2.set_ylim(-1.2, 1.7)

# ---------------------------------------------------------------------------
# Bottom rule box
# ---------------------------------------------------------------------------
rule_text = (
    "Euler's Theorem:  A connected graph has an Eulerian path \u2194 "
    "it has exactly 0 or 2 nodes of odd degree."
)
fig.text(0.5, 0.03, rule_text, fontsize=17, color=YELLOW, ha='center',
         va='center', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor=CARD_BG,
                   edgecolor=YELLOW, linewidth=2, alpha=0.9))

plt.subplots_adjust(wspace=0.25, top=0.90, bottom=0.12)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.close()
print(f'Saved: {OUTPUT_PATH}')
