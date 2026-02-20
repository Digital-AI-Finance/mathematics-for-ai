#!/usr/bin/env python3
"""
gen_13_knowledge_graph.py
Knowledge graph with entity-relation triples about Einstein.

Nodes: Einstein, Germany, Physics, Berlin, Relativity, Nobel Prize, 1921, Ulm
Edges with labeled relations form a directed graph.
Highlighted path: Einstein -> born_in -> Ulm -> located_in -> Germany -> capital -> Berlin

Output: ../images/13-knowledge-graph.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import networkx as nx

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '13-knowledge-graph.png')

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


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Build knowledge graph
    G = nx.DiGraph()

    entities = [
        'Einstein', 'Germany', 'Physics', 'Berlin',
        'Relativity', 'Nobel Prize', '1921', 'Ulm',
    ]
    for e in entities:
        G.add_node(e)

    triples = [
        ('Einstein',    'Ulm',          'born_in'),
        ('Ulm',         'Germany',      'located_in'),
        ('Germany',     'Berlin',       'capital'),
        ('Einstein',    'Physics',      'field'),
        ('Einstein',    'Relativity',   'developed'),
        ('Einstein',    'Nobel Prize',  'awarded'),
        ('Nobel Prize', '1921',         'year'),
    ]
    for head, tail, rel in triples:
        G.add_edge(head, tail, relation=rel)

    # Highlighted path
    highlight_edges = {
        ('Einstein', 'Ulm'),
        ('Ulm', 'Germany'),
        ('Germany', 'Berlin'),
    }
    highlight_nodes = {'Einstein', 'Ulm', 'Germany', 'Berlin'}

    # Manual layout -- generous spacing so every label fits in its node
    pos = {
        'Einstein':    ( 0.00,  0.00),
        'Ulm':         (-0.20, -0.65),
        'Germany':     ( 0.50, -0.50),
        'Berlin':      ( 0.85,  0.05),
        'Physics':     (-0.75, -0.35),
        'Relativity':  (-0.65,  0.55),
        'Nobel Prize': ( 0.15,  0.70),
        '1921':        ( 0.70,  0.60),
    }

    # Node sizes -- larger base so text fits; scale with degree
    degrees = dict(G.degree())
    base_size = 2800
    node_sizes = [base_size + degrees[n] * 1000 for n in G.nodes()]

    # Node colors: highlighted nodes brighter
    node_colors = []
    for n in G.nodes():
        if n in highlight_nodes:
            node_colors.append(YELLOW)
        else:
            node_colors.append(BLUE)

    # Figure
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(3840 / 200, 2160 / 200), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    # Generous axis limits so no node label is clipped
    all_x = [p[0] for p in pos.values()]
    all_y = [p[1] for p in pos.values()]
    pad = 0.30
    ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
    ax.set_ylim(min(all_y) - pad, max(all_y) + pad)

    # Draw non-highlighted edges first
    normal_edges = [e for e in G.edges() if (e[0], e[1]) not in highlight_edges]
    nx.draw_networkx_edges(
        G, pos, edgelist=normal_edges, ax=ax,
        edge_color=MUTED, width=1.8, alpha=0.5,
        arrows=True, arrowsize=20, arrowstyle='-|>',
        connectionstyle='arc3,rad=0.1',
        min_source_margin=25, min_target_margin=25,
    )

    # Draw highlighted edges (thick, bright yellow)
    highlight_edge_list = [e for e in G.edges() if (e[0], e[1]) in highlight_edges]
    nx.draw_networkx_edges(
        G, pos, edgelist=highlight_edge_list, ax=ax,
        edge_color=YELLOW, width=4.0, alpha=0.95,
        arrows=True, arrowsize=25, arrowstyle='-|>',
        connectionstyle='arc3,rad=0.1',
        min_source_margin=25, min_target_margin=25,
    )

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors='white', linewidths=1.5,
        alpha=0.92,
    )

    # Node labels -- draw manually so clip_on=False works for all labels
    for node, (x, y) in pos.items():
        ax.text(
            x, y, node,
            fontsize=12, fontweight='bold', color=BG,
            ha='center', va='center', zorder=10, clip_on=False,
        )

    # Edge labels (relation names)
    edge_labels = {(h, t): rel for h, t, rel in triples}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, ax=ax,
        font_size=9, font_color=MUTED,
        label_pos=0.45,
        bbox=dict(boxstyle='round,pad=0.15', facecolor=BG, edgecolor='none', alpha=0.8),
        rotate=True,
    )

    # Title
    ax.set_title(
        'Knowledge Graph: Facts as (Entity, Relation, Entity)',
        fontsize=30, fontweight='bold', color=TEXT, pad=24,
    )

    # Legend annotation
    ax.text(
        0.5, -0.03,
        'Highlighted path: Einstein  \u2192  born_in  \u2192  Ulm  \u2192  located_in  \u2192  Germany  \u2192  capital  \u2192  Berlin',
        transform=ax.transAxes, fontsize=15, color=YELLOW,
        ha='center', va='top', style='italic',
    )

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
