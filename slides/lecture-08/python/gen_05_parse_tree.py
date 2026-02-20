"""
gen_05_parse_tree.py
Two subplots showing tree structures in CS/AI:
LEFT:  NLP parse tree for "The cat sat on the mat"
RIGHT: Simple decision tree for a weather scenario

Output: ../images/05-parse-tree.png (3840x2160, 4K)
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
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '05-parse-tree.png')
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
# Helper: draw a tree given nodes, edges, positions, and styling info
# ---------------------------------------------------------------------------
def draw_labeled_tree(ax, nodes, edges, pos, node_styles, edge_labels=None):
    """
    nodes: list of (id, label)
    edges: list of (parent_id, child_id)
    pos: dict {id: (x, y)}
    node_styles: dict {id: {'color': ..., 'fontsize': ..., 'shape': ...}}
    edge_labels: optional dict {(parent, child): label}
    """
    # Draw edges first
    for parent, child in edges:
        x1, y1 = pos[parent]
        x2, y2 = pos[child]
        ax.plot([x1, x2], [y1, y2], color=MUTED, linewidth=2.0,
                solid_capstyle='round', zorder=1, alpha=0.7)

        # Edge label if any
        if edge_labels and (parent, child) in edge_labels:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            label = edge_labels[(parent, child)]
            ax.text(mx - 0.12, my, label, fontsize=10, color=ORANGE,
                    ha='center', va='center', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.1', facecolor=BG,
                              edgecolor='none', alpha=0.8))

    # Draw nodes
    for nid, label in nodes:
        x, y = pos[nid]
        style = node_styles.get(nid, {})
        color = style.get('color', BLUE)
        fs = style.get('fontsize', 13)
        shape = style.get('shape', 'round')
        is_leaf = style.get('leaf', False)

        if is_leaf:
            # Leaf: rounded rectangle
            tw = len(label) * 0.09 + 0.15
            rect = mpatches.FancyBboxPatch(
                (x - tw/2, y - 0.13), tw, 0.26,
                boxstyle=mpatches.BoxStyle.Round(pad=0.05),
                facecolor=CARD_BG, edgecolor=color, linewidth=1.5, zorder=3)
            ax.add_patch(rect)
        else:
            # Internal node: circle / ellipse
            tw = max(len(label) * 0.065 + 0.1, 0.18)
            ellipse = mpatches.Ellipse(
                (x, y), tw * 2, 0.28,
                facecolor=color, edgecolor=TEXT, linewidth=1.5,
                alpha=0.85, zorder=3)
            ax.add_patch(ellipse)

        text_color = TEXT if not is_leaf else color
        ax.text(x, y, label, fontsize=fs, fontweight='bold',
                color=text_color, ha='center', va='center', zorder=4)


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

fig.suptitle('Trees in Computer Science and AI',
             fontsize=30, fontweight='bold', color=TEXT, y=0.96)

# ===================================================================
# LEFT: NLP Parse Tree for "The cat sat on the mat"
# ===================================================================
# S -> NP VP
# NP -> DET N
# VP -> V PP
# PP -> P NP2
# NP2 -> DET2 N2

# Node IDs and labels
parse_nodes = [
    ('S', 'S'),
    ('NP1', 'NP'), ('VP', 'VP'),
    ('DET1', 'Det'), ('N1', 'N'),
    ('V', 'V'), ('PP', 'PP'),
    ('P', 'P'), ('NP2', 'NP'),
    ('DET2', 'Det'), ('N2', 'N'),
    # Leaf words
    ('w_the1', '"The"'), ('w_cat', '"cat"'),
    ('w_sat', '"sat"'),
    ('w_on', '"on"'),
    ('w_the2', '"the"'), ('w_mat', '"mat"'),
]

parse_edges = [
    ('S', 'NP1'), ('S', 'VP'),
    ('NP1', 'DET1'), ('NP1', 'N1'),
    ('VP', 'V'), ('VP', 'PP'),
    ('PP', 'P'), ('PP', 'NP2'),
    ('NP2', 'DET2'), ('NP2', 'N2'),
    ('DET1', 'w_the1'), ('N1', 'w_cat'),
    ('V', 'w_sat'),
    ('P', 'w_on'),
    ('DET2', 'w_the2'), ('N2', 'w_mat'),
]

# Manual top-down layout
parse_pos = {
    'S':     (0.0,  3.0),
    'NP1':   (-1.2, 2.2),
    'VP':    (1.2,  2.2),
    'DET1':  (-1.7, 1.4),
    'N1':    (-0.7, 1.4),
    'V':     (0.4,  1.4),
    'PP':    (2.0,  1.4),
    'P':     (1.3,  0.6),
    'NP2':   (2.7,  0.6),
    'DET2':  (2.2, -0.2),
    'N2':    (3.2, -0.2),
    'w_the1': (-1.7, 0.5),
    'w_cat':  (-0.7, 0.5),
    'w_sat':  (0.4,  0.5),
    'w_on':   (1.3, -0.3),
    'w_the2': (2.2, -1.0),
    'w_mat':  (3.2, -1.0),
}

parse_styles = {}
internal_nodes = ['S', 'NP1', 'VP', 'DET1', 'N1', 'V', 'PP', 'P', 'NP2', 'DET2', 'N2']
leaf_nodes = ['w_the1', 'w_cat', 'w_sat', 'w_on', 'w_the2', 'w_mat']
for nid in internal_nodes:
    parse_styles[nid] = {'color': BLUE, 'fontsize': 14}
for nid in leaf_nodes:
    parse_styles[nid] = {'color': YELLOW, 'fontsize': 12, 'leaf': True}

draw_labeled_tree(ax1, parse_nodes, parse_edges, parse_pos, parse_styles)
ax1.set_title('Parse Tree (NLP)', fontsize=22, color=TEXT, pad=15)
ax1.set_xlim(-2.8, 4.3)
ax1.set_ylim(-1.8, 3.8)

# Sentence below
ax1.text(0.75, -1.5, '"The cat sat on the mat"',
         fontsize=15, color=YELLOW, ha='center', va='center',
         style='italic',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG,
                   edgecolor=YELLOW, linewidth=1, alpha=0.7))

# ===================================================================
# RIGHT: Decision Tree
# ===================================================================
# Root: "Temperature > 30C?"
#   Yes -> "Humidity > 70%?"
#     Yes -> "Stay Inside"
#     No  -> "Use Sunscreen"
#   No  -> "Go Outside"

dt_nodes = [
    ('root',  'Temp > 30\u00b0C?'),
    ('humid', 'Humidity > 70%?'),
    ('no_hot', 'Go Outside'),
    ('stay',  'Stay Inside'),
    ('sun',   'Use Sunscreen'),
]

dt_edges = [
    ('root', 'humid'),
    ('root', 'no_hot'),
    ('humid', 'stay'),
    ('humid', 'sun'),
]

dt_pos = {
    'root':   (0.0,  2.5),
    'humid':  (-1.2, 1.3),
    'no_hot': (1.2,  1.3),
    'stay':   (-2.0, 0.1),
    'sun':    (-0.4, 0.1),
}

dt_edge_labels = {
    ('root', 'humid'):  'Yes',
    ('root', 'no_hot'): 'No',
    ('humid', 'stay'):  'Yes',
    ('humid', 'sun'):   'No',
}

dt_styles = {
    'root':   {'color': GREEN, 'fontsize': 12},
    'humid':  {'color': GREEN, 'fontsize': 12},
    'no_hot': {'color': YELLOW, 'fontsize': 12, 'leaf': True},
    'stay':   {'color': YELLOW, 'fontsize': 12, 'leaf': True},
    'sun':    {'color': YELLOW, 'fontsize': 12, 'leaf': True},
}

draw_labeled_tree(ax2, dt_nodes, dt_edges, dt_pos, dt_styles, dt_edge_labels)
ax2.set_title('Decision Tree (ML)', fontsize=22, color=TEXT, pad=15)
ax2.set_xlim(-3.0, 2.5)
ax2.set_ylim(-0.8, 3.5)

# Annotation
ax2.text(-0.4, -0.6,
         'Decision trees partition data recursively\nusing feature thresholds.',
         fontsize=12, color=MUTED, ha='center', va='center',
         style='italic', linespacing=1.5)

plt.subplots_adjust(wspace=0.2, top=0.88, bottom=0.06)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.close()
print(f'Saved: {OUTPUT_PATH}')
