#!/usr/bin/env python3
"""
gen_05_gradient_descent.py
3D surface plot showing gradient descent on a loss landscape with trajectory.
Output: ../images/05-gradient-descent.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '05-gradient-descent.png')

BG      = '#1b2631'
BLUE    = '#3498db'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
TEAL    = '#1abc9c'
ORANGE  = '#e67e22'
RED     = '#e74c3c'
TEXT    = '#ecf0f1'
MUTED   = '#95a5a6'


def loss_fn(x, y):
    """A smooth bowl with a slight twist for visual interest.
    Combination of quadratic bowl + slight asymmetry."""
    return 0.6 * x ** 2 + 0.9 * y ** 2 + 0.3 * x * y + 0.15 * np.sin(2 * x) * np.cos(2 * y)


def grad_fn(x, y):
    """Numerical gradient of loss_fn."""
    h = 1e-5
    dfdx = (loss_fn(x + h, y) - loss_fn(x - h, y)) / (2 * h)
    dfdy = (loss_fn(x, y + h) - loss_fn(x, y - h)) / (2 * h)
    return dfdx, dfdy


def simulate_gradient_descent(x0, y0, lr=0.12, n_steps=20):
    """Run gradient descent and return trajectory."""
    path = [(x0, y0, loss_fn(x0, y0))]
    x, y = x0, y0
    for _ in range(n_steps):
        dx, dy = grad_fn(x, y)
        x -= lr * dx
        y -= lr * dy
        path.append((x, y, loss_fn(x, y)))
    return np.array(path)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=BG)

    # Surface mesh
    grid = np.linspace(-3, 3, 150)
    X, Y = np.meshgrid(grid, grid)
    Z = loss_fn(X, Y)

    # Custom colormap: deep blue -> teal -> surface color
    colors_list = ['#0d1b2a', '#1b3a4b', '#1abc9c', '#2ecc71', '#f1c40f']
    cmap = LinearSegmentedColormap.from_list('loss_cmap', colors_list, N=256)

    # Plot surface
    ax.plot_surface(X, Y, Z, cmap=cmap, alpha=0.55, edgecolor='none',
                    rstride=3, cstride=3, zorder=1, antialiased=True)

    # Wireframe for depth cues
    ax.plot_wireframe(X, Y, Z, color=MUTED, alpha=0.06, rstride=8,
                      cstride=8, linewidth=0.4, zorder=2)

    # Gradient descent trajectory
    path = simulate_gradient_descent(x0=2.5, y0=2.2, lr=0.12, n_steps=18)
    n_pts = len(path)

    # Color gradient: red (high loss) -> yellow (mid) -> green (low loss)
    traj_colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71']
    traj_cmap = LinearSegmentedColormap.from_list('traj', traj_colors, N=n_pts)

    # Plot trajectory line segments
    for i in range(n_pts - 1):
        t = i / (n_pts - 1)
        color = traj_cmap(t)
        ax.plot(path[i:i+2, 0], path[i:i+2, 1], path[i:i+2, 2] + 0.15,
                color=color, linewidth=2.5, zorder=5)

    # Plot trajectory dots
    for i in range(n_pts):
        t = i / (n_pts - 1)
        color = traj_cmap(t)
        size = 60 if i in (0, n_pts - 1) else 30
        ax.scatter(path[i, 0], path[i, 1], path[i, 2] + 0.15,
                   color=color, s=size, edgecolors='white',
                   linewidths=0.8, zorder=6, depthshade=False)

    # Annotations
    ax.text(path[0, 0], path[0, 1], path[0, 2] + 1.2,
            'Start:\nHigh Loss', fontsize=11, fontweight='bold',
            color=RED, ha='center', va='bottom', zorder=7)

    ax.text(path[-1, 0] + 0.5, path[-1, 1] + 0.5, path[-1, 2] + 0.6,
            'Minimum:\nLow Loss', fontsize=11, fontweight='bold',
            color=GREEN, ha='center', va='bottom', zorder=7)

    # Step-size annotation near middle of path
    mid = n_pts // 2
    ax.text(path[mid, 0] - 1.5, path[mid, 1], path[mid, 2] + 1.5,
            r'$\theta_{t+1} = \theta_t - \eta \nabla L$',
            fontsize=12, color=YELLOW, ha='center', va='center', zorder=7)

    # Axis styling
    ax.set_xlabel('Parameter 1', fontsize=11, color=MUTED, labelpad=8)
    ax.set_ylabel('Parameter 2', fontsize=11, color=MUTED, labelpad=8)
    ax.set_zlabel('Loss', fontsize=11, color=MUTED, labelpad=8)
    ax.tick_params(colors=MUTED, labelsize=8)

    # Pane colors
    ax.xaxis.pane.set_facecolor(BG)
    ax.yaxis.pane.set_facecolor(BG)
    ax.zaxis.pane.set_facecolor(BG)
    ax.xaxis.pane.set_edgecolor(MUTED)
    ax.yaxis.pane.set_edgecolor(MUTED)
    ax.zaxis.pane.set_edgecolor(MUTED)
    ax.xaxis.pane.set_alpha(0.3)
    ax.yaxis.pane.set_alpha(0.3)
    ax.zaxis.pane.set_alpha(0.3)

    # Grid lines
    ax.xaxis._axinfo['grid']['color'] = MUTED
    ax.yaxis._axinfo['grid']['color'] = MUTED
    ax.zaxis._axinfo['grid']['color'] = MUTED
    ax.xaxis._axinfo['grid']['linewidth'] = 0.3
    ax.yaxis._axinfo['grid']['linewidth'] = 0.3
    ax.zaxis._axinfo['grid']['linewidth'] = 0.3

    # Viewing angle
    ax.view_init(elev=28, azim=-55)

    # Title and subtitle via figure text
    fig.text(0.5, 0.95, 'Gradient Descent: How AI Learns',
             fontsize=26, fontweight='bold', color=TEXT,
             ha='center', va='center', family='sans-serif')
    fig.text(0.5, 0.91, 'Follow the slope downhill, step by step',
             fontsize=14, fontstyle='italic', color=MUTED,
             ha='center', va='center', family='sans-serif')

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
