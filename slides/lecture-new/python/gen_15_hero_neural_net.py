#!/usr/bin/env python3
"""
gen_15_hero_neural_net.py
Neon-glow neural network diagram for the title slide.
Three layers: Input (4 nodes, blue), Hidden (6 nodes, teal), Output (3 nodes, yellow).
Output: ../images/15-hero-neural-net.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '15-hero-neural-net.png')

BG      = '#1b2631'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
TEAL    = '#1abc9c'
ORANGE  = '#e67e22'
RED     = '#e74c3c'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'


def draw_glow_line(ax, x0, y0, x1, y1, color, base_alpha=0.18):
    """Draw a neon-glow line: multiple passes at decreasing width."""
    widths = [6.0, 3.5, 2.0, 1.0, 0.4]
    alphas = [base_alpha * 0.5,
              base_alpha * 0.7,
              base_alpha * 0.9,
              base_alpha * 1.0,
              base_alpha * 1.0]
    for lw, alpha in zip(widths, alphas):
        ax.plot([x0, x1], [y0, y1],
                color=color, linewidth=lw, alpha=alpha,
                solid_capstyle='round', zorder=1)


def draw_glow_node(ax, cx, cy, radius, face_color, edge_color):
    """Draw a node with a soft outer glow."""
    # Outer glow rings
    for r_factor, alpha in [(2.8, 0.06), (2.0, 0.10), (1.5, 0.16)]:
        glow = mpatches.Circle((cx, cy), radius * r_factor,
                                facecolor=edge_color, edgecolor='none',
                                alpha=alpha, zorder=3)
        ax.add_patch(glow)
    # Main circle body
    node = mpatches.Circle((cx, cy), radius,
                             facecolor=face_color, edgecolor=edge_color,
                             linewidth=2.5, zorder=4)
    ax.add_patch(node)
    # Inner highlight
    hi = mpatches.Circle((cx - radius * 0.28, cy + radius * 0.28),
                           radius * 0.30,
                           facecolor='white', edgecolor='none',
                           alpha=0.20, zorder=5)
    ax.add_patch(hi)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # ------------------------------------------------------------------ layout
    # Layer x positions (centred in canvas with generous padding)
    layer_x = [0.22, 0.50, 0.78]

    # Node counts per layer
    n_nodes = [4, 6, 3]

    # Node colours
    node_colors_face = [
        '#0d2137',   # input  — dark blue fill
        '#0b2e2a',   # hidden — dark teal fill
        '#2e2506',   # output — dark yellow fill
    ]
    node_colors_edge = [BLUE, TEAL, YELLOW]

    node_radius = 0.038

    # Vertical spacing: distribute nodes evenly in [0.15, 0.85]
    y_margin_top    = 0.82
    y_margin_bottom = 0.18

    def node_y_positions(n):
        if n == 1:
            return [0.50]
        return list(np.linspace(y_margin_bottom, y_margin_top, n))

    # Build position lists
    positions = []
    for i, n in enumerate(n_nodes):
        ys = node_y_positions(n)
        xs = [layer_x[i]] * n
        positions.append(list(zip(xs, ys)))

    # ---------------------------------------------------------------- connections
    # Draw all connections first (behind nodes)
    conn_palette = [
        '#2e86c1',   # input→hidden: blue-ish
        '#17a589',   # hidden→output: teal-ish
    ]

    rng = np.random.default_rng(42)

    for layer_idx in range(len(positions) - 1):
        src_nodes = positions[layer_idx]
        dst_nodes = positions[layer_idx + 1]
        color = conn_palette[layer_idx]

        for (x0, y0) in src_nodes:
            for (x1, y1) in dst_nodes:
                # Vary alpha slightly per connection for visual depth
                alpha = rng.uniform(0.10, 0.22)
                draw_glow_line(ax, x0, y0, x1, y1, color, base_alpha=alpha)

    # ---------------------------------------------------------------- nodes
    for i, layer_nodes in enumerate(positions):
        fc = node_colors_face[i]
        ec = node_colors_edge[i]
        for (cx, cy) in layer_nodes:
            draw_glow_node(ax, cx, cy, node_radius, fc, ec)

    # ---------------------------------------------------------------- layer labels
    label_y = 0.09
    layer_labels = ['Input', 'Hidden', 'Output']
    label_colors = [BLUE, TEAL, YELLOW]

    for lx, lbl, lc in zip(layer_x, layer_labels, label_colors):
        ax.text(lx, label_y, lbl,
                ha='center', va='center',
                fontsize=22, fontweight='bold',
                color=lc, alpha=0.85,
                transform=ax.transData)

    # ---------------------------------------------------------------- subtle grid bg lines (atmosphere)
    for gx in np.linspace(0.0, 1.0, 25):
        ax.axvline(gx, color='#1e3448', linewidth=0.4, alpha=0.35, zorder=0)
    for gy in np.linspace(0.0, 1.0, 14):
        ax.axhline(gy, color='#1e3448', linewidth=0.4, alpha=0.35, zorder=0)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
