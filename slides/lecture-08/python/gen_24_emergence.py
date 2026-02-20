#!/usr/bin/env python3
"""
Generate slide 24: Emergence as Phase Transition.

Two panels side by side:
  Left:  LLM Emergent Abilities -- sigmoid curves for 3 tasks vs model size
  Right: Erdos-Renyi Phase Transition -- giant component fraction vs edge probability

Output: ../images/24-emergence-phase-transition.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expit

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '24-emergence-phase-transition.png')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG      = '#1b2631'
YELLOW  = '#f1c40f'
BLUE    = '#3498db'
TEAL    = '#2ecc71'
RED     = '#e74c3c'
ORANGE  = '#e67e22'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'


def draw_llm_panel(ax):
    """Left panel: LLM emergent abilities with sigmoid curves."""
    params = np.logspace(8, 12, 500)  # 10^8 to 10^12
    log_params = np.log10(params)

    # Sigmoid curves shifted at different scales
    # expit(k * (x - x0)) gives sigmoid centered at x0, steepness k
    tasks = [
        ('Arithmetic',       10.0, 8,  YELLOW),
        ('Reasoning',        10.7, 10, TEAL),
        ('Code Generation',  11.0, 10, RED),
    ]

    for label, center, steepness, color in tasks:
        accuracy = 100 * expit(steepness * (log_params - center))
        ax.plot(params, accuracy, color=color, lw=3.5, label=label)

        # Dashed vertical at threshold (50% accuracy point)
        threshold = 10 ** center
        ax.axvline(threshold, color=color, ls='--', lw=1.5, alpha=0.5)

    ax.set_xscale('log')
    ax.set_xlim(1e8, 1e12)
    ax.set_ylim(-5, 105)
    ax.set_xlabel('Model Parameters', fontsize=23, color=TEXT, labelpad=10)
    ax.set_ylabel('Task Accuracy (%)', fontsize=23, color=TEXT, labelpad=10)
    ax.set_title('LLM Emergent Abilities', fontsize=26, fontweight='bold',
                 color=YELLOW, pad=14)
    ax.legend(fontsize=23, loc='upper left', frameon=False, labelcolor=TEXT)
    ax.tick_params(colors=MUTED, labelsize=23)
    ax.grid(True, alpha=0.15, color=MUTED)

    # Annotation at critical region
    ax.annotate('Critical\nthreshold', xy=(1e10, 50), fontsize=23,
                color=MUTED, ha='center', va='bottom',
                style='italic')


def draw_er_panel(ax):
    """Right panel: Erdos-Renyi giant component phase transition."""
    n = 100
    p_crit = 1.0 / n  # = 0.01
    p = np.linspace(0, 0.025, 500)

    # Sigmoid approximation of giant component fraction
    # Sharp transition around p = 1/n
    steepness = 800  # sharp transition
    fraction = 100 * expit(steepness * (p - p_crit))

    ax.plot(p, fraction, color=BLUE, lw=3.5, label='Giant component')
    ax.fill_between(p, fraction, alpha=0.15, color=BLUE)

    # Critical threshold
    ax.axvline(p_crit, color=RED, ls='--', lw=2.5, alpha=0.7,
               label=f'$p_c = 1/n = {p_crit}$')

    # Labels for phases
    ax.text(0.004, 15, 'Many small\ncomponents',
            fontsize=23, color=MUTED, ha='center', style='italic')
    ax.text(0.018, 85, 'Giant component\nemerges',
            fontsize=23, color=BLUE, ha='center', fontweight='bold')

    ax.set_xlim(0, 0.025)
    ax.set_ylim(-5, 105)
    ax.set_xlabel('Edge Probability $p$', fontsize=23, color=TEXT, labelpad=10)
    ax.set_ylabel('Giant Component Fraction (%)', fontsize=23, color=TEXT,
                  labelpad=10)
    ax.set_title('Erd\u0151s\u2013R\u00e9nyi Phase Transition',
                 fontsize=26, fontweight='bold', color=BLUE, pad=14)
    ax.legend(fontsize=23, loc='upper left', frameon=False, labelcolor=TEXT)
    ax.tick_params(colors=MUTED, labelsize=23)
    ax.grid(True, alpha=0.15, color=MUTED)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19.2, 10.8), facecolor=BG)
    ax1.set_facecolor(BG)
    ax2.set_facecolor(BG)

    draw_llm_panel(ax1)
    draw_er_panel(ax2)

    fig.suptitle('Same Math, Different Systems',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)

    fig.text(0.5, 0.02,
             'Phase transitions explain why abilities "suddenly" appear at scale',
             ha='center', fontsize=23, color=MUTED)

    plt.tight_layout(rect=[0, 0.05, 1, 0.92])

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
