#!/usr/bin/env python3
"""
gen_14_attention_heatmap.py
Attention weight heatmap for a sample sentence showing which words attend to which.
Output: ../images/14-attention-heatmap.png
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '14-attention-heatmap.png')

BG     = '#1b2631'
BLUE   = '#3498db'
YELLOW = '#f1c40f'
GREEN  = '#2ecc71'
TEAL   = '#1abc9c'
ORANGE = '#e67e22'
RED    = '#e74c3c'
TEXT   = '#ecf0f1'
MUTED  = '#95a5a6'


def build_attention_matrix():
    """Build a plausible 6x6 attention matrix for 'The cat sat on the mat'.
    Row = query (what token is looking), Col = key (which token is attended to).
    Values are row-normalised so each query's weights sum to ~1.
    """
    tokens = ["The", "cat", "sat", "on", "the", "mat"]
    n = len(tokens)

    # Start with a low baseline
    A = np.full((n, n), 0.04)

    # Diagonal: moderate self-attention
    np.fill_diagonal(A, 0.18)

    # "The"  (0) → moderate self + cat
    A[0, 0] = 0.25
    A[0, 1] = 0.35   # determines which noun

    # "cat"  (1) → The, sat (subject of action)
    A[1, 0] = 0.32   # article
    A[1, 2] = 0.30   # verb

    # "sat"  (2) → cat (subject), on (prep start)
    A[2, 1] = 0.38   # who is sitting
    A[2, 3] = 0.22   # where

    # "on"   (3) → sat, the, mat (prepositional)
    A[3, 2] = 0.20
    A[3, 4] = 0.28
    A[3, 5] = 0.22

    # "the"  (4) → mat (which noun follows)
    A[4, 4] = 0.22
    A[4, 5] = 0.45

    # "mat"  (5) → on, the (location phrase)
    A[5, 3] = 0.30
    A[5, 4] = 0.38

    # Row-normalise
    A = A / A.sum(axis=1, keepdims=True)

    return tokens, A


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')

    tokens, attn = build_attention_matrix()
    n = len(tokens)

    # Custom colormap: dark blue → vivid yellow (pillar palette)
    cmap = LinearSegmentedColormap.from_list(
        'attn',
        ['#1b2631', '#1a5276', BLUE, TEAL, GREEN, YELLOW],
        N=256)

    fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG)

    # Left: heatmap (main panel)
    ax_heat = fig.add_axes([0.06, 0.12, 0.52, 0.72])
    ax_heat.set_facecolor(BG)

    im = ax_heat.imshow(attn, cmap=cmap, aspect='auto',
                        vmin=0.0, vmax=0.55)

    # Grid lines between cells
    for i in range(n + 1):
        ax_heat.axhline(i - 0.5, color='#2c3e50', linewidth=1.0)
        ax_heat.axvline(i - 0.5, color='#2c3e50', linewidth=1.0)

    # Annotate each cell with weight value
    for row in range(n):
        for col in range(n):
            val = attn[row, col]
            # Choose text color: dark for bright cells, light for dark
            text_color = BG if val > 0.30 else TEXT
            ax_heat.text(col, row, f'{val:.2f}',
                         ha='center', va='center',
                         fontsize=13.5, fontweight='bold',
                         color=text_color, family='monospace')

    # Tick labels
    ax_heat.set_xticks(range(n))
    ax_heat.set_yticks(range(n))
    ax_heat.set_xticklabels(tokens, fontsize=15, color=TEXT, fontweight='bold')
    ax_heat.set_yticklabels(tokens, fontsize=15, color=TEXT, fontweight='bold')
    ax_heat.xaxis.set_label_position('top')
    ax_heat.xaxis.tick_top()
    ax_heat.tick_params(axis='both', length=0, pad=8)

    ax_heat.set_xlabel('Key  (token being attended to)',
                       fontsize=13, color=MUTED, labelpad=12)
    ax_heat.xaxis.set_label_position('bottom')

    # Move x-axis label to bottom
    ax_heat.set_xlabel('')
    fig.text(0.06 + 0.52 / 2, 0.07,
             'Key  —  token being attended to',
             ha='center', va='center', fontsize=13, color=MUTED)
    fig.text(0.03, 0.12 + 0.72 / 2,
             'Query  —  token doing the attending',
             ha='center', va='center', fontsize=13, color=MUTED,
             rotation=90)

    # Colorbar
    cbar_ax = fig.add_axes([0.60, 0.12, 0.015, 0.72])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.ax.yaxis.set_tick_params(color=MUTED, labelsize=10)
    cbar.outline.set_edgecolor(MUTED)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=MUTED)
    cbar.set_label('Attention weight', fontsize=11, color=MUTED, labelpad=10)

    # Right panel: interpretation annotations
    ax_notes = fig.add_axes([0.64, 0.12, 0.33, 0.72])
    ax_notes.set_facecolor(BG)
    ax_notes.axis('off')

    # Header
    ax_notes.text(0.5, 0.97, 'How to Read This',
                  ha='center', va='top', fontsize=16,
                  fontweight='bold', color=TEXT, transform=ax_notes.transAxes)

    sentence = '"The  cat  sat  on  the  mat"'
    ax_notes.text(0.5, 0.91, sentence,
                  ha='center', va='top', fontsize=13,
                  color=YELLOW, fontstyle='italic',
                  transform=ax_notes.transAxes)

    explanations = [
        (GREEN,  '"cat"  →  The, sat',
                 '"cat" checks the article before it\nand the verb it performs'),
        (ORANGE, '"sat"  →  cat, on',
                 '"sat" needs to know who is sitting\nand the location preposition'),
        (TEAL,   '"mat"  →  on, the',
                 '"mat" ties back to "on" and\nthe article "the" before it'),
        (BLUE,   'Diagonal ≈ 0.18–0.25',
                 'Every word attends to itself\nwith moderate weight'),
        (YELLOW, 'Bright cells = strong attention',
                 'Yellow / green cells show\nthe most important connections'),
    ]

    y = 0.80
    for color, heading, body in explanations:
        # Colored bullet
        ax_notes.add_patch(mpatches.FancyBboxPatch(
            (0.02, y - 0.025), 0.96, 0.095,
            boxstyle='round,pad=0.01',
            facecolor=color, alpha=0.10,
            edgecolor=color, linewidth=0.8,
            transform=ax_notes.transAxes, clip_on=False))

        ax_notes.text(0.06, y + 0.04, heading,
                      ha='left', va='center', fontsize=11,
                      fontweight='bold', color=color,
                      transform=ax_notes.transAxes)
        ax_notes.text(0.06, y - 0.008, body,
                      ha='left', va='top', fontsize=9.5,
                      color=MUTED, linespacing=1.35,
                      transform=ax_notes.transAxes)
        y -= 0.145

    # Key insight box
    y_box = 0.05
    ax_notes.add_patch(mpatches.FancyBboxPatch(
        (0.02, y_box), 0.96, 0.12,
        boxstyle='round,pad=0.015',
        facecolor='#0d2137', edgecolor=TEAL,
        linewidth=1.5, transform=ax_notes.transAxes, clip_on=False))
    ax_notes.text(0.5, y_box + 0.085,
                  'Key insight: Transformers learn WHICH words\nto pay attention to — automatically!',
                  ha='center', va='center', fontsize=10.5,
                  color=TEAL, linespacing=1.4,
                  transform=ax_notes.transAxes)

    # Main title
    fig.text(0.5, 0.965,
             'Attention: Which Words Look at Which?',
             ha='center', va='top', fontsize=22,
             fontweight='bold', color=TEXT, family='sans-serif')
    fig.text(0.5, 0.935,
             'Each word decides which other words are relevant  '
             '("Attention Is All You Need", 2017)',
             ha='center', va='top', fontsize=13,
             color=MUTED, family='sans-serif', fontstyle='italic')

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
