#!/usr/bin/env python3
"""
gen_17_matrix_multiply.py
Annotated matrix multiplication diagram: W (3x3) times x (3x1) equals y (3x1).
One row of W and the column of x are highlighted to show the dot-product mechanism.
Output: ../images/17-matrix-multiply.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '17-matrix-multiply.png')

BG     = '#1b2631'
BLUE   = '#3498db'
YELLOW = '#f1c40f'
GREEN  = '#2ecc71'
TEAL   = '#1abc9c'
ORANGE = '#e67e22'
RED    = '#e74c3c'
TEXT   = '#ecf0f1'
MUTED  = '#95a5a6'

# Dim variants for non-highlighted cells
BLUE_DIM   = '#1a4a6e'
GREEN_DIM  = '#1a5c36'
YELLOW_DIM = '#7a6208'

# Cell values
W = np.array([
    [0.8, -0.3,  0.5],
    [0.2,  0.9, -0.4],
    [-0.6, 0.1,  0.7],
])
x = np.array([[1.2], [-0.8], [0.5]])
y = W @ x  # shape (3,1)

HIGHLIGHT_ROW = 1   # which row of W / which cell of y to highlight


def draw_matrix(ax, values, x0, y0, cell_w, cell_h,
                highlight_row=None, highlight_col=None,
                face_bright=None, face_dim=None,
                full_highlight=False):
    """Draw a matrix as a grid of Rectangle patches with text values.

    Parameters
    ----------
    full_highlight : if True every cell in the matrix gets the bright colour
                     (used for the x vector column).
    """
    rows, cols = values.shape
    patches = {}
    for r in range(rows):
        for c in range(cols):
            is_bright = full_highlight or (
                (highlight_row is not None and r == highlight_row) or
                (highlight_col is not None and c == highlight_col)
            )
            fc = face_bright if is_bright else face_dim
            rect = mpatches.FancyBboxPatch(
                (x0 + c * cell_w, y0 - r * cell_h),
                cell_w * 0.92, cell_h * 0.88,
                boxstyle='round,pad=0.02',
                facecolor=fc, edgecolor=BG, linewidth=1.5,
                transform=ax.transData, clip_on=False)
            ax.add_patch(rect)
            cx = x0 + c * cell_w + cell_w * 0.46
            cy = y0 - r * cell_h + cell_h * 0.44
            val_str = f'{values[r, c]:+.2f}'
            tc = TEXT if is_bright else MUTED
            ax.text(cx, cy, val_str, ha='center', va='center',
                    fontsize=17, fontweight='bold', color=tc,
                    family='monospace')
            patches[(r, c)] = rect
    return patches


def bracket(ax, x0, y0, height, opening='left', color=TEXT, lw=2.5):
    """Draw a square bracket on the left or right side of a matrix region."""
    arm = height * 0.08
    if opening == 'left':
        xs = [x0 + arm, x0, x0, x0 + arm]
        ys = [y0,        y0, y0 - height, y0 - height]
    else:
        xs = [x0 - arm, x0, x0, x0 - arm]
        ys = [y0,        y0, y0 - height, y0 - height]
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle='round',
            transform=ax.transData, clip_on=False)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    # ------------------------------------------------------------------
    # Layout geometry
    # ------------------------------------------------------------------
    cell_w = 0.10
    cell_h = 0.14

    rows_W, cols_W = 3, 3
    rows_x, cols_x = 3, 1
    rows_y, cols_y = 3, 1

    mat_top = 0.72          # y of the top-left corner of each matrix top row

    # x positions (left edge of each matrix block)
    pad_sym = 0.06          # gap for × and = symbols
    x_W = 0.08
    x_op1 = x_W + cols_W * cell_w + 0.01          # × operator
    x_x = x_op1 + pad_sym                          # matrix x
    x_op2 = x_x + cols_x * cell_w + 0.01          # = operator
    x_y  = x_op2 + pad_sym                         # result y

    bkt_gap = 0.018         # gap between bracket and cell column

    # ------------------------------------------------------------------
    # Draw W (3x3)
    # ------------------------------------------------------------------
    draw_matrix(ax, W, x_W, mat_top, cell_w, cell_h,
                highlight_row=HIGHLIGHT_ROW,
                face_bright=BLUE, face_dim=BLUE_DIM)

    # Left + right brackets for W
    total_h = rows_W * cell_h
    bracket(ax, x_W - bkt_gap, mat_top + cell_h * 0.88, total_h,
            opening='left', color=TEXT)
    bracket(ax, x_W + cols_W * cell_w * 0.92 + bkt_gap,
            mat_top + cell_h * 0.88, total_h,
            opening='right', color=TEXT)

    # ------------------------------------------------------------------
    # Operator ×
    # ------------------------------------------------------------------
    op_y = mat_top - (rows_W * cell_h) / 2 + cell_h * 0.44
    ax.text(x_op1 + pad_sym * 0.45, op_y, '\u00d7',
            ha='center', va='center', fontsize=40,
            fontweight='bold', color=TEXT)

    # ------------------------------------------------------------------
    # Draw x (3x1) — full highlight green
    # ------------------------------------------------------------------
    draw_matrix(ax, x, x_x, mat_top, cell_w, cell_h,
                full_highlight=True,
                face_bright=GREEN, face_dim=GREEN_DIM)

    bracket(ax, x_x - bkt_gap, mat_top + cell_h * 0.88, total_h,
            opening='left', color=TEXT)
    bracket(ax, x_x + cols_x * cell_w * 0.92 + bkt_gap,
            mat_top + cell_h * 0.88, total_h,
            opening='right', color=TEXT)

    # ------------------------------------------------------------------
    # Operator =
    # ------------------------------------------------------------------
    ax.text(x_op2 + pad_sym * 0.45, op_y, '=',
            ha='center', va='center', fontsize=40,
            fontweight='bold', color=TEXT)

    # ------------------------------------------------------------------
    # Draw y (3x1) — only HIGHLIGHT_ROW cell bright yellow
    # ------------------------------------------------------------------
    draw_matrix(ax, y, x_y, mat_top, cell_w, cell_h,
                highlight_row=HIGHLIGHT_ROW,
                face_bright=YELLOW, face_dim=YELLOW_DIM)

    bracket(ax, x_y - bkt_gap, mat_top + cell_h * 0.88, total_h,
            opening='left', color=TEXT)
    bracket(ax, x_y + cols_y * cell_w * 0.92 + bkt_gap,
            mat_top + cell_h * 0.88, total_h,
            opening='right', color=TEXT)

    # ------------------------------------------------------------------
    # Annotation: arc / arrow showing row DOT col = cell
    # ------------------------------------------------------------------
    # Centre of highlighted row of W (middle cell of row HIGHLIGHT_ROW)
    row_mid_x = x_W + 1.5 * cell_w * 0.92       # approx horizontal mid of W
    row_mid_y = mat_top - HIGHLIGHT_ROW * cell_h + cell_h * 0.44

    # Centre of x column
    col_mid_x = x_x + cell_w * 0.46
    col_mid_y = mat_top - 1 * cell_h + cell_h * 0.44  # vertical mid of x

    # Centre of result cell
    res_mid_x = x_y + cell_w * 0.46
    res_mid_y = mat_top - HIGHLIGHT_ROW * cell_h + cell_h * 0.44

    # Curved annotation below the matrices
    ann_y = mat_top - rows_W * cell_h - 0.04

    # Left dot-product bracket
    ax.annotate('', xy=(col_mid_x, ann_y + 0.01),
                xytext=(row_mid_x, ann_y + 0.01),
                arrowprops=dict(
                    arrowstyle='->', color=ORANGE,
                    lw=2.0,
                    connectionstyle='arc3,rad=0.0'))

    # Arrow from dot-product zone to result cell
    ax.annotate('', xy=(res_mid_x, ann_y + 0.01),
                xytext=(col_mid_x + 0.04, ann_y + 0.01),
                arrowprops=dict(
                    arrowstyle='->', color=ORANGE,
                    lw=2.0,
                    connectionstyle='arc3,rad=0.0'))

    # Dot-product label
    mid_ann_x = (row_mid_x + col_mid_x + 0.04) / 2
    ax.text(mid_ann_x, ann_y - 0.04,
            'dot product', ha='center', va='top',
            fontsize=15, color=ORANGE, fontstyle='italic')

    # Arrow from result annotation to result cell
    ax.annotate('', xy=(res_mid_x, res_mid_y - cell_h * 0.44),
                xytext=(res_mid_x, ann_y + 0.01),
                arrowprops=dict(
                    arrowstyle='->', color=YELLOW,
                    lw=2.0,
                    connectionstyle='arc3,rad=0.0'))

    # ------------------------------------------------------------------
    # Vertical highlight line on x vector
    # ------------------------------------------------------------------
    # Already full-bright; add a tinted glow rectangle behind x column
    glow = mpatches.FancyBboxPatch(
        (x_x - 0.008, mat_top + cell_h * 0.88 - total_h - 0.005),
        cell_w * 0.92 + 0.016, total_h + 0.01,
        boxstyle='round,pad=0.01',
        facecolor='none', edgecolor=GREEN, linewidth=2.2, alpha=0.5,
        transform=ax.transData, clip_on=False)
    ax.add_patch(glow)

    # Horizontal highlight line on row HIGHLIGHT_ROW of W
    glow_row = mpatches.FancyBboxPatch(
        (x_W - 0.008,
         mat_top - HIGHLIGHT_ROW * cell_h - 0.005),
        cols_W * cell_w * 0.92 + 0.016, cell_h * 0.88 + 0.01,
        boxstyle='round,pad=0.01',
        facecolor='none', edgecolor=BLUE, linewidth=2.2, alpha=0.6,
        transform=ax.transData, clip_on=False)
    ax.add_patch(glow_row)

    # ------------------------------------------------------------------
    # Matrix labels
    # ------------------------------------------------------------------
    label_y = mat_top + cell_h * 0.88 + 0.06
    lbl_cx_W = x_W + cols_W * cell_w * 0.92 / 2
    lbl_cx_x = x_x + cols_x * cell_w * 0.92 / 2
    lbl_cx_y = x_y + cols_y * cell_w * 0.92 / 2

    ax.text(lbl_cx_W, label_y, 'Weight Matrix  W',
            ha='center', va='bottom', fontsize=18,
            fontweight='bold', color=BLUE)
    ax.text(lbl_cx_x, label_y, 'Input  x',
            ha='center', va='bottom', fontsize=18,
            fontweight='bold', color=GREEN)
    ax.text(lbl_cx_y, label_y, 'Output  y',
            ha='center', va='bottom', fontsize=18,
            fontweight='bold', color=YELLOW)

    # Dimensions
    ax.text(lbl_cx_W, label_y - 0.04, '(3 \u00d7 3)',
            ha='center', va='top', fontsize=12, color=MUTED)
    ax.text(lbl_cx_x, label_y - 0.04, '(3 \u00d7 1)',
            ha='center', va='top', fontsize=12, color=MUTED)
    ax.text(lbl_cx_y, label_y - 0.04, '(3 \u00d7 1)',
            ha='center', va='top', fontsize=12, color=MUTED)

    # ------------------------------------------------------------------
    # Right-side annotation panel
    # ------------------------------------------------------------------
    rx = x_y + cols_y * cell_w * 0.92 + 0.10
    ry = 0.80

    ax.text(rx, ry, 'How It Works', ha='left', va='top',
            fontsize=18, fontweight='bold', color=TEXT)

    steps = [
        (BLUE,   'Highlighted row of W',
                 'The second row  [0.20,  0.90,  -0.40]\n'
                 'represents one neuron\'s weights.'),
        (GREEN,  'Input column x',
                 'The vector  [1.20,  -0.80,  0.50]\n'
                 'is the data flowing into the layer.'),
        (ORANGE, 'Dot product',
                 '0.20\u00d71.20 + 0.90\u00d7(\u22120.80) + (\u22120.40)\u00d70.50\n'
                 f'= {y[HIGHLIGHT_ROW,0]:+.3f}'),
        (YELLOW, 'Result cell y\u2082',
                 'One number  \u2014  the activation of\n'
                 'that single neuron.'),
    ]

    sy = ry - 0.08
    for color, heading, body in steps:
        ax.add_patch(mpatches.FancyBboxPatch(
            (rx - 0.01, sy - 0.07), 0.30, 0.10,
            boxstyle='round,pad=0.01',
            facecolor=color, alpha=0.12,
            edgecolor=color, linewidth=0.8,
            transform=ax.transData, clip_on=False))
        ax.text(rx + 0.005, sy - 0.005, heading, ha='left', va='top',
                fontsize=13, fontweight='bold', color=color)
        ax.text(rx + 0.005, sy - 0.032, body, ha='left', va='top',
                fontsize=10.5, color=MUTED, linespacing=1.4)
        sy -= 0.13

    # Key insight
    ax.add_patch(mpatches.FancyBboxPatch(
        (rx - 0.01, sy - 0.04), 0.30, 0.075,
        boxstyle='round,pad=0.01',
        facecolor='#0d2137', edgecolor=TEAL,
        linewidth=1.5,
        transform=ax.transData, clip_on=False))
    ax.text(rx + 0.14, sy + 0.0,
            'Each output neuron = one row\u2019s dot product.\n'
            'Three rows \u2192 three outputs\u2014done in parallel!',
            ha='center', va='top', fontsize=11,
            color=TEAL, linespacing=1.4)

    # ------------------------------------------------------------------
    # Main title
    # ------------------------------------------------------------------
    fig.text(0.5, 0.965,
             'Matrix Multiplication: The Engine of Every Neural Layer',
             ha='center', va='top', fontsize=24,
             fontweight='bold', color=TEXT)
    fig.text(0.5, 0.935,
             'y = W\u00b7x   \u2014   each output row is a dot product of one weight row with the input',
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
