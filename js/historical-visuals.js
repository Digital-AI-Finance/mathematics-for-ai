/**
 * historical-visuals.js
 * Mathematics for AI — Historical diagram recreations
 *
 * Renders three SVG visualizations:
 *   1. Nightingale's Rose (polar area / coxcomb chart) → #viz-nightingale
 *   2. Wald's Bomber Diagram (survivorship bias)       → #viz-wald
 *   3. Perceptron Schematic (Rosenblatt 1958)          → #viz-perceptron
 *
 * Dependencies: none (vanilla JS + inline SVG)
 * Site palette:
 *   primary   #1a237e   (dark blue)
 *   secondary #00897b   (teal)
 *   accent    #ff8f00   (amber)
 *   red       #e74c3c
 */

// ─── PALETTE ─────────────────────────────────────────────────────────────────
const COLORS = {
  primary:   '#1a237e',
  secondary: '#00897b',
  accent:    '#ff8f00',
  red:       '#e74c3c',
  disease:   '#00897b',   // teal/blue — preventable disease
  wounds:    '#e74c3c',   // red       — battle wounds
  other:     '#90a4ae',   // cool grey — other causes
  clean:     '#a5d6a7',   // soft green — Wald's unshot areas
  bg:        '#f5f7ff',   // very light blue-white
};

// ─── SVG HELPERS ─────────────────────────────────────────────────────────────

/**
 * Create an SVG element with given attributes.
 * @param {string} tag
 * @param {Object} attrs
 * @returns {SVGElement}
 */
function svgEl(tag, attrs = {}) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) {
    el.setAttribute(k, v);
  }
  return el;
}

/**
 * Polar to Cartesian conversion (angles start at top, go clockwise).
 * @param {number} cx   — centre x
 * @param {number} cy   — centre y
 * @param {number} r    — radius
 * @param {number} deg  — angle in degrees (0 = top)
 * @returns {{x: number, y: number}}
 */
function polarToCart(cx, cy, r, deg) {
  const rad = ((deg - 90) * Math.PI) / 180;
  return {
    x: cx + r * Math.cos(rad),
    y: cy + r * Math.sin(rad),
  };
}

/**
 * Build an SVG path string for a polar-area segment (pie wedge with given radius).
 */
function arcPath(cx, cy, r, startDeg, endDeg) {
  if (r < 1) r = 1; // ensure minimal visible arc
  const start = polarToCart(cx, cy, r, startDeg);
  const end   = polarToCart(cx, cy, r, endDeg);
  const large  = endDeg - startDeg > 180 ? 1 : 0;
  return [
    `M ${cx} ${cy}`,
    `L ${start.x} ${start.y}`,
    `A ${r} ${r} 0 ${large} 1 ${end.x} ${end.y}`,
    'Z',
  ].join(' ');
}

// ─────────────────────────────────────────────────────────────────────────────
// VISUAL 1: NIGHTINGALE'S ROSE
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Renders Florence Nightingale's polar-area "coxcomb" diagram.
 * @param {string} containerId
 */
function renderNightingaleRose(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  // ── Data (April 1854 → March 1855, 12 months) ──
  const months = [
    'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar'
  ];
  const disease = [1, 12, 11, 359, 828, 788, 503, 844, 1725, 2761, 2120, 1205];
  const wounds  = [0,  0,  0,   2,  11,  17,   7,   2,   37,  114,   83,   46];
  const other   = [5,  9,  7,  23,  30,  32,  28,  48,  122,  361,  172,   91];

  const n       = months.length;            // 12 segments
  const segDeg  = 360 / n;                  // 30° per month
  const maxVal  = Math.max(...disease);     // scale to disease maximum
  const W = 360, H = 420;
  const cx = W / 2, cy = (H - 70) / 2 + 10; // centre of rose
  const maxR = Math.min(cx, cy) - 20;        // max radius in px

  // scale: radius proportional to sqrt(value) for area perception
  const scale = (v) => maxR * Math.sqrt(v / maxVal);

  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`,
    width: '100%',
    'max-width': '360px',
    role: 'img',
    'aria-label': "Nightingale's Rose Diagram — causes of death in the Crimean War",
    style: 'display:block;margin:auto;',
  });

  // Background circle (aesthetic reference ring)
  svg.appendChild(svgEl('circle', {
    cx, cy, r: maxR,
    fill: COLORS.bg, stroke: '#cfd8dc', 'stroke-width': '1',
  }));

  // Draw three layers per segment (back → front: disease, other, wounds)
  for (let i = 0; i < n; i++) {
    const startDeg = i * segDeg - segDeg / 2;  // centre each wedge on its position
    const endDeg   = startDeg + segDeg;

    // Disease (largest, drawn first / underneath)
    svg.appendChild(svgEl('path', {
      d:       arcPath(cx, cy, scale(disease[i]), startDeg, endDeg),
      fill:    COLORS.disease,
      opacity: '0.80',
      stroke:  '#fff',
      'stroke-width': '0.8',
    }));

    // Other causes
    svg.appendChild(svgEl('path', {
      d:       arcPath(cx, cy, scale(other[i]), startDeg, endDeg),
      fill:    COLORS.other,
      opacity: '0.85',
      stroke:  '#fff',
      'stroke-width': '0.8',
    }));

    // Wounds (smallest, drawn on top)
    svg.appendChild(svgEl('path', {
      d:       arcPath(cx, cy, scale(wounds[i]), startDeg, endDeg),
      fill:    COLORS.wounds,
      opacity: '0.90',
      stroke:  '#fff',
      'stroke-width': '0.8',
    }));

    // Month label along the outer edge
    const labelAngle = i * segDeg;
    const labelR     = maxR + 14;
    const lp         = polarToCart(cx, cy, labelR, labelAngle);
    const label = svgEl('text', {
      x:           lp.x,
      y:           lp.y,
      'text-anchor':    'middle',
      'dominant-baseline': 'middle',
      'font-size': '9',
      'font-family': 'Inter, sans-serif',
      fill:        '#455a64',
    });
    label.textContent = months[i];
    svg.appendChild(label);
  }

  // Centre dot
  svg.appendChild(svgEl('circle', { cx, cy, r: '4', fill: '#455a64' }));

  // ── Legend ──────────────────────────────────────────────────────────────────
  const legendItems = [
    { color: COLORS.disease, label: 'Preventable Disease' },
    { color: COLORS.wounds,  label: 'Battle Wounds' },
    { color: COLORS.other,   label: 'Other Causes' },
  ];
  const legendY = cy + maxR + 28;
  const legendX = [30, 155, 265];

  legendItems.forEach((item, i) => {
    svg.appendChild(svgEl('rect', {
      x: legendX[i], y: legendY,
      width: '12', height: '12',
      fill:   item.color, rx: '2',
    }));
    const lt = svgEl('text', {
      x: legendX[i] + 16, y: legendY + 10,
      'font-size': '9', 'font-family': 'Inter, sans-serif',
      fill: '#37474f',
    });
    lt.textContent = item.label;
    svg.appendChild(lt);
  });

  // ── Caption ─────────────────────────────────────────────────────────────────
  const caption = svgEl('text', {
    x: cx, y: H - 12,
    'text-anchor': 'middle',
    'font-size': '9', 'font-family': 'Inter, sans-serif',
    'font-style': 'italic',
    fill: '#546e7a',
  });
  caption.textContent = 'Florence Nightingale, 1858 \u2014 Data visualization that changed history';
  svg.appendChild(caption);

  container.appendChild(svg);
}

// ─────────────────────────────────────────────────────────────────────────────
// VISUAL 2: WALD'S BOMBER DIAGRAM
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Renders a top-down bomber silhouette illustrating survivorship bias.
 * @param {string} containerId
 */
function renderWaldBomber(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const W = 520, H = 320;
  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`,
    width: '100%',
    role: 'img',
    'aria-label': "Wald's Bomber Diagram illustrating survivorship bias",
    style: 'display:block;margin:auto;',
  });

  const stroke = { stroke: COLORS.primary, 'stroke-width': '2', fill: 'none' };

  // ── Plane silhouette (top-down view) ─────────────────────────────────────
  // Fuselage: a long rounded rectangle centred horizontally
  const fx = 190, fy = 60, fw = 140, fh = 200;   // fuselage rect
  const fcx = fx + fw / 2;                         // fuselage centre x
  svg.appendChild(svgEl('rect', {
    x: fx, y: fy, width: fw, height: fh,
    rx: '30',
    fill: '#e8eaf6', stroke: COLORS.primary, 'stroke-width': '2',
  }));

  // Left wing: trapezoid
  const lwPath = `M ${fx} ${fy + 60} L ${fx - 110} ${fy + 90} L ${fx - 110} ${fy + 130} L ${fx} ${fy + 160} Z`;
  svg.appendChild(svgEl('path', {
    d: lwPath,
    fill: '#e8eaf6', stroke: COLORS.primary, 'stroke-width': '2',
  }));

  // Right wing: mirror
  const rwPath = `M ${fx + fw} ${fy + 60} L ${fx + fw + 110} ${fy + 90} L ${fx + fw + 110} ${fy + 130} L ${fx + fw} ${fy + 160} Z`;
  svg.appendChild(svgEl('path', {
    d: rwPath,
    fill: '#e8eaf6', stroke: COLORS.primary, 'stroke-width': '2',
  }));

  // Tail fins: small swept shapes
  const ltPath = `M ${fx + 15} ${fy + fh - 20} L ${fx - 30} ${fy + fh + 20} L ${fx + 10} ${fy + fh + 10} Z`;
  svg.appendChild(svgEl('path', { d: ltPath, fill: '#e8eaf6', stroke: COLORS.primary, 'stroke-width': '1.5' }));
  const rtPath = `M ${fx + fw - 15} ${fy + fh - 20} L ${fx + fw + 30} ${fy + fh + 20} L ${fx + fw - 10} ${fy + fh + 10} Z`;
  svg.appendChild(svgEl('path', { d: rtPath, fill: '#e8eaf6', stroke: COLORS.primary, 'stroke-width': '1.5' }));

  // Engine pods (on each wing)
  const engineY = fy + 100;
  [fx - 70, fx - 40, fx + fw + 30, fx + fw + 60].forEach(ex => {
    svg.appendChild(svgEl('ellipse', {
      cx: ex, cy: engineY, rx: '14', ry: '8',
      fill: COLORS.clean, stroke: COLORS.primary, 'stroke-width': '1.5',
    }));
  });

  // Cockpit highlight (front of fuselage, green = Wald's target)
  svg.appendChild(svgEl('ellipse', {
    cx: fcx, cy: fy + 35, rx: '28', ry: '20',
    fill: COLORS.clean, 'fill-opacity': '0.55',
    stroke: '#388e3c', 'stroke-width': '1.5', 'stroke-dasharray': '4 2',
  }));

  // ── Bullet holes (red dots on wings & fuselage mid-section) ──────────────
  // Holes are placed on wings and mid-fuselage; cockpit & engines are CLEAR.
  const holes = [
    // Left wing cluster
    { x: fx - 90, y: fy + 95 },
    { x: fx - 80, y: fy + 108 },
    { x: fx - 65, y: fy + 100 },
    { x: fx - 55, y: fy + 118 },
    { x: fx - 45, y: fy + 105 },
    { x: fx - 75, y: fy + 128 },
    // Right wing cluster
    { x: fx + fw + 50, y: fy + 95 },
    { x: fx + fw + 75, y: fy + 108 },
    { x: fx + fw + 60, y: fy + 115 },
    { x: fx + fw + 85, y: fy + 100 },
    { x: fx + fw + 40, y: fy + 122 },
    { x: fx + fw + 70, y: fy + 128 },
    // Fuselage mid-section
    { x: fcx - 25, y: fy + 100 },
    { x: fcx + 15, y: fy + 115 },
    { x: fcx - 10, y: fy + 130 },
    { x: fcx + 30, y: fy + 105 },
    { x: fcx - 35, y: fy + 145 },
    { x: fcx + 5,  y: fy + 155 },
  ];

  holes.forEach(h => {
    svg.appendChild(svgEl('circle', {
      cx: h.x, cy: h.y, r: '4',
      fill: COLORS.red, 'fill-opacity': '0.85',
      stroke: '#b71c1c', 'stroke-width': '0.8',
    }));
  });

  // ── Annotation arrows & labels ────────────────────────────────────────────
  // Arrow: generals (pointing to wing holes)
  const arrStyle = {
    stroke: '#37474f', 'stroke-width': '1.5',
    fill: 'none', 'marker-end': 'url(#arrowhead)',
  };

  // Define arrowhead marker
  const defs = svgEl('defs', {});
  const marker = svgEl('marker', {
    id: 'arrowhead', markerWidth: '8', markerHeight: '6',
    refX: '6', refY: '3', orient: 'auto',
  });
  marker.appendChild(svgEl('polygon', {
    points: '0 0, 8 3, 0 6',
    fill: '#37474f',
  }));
  defs.appendChild(marker);
  svg.insertBefore(defs, svg.firstChild);

  // Generals' arrow: from top-left label down to left-wing hole cluster
  svg.appendChild(svgEl('line', {
    x1: '65', y1: '38', x2: fx - 72, y2: fy + 96,
    ...arrStyle,
  }));
  const genBox = svgEl('text', {
    x: '5', y: '28',
    'font-size': '10', 'font-family': 'Inter, sans-serif',
    fill: '#b71c1c', 'font-weight': '600',
  });
  genBox.textContent = 'Generals: \u201CArmore here!\u201D';
  svg.appendChild(genBox);
  const genSub = svgEl('text', {
    x: '5', y: '40',
    'font-size': '9', 'font-family': 'Inter, sans-serif',
    fill: '#546e7a', 'font-style': 'italic',
  });
  genSub.textContent = '(where the holes are)';
  svg.appendChild(genSub);

  // Wald's arrow: from bottom-right label up to cockpit/engine area
  svg.appendChild(svgEl('line', {
    x1: '395', y1: '278', x2: fcx + 28, y2: fy + 50,
    ...arrStyle,
  }));
  const waldBox = svgEl('text', {
    x: '320', y: '292',
    'font-size': '10', 'font-family': 'Inter, sans-serif',
    fill: '#2e7d32', 'font-weight': '600',
  });
  waldBox.textContent = 'Wald: \u201CArmore HERE!\u201D';
  svg.appendChild(waldBox);
  const waldSub = svgEl('text', {
    x: '310', y: '305',
    'font-size': '9', 'font-family': 'Inter, sans-serif',
    fill: '#546e7a', 'font-style': 'italic',
  });
  waldSub.textContent = '(planes hit here didn\u2019t come back)';
  svg.appendChild(waldSub);

  // Caption at bottom
  const caption = svgEl('text', {
    x: W / 2, y: H - 4,
    'text-anchor': 'middle',
    'font-size': '8.5', 'font-family': 'Inter, sans-serif',
    'font-style': 'italic', fill: '#546e7a',
  });
  caption.textContent = 'Abraham Wald, 1943 \u2014 Survivorship Bias: the missing holes matter most';
  svg.appendChild(caption);

  container.appendChild(svg);
}

// ─────────────────────────────────────────────────────────────────────────────
// VISUAL 3: PERCEPTRON SCHEMATIC
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Renders Rosenblatt's Perceptron diagram with animated signal flow.
 * @param {string} containerId
 */
function renderPerceptron(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const W = 520, H = 270;
  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`,
    width: '100%',
    role: 'img',
    'aria-label': "Rosenblatt's Perceptron diagram, 1958",
    style: 'display:block;margin:auto;',
  });

  // ── Layout constants ───────────────────────────────────────────────────────
  const inputX  = 70;
  const sumX    = 230;
  const threshX = 350;
  const outX    = 465;
  const inputYs = [75, 140, 205];    // y-positions for the 3 inputs
  const sumY    = 140;
  const outY    = 140;
  const nodeR   = 22;
  const smallR  = 16;

  // ── Defs: arrowhead + glow filter ─────────────────────────────────────────
  const defs = svgEl('defs', {});

  const arrowMark = svgEl('marker', {
    id: 'arr-p', markerWidth: '8', markerHeight: '6',
    refX: '6', refY: '3', orient: 'auto',
  });
  arrowMark.appendChild(svgEl('polygon', {
    points: '0 0, 8 3, 0 6', fill: '#37474f',
  }));
  defs.appendChild(arrowMark);

  // Animated glow marker (amber)
  const arrActive = svgEl('marker', {
    id: 'arr-active', markerWidth: '8', markerHeight: '6',
    refX: '6', refY: '3', orient: 'auto',
  });
  arrActive.appendChild(svgEl('polygon', {
    points: '0 0, 8 3, 0 6', fill: COLORS.accent,
  }));
  defs.appendChild(arrActive);

  svg.appendChild(defs);

  // ── Background ─────────────────────────────────────────────────────────────
  svg.appendChild(svgEl('rect', {
    x: 0, y: 0, width: W, height: H,
    fill: COLORS.bg, rx: '8',
  }));

  // ── Draw connection arrows (base state, grey) ──────────────────────────────
  // Group ids for animation
  const connGroup = svgEl('g', { id: 'perc-connections' });

  // Input → sum arrows
  inputYs.forEach((iy, idx) => {
    const line = svgEl('line', {
      id:  `perc-line-${idx}`,
      x1:  inputX + nodeR, y1: iy,
      x2:  sumX - nodeR,   y2: sumY,
      stroke: '#90a4ae', 'stroke-width': '2',
      'marker-end': 'url(#arr-p)',
    });
    connGroup.appendChild(line);

    // Weight label on each connection
    const midX = (inputX + nodeR + sumX - nodeR) / 2;
    const midY = (iy + sumY) / 2 - 10;
    const wLabel = svgEl('text', {
      id:   `perc-w-${idx}`,
      x:    midX, y: midY,
      'text-anchor': 'middle',
      'font-size': '12', 'font-family': 'Inter, sans-serif',
      fill: COLORS.accent, 'font-weight': '700',
    });
    wLabel.textContent = ['w\u2081', 'w\u2082', 'w\u2083'][idx];
    connGroup.appendChild(wLabel);
  });

  // Sum → Threshold arrow
  connGroup.appendChild(svgEl('line', {
    id: 'perc-line-3',
    x1: sumX + nodeR, y1: sumY,
    x2: threshX - 4,  y2: outY,
    stroke: '#90a4ae', 'stroke-width': '2',
    'marker-end': 'url(#arr-p)',
  }));

  // Threshold → Output arrow
  connGroup.appendChild(svgEl('line', {
    id: 'perc-line-4',
    x1: threshX + 46, y1: outY,
    x2: outX - nodeR - 2, y2: outY,
    stroke: '#90a4ae', 'stroke-width': '2',
    'marker-end': 'url(#arr-p)',
  }));

  svg.appendChild(connGroup);

  // ── Input nodes ────────────────────────────────────────────────────────────
  const inputLabels = ['x\u2081', 'x\u2082', 'x\u2083'];
  inputYs.forEach((iy, idx) => {
    svg.appendChild(svgEl('circle', {
      id:    `perc-in-${idx}`,
      cx:    inputX, cy: iy, r: nodeR,
      fill:  COLORS.primary, stroke: '#fff', 'stroke-width': '2',
    }));
    const lbl = svgEl('text', {
      x: inputX, y: iy + 5,
      'text-anchor': 'middle',
      'font-size': '14', 'font-family': 'Inter, sans-serif',
      fill: '#fff', 'font-weight': '600',
    });
    lbl.textContent = inputLabels[idx];
    svg.appendChild(lbl);
  });

  // ── Summation node ─────────────────────────────────────────────────────────
  svg.appendChild(svgEl('circle', {
    id:   'perc-sum',
    cx:   sumX, cy: sumY, r: nodeR,
    fill: COLORS.secondary, stroke: '#fff', 'stroke-width': '2',
  }));
  const sigmaLbl = svgEl('text', {
    x: sumX, y: sumY + 6,
    'text-anchor': 'middle',
    'font-size': '18', 'font-family': 'Inter, sans-serif',
    fill: '#fff', 'font-weight': '700',
  });
  sigmaLbl.textContent = '\u03A3';
  svg.appendChild(sigmaLbl);

  // ── Threshold box (step function) ─────────────────────────────────────────
  const thw = 46, thh = 36;
  svg.appendChild(svgEl('rect', {
    id:   'perc-thresh',
    x:    threshX, y: outY - thh / 2,
    width: thw, height: thh,
    fill: '#5c6bc0', stroke: '#fff', 'stroke-width': '2', rx: '6',
  }));
  // Step-function mini-icon inside
  const stepPath = `M ${threshX + 6} ${outY + 8} L ${threshX + 18} ${outY + 8} L ${threshX + 18} ${outY - 8} L ${threshX + 40} ${outY - 8}`;
  svg.appendChild(svgEl('path', {
    d: stepPath,
    stroke: '#fff', 'stroke-width': '2', fill: 'none',
    'stroke-linecap': 'round', 'stroke-linejoin': 'round',
  }));

  // ── Output node ────────────────────────────────────────────────────────────
  svg.appendChild(svgEl('circle', {
    id:   'perc-out',
    cx:   outX, cy: outY, r: smallR,
    fill: COLORS.secondary, stroke: '#fff', 'stroke-width': '2',
  }));
  const outLbl = svgEl('text', {
    x: outX, y: outY + 5,
    'text-anchor': 'middle',
    'font-size': '11', 'font-family': 'Inter, sans-serif',
    fill: '#fff', 'font-weight': '700',
  });
  outLbl.textContent = '0|1';
  svg.appendChild(outLbl);

  // ── Node labels below each element ────────────────────────────────────────
  const labels = [
    { x: inputX,  y: inputYs[2] + nodeR + 14, text: 'Inputs' },
    { x: sumX,    y: sumY + nodeR + 14,        text: 'Weighted sum' },
    { x: threshX + thw / 2, y: outY + thh / 2 + 14, text: 'Threshold' },
    { x: outX,    y: outY + smallR + 14,       text: 'Output' },
  ];
  labels.forEach(lb => {
    const t = svgEl('text', {
      x: lb.x, y: lb.y,
      'text-anchor': 'middle',
      'font-size': '9', 'font-family': 'Inter, sans-serif',
      fill: '#546e7a',
    });
    t.textContent = lb.text;
    svg.appendChild(t);
  });

  // ── Caption ────────────────────────────────────────────────────────────────
  const caption = svgEl('text', {
    x: W / 2, y: H - 6,
    'text-anchor': 'middle',
    'font-size': '9', 'font-family': 'Inter, sans-serif',
    'font-style': 'italic', fill: '#546e7a',
  });
  caption.textContent = "Frank Rosenblatt\u2019s Perceptron, 1958 \u2014 \u201CNew Navy Device Learns by Doing\u201D";
  svg.appendChild(caption);

  container.appendChild(svg);

  // ── Scroll-triggered animation ────────────────────────────────────────────
  _animatePerceptronOnScroll(svg);
}

/**
 * Uses IntersectionObserver to fire the perceptron signal-flow animation
 * once when the SVG scrolls into view.
 * @param {SVGElement} svg
 */
function _animatePerceptronOnScroll(svg) {
  let animated = false;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !animated) {
          animated = true;
          _runPerceptronAnimation(svg);
          observer.disconnect();
        }
      });
    },
    { threshold: 0.4 }
  );

  observer.observe(svg);
}

/**
 * Animates the perceptron connections lighting up left-to-right.
 * Lines flash to amber; nodes briefly glow.
 * @param {SVGElement} svg
 */
function _runPerceptronAnimation(svg) {
  const activeColor  = COLORS.accent;
  const defaultColor = '#90a4ae';
  const delay        = 350;  // ms between stages

  // Stage order: [input lines 0,1,2 simultaneously] → sum → threshold → output
  const stages = [
    {
      lines:  ['perc-line-0', 'perc-line-1', 'perc-line-2'],
      nodes:  ['perc-in-0', 'perc-in-1', 'perc-in-2'],
      delayMs: 0,
    },
    {
      lines:  ['perc-line-3'],
      nodes:  ['perc-sum'],
      delayMs: delay,
    },
    {
      lines:  ['perc-line-4'],
      nodes:  ['perc-thresh'],
      delayMs: delay * 2,
    },
    {
      lines:  [],
      nodes:  ['perc-out'],
      delayMs: delay * 3,
    },
  ];

  stages.forEach(stage => {
    // Light up
    setTimeout(() => {
      stage.lines.forEach(id => {
        const el = svg.querySelector(`#${id}`);
        if (el) {
          el.setAttribute('stroke', activeColor);
          el.setAttribute('stroke-width', '3');
          el.setAttribute('marker-end', 'url(#arr-active)');
        }
      });
      stage.nodes.forEach(id => {
        const el = svg.querySelector(`#${id}`);
        if (el) {
          el.style.filter = `drop-shadow(0 0 6px ${activeColor})`;
        }
      });
    }, stage.delayMs);

    // Dim back (after +600 ms)
    setTimeout(() => {
      stage.lines.forEach(id => {
        const el = svg.querySelector(`#${id}`);
        if (el) {
          el.setAttribute('stroke', defaultColor);
          el.setAttribute('stroke-width', '2');
          el.setAttribute('marker-end', 'url(#arr-p)');
        }
      });
      stage.nodes.forEach(id => {
        const el = svg.querySelector(`#${id}`);
        if (el) el.style.filter = '';
      });
    }, stage.delayMs + 600);
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// INIT — call all three renderers on DOMContentLoaded
// ─────────────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  renderNightingaleRose('viz-nightingale');
  renderWaldBomber('viz-wald');
  renderPerceptron('viz-perceptron');
});
