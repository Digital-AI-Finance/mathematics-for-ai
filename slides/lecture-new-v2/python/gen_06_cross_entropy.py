#!/usr/bin/env python3
"""
gen_06_cross_entropy.py
Cross-entropy visualized: true distribution P vs model prediction Q
for five tokens, with gap shading and minimization annotation.
Output: ../images/06-cross-entropy.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '06-cross-entropy.png')

BG = '#1b2631'; BLUE = '#3498db'; YELLOW = '#f1c40f'; GREEN = '#2ecc71'; TEAL = '#1abc9c'
ORANGE = '#e67e22'; RED = '#e74c3c'; TEXT = '#ecf0f1'; MUTED = '#95a5a6'


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)

    # Data
    tokens = ['"Paris"', '"London"', '"the"', '"Berlin"', '"Tokyo"']
    P = np.array([0.85, 0.05, 0.04, 0.03, 0.03])
    Q = np.array([0.40, 0.25, 0.15, 0.12, 0.08])

    x = np.arange(len(tokens))
    bar_w = 0.32

    # Draw bars
    bars_p = ax.bar(x - bar_w / 2 - 0.02, P, bar_w, color=GREEN, alpha=0.90,
                    edgecolor='white', linewidth=1.2, label='P (true)', zorder=3)
    bars_q = ax.bar(x + bar_w / 2 + 0.02, Q, bar_w, color=BLUE, alpha=0.90,
                    edgecolor='white', linewidth=1.2, label='Q (model)', zorder=3)

    # Bar value labels
    for bar in bars_p:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.015,
                f'{h:.2f}', ha='center', va='bottom', fontsize=14,
                fontweight='bold', color=GREEN, zorder=4)
    for bar in bars_q:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.015,
                f'{h:.2f}', ha='center', va='bottom', fontsize=14,
                fontweight='bold', color=BLUE, zorder=4)

    # Gap shading between P and Q bars with arrows
    for i in range(len(tokens)):
        p_val = P[i]
        q_val = Q[i]
        cx_p = x[i] - bar_w / 2 - 0.02
        cx_q = x[i] + bar_w / 2 + 0.02
        mid_x = x[i]

        # Shaded gap region between bar tops
        top = max(p_val, q_val)
        bot = min(p_val, q_val)
        if abs(p_val - q_val) > 0.005:
            ax.fill_between(
                [cx_p + bar_w / 2, cx_q + bar_w / 2],
                [bot, bot], [top, top],
                color=RED, alpha=0.18, zorder=2)
            # Vertical arrow showing gap
            arrow = FancyArrowPatch(
                (mid_x, q_val if q_val < p_val else p_val),
                (mid_x, p_val if q_val < p_val else q_val),
                arrowstyle='<->', color=RED, lw=1.8,
                mutation_scale=14, zorder=5)
            ax.add_patch(arrow)

    # Cross-entropy value
    H_pq = -np.sum(P * np.log(Q))
    H_pq_str = f'{H_pq:.3f}'

    # Formula annotation
    ax.text(0.50, -0.22,
            r'$H(P, Q) \;=\; -\sum P(x)\,\log\,Q(x)$'
            f'  =  {H_pq_str} nats',
            transform=ax.transAxes, fontsize=22, color=YELLOW,
            ha='center', va='top', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=BG,
                      edgecolor=YELLOW, alpha=0.8, linewidth=2))

    # "Training reduces this gap" annotation -- positioned between bar groups
    ax.annotate(
        'Training reduces\nthis gap',
        xy=(x[0], 0.62), xytext=(x[0] + 0.65, 0.62),
        fontsize=17, color=RED,
        fontweight='bold', ha='left', va='center',
        arrowprops=dict(arrowstyle='->', color=RED, lw=2.0,
                        connectionstyle='arc3,rad=-0.2'),
        bbox=dict(boxstyle='round,pad=0.35', facecolor=BG,
                  edgecolor=RED, alpha=0.85, linewidth=1.5))

    # Curved arrow from Q toward P labeled "Cross-entropy minimization"
    ax.annotate(
        'Cross-entropy\nminimization',
        xy=(x[0] - bar_w / 2 - 0.02 + bar_w, P[0] - 0.05),
        xytext=(x[1] + bar_w / 2 + 0.02 + bar_w / 2, 0.72),
        fontsize=15, color=ORANGE, fontweight='bold',
        ha='center', va='center',
        arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2.5,
                        connectionstyle='arc3,rad=0.3'),
        bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                  edgecolor=ORANGE, alpha=0.7, linewidth=1.2))

    # Axes
    ax.set_xticks(x)
    ax.set_xticklabels(tokens, fontsize=18, fontweight='bold', color=TEXT)
    ax.set_ylabel('Probability', fontsize=20, color=TEXT, labelpad=12)
    ax.set_ylim(0, 1.05)
    ax.tick_params(axis='y', colors=MUTED, labelsize=16)
    ax.grid(axis='y', alpha=0.15, color=MUTED)
    ax.legend(fontsize=18, loc='upper right', frameon=False, labelcolor=TEXT)

    # Title
    fig.suptitle('Cross-Entropy: Measuring Prediction Error',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)
    fig.text(0.5, 0.91,
             'Next token prediction: "The capital of France is ___"',
             ha='center', fontsize=20, color=MUTED, style='italic')

    plt.tight_layout(rect=[0, 0.12, 1, 0.88])

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
