#!/usr/bin/env python3
"""
gen_13_loss_curve.py
Training loss curve showing convergence of a language model.
Output: ../images/13-loss-curve.png
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '13-loss-curve.png')

BG     = '#1b2631'
BLUE   = '#3498db'
YELLOW = '#f1c40f'
GREEN  = '#2ecc71'
TEAL   = '#1abc9c'
ORANGE = '#e67e22'
RED    = '#e74c3c'
TEXT   = '#ecf0f1'
MUTED  = '#95a5a6'


def smooth_loss(steps, init=4.05, final=1.52, decay=0.000045):
    """Exponential decay curve with asymptote at `final`."""
    return final + (init - final) * np.exp(-decay * steps)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    rng = np.random.default_rng(7)
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)

    # ---- Build training steps ----
    steps = np.linspace(0, 100_000, 2000)

    # Training loss: smooth + realistic noise (larger at start, smaller at end)
    train_base = smooth_loss(steps)
    noise_scale = 0.08 * np.exp(-steps / 30_000) + 0.015
    noise = rng.normal(0, noise_scale, len(steps))
    train_loss = train_base + noise

    # Validation loss: slightly above training, converges a bit slower
    val_base = smooth_loss(steps, init=4.20, final=1.68, decay=0.000038)
    val_noise = rng.normal(0, 0.025, len(steps))
    val_loss = val_base + val_noise

    # ---- Shade background phases ----
    fast_end   = 25_000
    medium_end = 60_000

    ax.axvspan(0,          fast_end,   alpha=0.08, color=GREEN,  zorder=0)
    ax.axvspan(fast_end,   medium_end, alpha=0.06, color=YELLOW, zorder=0)
    ax.axvspan(medium_end, 100_000,    alpha=0.05, color=RED,    zorder=0)

    # ---- Plot curves ----
    ax.plot(steps, val_loss,
            color=ORANGE, linewidth=2.2, alpha=0.75,
            label='Validation loss', zorder=3)
    ax.plot(steps, train_loss,
            color=BLUE, linewidth=2.8, alpha=0.95,
            label='Training loss', zorder=4)

    # ---- Phase annotation arrows + labels ----
    # Fast learning
    mid_fast = fast_end / 2
    y_fast   = smooth_loss(mid_fast) + 0.35
    ax.annotate(
        'Fast Learning',
        xy=(mid_fast, smooth_loss(mid_fast) + 0.05),
        xytext=(mid_fast, y_fast),
        ha='center', va='bottom',
        fontsize=13, fontweight='bold', color=GREEN,
        arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.6),
        zorder=6)
    ax.text(mid_fast, y_fast + 0.12,
            'Steep gradient →\nloss drops quickly',
            ha='center', va='bottom', fontsize=10,
            color=GREEN, alpha=0.8, linespacing=1.4)

    # Diminishing returns
    mid_dim = (fast_end + medium_end) / 2
    y_dim   = smooth_loss(mid_dim) + 0.40
    ax.annotate(
        'Diminishing Returns',
        xy=(mid_dim, smooth_loss(mid_dim) + 0.05),
        xytext=(mid_dim, y_dim),
        ha='center', va='bottom',
        fontsize=13, fontweight='bold', color=YELLOW,
        arrowprops=dict(arrowstyle='->', color=YELLOW, lw=1.6),
        zorder=6)
    ax.text(mid_dim, y_dim + 0.12,
            'Gradient flattens →\nsmaller steps forward',
            ha='center', va='bottom', fontsize=10,
            color=YELLOW, alpha=0.8, linespacing=1.4)

    # Convergence
    mid_conv = (medium_end + 100_000) / 2
    y_conv   = smooth_loss(mid_conv) + 0.45
    ax.annotate(
        'Convergence',
        xy=(mid_conv, smooth_loss(mid_conv) + 0.05),
        xytext=(mid_conv, y_conv),
        ha='center', va='bottom',
        fontsize=13, fontweight='bold', color=RED,
        arrowprops=dict(arrowstyle='->', color=RED, lw=1.6),
        zorder=6)
    ax.text(mid_conv, y_conv + 0.12,
            'Near-zero gradient →\nmodel stops improving',
            ha='center', va='bottom', fontsize=10,
            color=RED, alpha=0.8, linespacing=1.4)

    # ---- Horizontal dashed line at final loss ----
    ax.axhline(y=1.52, color=MUTED, linewidth=1.0,
               linestyle='--', alpha=0.5, zorder=2)
    ax.text(101_500, 1.52, 'Final\nloss ≈ 1.52',
            ha='left', va='center', fontsize=9.5,
            color=MUTED, family='sans-serif')

    # ---- Highlight the gap between train and val at end ----
    end_step = 95_000
    t_val  = smooth_loss(end_step, init=4.20, final=1.68, decay=0.000038)
    t_train = smooth_loss(end_step)
    ax.annotate('',
                xy=(end_step, t_val),
                xytext=(end_step, t_train),
                arrowprops=dict(arrowstyle='<->', color=TEAL, lw=1.4))
    ax.text(end_step + 1800, (t_val + t_train) / 2,
            'Generalisation\ngap',
            ha='left', va='center', fontsize=9.5,
            color=TEAL, linespacing=1.3)

    # ---- Axes styling ----
    ax.set_xlim(-1_000, 104_000)
    ax.set_ylim(0.9, 4.8)

    ax.set_xlabel('Training Steps', fontsize=14, color=MUTED, labelpad=10)
    ax.set_ylabel('Loss', fontsize=14, color=MUTED, labelpad=10)

    ax.tick_params(colors=MUTED, labelsize=10)
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{int(x/1000)}k' if x > 0 else '0'))

    for spine in ax.spines.values():
        spine.set_edgecolor('#2c3e50')

    ax.grid(True, color='#2c3e50', linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)

    # ---- Legend ----
    handles = [
        mpatches.Patch(color=BLUE,   label='Training loss'),
        mpatches.Patch(color=ORANGE, label='Validation loss'),
    ]
    ax.legend(handles=handles, fontsize=12,
              facecolor='#2c3e50', edgecolor=MUTED,
              labelcolor=TEXT, framealpha=0.9,
              loc='upper right')

    # ---- Title ----
    ax.set_title(
        'Training a Language Model\n'
        r'$\it{Loss\ decreases\ as\ the\ model\ sees\ more\ data}$',
        fontsize=20, fontweight='bold', color=TEXT,
        pad=18, linespacing=1.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
