#!/usr/bin/env python3
"""
gen_18_backprop_flow.py
Computation graph showing forward pass (left-to-right, green arrows) and
backward pass / backpropagation (right-to-left, orange arrows) with gradient
labels on each backward edge.
Output: ../images/18-backprop-flow.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '18-backprop-flow.png')

BG     = '#1b2631'
BLUE   = '#3498db'
YELLOW = '#f1c40f'
GREEN  = '#2ecc71'
TEAL   = '#1abc9c'
ORANGE = '#e67e22'
RED    = '#e74c3c'
TEXT   = '#ecf0f1'
MUTED  = '#95a5a6'


# Node definitions: (label, fill colour, text colour)
NODES = [
    ('Input\nx', MUTED,  BG),
    ('W\xb7x + b', BLUE,  TEXT),
    ('ReLU', GREEN, BG),
    ('Softmax', TEAL,  BG),
    ('Loss\nL',   RED,   TEXT),
]

# Gradient labels for backward arrows (between adjacent node pairs)
# Index i  =  arrow from node i+1 back to node i
GRAD_LABELS = [
    'dL/dx',        # Softmax -> ReLU
    'dL/d(Wx+b)',   # ReLU    -> linear
    'dL/dReLU',     # Softmax -> ReLU  (corrected below)
    'dL/dSoftmax',  # Loss    -> Softmax
]
# Reassign so index matches left-edge of arrow (node index receiving gradient)
# bwd arrow 0: Loss -> Softmax  (right edge nodes[4] -> nodes[3])
# bwd arrow 1: Softmax -> ReLU
# bwd arrow 2: ReLU -> linear
# bwd arrow 3: linear -> input
GRAD_LABELS = [
    'dL/dSoftmax',
    'dL/dReLU',
    'dL/d(Wx+b)',
    'dL/dx',
]


def draw_node(ax, cx, cy, label, fc, tc, box_w=0.13, box_h=0.14):
    """Draw a rounded rectangle node and return its centre coords."""
    rect = mpatches.FancyBboxPatch(
        (cx - box_w / 2, cy - box_h / 2),
        box_w, box_h,
        boxstyle='round,pad=0.02',
        facecolor=fc, edgecolor=TEXT, linewidth=1.8,
        transform=ax.transData, clip_on=False)
    ax.add_patch(rect)
    ax.text(cx, cy, label,
            ha='center', va='center',
            fontsize=15, fontweight='bold', color=tc,
            linespacing=1.3)
    return cx, cy


def arrow(ax, x0, y0, x1, y1, color, lw=2.5, rad=0.0, label='',
          label_va='bottom', label_offset=0.04):
    """Draw a curved arrow and optional label."""
    style = f'arc3,rad={rad}'
    ax.annotate('',
                xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(
                    arrowstyle='->', color=color,
                    lw=lw,
                    connectionstyle=style),
                annotation_clip=False)
    if label:
        mx = (x0 + x1) / 2
        my = (y0 + y1) / 2
        if rad != 0.0:
            # Offset label perpendicular to chord
            dx = x1 - x0
            dy = y1 - y0
            length = max((dx**2 + dy**2)**0.5, 1e-9)
            nx = -dy / length
            ny = dx / length
            sign = 1 if rad > 0 else -1
            mx += sign * nx * abs(rad) * 0.5
            my += sign * ny * abs(rad) * 0.5
        va = label_va
        dy_off = label_offset if va == 'bottom' else -label_offset
        ax.text(mx, my + dy_off, label,
                ha='center', va=va,
                fontsize=12, color=color, fontstyle='italic')


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    # ------------------------------------------------------------------
    # Node positions  (evenly spaced across x, centred vertically)
    # ------------------------------------------------------------------
    n = len(NODES)
    xs = np.linspace(0.12, 0.88, n)
    cy = 0.52         # vertical centre for all nodes
    box_w = 0.13
    box_h = 0.15

    centres = []
    for i, (label, fc, tc) in enumerate(NODES):
        cx, cy_ = draw_node(ax, xs[i], cy, label, fc, tc,
                            box_w=box_w, box_h=box_h)
        centres.append((cx, cy_))

    # ------------------------------------------------------------------
    # Forward pass arrows (above nodes, left to right)
    # ------------------------------------------------------------------
    fwd_y_offset = 0.08      # how far above centre the arrow travels
    fwd_arrow_y  = cy + fwd_y_offset

    for i in range(n - 1):
        x0 = centres[i][0] + box_w / 2
        x1 = centres[i + 1][0] - box_w / 2
        # Draw horizontal arrow above node row
        arrow(ax, x0, fwd_arrow_y, x1, fwd_arrow_y,
              color=GREEN, lw=2.8, rad=0.0,
              label='forward' if i == 0 else '',
              label_va='bottom', label_offset=0.035)

    # "Forward pass" label
    ax.text((centres[0][0] + centres[-1][0]) / 2,
            fwd_arrow_y + 0.055,
            'Forward Pass',
            ha='center', va='bottom',
            fontsize=16, fontweight='bold', color=GREEN)
    # left-to-right indicator
    ax.annotate('', xy=(centres[-1][0], fwd_arrow_y + 0.05),
                xytext=(centres[0][0], fwd_arrow_y + 0.05),
                arrowprops=dict(arrowstyle='->', color=GREEN,
                                lw=1.5, linestyle='dashed'),
                annotation_clip=False)

    # ------------------------------------------------------------------
    # Backward pass arrows (below nodes, right to left)
    # ------------------------------------------------------------------
    bwd_y_offset = 0.08
    bwd_arrow_y  = cy - bwd_y_offset

    for i in range(n - 1, 0, -1):
        x0 = centres[i][0] - box_w / 2
        x1 = centres[i - 1][0] + box_w / 2
        grad_idx = n - 1 - i     # 0 for Loss->Softmax, 1 for Softmax->ReLU, ...
        lbl = GRAD_LABELS[grad_idx] if grad_idx < len(GRAD_LABELS) else ''
        arrow(ax, x0, bwd_arrow_y, x1, bwd_arrow_y,
              color=ORANGE, lw=2.8, rad=0.0,
              label=lbl,
              label_va='top', label_offset=0.035)

    # "Backward Pass" label
    ax.text((centres[0][0] + centres[-1][0]) / 2,
            bwd_arrow_y - 0.055,
            'Backward Pass  (Backpropagation)',
            ha='center', va='top',
            fontsize=16, fontweight='bold', color=ORANGE)
    ax.annotate('', xy=(centres[0][0], bwd_arrow_y - 0.05),
                xytext=(centres[-1][0], bwd_arrow_y - 0.05),
                arrowprops=dict(arrowstyle='->', color=ORANGE,
                                lw=1.5, linestyle='dashed'),
                annotation_clip=False)

    # ------------------------------------------------------------------
    # Vertical connector lines from forward arrow down to nodes and from
    # nodes down to backward arrow (visual flow guidance)
    # ------------------------------------------------------------------
    for cx, cy_ in centres:
        # top connector
        ax.plot([cx, cx], [cy_ + box_h / 2, fwd_arrow_y],
                color=MUTED, lw=0.8, alpha=0.4, linestyle=':')
        # bottom connector
        ax.plot([cx, cx], [cy_ - box_h / 2, bwd_arrow_y],
                color=MUTED, lw=0.8, alpha=0.4, linestyle=':')

    # ------------------------------------------------------------------
    # Chain-rule annotation box (right panel)
    # ------------------------------------------------------------------
    rx = 0.73
    ry = 0.88
    box_rx = rx - 0.01

    ax.add_patch(mpatches.FancyBboxPatch(
        (box_rx, 0.64), 0.25, 0.24,
        boxstyle='round,pad=0.015',
        facecolor='#0d2137', edgecolor=TEAL,
        linewidth=1.5,
        transform=ax.transData, clip_on=False))
    ax.text(rx + 0.115, 0.875,
            'Chain Rule', ha='center', va='top',
            fontsize=15, fontweight='bold', color=TEAL)
    ax.text(rx + 0.115, 0.845,
            'dL/dW  =  dL/dy . dy/dW',
            ha='center', va='top',
            fontsize=13, color=TEXT, family='monospace')
    ax.text(rx + 0.115, 0.810,
            'Each gradient layer\nmultiplies the one ahead.',
            ha='center', va='top',
            fontsize=11, color=MUTED, linespacing=1.4)

    # ------------------------------------------------------------------
    # Bottom explanation strip
    # ------------------------------------------------------------------
    explanations = [
        (MUTED,  'Input x',       'Raw features\nentering the net'),
        (BLUE,   'W\xb7x + b',    'Linear transform:\nweights & bias'),
        (GREEN,  'ReLU',          'Non-linearity:\nmax(0, z)'),
        (TEAL,   'Softmax',       'Probabilities:\nexp(z) / sum'),
        (RED,    'Loss L',        'Cross-entropy:\nhow wrong we are'),
    ]

    strip_y = 0.22
    for i, (color, heading, body) in enumerate(explanations):
        bx = xs[i]
        ax.add_patch(mpatches.FancyBboxPatch(
            (bx - 0.065, strip_y - 0.065), 0.13, 0.12,
            boxstyle='round,pad=0.01',
            facecolor=color, alpha=0.12,
            edgecolor=color, linewidth=0.8,
            transform=ax.transData, clip_on=False))
        ax.text(bx, strip_y + 0.028, heading,
                ha='center', va='center',
                fontsize=12, fontweight='bold', color=color)
        ax.text(bx, strip_y - 0.018, body,
                ha='center', va='top',
                fontsize=10, color=MUTED, linespacing=1.3)

    # ------------------------------------------------------------------
    # Main title
    # ------------------------------------------------------------------
    fig.text(0.5, 0.967,
             'Backpropagation: How Neural Networks Learn',
             ha='center', va='top', fontsize=24,
             fontweight='bold', color=TEXT)
    fig.text(0.5, 0.937,
             'Forward pass computes predictions;  '
             'backward pass propagates gradients via the chain rule',
             ha='center', va='top', fontsize=14,
             color=MUTED, fontstyle='italic')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
