#!/usr/bin/env python3
"""
gen_02_word_vectors.py
2D scatter plot of the king-man+woman=queen word embedding analogy.
Output: ../images/02-word-vectors.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '02-word-vectors.png')

BG      = '#1b2631'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
TEAL    = '#1abc9c'
ORANGE  = '#e67e22'
RED     = '#e74c3c'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)

    # Word positions forming a parallelogram
    words = {
        'King':  np.array([1.0, 3.0]),
        'Queen': np.array([3.5, 3.0]),
        'Man':   np.array([1.0, 1.0]),
        'Woman': np.array([3.5, 1.0]),
    }

    # Scatter additional "noise" words for context
    rng = np.random.RandomState(42)
    bg_words = {
        'dog': (0.2, 0.3), 'cat': (0.5, 0.5), 'run': (-0.5, 2.0),
        'happy': (4.5, 2.2), 'car': (-0.8, 0.8), 'child': (2.2, 0.4),
        'prince': (2.2, 3.5), 'throne': (0.3, 3.8), 'dress': (4.2, 0.5),
        'crown': (2.3, 3.9), 'boy': (0.5, 1.5), 'girl': (3.8, 1.5),
    }

    # Draw background words
    for w, (wx, wy) in bg_words.items():
        ax.scatter(wx, wy, s=30, c=MUTED, alpha=0.35, zorder=1)
        ax.text(wx + 0.08, wy + 0.08, w, fontsize=8, color=MUTED,
                alpha=0.5, family='sans-serif', zorder=1)

    # Subtle grid
    ax.set_xlim(-1.5, 5.5)
    ax.set_ylim(-0.5, 5.0)
    ax.grid(True, alpha=0.12, linewidth=0.5, color=MUTED)

    # Color scheme: gender direction = ORANGE, royalty direction = BLUE
    gender_color = ORANGE
    royalty_color = BLUE

    # Draw directional arrows (parallelogram edges)
    arrow_kw = dict(arrowstyle='->', mutation_scale=18, linewidth=2.5, zorder=3)

    # Gender direction (horizontal): King->Queen, Man->Woman
    for start, end in [('Man', 'Woman'), ('King', 'Queen')]:
        a = FancyArrowPatch(
            words[start], words[end],
            color=gender_color, **arrow_kw,
        )
        ax.add_patch(a)

    # Royalty direction (vertical): Man->King, Woman->Queen
    for start, end in [('Man', 'King'), ('Woman', 'Queen')]:
        a = FancyArrowPatch(
            words[start], words[end],
            color=royalty_color, **arrow_kw,
        )
        ax.add_patch(a)

    # Plot the 4 main words as large dots
    colors_map = {'King': BLUE, 'Queen': RED, 'Man': TEAL, 'Woman': GREEN}
    for word, pos in words.items():
        ax.scatter(*pos, s=280, c=colors_map[word], edgecolors='white',
                   linewidths=2, zorder=5)
        # Label offset depends on position
        offset_x = -0.35 if word in ('King', 'Man') else 0.2
        offset_y = 0.22
        ax.text(pos[0] + offset_x, pos[1] + offset_y, word,
                fontsize=17, fontweight='bold', color=colors_map[word],
                family='sans-serif', zorder=6)

    # Direction labels
    mid_gender_top = (words['King'] + words['Queen']) / 2
    ax.text(mid_gender_top[0], mid_gender_top[1] + 0.35,
            'Gender direction', ha='center', fontsize=11, fontstyle='italic',
            color=gender_color, family='sans-serif', zorder=6)

    mid_royalty_left = (words['Man'] + words['King']) / 2
    ax.text(mid_royalty_left[0] - 0.55, mid_royalty_left[1],
            'Royalty\ndirection', ha='center', va='center',
            fontsize=11, fontstyle='italic',
            color=royalty_color, family='sans-serif', zorder=6,
            rotation=90)

    # Equation box
    eq_x, eq_y = 3.8, 4.3
    ax.text(eq_x, eq_y,
            r'$\vec{\mathrm{king}} - \vec{\mathrm{man}} + \vec{\mathrm{woman}} \approx \vec{\mathrm{queen}}$',
            fontsize=18, color=YELLOW, family='sans-serif',
            ha='center', va='center', zorder=7,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#2c3e50',
                      edgecolor=YELLOW, alpha=0.9, linewidth=1.5))

    # Title
    ax.set_title('Word Vectors: Arithmetic with Meaning',
                 fontsize=24, fontweight='bold', color=TEXT,
                 family='sans-serif', pad=20)

    # Clean up axes
    ax.set_xlabel('Embedding Dimension 1', fontsize=12, color=MUTED,
                  family='sans-serif')
    ax.set_ylabel('Embedding Dimension 2', fontsize=12, color=MUTED,
                  family='sans-serif')
    ax.tick_params(colors=MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(MUTED)
        spine.set_alpha(0.3)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
