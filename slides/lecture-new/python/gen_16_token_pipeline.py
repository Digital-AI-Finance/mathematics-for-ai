#!/usr/bin/env python3
"""
gen_16_token_pipeline.py
Horizontal LLM pipeline flow diagram: five stages connected by arrows.
Your Text → Tokenizer → Embeddings → Transformer → Next Word
Output: ../images/16-token-pipeline.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '16-token-pipeline.png')

BG      = '#1b2631'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
TEAL    = '#1abc9c'
ORANGE  = '#e67e22'
RED     = '#e74c3c'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'


def make_dark(hex_color, factor=0.15):
    """Return a very dark version of a colour for box fills."""
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255
    r2, g2, b2 = [int(c * factor * 255) for c in (r, g, b)]
    return f'#{r2:02x}{g2:02x}{b2:02x}'


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # ------------------------------------------------------------------ stages
    stages = [
        {
            'label':    'Your Text',
            'sublabel': 'Input',
            'color':    TEXT,
            'fill':     '#1e2d3d',
        },
        {
            'label':    'Tokenizer',
            'sublabel': 'Linear Algebra',
            'color':    BLUE,
            'fill':     make_dark(BLUE, 0.14),
        },
        {
            'label':    'Embeddings',
            'sublabel': 'Linear Algebra',
            'color':    GREEN,
            'fill':     make_dark(GREEN, 0.14),
        },
        {
            'label':    'Transformer',
            'sublabel': 'Prob + Calc',
            'color':    ORANGE,
            'fill':     make_dark(ORANGE, 0.14),
        },
        {
            'label':    'Next Word',
            'sublabel': 'Info Theory',
            'color':    TEAL,
            'fill':     make_dark(TEAL, 0.14),
        },
    ]

    n = len(stages)

    # Layout: boxes centred at these x positions on y=0.50
    x_margin  = 0.08
    x_spacing = (1.0 - 2 * x_margin) / (n - 1)
    box_w     = 0.130
    box_h     = 0.200
    centre_y  = 0.52

    box_centres = [x_margin + i * x_spacing for i in range(n)]

    # ------------------------------------------------------------------ draw arrows first
    arrow_y = centre_y
    for i in range(n - 1):
        x_start = box_centres[i] + box_w / 2 + 0.008
        x_end   = box_centres[i + 1] - box_w / 2 - 0.008

        # Glow shaft
        for lw, alpha in [(10, 0.06), (6, 0.10), (3, 0.18), (1.5, 0.50)]:
            ax.annotate('',
                        xy=(x_end, arrow_y),
                        xytext=(x_start, arrow_y),
                        xycoords='data', textcoords='data',
                        arrowprops=dict(
                            arrowstyle='-',
                            color=MUTED,
                            lw=lw,
                            alpha=alpha,
                        ))

        # Arrowhead (solid)
        ax.annotate('',
                    xy=(x_end, arrow_y),
                    xytext=(x_start + (x_end - x_start) * 0.85, arrow_y),
                    xycoords='data', textcoords='data',
                    arrowprops=dict(
                        arrowstyle='-|>',
                        color=TEXT,
                        lw=2.0,
                        mutation_scale=22,
                    ))

    # ------------------------------------------------------------------ draw boxes
    for i, stage in enumerate(stages):
        cx = box_centres[i]
        bx = cx - box_w / 2
        by = centre_y - box_h / 2

        # Drop shadow
        shadow = mpatches.FancyBboxPatch(
            (bx + 0.005, by - 0.008), box_w, box_h,
            boxstyle='round,pad=0.018',
            facecolor='black', edgecolor='none',
            alpha=0.45, zorder=2,
            transform=ax.transData
        )
        ax.add_patch(shadow)

        # Main box
        box = mpatches.FancyBboxPatch(
            (bx, by), box_w, box_h,
            boxstyle='round,pad=0.018',
            facecolor=stage['fill'],
            edgecolor=stage['color'],
            linewidth=2.8,
            zorder=3,
            transform=ax.transData
        )
        ax.add_patch(box)

        # Top glow stripe
        stripe = mpatches.FancyBboxPatch(
            (bx + 0.006, by + box_h - 0.022), box_w - 0.012, 0.018,
            boxstyle='round,pad=0.004',
            facecolor=stage['color'], edgecolor='none',
            alpha=0.35, zorder=4,
            transform=ax.transData
        )
        ax.add_patch(stripe)

        # Stage name
        ax.text(cx, centre_y + 0.030, stage['label'],
                ha='center', va='center',
                fontsize=19, fontweight='bold',
                color=stage['color'],
                zorder=5, transform=ax.transData)

        # Index number (small, top-right of box)
        ax.text(cx + box_w / 2 - 0.016, centre_y + box_h / 2 - 0.022,
                str(i + 1),
                ha='center', va='center',
                fontsize=10, fontweight='bold',
                color=stage['color'], alpha=0.55,
                zorder=5, transform=ax.transData)

    # ------------------------------------------------------------------ sublabels (below boxes)
    sub_y = centre_y - box_h / 2 - 0.060

    for i, stage in enumerate(stages):
        cx = box_centres[i]

        # Pill background
        pill_w = box_w * 0.86
        pill_h = 0.055
        pill = mpatches.FancyBboxPatch(
            (cx - pill_w / 2, sub_y - pill_h / 2 + 0.010),
            pill_w, pill_h,
            boxstyle='round,pad=0.012',
            facecolor=stage['color'], edgecolor='none',
            alpha=0.14, zorder=2,
            transform=ax.transData
        )
        ax.add_patch(pill)

        ax.text(cx, sub_y + 0.014, stage['sublabel'],
                ha='center', va='center',
                fontsize=13.5, fontweight='bold',
                color=stage['color'], alpha=0.90,
                zorder=3, transform=ax.transData)

    # ------------------------------------------------------------------ title + subtitle
    fig.text(0.50, 0.935,
             'How an LLM Processes Text',
             ha='center', va='top',
             fontsize=28, fontweight='bold',
             color=TEXT)
    fig.text(0.50, 0.895,
             'Five mathematical stages from raw input to predicted next word',
             ha='center', va='top',
             fontsize=15, color=MUTED, fontstyle='italic')

    # ------------------------------------------------------------------ bottom caption row
    math_labels = [
        ('Input', 'raw string'),
        ('Tokens', 'integer IDs'),
        ('Vectors', 'ℝⁿ space'),
        ('Attention', '∑ softmax(QKᵀ/√d) · V'),
        ('P(word)', 'argmax / sample'),
    ]
    cap_y = 0.115
    for i, (cap_top, cap_bot) in enumerate(math_labels):
        cx = box_centres[i]
        ax.text(cx, cap_y + 0.028, cap_top,
                ha='center', va='center',
                fontsize=11, fontweight='bold',
                color=TEXT, alpha=0.65,
                zorder=3, transform=ax.transData)
        ax.text(cx, cap_y - 0.002, cap_bot,
                ha='center', va='center',
                fontsize=9.5,
                color=MUTED, alpha=0.80,
                zorder=3, transform=ax.transData)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
