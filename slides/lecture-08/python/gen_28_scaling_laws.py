#!/usr/bin/env python3
"""
Generate slide 28: Phase Transitions -- From Graphs to AI.

Dual panel:
  Left:  Erdos-Renyi giant component fraction vs edge probability
  Right: LLM scaling law (loss vs parameters, log-log)

Output: ../images/28-scaling-laws.png (3840x2160, 4K)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expit

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '28-scaling-laws.png')

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


def draw_er_panel(ax):
    """Left: Erdos-Renyi giant component fraction vs edge probability."""
    n = 100
    p_crit = 1.0 / n
    p = np.linspace(0, 0.025, 500)

    steepness = 800
    fraction = expit(steepness * (p - p_crit))

    ax.plot(p, fraction, color=BLUE, lw=3.5, label='Giant component fraction')
    ax.fill_between(p, fraction, alpha=0.15, color=BLUE)

    # Critical threshold
    ax.axvline(p_crit, color=RED, ls='--', lw=2.5, alpha=0.7,
               label=f'$p_c = 1/n = {p_crit}$')

    # Phase labels
    ax.text(0.004, 0.15, 'Many small\ncomponents',
            fontsize=23, color=MUTED, ha='center', style='italic')
    ax.text(0.018, 0.85, 'Giant component\nemerges',
            fontsize=23, color=BLUE, ha='center', fontweight='bold')

    ax.set_xlim(0, 0.025)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel('Edge Probability $p$', fontsize=23, color=TEXT, labelpad=10)
    ax.set_ylabel('Giant Component Fraction', fontsize=23, color=TEXT,
                  labelpad=10)
    ax.set_title('Erd\u0151s\u2013R\u00e9nyi Phase Transition',
                 fontsize=26, fontweight='bold', color=BLUE, pad=14)
    ax.legend(fontsize=18, loc='upper left', frameon=False, labelcolor=TEXT)
    ax.tick_params(colors=MUTED, labelsize=18)
    ax.grid(True, alpha=0.15, color=MUTED)


def draw_scaling_panel(ax):
    """Right: LLM scaling law -- loss vs parameters (log-log)."""
    # Parameters range
    N = np.logspace(7, 12, 500)
    N_c = 8e13  # critical scale constant
    alpha = 0.076

    # Chinchilla-style power law: L(N) = (N_c / N) ^ alpha
    loss = (N_c / N) ** alpha

    ax.plot(N, loss, color=YELLOW, lw=3.5, label='$L(N) = (N_c / N)^{0.076}$')

    # Emergent abilities band
    em_lo, em_hi = 3e10, 3e11
    ax.axvspan(em_lo, em_hi, alpha=0.12, color=TEAL, zorder=0)
    ax.text(np.sqrt(em_lo * em_hi), loss.max() * 0.97,
            'Emergent\nabilities', fontsize=18, color=TEAL,
            ha='center', va='top', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
                      edgecolor=TEAL, alpha=0.7))

    # Model annotations
    models = [
        ('GPT-2',  1.5e9,  MUTED),
        ('GPT-3',  1.75e11, BLUE),
        ('GPT-4',  1e12,   YELLOW),
    ]
    for name, n_params, colour in models:
        l_val = (N_c / n_params) ** alpha
        ax.plot(n_params, l_val, 'o', color=colour, markersize=12,
                zorder=5, markeredgecolor='white', markeredgewidth=1.5)
        ax.annotate(name, xy=(n_params, l_val),
                    xytext=(n_params * 1.8, l_val * 1.05),
                    fontsize=18, color=colour, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=colour, lw=1.5))

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e7, 2e12)
    ax.set_xlabel('Parameters', fontsize=23, color=TEXT, labelpad=10)
    ax.set_ylabel('Loss', fontsize=23, color=TEXT, labelpad=10)
    ax.set_title('LLM Scaling Law', fontsize=26, fontweight='bold',
                 color=YELLOW, pad=14)
    ax.legend(fontsize=18, loc='upper right', frameon=False, labelcolor=TEXT)
    ax.tick_params(colors=MUTED, labelsize=18)
    ax.grid(True, alpha=0.15, color=MUTED)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19.2, 10.8), facecolor=BG)
    ax1.set_facecolor(BG)
    ax2.set_facecolor(BG)

    draw_er_panel(ax1)
    draw_scaling_panel(ax2)

    fig.suptitle('Phase Transitions: From Graphs to AI',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)

    fig.text(0.5, 0.02,
             'Same mathematical pattern \u2014 '
             'quantitative change produces qualitative leap',
             ha='center', fontsize=23, color=MUTED)

    plt.tight_layout(rect=[0, 0.05, 1, 0.92])

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
