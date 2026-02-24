#!/usr/bin/env python3
"""
gen_08_optimizers.py
2D contour plot with three optimizer trajectories (SGD, Momentum, Adam)
on an elongated valley (Rosenbrock-like) function.
Output: ../images/08-optimizers.png (3840x2160, 4K)
"""
import os
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '08-optimizers.png')

BG = '#1b2631'; BLUE = '#3498db'; YELLOW = '#f1c40f'; GREEN = '#2ecc71'; TEAL = '#1abc9c'
ORANGE = '#e67e22'; RED = '#e74c3c'; TEXT = '#ecf0f1'; MUTED = '#95a5a6'


def rosenbrock(x, y, a=1.0, b=10.0):
    """Rosenbrock function: f(x,y) = (a-x)^2 + b*(y-x^2)^2"""
    return (a - x) ** 2 + b * (y - x ** 2) ** 2


def rosenbrock_grad(x, y, a=1.0, b=10.0):
    """Gradient of Rosenbrock function."""
    dfdx = -2 * (a - x) + b * 2 * (y - x ** 2) * (-2 * x)
    dfdy = b * 2 * (y - x ** 2)
    return np.array([dfdx, dfdy])


def simulate_sgd(x0, y0, lr=0.001, n_steps=300):
    """Vanilla SGD with small noise for realism."""
    path = [(x0, y0)]
    pos = np.array([x0, y0], dtype=float)
    rng = np.random.RandomState(42)
    for _ in range(n_steps):
        grad = rosenbrock_grad(pos[0], pos[1])
        noise = rng.randn(2) * 0.3
        pos = pos - lr * (grad + noise)
        pos = np.clip(pos, -2.0, 2.5)
        path.append((pos[0], pos[1]))
    return np.array(path)


def simulate_momentum(x0, y0, lr=0.001, mu=0.9, n_steps=200):
    """SGD with momentum."""
    path = [(x0, y0)]
    pos = np.array([x0, y0], dtype=float)
    vel = np.zeros(2)
    rng = np.random.RandomState(42)
    for _ in range(n_steps):
        grad = rosenbrock_grad(pos[0], pos[1])
        noise = rng.randn(2) * 0.1
        vel = mu * vel - lr * (grad + noise)
        pos = pos + vel
        pos = np.clip(pos, -2.0, 2.5)
        path.append((pos[0], pos[1]))
    return np.array(path)


def simulate_adam(x0, y0, lr=0.01, beta1=0.9, beta2=0.999, eps=1e-8,
                  n_steps=120):
    """Adam optimizer."""
    path = [(x0, y0)]
    pos = np.array([x0, y0], dtype=float)
    m = np.zeros(2)
    v = np.zeros(2)
    for t in range(1, n_steps + 1):
        grad = rosenbrock_grad(pos[0], pos[1])
        m = beta1 * m + (1 - beta1) * grad
        v = beta2 * v + (1 - beta2) * grad ** 2
        m_hat = m / (1 - beta1 ** t)
        v_hat = v / (1 - beta2 ** t)
        pos = pos - lr * m_hat / (np.sqrt(v_hat) + eps)
        pos = np.clip(pos, -2.0, 2.5)
        path.append((pos[0], pos[1]))
    return np.array(path)


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=BG)
    ax.set_facecolor(BG)

    # Contour plot of Rosenbrock function
    xg = np.linspace(-1.8, 2.2, 500)
    yg = np.linspace(-0.8, 3.5, 500)
    X, Y = np.meshgrid(xg, yg)
    Z = rosenbrock(X, Y)

    # Log-scale levels for better visualization
    levels = np.logspace(-1, 3.5, 30)
    ax.contourf(X, Y, Z, levels=levels, cmap='magma', alpha=0.55, zorder=0)
    ax.contour(X, Y, Z, levels=levels, colors=[MUTED], alpha=0.25,
               linewidths=0.6, zorder=1)

    # Starting point
    x0, y0 = -1.2, 2.5

    # Simulate trajectories
    path_sgd = simulate_sgd(x0, y0, lr=0.0008, n_steps=350)
    path_mom = simulate_momentum(x0, y0, lr=0.001, mu=0.85, n_steps=250)
    path_adam = simulate_adam(x0, y0, lr=0.008, n_steps=150)

    # Plot trajectories
    trajectories = [
        (path_sgd, RED, 'SGD (1951)', 1.8, 40),
        (path_mom, ORANGE, 'Momentum (1964)', 2.2, 25),
        (path_adam, GREEN, 'Adam (2014)', 2.8, 10),
    ]

    for path, color, label, lw, subsample in trajectories:
        # Subsample for cleaner lines
        idx = np.arange(0, len(path), max(1, subsample // 5))
        ax.plot(path[idx, 0], path[idx, 1], color=color, lw=lw,
                alpha=0.85, label=label, zorder=3)
        # Arrow markers along path for direction
        for j in range(0, len(idx) - 1, max(1, len(idx) // 8)):
            k = idx[j]
            k_next = min(k + subsample, len(path) - 1)
            dx = path[k_next, 0] - path[k, 0]
            dy = path[k_next, 1] - path[k, 1]
            if abs(dx) + abs(dy) > 0.01:
                ax.annotate('', xy=(path[k, 0] + dx * 0.5,
                                    path[k, 1] + dy * 0.5),
                            xytext=(path[k, 0], path[k, 1]),
                            arrowprops=dict(arrowstyle='->', color=color,
                                            lw=1.5),
                            zorder=4)

    # Start point
    ax.plot(x0, y0, 'o', color=TEXT, markersize=14, markeredgecolor='white',
            markeredgewidth=2, zorder=6)
    ax.text(x0 + 0.15, y0 + 0.2, 'Start', fontsize=16, color=TEXT,
            fontweight='bold', zorder=6)

    # Minimum star
    ax.plot(1.0, 1.0, '*', color=YELLOW, markersize=28,
            markeredgecolor='white', markeredgewidth=1.5, zorder=6)
    ax.text(1.0, 0.55, 'Minimum', fontsize=16, color=YELLOW,
            fontweight='bold', ha='center', zorder=6)

    # Legend
    legend = ax.legend(fontsize=20, loc='upper right', frameon=True,
                       fancybox=True, framealpha=0.7, edgecolor=MUTED,
                       labelcolor=TEXT)
    legend.get_frame().set_facecolor(BG)

    # Labels
    ax.set_xlabel('$w_1$', fontsize=22, color=TEXT, labelpad=10)
    ax.set_ylabel('$w_2$', fontsize=22, color=TEXT, labelpad=10)
    ax.tick_params(colors=MUTED, labelsize=16)

    # Title
    fig.suptitle('The Evolution of Optimizers',
                 fontsize=34, fontweight='bold', color=TEXT, y=0.97)
    fig.text(0.5, 0.91,
             'Finding the minimum of $f(w) = (1 - w_1)^2 + 10(w_2 - w_1^2)^2$',
             ha='center', fontsize=20, color=MUTED, style='italic')

    plt.tight_layout(rect=[0, 0.02, 1, 0.88])

    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f'Saved: {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()
