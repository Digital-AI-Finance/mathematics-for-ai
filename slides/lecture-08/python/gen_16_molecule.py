#!/usr/bin/env python3
"""
gen_16_molecule.py
Caffeine molecule (C8H10N4O2) rendered as a graph.

Skeletal formula style: only heavy atoms (C, N, O) shown as nodes,
bonds as edges. Double bonds drawn as parallel lines.
Two fused rings: 6-membered pyrimidinedione + 5-membered imidazole.

Output: ../images/16-molecule-graph.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '16-molecule-graph.png')

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

ATOM_COLORS = {
    'C': BLUE,
    'N': GREEN,
    'O': RED,
}

# ---------------------------------------------------------------------------
# Caffeine structure (manual coordinates matching actual geometry)
# ---------------------------------------------------------------------------
# Caffeine: two fused rings
#   6-membered ring (pyrimidine): atoms 0-5
#   5-membered ring (imidazole): atoms 3,4,6,7,8 (shares edge 3-4)
#   Methyl groups: atoms 9,10,11 (CH3 attached to N atoms)
#   Oxygens: atoms 12,13 (=O on carbons)

# Using a coordinate system that approximates the real molecular geometry.
# Hexagonal ring on the left, pentagonal ring on the right.
SCALE = 1.4

# 6-membered ring (left) - roughly hexagonal
hex_r = 1.0 * SCALE
hex_cx, hex_cy = 0.0, 0.0
hex_angles = [90, 150, 210, 270, 330, 30]  # degrees, starting top

# Pentagonal ring (right) - fused to the hex ring at positions 4,5
pent_r = 0.85 * SCALE

# Manually place atoms for caffeine with correct topology:
#
#    O=C2---N1(CH3)---C6=O
#       |              |
#       N3(CH3)       C5
#       |            / |
#       C4====N7     |
#        \   /      |
#         N9(CH3)---C8
#
# A cleaner 2D layout:

ATOMS = {
    # id: (element, x, y)
    # 6-membered ring
    'N1':  ('N', -1.2 * SCALE,  0.7 * SCALE),
    'C2':  ('C',  0.0 * SCALE,  1.2 * SCALE),
    'N3':  ('N',  1.2 * SCALE,  0.7 * SCALE),
    'C4':  ('C',  1.2 * SCALE, -0.7 * SCALE),
    'C5':  ('C',  0.0 * SCALE, -1.2 * SCALE),
    'C6':  ('C', -1.2 * SCALE, -0.7 * SCALE),
    # 5-membered ring extension
    'N7':  ('N',  2.3 * SCALE, -1.2 * SCALE),
    'C8':  ('C',  2.8 * SCALE,  0.0 * SCALE),
    'N9':  ('N',  2.3 * SCALE,  1.2 * SCALE),
    # Methyl groups (just the C of CH3)
    'Me1': ('C', -2.4 * SCALE,  1.3 * SCALE),
    'Me3': ('C',  1.2 * SCALE,  2.0 * SCALE),
    'Me7': ('C',  2.8 * SCALE, -2.3 * SCALE),
    # Oxygens (=O)
    'O2':  ('O',  0.0 * SCALE,  2.5 * SCALE),
    'O6':  ('O', -2.4 * SCALE, -1.3 * SCALE),
}

# Bonds: (atom1, atom2, bond_order)
BONDS = [
    # 6-membered ring
    ('N1', 'C2', 1),
    ('C2', 'N3', 1),
    ('N3', 'C4', 1),
    ('C4', 'C5', 2),
    ('C5', 'C6', 1),
    ('C6', 'N1', 1),
    # 5-membered ring
    ('C4', 'N9', 1),
    ('N9', 'C8', 2),
    ('C8', 'N7', 1),
    ('N7', 'C5', 1),
    # Methyl groups
    ('N1', 'Me1', 1),
    ('N3', 'Me3', 1),
    ('N7', 'Me7', 1),
    # Oxygens (double bonds)
    ('C2', 'O2', 2),
    ('C6', 'O6', 2),
]


def draw_bond(ax, p1, p2, order=1, single_color=MUTED, double_color=TEXT):
    """Draw a single or double bond between two points."""
    x1, y1 = p1
    x2, y2 = p2

    if order == 1:
        ax.plot([x1, x2], [y1, y2], color=single_color, linewidth=2.5,
                solid_capstyle='round', zorder=2, alpha=0.8)
    elif order == 2:
        # Two parallel lines offset perpendicular to the bond direction
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        if length == 0:
            return
        nx_ = -dy / length * 0.08 * SCALE
        ny_ = dx / length * 0.08 * SCALE

        ax.plot([x1 + nx_, x2 + nx_], [y1 + ny_, y2 + ny_],
                color=double_color, linewidth=2.5, solid_capstyle='round',
                zorder=2, alpha=0.9)
        ax.plot([x1 - nx_, x2 - nx_], [y1 - ny_, y2 - ny_],
                color=double_color, linewidth=2.5, solid_capstyle='round',
                zorder=2, alpha=0.9)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(3840 / 200, 2160 / 200), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw bonds
    for a1, a2, order in BONDS:
        p1 = (ATOMS[a1][1], ATOMS[a1][2])
        p2 = (ATOMS[a2][1], ATOMS[a2][2])
        draw_bond(ax, p1, p2, order)

    # Draw atoms as circles
    for aid, (element, x, y) in ATOMS.items():
        color = ATOM_COLORS[element]
        # Larger circles for heteroatoms, smaller for carbon
        radius = 0.28 * SCALE if element in ('N', 'O') else 0.22 * SCALE
        circle = plt.Circle(
            (x, y), radius, facecolor=color,
            edgecolor='white', linewidth=2.0, zorder=5, alpha=0.92,
        )
        ax.add_patch(circle)

        # Label with element symbol
        label = element
        if aid.startswith('Me'):
            label = 'CH\u2083'
            fontsize = 9
        else:
            fontsize = 13
        ax.text(
            x, y, label, fontsize=fontsize, fontweight='bold',
            color='white', ha='center', va='center', zorder=6,
            path_effects=[pe.withStroke(linewidth=2, foreground='#00000088')],
        )

    # Legend: element colors
    legend_x = 5.5 * SCALE
    legend_y = 2.0 * SCALE
    for i, (elem, color) in enumerate([('C  Carbon', BLUE),
                                        ('N  Nitrogen', GREEN),
                                        ('O  Oxygen', RED)]):
        ax.plot(legend_x, legend_y - i * 0.6 * SCALE, 'o', color=color,
                markersize=12, zorder=8)
        ax.text(legend_x + 0.3 * SCALE, legend_y - i * 0.6 * SCALE, elem,
                fontsize=13, color=TEXT, va='center', zorder=8)

    # Title
    ax.set_title(
        'Molecular Graphs for Drug Discovery',
        fontsize=30, fontweight='bold', color=TEXT, pad=24,
    )

    # Molecule name
    ax.text(
        0.0, -3.5 * SCALE,
        'Caffeine \u2014 C\u2088H\u2081\u2080N\u2084O\u2082',
        fontsize=22, fontweight='bold', color=TEXT,
        ha='center', va='center',
    )

    # Annotations
    ax.text(
        0.0, -4.2 * SCALE,
        'Atoms = Nodes,  Bonds = Edges',
        fontsize=16, color=MUTED, ha='center', va='center', style='italic',
    )
    ax.text(
        0.0, -4.9 * SCALE,
        'GNN predicts:  \u2615 Stimulant = TRUE',
        fontsize=16, color=GREEN, ha='center', va='center',
        fontweight='bold',
    )

    # Auto-scale
    all_x = [ATOMS[a][1] for a in ATOMS]
    all_y = [ATOMS[a][2] for a in ATOMS]
    margin = 2.5 * SCALE
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin + 3 * SCALE)
    ax.set_ylim(min(all_y) - margin - 2.0 * SCALE, max(all_y) + margin)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
