"""
gen_04_cayley_trees.py
All labeled trees for n=2, 3, 4 arranged in rows illustrating Cayley's formula.
- Row 1 (n=2): 1 tree.       T_2 = 2^0 = 1
- Row 2 (n=3): 3 trees.      T_3 = 3^1 = 3
- Row 3 (n=4): 16 trees.     T_4 = 4^2 = 16

Output: ../images/04-cayley-trees.png (3840x2160, 4K)
"""

import os
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '04-cayley-trees.png')
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
# Generate all labeled trees on n nodes using Prufer sequences
# ---------------------------------------------------------------------------
def prufer_to_tree(prufer_seq, n):
    """Convert a Prufer sequence to a tree (edge list). Nodes labeled 1..n."""
    degree = {i: 1 for i in range(1, n + 1)}
    for v in prufer_seq:
        degree[v] += 1

    edges = []
    seq = list(prufer_seq)
    for v in seq:
        for u in range(1, n + 1):
            if degree[u] == 1:
                edges.append((u, v))
                degree[u] -= 1
                degree[v] -= 1
                break
    # Last edge: two remaining nodes with degree 1
    last = [u for u in range(1, n + 1) if degree[u] == 1]
    if len(last) == 2:
        edges.append((last[0], last[1]))
    return edges


def all_labeled_trees(n):
    """Generate all labeled trees on n nodes via Prufer sequences."""
    if n == 1:
        return [nx.Graph()]
    if n == 2:
        G = nx.Graph()
        G.add_edge(1, 2)
        return [G]

    trees = []
    # Prufer sequences have length n-2, elements from {1, ..., n}
    for seq in itertools.product(range(1, n + 1), repeat=n - 2):
        edges = prufer_to_tree(seq, n)
        G = nx.Graph()
        G.add_nodes_from(range(1, n + 1))
        G.add_edges_from(edges)
        trees.append(G)
    return trees

# ---------------------------------------------------------------------------
# Layout for small trees inside a cell
# ---------------------------------------------------------------------------
def tree_layout(G, n):
    """Produce a compact layout for a small labeled tree."""
    if n == 2:
        return {1: (-0.3, 0), 2: (0.3, 0)}
    if n == 3:
        # Star-like or path-like
        # Find if there is a degree-2 node (center of star)
        center = [v for v in G.nodes() if G.degree(v) == 2]
        if center:
            c = center[0]
            leaves = [v for v in G.nodes() if v != c]
            return {c: (0, -0.15), leaves[0]: (-0.3, 0.25), leaves[1]: (0.3, 0.25)}
        else:
            # Path: arrange linearly
            path = list(nx.dfs_preorder_nodes(G, source=1))
            return {path[0]: (-0.3, 0), path[1]: (0, 0), path[2]: (0.3, 0)}

    # n == 4
    # Use spring layout with fixed seed for consistency, then normalize
    pos = nx.spring_layout(G, seed=hash(tuple(sorted(G.edges()))) % 2**31,
                           k=1.2, iterations=50)
    # Normalize to [-0.35, 0.35]
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    xrange = max(xmax - xmin, 0.01)
    yrange = max(ymax - ymin, 0.01)
    for v in pos:
        pos[v] = (
            (pos[v][0] - xmin) / xrange * 0.6 - 0.3,
            (pos[v][1] - ymin) / yrange * 0.5 - 0.25,
        )
    return pos

# ---------------------------------------------------------------------------
# Drawing function for one tree in a given axes region
# ---------------------------------------------------------------------------
def draw_tree_cell(ax, G, n, cx, cy, cell_w, cell_h):
    """Draw a small tree centered at (cx, cy) within a cell of size cell_w x cell_h."""
    pos = tree_layout(G, n)
    scale_x = cell_w * 0.7
    scale_y = cell_h * 0.55

    # Draw edges
    for u, v in G.edges():
        x1 = cx + pos[u][0] * scale_x
        y1 = cy + pos[u][1] * scale_y
        x2 = cx + pos[v][0] * scale_x
        y2 = cy + pos[v][1] * scale_y
        ax.plot([x1, x2], [y1, y2], color=TEAL, linewidth=1.8,
                solid_capstyle='round', zorder=2)

    # Draw nodes
    node_r = cell_w * 0.06
    for v_node in G.nodes():
        x = cx + pos[v_node][0] * scale_x
        y = cy + pos[v_node][1] * scale_y
        circle = plt.Circle((x, y), node_r, facecolor=CARD_BG,
                             edgecolor=TEAL, linewidth=1.2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, str(v_node), fontsize=7, fontweight='bold',
                color=TEXT, ha='center', va='center', zorder=4)

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(3840/200, 2160/200), dpi=200)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.axis('off')

# Total layout area
total_w = 16.0
total_h = 9.0
ax.set_xlim(0, total_w)
ax.set_ylim(0, total_h)

# ---------------------------------------------------------------------------
# Row 1: n=2, T_2 = 1 tree
# ---------------------------------------------------------------------------
trees_2 = all_labeled_trees(2)
row_y = 7.8
cell_w = 2.0
cell_h = 1.2
x_start = total_w / 2 - (len(trees_2) * cell_w) / 2

ax.text(0.5, row_y, r'$n = 2$', fontsize=18, color=YELLOW, fontweight='bold',
        va='center')
ax.text(0.5, row_y - 0.5, r'$T_2 = 1$', fontsize=14, color=MUTED, va='center')

for i, tree in enumerate(trees_2):
    cx = x_start + i * cell_w + cell_w / 2
    cy = row_y - 0.15
    # Cell background
    rect = mpatches.FancyBboxPatch(
        (cx - cell_w*0.45, cy - cell_h*0.45), cell_w*0.9, cell_h*0.9,
        boxstyle=mpatches.BoxStyle.Round(pad=0.05),
        facecolor=CARD_BG, edgecolor=MUTED, linewidth=0.8, alpha=0.5, zorder=1)
    ax.add_patch(rect)
    draw_tree_cell(ax, tree, 2, cx, cy, cell_w, cell_h)

# ---------------------------------------------------------------------------
# Row 2: n=3, T_3 = 3 trees
# ---------------------------------------------------------------------------
trees_3 = all_labeled_trees(3)
row_y = 6.0
x_start = total_w / 2 - (len(trees_3) * cell_w) / 2

ax.text(0.5, row_y, r'$n = 3$', fontsize=18, color=YELLOW, fontweight='bold',
        va='center')
ax.text(0.5, row_y - 0.5, r'$T_3 = 3$', fontsize=14, color=MUTED, va='center')

for i, tree in enumerate(trees_3):
    cx = x_start + i * cell_w + cell_w / 2
    cy = row_y - 0.15
    rect = mpatches.FancyBboxPatch(
        (cx - cell_w*0.45, cy - cell_h*0.45), cell_w*0.9, cell_h*0.9,
        boxstyle=mpatches.BoxStyle.Round(pad=0.05),
        facecolor=CARD_BG, edgecolor=MUTED, linewidth=0.8, alpha=0.5, zorder=1)
    ax.add_patch(rect)
    draw_tree_cell(ax, tree, 3, cx, cy, cell_w, cell_h)

# ---------------------------------------------------------------------------
# Row 3: n=4, T_4 = 16 trees in 4x4 grid
# ---------------------------------------------------------------------------
trees_4 = all_labeled_trees(4)
row_y_top = 4.2
cell_w4 = 2.0
cell_h4 = 1.1
cols = 8
rows_needed = 2  # 16 trees in 8x2

ax.text(total_w / 2, row_y_top + 0.8, r'$n = 4$,  $T_4 = 16$', fontsize=18,
        color=YELLOW, fontweight='bold', va='center', ha='center')

grid_w = cols * cell_w4
x_start4 = (total_w - grid_w) / 2

for idx, tree in enumerate(trees_4):
    col = idx % cols
    row = idx // cols
    cx = x_start4 + col * cell_w4 + cell_w4 / 2
    cy = row_y_top - row * cell_h4 - 0.3

    rect = mpatches.FancyBboxPatch(
        (cx - cell_w4*0.45, cy - cell_h4*0.42), cell_w4*0.9, cell_h4*0.84,
        boxstyle=mpatches.BoxStyle.Round(pad=0.05),
        facecolor=CARD_BG, edgecolor=MUTED, linewidth=0.6, alpha=0.4, zorder=1)
    ax.add_patch(rect)
    draw_tree_cell(ax, tree, 4, cx, cy, cell_w4, cell_h4)

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
ax.text(total_w / 2, total_h - 0.25,
        "Cayley's Formula:  The number of labeled trees on n nodes is  $T_n = n^{n-2}$",
        fontsize=26, fontweight='bold', color=TEXT, ha='center', va='top')

# Bottom annotation
ax.text(total_w / 2, 0.4,
        '$T_2 = 2^0 = 1$          $T_3 = 3^1 = 3$          $T_4 = 4^2 = 16$'
        '          $T_5 = 5^3 = 125$          $T_{10} = 10^8 = 100{,}000{,}000$',
        fontsize=15, color=MUTED, ha='center', va='center', style='italic')

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.close()
print(f'Saved: {OUTPUT_PATH}')
