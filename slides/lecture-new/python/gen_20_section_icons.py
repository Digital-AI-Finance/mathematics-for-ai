#!/usr/bin/env python3
"""
gen_20_section_icons.py
Five section-divider watermark icons — one large mathematical symbol per pillar,
rendered at low opacity on a dark background.
Output:
    ../images/20a-icon-linalg.png
    ../images/20b-icon-prob.png
    ../images/20c-icon-calc.png
    ../images/20d-icon-info.png
    ../images/20e-icon-optim.png
(each 3840x2160, 4K)
"""
import os
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BG      = '#1b2631'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
TEAL    = '#1abc9c'
ORANGE  = '#e67e22'
RED     = '#e74c3c'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'

# (output_filename, symbol, color)
ICONS = [
    ('20a-icon-linalg.png', '[M]',  BLUE),
    ('20b-icon-prob.png',   'P(x)', GREEN),
    ('20c-icon-calc.png',   '\u2207', ORANGE),   # ∇ nabla
    ('20d-icon-info.png',   'H',    TEAL),
    ('20e-icon-optim.png',  '\u2193', YELLOW),   # ↓ down arrow
]


def main():
    for filename, symbol, color in ICONS:
        output_path = os.path.join(SCRIPT_DIR, '..', 'images', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
        ax.set_facecolor(BG)
        fig.patch.set_facecolor(BG)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        ax.text(
            0.5, 0.5,
            symbol,
            ha='center', va='center',
            fontsize=400,
            alpha=0.15,
            color=color,
            transform=ax.transAxes,
            clip_on=False,
        )

        plt.savefig(output_path, dpi=200, bbox_inches='tight',
                    facecolor=BG, edgecolor='none')
        plt.close(fig)
        print(f'Saved: {os.path.abspath(output_path)}')


if __name__ == '__main__':
    main()
