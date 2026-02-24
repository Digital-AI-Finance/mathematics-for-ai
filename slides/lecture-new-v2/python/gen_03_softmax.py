#!/usr/bin/env python3
"""
gen_03_softmax.py
Dual-panel bar chart: raw logits vs. softmax probabilities.
Output: ../images/03-softmax.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '03-softmax.png')

BG      = '#1b2631'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
TEAL    = '#1abc9c'
ORANGE  = '#e67e22'
RED     = '#e74c3c'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'


def softmax(z):
    """Numerically stable softmax."""
    e = np.exp(z - np.max(z))
    return e / e.sum()


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')
    fig, (ax_left, ax_right) = plt.subplots(
        1, 2, figsize=(19.2, 10.8), facecolor=BG,
        gridspec_kw={'width_ratios': [1, 1], 'wspace': 0.35},
    )

    tokens = ['"the"', '"a"', '"cat"', '"dog"', '"Paris"']
    logits = np.array([2.5, 1.0, -0.5, 3.1, 0.2])
    probs = softmax(logits)

    x = np.arange(len(tokens))
    bar_w = 0.55

    # --- Left panel: Raw Logits ---
    ax_left.set_facecolor(BG)
    logit_colors = [MUTED if v >= 0 else RED for v in logits]
    bars_l = ax_left.bar(x, logits, width=bar_w, color=logit_colors,
                         edgecolor='white', linewidth=0.8, alpha=0.8, zorder=3)
    # Value labels on bars
    for bar, val in zip(bars_l, logits):
        y_pos = bar.get_height() + 0.12 if val >= 0 else bar.get_height() - 0.3
        ax_left.text(bar.get_x() + bar.get_width() / 2, y_pos,
                     f'{val:.1f}', ha='center', va='bottom' if val >= 0 else 'top',
                     fontsize=14, fontweight='bold', color=TEXT,
                     family='sans-serif', zorder=4)

    ax_left.set_xticks(x)
    ax_left.set_xticklabels(tokens, fontsize=13, color=TEXT, family='sans-serif')
    ax_left.set_ylabel('Score (logit)', fontsize=13, color=MUTED,
                       family='sans-serif')
    ax_left.set_title('Raw Logits', fontsize=20, fontweight='bold',
                      color=TEXT, family='sans-serif', pad=15)
    ax_left.axhline(0, color=MUTED, linewidth=0.8, alpha=0.5)
    ax_left.set_ylim(-1.5, 4.5)
    ax_left.tick_params(colors=MUTED, labelsize=10)
    for spine in ax_left.spines.values():
        spine.set_color(MUTED)
        spine.set_alpha(0.3)
    ax_left.grid(axis='y', alpha=0.12, color=MUTED)

    # --- Right panel: After Softmax ---
    ax_right.set_facecolor(BG)
    green_shades = [GREEN if p == probs.max() else TEAL for p in probs]
    bars_r = ax_right.bar(x, probs, width=bar_w, color=green_shades,
                          edgecolor='white', linewidth=0.8, alpha=0.85, zorder=3)
    # Percentage labels
    for bar, p in zip(bars_r, probs):
        ax_right.text(bar.get_x() + bar.get_width() / 2,
                      bar.get_height() + 0.008,
                      f'{p:.1%}', ha='center', va='bottom',
                      fontsize=14, fontweight='bold', color=TEXT,
                      family='sans-serif', zorder=4)

    ax_right.set_xticks(x)
    ax_right.set_xticklabels(tokens, fontsize=13, color=TEXT, family='sans-serif')
    ax_right.set_ylabel('Probability', fontsize=13, color=MUTED,
                        family='sans-serif')
    ax_right.set_title('After Softmax', fontsize=20, fontweight='bold',
                       color=TEXT, family='sans-serif', pad=15)
    ax_right.set_ylim(0, 0.55)
    ax_right.tick_params(colors=MUTED, labelsize=10)
    for spine in ax_right.spines.values():
        spine.set_color(MUTED)
        spine.set_alpha(0.3)
    ax_right.grid(axis='y', alpha=0.12, color=MUTED)

    # Sum annotation
    ax_right.text(len(tokens) - 1, 0.50,
                  r'$\Sigma = 1.00$',
                  fontsize=14, color=YELLOW, ha='right', va='top',
                  family='sans-serif',
                  bbox=dict(boxstyle='round,pad=0.3', facecolor='#2c3e50',
                            edgecolor=YELLOW, alpha=0.8))

    # Arrow between panels using figure-level annotation
    fig.text(0.5, 0.5, r'softmax', fontsize=20, fontweight='bold',
             ha='center', va='center', color=YELLOW,
             family='sans-serif', zorder=10,
             transform=fig.transFigure)
    fig.text(0.5, 0.44, r'$\longrightarrow$', fontsize=36,
             ha='center', va='center', color=YELLOW,
             family='sans-serif', zorder=10,
             transform=fig.transFigure)

    # Formula at top center
    fig.text(0.5, 0.93,
             r'$P(w_i) = \dfrac{e^{z_i}}{\sum_j e^{z_j}}$',
             fontsize=22, ha='center', va='center', color=ORANGE,
             family='sans-serif', zorder=10,
             transform=fig.transFigure)

    # Main title
    fig.suptitle('From Scores to Probabilities',
                 fontsize=28, fontweight='bold', color=TEXT,
                 family='sans-serif', y=0.99)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
