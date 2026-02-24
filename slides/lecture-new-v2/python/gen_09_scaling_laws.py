#!/usr/bin/env python3
"""
gen_09_scaling_laws.py
Log-log plot of LLM scaling laws with power law fit,
model annotations, and emergent abilities region.
NO scipy -- uses numpy sigmoid only.
Output: ../images/09-scaling-laws.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '09-scaling-laws.png')

BG = '#1b2631'; BLUE = '#3498db'; YELLOW = '#f1c40f'; GREEN = '#2ecc71'; TEAL = '#1abc9c'
ORANGE = '#e67e22'; RED = '#e74c3c'; TEXT = '#ecf0f1'; MUTED = '#95a5a6'


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)

    # Power law: L(N) = (N_c / N)^alpha
    N = np.logspace(7, 13, 600)
    N_c = 8e13
    alpha = 0.076
    loss = (N_c / N) ** alpha

    # Main curve
    ax.plot(N, loss, color=YELLOW, lw=4.0, zorder=3,
            label=r'$L(N) = (N_c\,/\,N)^{\,0.076}$')

    # Confidence band (simulated spread)
    loss_upper = loss * 1.06
    loss_lower = loss * 0.94
    ax.fill_between(N, loss_lower, loss_upper, color=YELLOW,
                    alpha=0.10, zorder=2)

    # Emergent abilities region
    em_lo, em_hi = 3e10, 3e11
    ax.axvspan(em_lo, em_hi, alpha=0.14, color=TEAL, zorder=1)
    em_center = np.sqrt(em_lo * em_hi)
    ax.text(em_center, loss.max() * 0.97, 'Emergent\nAbilities',
            fontsize=20, color=TEAL, ha='center', va='top',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.35', facecolor=BG,
                      edgecolor=TEAL, alpha=0.8, linewidth=1.5))

    # Scattered data points along the curve (simulated research data)
    rng = np.random.RandomState(7)
    n_pts = 40
    data_N = np.logspace(7.5, 12.5, n_pts)
    data_loss = (N_c / data_N) ** alpha * (1 + rng.randn(n_pts) * 0.03)
    ax.scatter(data_N, data_loss, s=30, color=MUTED, alpha=0.5,
               zorder=2, edgecolors='none')

    # Model annotations
    models = [
        ('GPT-2\n1.5B', 1.5e9, MUTED, (-50, 35)),
        ('GPT-3\n175B', 1.75e11, BLUE, (40, 30)),
        ('GPT-4\n~1T', 1e12, YELLOW, (45, -25)),
    ]
    for name, n_params, colour, offset in models:
        l_val = (N_c / n_params) ** alpha
        ax.plot(n_params, l_val, 'o', color=colour, markersize=16,
                zorder=5, markeredgecolor='white', markeredgewidth=2)
        ax.annotate(name, xy=(n_params, l_val),
                    xytext=offset, textcoords='offset points',
                    fontsize=17, color=colour, fontweight='bold',
                    ha='center', va='center',
                    arrowprops=dict(arrowstyle='->', color=colour, lw=2),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                              edgecolor=colour, alpha=0.7, linewidth=1.2))

    # Axes
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e7, 2e13)
    ax.set_xlabel('Parameters', fontsize=24, color=TEXT, labelpad=12)
    ax.set_ylabel('Loss', fontsize=24, color=TEXT, labelpad=12)
    ax.tick_params(colors=MUTED, labelsize=18)
    ax.grid(True, alpha=0.15, color=MUTED, which='both')

    # Legend
    legend = ax.legend(fontsize=20, loc='upper right', frameon=True,
                       fancybox=True, framealpha=0.7, edgecolor=MUTED,
                       labelcolor=TEXT)
    legend.get_frame().set_facecolor(BG)

    # Annotation: power law across orders of magnitude
    ax.annotate(
        '7 orders of magnitude',
        xy=(3e7, (N_c / 3e7) ** alpha),
        xytext=(3e8, (N_c / 3e7) ** alpha * 1.12),
        fontsize=15, color=MUTED, style='italic',
        arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.5))

    ax.annotate(
        '',
        xy=(5e12, (N_c / 5e12) ** alpha),
        xytext=(3e8, (N_c / 3e7) ** alpha * 1.12),
        arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.5))

    # Title
    fig.suptitle('Scaling Laws: More Math, Better AI',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)
    fig.text(0.5, 0.91,
             'Performance follows a precise power law across '
             '7 orders of magnitude',
             ha='center', fontsize=22, color=MUTED, style='italic')

    plt.tight_layout(rect=[0, 0.02, 1, 0.88])

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
