#!/usr/bin/env python3
"""
gen_18_milgram_letters.py
Milgram's 1967 "Six Degrees" letter experiment.

A chain of 6 person-nodes from "You (Nebraska)" to "Target (Boston)",
illustrating how a letter passes through ~6 intermediaries.
Arrows show the letter's path through the chain.

Output: ../images/18-milgram-letters.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import networkx as nx

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '18-milgram-letters.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG      = '#1b2631'
CARD_BG = '#1e3044'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'

# ---------------------------------------------------------------------------
# Chain definition
# ---------------------------------------------------------------------------
NODES = [
    ('You\n(Nebraska)', BLUE),
    ('Friend 1\nKansas',  GREEN),
    ('Friend 2\nMissouri', GREEN),
    ('Friend 3\nOhio',    GREEN),
    ('Friend 4\nNew York', GREEN),
    ('Friend 5\nConn.',   GREEN),
    ('Target\n(Boston)',  YELLOW),
]

N = len(NODES)   # 7 nodes  →  6 hops


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # -----------------------------------------------------------------------
    # Build directed path graph
    # -----------------------------------------------------------------------
    G = nx.DiGraph()
    G.add_nodes_from(range(N))
    G.add_edges_from([(i, i + 1) for i in range(N - 1)])

    # Fixed left-to-right layout (spread across canvas)
    xs = np.linspace(0.5, 15.5, N)
    y_main = 5.2
    pos = {i: (xs[i], y_main) for i in range(N)}

    # -----------------------------------------------------------------------
    # Figure
    # -----------------------------------------------------------------------
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(3840 / 200, 2160 / 200), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.5, 17.0)
    ax.set_ylim(0.0, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # -----------------------------------------------------------------------
    # Draw connecting edges (arrows)
    # -----------------------------------------------------------------------
    for i in range(N - 1):
        x1, y1 = pos[i]
        x2, y2 = pos[i + 1]
        # nudge arrow endpoints away from node centres
        dx = x2 - x1
        ax.annotate(
            '', xy=(x2 - 0.30, y2), xytext=(x1 + 0.30, y1),
            arrowprops=dict(
                arrowstyle='-|>', color=MUTED, lw=2.5,
                mutation_scale=24, shrinkA=0, shrinkB=0,
            ),
            zorder=2,
        )
        # Draw a subtle dashed connecting line as well
        ax.plot([x1 + 0.30, x2 - 0.30], [y1, y2],
                color=MUTED, linewidth=1.5, linestyle='--',
                alpha=0.35, zorder=1)

    # -----------------------------------------------------------------------
    # Draw hop count labels above edges
    # -----------------------------------------------------------------------
    hop_labels = ['Hop 1', 'Hop 2', 'Hop 3', 'Hop 4', 'Hop 5', 'Hop 6']
    for i, label in enumerate(hop_labels):
        mx = (pos[i][0] + pos[i + 1][0]) / 2
        my = y_main + 0.72
        ax.text(mx, my, label, fontsize=11, color=MUTED,
                ha='center', va='center', style='italic',
                path_effects=[pe.withStroke(linewidth=2, foreground=BG)])

    # -----------------------------------------------------------------------
    # Draw nodes as circles with labels below
    # -----------------------------------------------------------------------
    NODE_R = 0.45
    for i, (label, color) in enumerate(NODES):
        x, y = pos[i]

        # Glow / halo
        glow = plt.Circle((x, y), NODE_R + 0.12, color=color,
                           alpha=0.18, zorder=3)
        ax.add_patch(glow)

        # Main circle
        circle = plt.Circle((x, y), NODE_R, color=color,
                             ec='white', linewidth=2.5, zorder=4)
        ax.add_patch(circle)

        # Node index (1-based) inside circle
        ax.text(x, y, str(i + 1) if 0 < i < N - 1 else ('S' if i == 0 else 'T'),
                fontsize=18, fontweight='bold',
                color=BG if color == YELLOW else 'white',
                ha='center', va='center', zorder=5,
                path_effects=[pe.withStroke(linewidth=2, foreground=color)])

        # Label below each node
        ax.text(x, y - NODE_R - 0.50, label,
                fontsize=12, fontweight='bold', color=color,
                ha='center', va='top', zorder=5, linespacing=1.4,
                path_effects=[pe.withStroke(linewidth=3, foreground=BG)])

    # -----------------------------------------------------------------------
    # "~6 steps" annotation arc above the chain
    # -----------------------------------------------------------------------
    # A curved double-headed arrow spanning all nodes
    ax.annotate(
        '', xy=(pos[N - 1][0], y_main + NODE_R + 0.18),
        xytext=(pos[0][0], y_main + NODE_R + 0.18),
        arrowprops=dict(
            arrowstyle='<->', color=YELLOW, lw=2.0,
            connectionstyle='arc3,rad=-0.35',
            mutation_scale=18,
        ),
        zorder=6,
    )
    ax.text(
        (pos[0][0] + pos[N - 1][0]) / 2, y_main + NODE_R + 1.62,
        '~6 steps to reach anyone',
        fontsize=22, fontweight='bold', color=YELLOW,
        ha='center', va='center', zorder=7,
        path_effects=[pe.withStroke(linewidth=4, foreground=BG)],
    )

    # -----------------------------------------------------------------------
    # Envelope icon (letter) moving along the path — placed midway
    # -----------------------------------------------------------------------
    # Draw a small stylised envelope at the midpoint of hop 3
    ex = (pos[2][0] + pos[3][0]) / 2
    ey = y_main + 1.25
    env_w, env_h = 0.60, 0.38
    envelope = mpatches.FancyBboxPatch(
        (ex - env_w / 2, ey - env_h / 2), env_w, env_h,
        boxstyle='square,pad=0.04',
        facecolor=CARD_BG, edgecolor=MUTED, linewidth=1.5, zorder=6,
        alpha=0.90,
    )
    ax.add_patch(envelope)
    # Envelope flap (V lines)
    ax.plot([ex - env_w / 2, ex, ex + env_w / 2],
            [ey + env_h / 2, ey + 0.05, ey + env_h / 2],
            color=MUTED, linewidth=1.2, zorder=7)
    ax.text(ex, ey - 0.06, 'Letter', fontsize=9, color=MUTED,
            ha='center', va='center', zorder=8)

    # -----------------------------------------------------------------------
    # Legend
    # -----------------------------------------------------------------------
    legend_handles = [
        mpatches.Patch(color=BLUE,   label='Source (Nebraska)'),
        mpatches.Patch(color=GREEN,  label='Intermediate contacts'),
        mpatches.Patch(color=YELLOW, label='Target (Boston)'),
    ]
    fig.legend(
        handles=legend_handles, loc='lower center', ncol=3,
        fontsize=15, frameon=False, labelcolor=TEXT,
        handlelength=2.0, bbox_to_anchor=(0.5, 0.03),
    )

    # -----------------------------------------------------------------------
    # Subtitle bar at bottom
    # -----------------------------------------------------------------------
    ax.text(
        8.25, 1.35,
        'Milgram (1967): Letters mailed to strangers in Nebraska reached a Boston '
        'stockbroker in ~6 hops on average.',
        fontsize=13, color=MUTED, ha='center', va='center',
        style='italic', wrap=True,
        path_effects=[pe.withStroke(linewidth=2, foreground=BG)],
    )

    # -----------------------------------------------------------------------
    # Title
    # -----------------------------------------------------------------------
    ax.set_title(
        "Milgram's Small-World Experiment — Six Degrees of Separation (1967)",
        fontsize=30, fontweight='bold', color=TEXT, pad=22,
    )

    # -----------------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------------
    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
