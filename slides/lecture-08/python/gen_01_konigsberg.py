"""
gen_01_konigsberg.py
Stylized map of Konigsberg with 7 bridges.
Four landmasses separated by the Pregel river, connected by 7 bridges.

Historical layout:
  A = Altstadt (north bank)
  D = Vorstadt (south bank)
  C = Kneiphof (island in the river)
  B = Lomse (east bank)
Bridges: A-C:2, D-C:2, B-C:1, A-B:1, D-B:1  (total 7)
Degrees: A=3, B=3, C=5, D=3  (all odd -> no Eulerian path)

Output: ../images/01-konigsberg-map.png (3840x2160, 4K)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'images', '01-konigsberg-map.png')
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG        = '#1b2631'
CARD_BG   = '#1e3044'
BLUE      = '#3498db'
YELLOW    = '#f1c40f'
GREEN     = '#2ecc71'
TEAL      = '#1abc9c'
ORANGE    = '#e67e22'
RED       = '#e74c3c'
PURPLE    = '#9b59b6'
TEXT      = '#ecf0f1'
MUTED     = '#95a5a6'

BRIDGE_COLORS = [ORANGE, YELLOW, GREEN, TEAL, BLUE, RED, PURPLE]

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(3840/200, 2160/200), dpi=200)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(-1.0, 13.0)
ax.set_ylim(-2.0, 9.5)
ax.set_aspect('equal')
ax.axis('off')

# ---------------------------------------------------------------------------
# River (Pregel) flowing left-to-right, splitting around island C
# ---------------------------------------------------------------------------
def draw_river_band(ax, ctrl_points, width=0.7, color=BLUE, alpha=0.22):
    """Draw a wide river as a thick bezier curve."""
    t = np.linspace(0, 1, 300)
    p0, p1, p2, p3 = ctrl_points
    curve = (
        (1-t)**3 * np.array(p0)[:, None]
        + 3*(1-t)**2*t * np.array(p1)[:, None]
        + 3*(1-t)*t**2 * np.array(p2)[:, None]
        + t**3 * np.array(p3)[:, None]
    )
    ax.plot(curve[0], curve[1], color=color, alpha=alpha, linewidth=width*40,
            solid_capstyle='round', zorder=1)
    ax.plot(curve[0], curve[1], color=color, alpha=alpha*0.5, linewidth=width*15,
            solid_capstyle='round', zorder=1)

# Upper branch (between A=north and C=island)
draw_river_band(ax, [(-2, 5.8), (3, 6.0), (8, 5.8), (14, 5.5)], width=0.75)
# Lower branch (between C=island and D=south)
draw_river_band(ax, [(-2, 2.8), (3, 2.6), (8, 2.8), (14, 3.0)], width=0.75)
# Left confluence
draw_river_band(ax, [(-2, 4.3), (0, 4.3), (0.5, 5.2), (-2, 5.8)], width=0.4)
draw_river_band(ax, [(-2, 4.3), (0, 4.3), (0.5, 3.4), (-2, 2.8)], width=0.4)
# Right side -- river merges then flows to B=east
draw_river_band(ax, [(14, 5.5), (11, 4.8), (11, 3.8), (14, 3.0)], width=0.45)

# ---------------------------------------------------------------------------
# Landmasses (rounded rectangles)
# ---------------------------------------------------------------------------
def draw_landmass(ax, xy, w, h, label, sublabel='', label_offset=(0, 0)):
    """Draw a rounded rectangle landmass with labels."""
    rx, ry = xy
    rr = mpatches.FancyBboxPatch(
        (rx, ry), w, h,
        boxstyle=mpatches.BoxStyle.Round(pad=0.3),
        facecolor=CARD_BG, edgecolor=MUTED, linewidth=2, zorder=3
    )
    ax.add_patch(rr)
    cx = rx + w / 2 + label_offset[0]
    cy = ry + h / 2 + label_offset[1]
    ax.text(cx, cy, label, fontsize=30, fontweight='bold', color=TEXT,
            ha='center', va='center', zorder=5,
            path_effects=[pe.withStroke(linewidth=4, foreground=BG)])
    if sublabel:
        ax.text(cx, cy - 0.55, sublabel, fontsize=11, color=MUTED,
                ha='center', va='center', zorder=5, style='italic')

# A: north bank (wide, across top)
draw_landmass(ax, (0.5, 6.5), 8.0, 1.8, 'A', 'Altstadt (north)')
# D: south bank (wide, across bottom)
draw_landmass(ax, (0.5, 0.2), 8.0, 1.8, 'D', 'Vorstadt (south)')
# C: island in center
draw_landmass(ax, (2.5, 3.3), 5.0, 2.0, 'C', 'Kneiphof (island)')
# B: east bank (right side, tall)
draw_landmass(ax, (9.5, 1.5), 2.8, 5.5, 'B', 'Lomse (east)', label_offset=(0, 0.5))

# ---------------------------------------------------------------------------
# Bridges
# ---------------------------------------------------------------------------
# Historical 7 bridges:
#   A-C: 2 (north bank to island)
#   D-C: 2 (south bank to island)
#   B-C: 1 (east bank to island)
#   A-B: 1 (north bank to east bank)
#   D-B: 1 (south bank to east bank)
bridges = [
    # Bridge 1: A-C (left bridge, north to island)
    {'from': (3.2, 6.5), 'to': (3.8, 5.3), 'color': BRIDGE_COLORS[0], 'label': '1'},
    # Bridge 2: A-C (right bridge, north to island)
    {'from': (5.8, 6.5), 'to': (5.5, 5.3), 'color': BRIDGE_COLORS[1], 'label': '2'},
    # Bridge 3: D-C (left bridge, south to island)
    {'from': (3.5, 2.0), 'to': (3.8, 3.3), 'color': BRIDGE_COLORS[2], 'label': '3'},
    # Bridge 4: D-C (right bridge, south to island)
    {'from': (6.0, 2.0), 'to': (5.8, 3.3), 'color': BRIDGE_COLORS[3], 'label': '4'},
    # Bridge 5: B-C (east bank to island)
    {'from': (9.5, 4.3), 'to': (7.5, 4.3), 'color': BRIDGE_COLORS[4], 'label': '5'},
    # Bridge 6: A-B (north bank to east bank)
    {'from': (8.5, 6.5), 'to': (9.5, 5.8), 'color': BRIDGE_COLORS[5], 'label': '6'},
    # Bridge 7: D-B (south bank to east bank)
    {'from': (8.5, 2.0), 'to': (9.5, 2.8), 'color': BRIDGE_COLORS[6], 'label': '7'},
]

for b in bridges:
    x1, y1 = b['from']
    x2, y2 = b['to']
    color = b['color']

    # Draw bridge as a thick line with dark outline
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=8, solid_capstyle='round',
            zorder=4, alpha=0.9,
            path_effects=[pe.withStroke(linewidth=13, foreground=BG)])

    # Bridge number label at midpoint
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mx, my, b['label'], fontsize=14, fontweight='bold', color=TEXT,
            ha='center', va='center', zorder=6,
            bbox=dict(boxstyle='round,pad=0.2', facecolor=color, edgecolor='none', alpha=0.85))

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
ax.set_title('The Seven Bridges of K\u00f6nigsberg (1736)',
             fontsize=34, fontweight='bold', color=TEXT, pad=20)

# Subtitle
ax.text(6.0, -1.3,
        'Can you cross every bridge exactly once and return to the start?',
        fontsize=17, color=MUTED, ha='center', va='center', style='italic')

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.close()
print(f'Saved: {OUTPUT_PATH}')
