/**
 * visualizations.js
 * Mathematics for AI -- Interactive SVG/Canvas data visualizations
 *
 * Seven self-contained visualizations that render into container elements
 * found by ID. Each checks for its container before rendering (graceful
 * degradation). Uses the site palette:
 *   primary   #1a237e
 *   secondary #00897b
 *   accent    #ff8f00
 *   red       #e74c3c
 *   surface   #ffffff
 *   math-bg   #e8eaf6
 */

/* =========================================================================
   HELPERS
   ========================================================================= */

const VIZ_COLORS = {
  primary:   '#1a237e',
  secondary: '#00897b',
  accent:    '#ff8f00',
  red:       '#e74c3c',
  surface:   '#ffffff',
  mathBg:    '#e8eaf6',
  gold:      '#FFD700',
  textLight: '#616161',
  text:      '#212121',
  border:    '#e0e0e0',
};

/** Create an SVG element with the given tag and attributes. */
function svgEl(tag, attrs) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  if (attrs) {
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
  }
  return el;
}

/** Sigmoid function. */
function sigmoid(x) {
  return 1 / (1 + Math.exp(-x));
}

/** Normal PDF, mu=0, sigma=1. */
function normalPDF(x) {
  return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI);
}

/** Clamp value between min and max. */
function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(hi, v));
}

/** Check for reduced-motion preference. */
function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}


/* =========================================================================
   1. SIGMOID S-CURVE  (#viz-sigmoid)
   ========================================================================= */

function renderSigmoid(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const W = 400, H = 300;
  const pad = { top: 20, right: 30, bottom: 40, left: 55 };
  const plotW = W - pad.left - pad.right;
  const plotH = H - pad.top - pad.bottom;

  const xMin = -6, xMax = 6, yMin = 0, yMax = 1;

  function toSVGX(x) { return pad.left + ((x - xMin) / (xMax - xMin)) * plotW; }
  function toSVGY(y) { return pad.top + (1 - (y - yMin) / (yMax - yMin)) * plotH; }
  function fromSVGX(sx) { return xMin + ((sx - pad.left) / plotW) * (xMax - xMin); }

  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`,
    width: '100%',
    style: 'max-width:400px;display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;',
    role: 'img',
    'aria-label': 'Sigmoid S-curve visualization showing how the sigmoid function maps inputs to probabilities between 0 and 1',
  });

  // Background
  svg.appendChild(svgEl('rect', {
    x: 0, y: 0, width: W, height: H, fill: VIZ_COLORS.surface, rx: 8,
  }));

  // Plot area background
  svg.appendChild(svgEl('rect', {
    x: pad.left, y: pad.top, width: plotW, height: plotH,
    fill: VIZ_COLORS.mathBg, rx: 4,
  }));

  // Grid lines
  [0, 0.25, 0.5, 0.75, 1].forEach(y => {
    svg.appendChild(svgEl('line', {
      x1: pad.left, y1: toSVGY(y), x2: pad.left + plotW, y2: toSVGY(y),
      stroke: VIZ_COLORS.border, 'stroke-width': 0.5,
    }));
  });
  [-4, -2, 0, 2, 4].forEach(x => {
    svg.appendChild(svgEl('line', {
      x1: toSVGX(x), y1: pad.top, x2: toSVGX(x), y2: pad.top + plotH,
      stroke: VIZ_COLORS.border, 'stroke-width': 0.5,
    }));
  });

  // Axes
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: pad.top + plotH, x2: pad.left + plotW, y2: pad.top + plotH,
    stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: pad.top, x2: pad.left, y2: pad.top + plotH,
    stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));

  // Axis labels
  const xLabel = svgEl('text', {
    x: pad.left + plotW / 2, y: H - 4, 'text-anchor': 'middle',
    fill: VIZ_COLORS.textLight, 'font-size': '11',
  });
  xLabel.textContent = 'Input Score';
  svg.appendChild(xLabel);

  const yLabel = svgEl('text', {
    x: 12, y: pad.top + plotH / 2, 'text-anchor': 'middle',
    fill: VIZ_COLORS.textLight, 'font-size': '11',
    transform: `rotate(-90, 12, ${pad.top + plotH / 2})`,
  });
  yLabel.textContent = 'Probability';
  svg.appendChild(yLabel);

  // Tick labels
  [-4, -2, 0, 2, 4].forEach(x => {
    const t = svgEl('text', {
      x: toSVGX(x), y: pad.top + plotH + 14, 'text-anchor': 'middle',
      fill: VIZ_COLORS.textLight, 'font-size': '9',
    });
    t.textContent = x;
    svg.appendChild(t);
  });
  [0, 0.25, 0.5, 0.75, 1].forEach(y => {
    const t = svgEl('text', {
      x: pad.left - 6, y: toSVGY(y) + 3, 'text-anchor': 'end',
      fill: VIZ_COLORS.textLight, 'font-size': '9',
    });
    t.textContent = y.toFixed(2);
    svg.appendChild(t);
  });

  // Decision boundary at y=0.5
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: toSVGY(0.5), x2: pad.left + plotW, y2: toSVGY(0.5),
    stroke: VIZ_COLORS.accent, 'stroke-width': 1.5, 'stroke-dasharray': '6,3',
  }));
  const dbLabel = svgEl('text', {
    x: pad.left + plotW - 2, y: toSVGY(0.5) - 5, 'text-anchor': 'end',
    fill: VIZ_COLORS.accent, 'font-size': '9', 'font-weight': '600',
  });
  dbLabel.textContent = 'Decision Boundary';
  svg.appendChild(dbLabel);

  // Dotted line at y=0.73
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: toSVGY(0.73), x2: pad.left + plotW, y2: toSVGY(0.73),
    stroke: VIZ_COLORS.primary, 'stroke-width': 1, 'stroke-dasharray': '3,3', opacity: 0.5,
  }));

  // BankBot label at sigma(1.0) ~ 0.73
  const bbX = toSVGX(1.0), bbY = toSVGY(0.73);
  svg.appendChild(svgEl('circle', {
    cx: bbX, cy: bbY, r: 4, fill: VIZ_COLORS.primary,
  }));
  const bbText = svgEl('text', {
    x: bbX + 8, y: bbY - 8, fill: VIZ_COLORS.primary,
    'font-size': '8.5', 'font-weight': '600',
  });
  bbText.textContent = 'BankBot: 73% confident';
  svg.appendChild(bbText);

  // Sigmoid curve
  let pathD = '';
  const steps = 200;
  for (let i = 0; i <= steps; i++) {
    const x = xMin + (i / steps) * (xMax - xMin);
    const y = sigmoid(x);
    const sx = toSVGX(x), sy = toSVGY(y);
    pathD += (i === 0 ? 'M' : 'L') + sx.toFixed(1) + ',' + sy.toFixed(1);
  }
  svg.appendChild(svgEl('path', {
    d: pathD, fill: 'none', stroke: VIZ_COLORS.secondary,
    'stroke-width': 3, 'stroke-linecap': 'round',
  }));

  // Interactive dot
  const dot = svgEl('circle', {
    cx: toSVGX(0), cy: toSVGY(0.5), r: 6,
    fill: VIZ_COLORS.secondary, stroke: VIZ_COLORS.surface, 'stroke-width': 2,
    style: 'pointer-events:none;',
  });
  svg.appendChild(dot);

  const coordLabel = svgEl('text', {
    x: toSVGX(0) + 10, y: toSVGY(0.5) - 10,
    fill: VIZ_COLORS.text, 'font-size': '9', 'font-weight': '600',
    style: 'pointer-events:none;',
  });
  coordLabel.textContent = '(0.00, 0.50)';
  svg.appendChild(coordLabel);

  // Hover / touch interaction
  const hitArea = svgEl('rect', {
    x: pad.left, y: pad.top, width: plotW, height: plotH,
    fill: 'transparent', style: 'cursor:crosshair;',
  });
  svg.appendChild(hitArea);

  function updateDot(svgX) {
    const xVal = clamp(fromSVGX(svgX), xMin, xMax);
    const yVal = sigmoid(xVal);
    const cx = toSVGX(xVal), cy = toSVGY(yVal);
    dot.setAttribute('cx', cx);
    dot.setAttribute('cy', cy);
    const labelX = cx + 10 > pad.left + plotW - 60 ? cx - 70 : cx + 10;
    coordLabel.setAttribute('x', labelX);
    coordLabel.setAttribute('y', cy - 10);
    coordLabel.textContent = `(${xVal.toFixed(2)}, ${yVal.toFixed(2)})`;
  }

  function getSVGPoint(evt) {
    const pt = svg.createSVGPoint();
    const touch = evt.touches ? evt.touches[0] : evt;
    pt.x = touch.clientX;
    pt.y = touch.clientY;
    return pt.matrixTransform(svg.getScreenCTM().inverse());
  }

  hitArea.addEventListener('mousemove', (e) => updateDot(getSVGPoint(e).x));
  hitArea.addEventListener('touchmove', (e) => {
    e.preventDefault();
    updateDot(getSVGPoint(e).x);
  }, { passive: false });

  container.appendChild(svg);
}


/* =========================================================================
   2. BELL CURVE  (#viz-bellcurve)
   ========================================================================= */

function renderBellCurve(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const W = 500, H = 300;
  const pad = { top: 30, right: 30, bottom: 50, left: 50 };
  const plotW = W - pad.left - pad.right;
  const plotH = H - pad.top - pad.bottom;

  const xMin = -4.5, xMax = 4.5;
  const yMax = 0.45;

  function toX(x) { return pad.left + ((x - xMin) / (xMax - xMin)) * plotW; }
  function toY(y) { return pad.top + (1 - y / yMax) * plotH; }

  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`, width: '100%',
    style: 'max-width:500px;display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;',
    role: 'img',
    'aria-label': 'Bell curve showing normal distribution with shaded regions for normal spending, unusual activity, and fraud alerts',
  });

  svg.appendChild(svgEl('rect', { x: 0, y: 0, width: W, height: H, fill: VIZ_COLORS.surface, rx: 8 }));

  // Shaded regions -- build paths for each zone
  function areaPath(x1, x2) {
    let d = `M${toX(x1).toFixed(1)},${toY(0).toFixed(1)}`;
    const steps = 100;
    for (let i = 0; i <= steps; i++) {
      const x = x1 + (i / steps) * (x2 - x1);
      d += ` L${toX(x).toFixed(1)},${toY(normalPDF(x)).toFixed(1)}`;
    }
    d += ` L${toX(x2).toFixed(1)},${toY(0).toFixed(1)} Z`;
    return d;
  }

  // Beyond +/- 2 sigma (red - fraud zone)
  svg.appendChild(svgEl('path', { d: areaPath(xMin, -2), fill: 'rgba(231,76,60,0.18)' }));
  svg.appendChild(svgEl('path', { d: areaPath(2, xMax), fill: 'rgba(231,76,60,0.18)' }));

  // +/-1 to +/-2 sigma (amber - unusual)
  svg.appendChild(svgEl('path', { d: areaPath(-2, -1), fill: 'rgba(255,143,0,0.15)' }));
  svg.appendChild(svgEl('path', { d: areaPath(1, 2), fill: 'rgba(255,143,0,0.15)' }));

  // -1 to +1 sigma (teal - normal)
  svg.appendChild(svgEl('path', { d: areaPath(-1, 1), fill: 'rgba(0,137,123,0.18)' }));

  // The curve itself
  let curvePath = '';
  const steps = 300;
  for (let i = 0; i <= steps; i++) {
    const x = xMin + (i / steps) * (xMax - xMin);
    curvePath += (i === 0 ? 'M' : 'L') + toX(x).toFixed(1) + ',' + toY(normalPDF(x)).toFixed(1);
  }
  svg.appendChild(svgEl('path', {
    d: curvePath, fill: 'none', stroke: VIZ_COLORS.primary, 'stroke-width': 2.5,
  }));

  // Axes
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: toY(0), x2: pad.left + plotW, y2: toY(0),
    stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));

  // Sigma tick marks and labels
  [-3, -2, -1, 0, 1, 2, 3].forEach(s => {
    svg.appendChild(svgEl('line', {
      x1: toX(s), y1: toY(0), x2: toX(s), y2: toY(0) + 6,
      stroke: VIZ_COLORS.text, 'stroke-width': 1,
    }));
    const t = svgEl('text', {
      x: toX(s), y: toY(0) + 18, 'text-anchor': 'middle',
      fill: VIZ_COLORS.textLight, 'font-size': '9',
    });
    t.textContent = s === 0 ? '\u03BC' : (s > 0 ? `+${s}\u03C3` : `${s}\u03C3`);
    svg.appendChild(t);
  });

  // Zone labels
  const labelStyle = { 'text-anchor': 'middle', 'font-size': '9', 'font-weight': '600' };

  const normalLabel = svgEl('text', {
    x: toX(0), y: toY(normalPDF(0)) - 12, ...labelStyle, fill: VIZ_COLORS.secondary,
  });
  normalLabel.textContent = 'Normal Spending';
  svg.appendChild(normalLabel);

  [{ x: -1.5, text: 'Unusual' }, { x: 1.5, text: 'Unusual' }].forEach(({ x, text }) => {
    const l = svgEl('text', {
      x: toX(x), y: toY(normalPDF(x)) - 8, ...labelStyle, fill: VIZ_COLORS.accent,
    });
    l.textContent = text;
    svg.appendChild(l);
  });

  [{ x: -3.2 }, { x: 3.2 }].forEach(({ x }) => {
    const l = svgEl('text', {
      x: toX(x), y: toY(0) - 30, ...labelStyle, fill: VIZ_COLORS.red, 'font-size': '8',
    });
    l.textContent = 'Fraud Alert!';
    svg.appendChild(l);
  });

  // Mia's TV purchase at x=3.5
  const miaX = toX(3.5), miaY = toY(normalPDF(3.5));
  svg.appendChild(svgEl('line', {
    x1: miaX, y1: toY(0), x2: miaX, y2: miaY - 10,
    stroke: VIZ_COLORS.red, 'stroke-width': 1.5, 'stroke-dasharray': '4,2',
  }));
  svg.appendChild(svgEl('circle', {
    cx: miaX, cy: miaY - 10, r: 5, fill: VIZ_COLORS.red,
  }));
  const miaLabel = svgEl('text', {
    x: miaX - 8, y: miaY - 22, 'text-anchor': 'end',
    fill: VIZ_COLORS.red, 'font-size': '8', 'font-weight': '600',
  });
  miaLabel.textContent = "Mia's TV purchase in Lagos";
  svg.appendChild(miaLabel);

  // X-axis label
  const xLabel = svgEl('text', {
    x: pad.left + plotW / 2, y: H - 6, 'text-anchor': 'middle',
    fill: VIZ_COLORS.textLight, 'font-size': '11',
  });
  xLabel.textContent = 'Standard Deviations from Mean Spending';
  svg.appendChild(xLabel);

  container.appendChild(svg);
}


/* =========================================================================
   3. SCATTER PLOT WITH DECISION BOUNDARY  (#viz-scatter)
   ========================================================================= */

function renderScatter(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const W = 500, H = 350;
  const pad = { top: 20, right: 30, bottom: 45, left: 55 };
  const plotW = W - pad.left - pad.right;
  const plotH = H - pad.top - pad.bottom;

  // Data range
  const xRange = [0, 1000], yRange = [0, 500];

  function toX(v) { return pad.left + ((v - xRange[0]) / (xRange[1] - xRange[0])) * plotW; }
  function toY(v) { return pad.top + (1 - (v - yRange[0]) / (yRange[1] - yRange[0])) * plotH; }

  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`, width: '100%',
    style: 'max-width:500px;display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;',
    role: 'img',
    'aria-label': 'Scatter plot of transactions with green legitimate points, red fraud points, and an animated decision boundary line',
  });

  svg.appendChild(svgEl('rect', { x: 0, y: 0, width: W, height: H, fill: VIZ_COLORS.surface, rx: 8 }));
  svg.appendChild(svgEl('rect', { x: pad.left, y: pad.top, width: plotW, height: plotH, fill: VIZ_COLORS.mathBg, rx: 4 }));

  // Axes
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: pad.top + plotH, x2: pad.left + plotW, y2: pad.top + plotH,
    stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: pad.top, x2: pad.left, y2: pad.top + plotH,
    stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));

  // Axis labels
  const xLabel = svgEl('text', {
    x: pad.left + plotW / 2, y: H - 5, 'text-anchor': 'middle',
    fill: VIZ_COLORS.textLight, 'font-size': '11',
  });
  xLabel.textContent = 'Transaction Amount ($)';
  svg.appendChild(xLabel);

  const yLabel = svgEl('text', {
    x: 12, y: pad.top + plotH / 2, 'text-anchor': 'middle',
    fill: VIZ_COLORS.textLight, 'font-size': '11',
    transform: `rotate(-90, 12, ${pad.top + plotH / 2})`,
  });
  yLabel.textContent = 'Distance from Home (mi)';
  svg.appendChild(yLabel);

  // Tick labels
  [0, 250, 500, 750, 1000].forEach(v => {
    const t = svgEl('text', {
      x: toX(v), y: pad.top + plotH + 14, 'text-anchor': 'middle',
      fill: VIZ_COLORS.textLight, 'font-size': '8',
    });
    t.textContent = v;
    svg.appendChild(t);
  });
  [0, 100, 200, 300, 400, 500].forEach(v => {
    const t = svgEl('text', {
      x: pad.left - 6, y: toY(v) + 3, 'text-anchor': 'end',
      fill: VIZ_COLORS.textLight, 'font-size': '8',
    });
    t.textContent = v;
    svg.appendChild(t);
  });

  // Generate data points with seeded randomness for consistency
  function seededRandom(seed) {
    let s = seed;
    return function () {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
  }
  const rand = seededRandom(42);

  const legit = [];
  for (let i = 0; i < 30; i++) {
    legit.push({
      x: 50 + rand() * 400,
      y: 10 + rand() * 180,
    });
  }

  const fraud = [];
  for (let i = 0; i < 8; i++) {
    fraud.push({
      x: 500 + rand() * 450,
      y: 200 + rand() * 280,
    });
  }

  // Draw legit points
  legit.forEach(p => {
    svg.appendChild(svgEl('circle', {
      cx: toX(p.x), cy: toY(p.y), r: 5,
      fill: VIZ_COLORS.secondary, opacity: 0.75,
    }));
  });

  // Draw fraud points
  fraud.forEach(p => {
    svg.appendChild(svgEl('circle', {
      cx: toX(p.x), cy: toY(p.y), r: 5,
      fill: VIZ_COLORS.red, opacity: 0.8,
    }));
  });

  // Ambiguous point on the boundary
  const ambX = 480, ambY = 210;
  svg.appendChild(svgEl('circle', {
    cx: toX(ambX), cy: toY(ambY), r: 7,
    fill: VIZ_COLORS.accent, stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));
  const ambLabel = svgEl('text', {
    x: toX(ambX) + 12, y: toY(ambY) + 4,
    fill: VIZ_COLORS.accent, 'font-size': '9', 'font-weight': '700',
  });
  ambLabel.textContent = '? Where does this one go?';
  svg.appendChild(ambLabel);

  // Decision boundary -- animated line
  const boundaryLine = svgEl('line', {
    x1: toX(350), y1: toY(0), x2: toX(650), y2: toY(500),
    stroke: VIZ_COLORS.primary, 'stroke-width': 2.5,
    'stroke-dasharray': '6,3',
  });

  // Animation: draw-in effect
  const lineLen = Math.sqrt(Math.pow(toX(650) - toX(350), 2) + Math.pow(toY(500) - toY(0), 2));
  boundaryLine.setAttribute('stroke-dasharray', lineLen);
  boundaryLine.setAttribute('stroke-dashoffset', lineLen);
  svg.appendChild(boundaryLine);

  // Legend
  const legendY = pad.top + 12;
  svg.appendChild(svgEl('circle', { cx: pad.left + plotW - 110, cy: legendY, r: 4, fill: VIZ_COLORS.secondary }));
  const legText = svgEl('text', { x: pad.left + plotW - 102, y: legendY + 3, fill: VIZ_COLORS.textLight, 'font-size': '8' });
  legText.textContent = 'Legit';
  svg.appendChild(legText);

  svg.appendChild(svgEl('circle', { cx: pad.left + plotW - 60, cy: legendY, r: 4, fill: VIZ_COLORS.red }));
  const frText = svgEl('text', { x: pad.left + plotW - 52, y: legendY + 3, fill: VIZ_COLORS.textLight, 'font-size': '8' });
  frText.textContent = 'Fraud';
  svg.appendChild(frText);

  container.appendChild(svg);

  // Animate the decision boundary on scroll into view
  const reduced = prefersReducedMotion();
  function animateBoundary() {
    if (reduced) {
      boundaryLine.setAttribute('stroke-dashoffset', 0);
      return;
    }
    const start = performance.now();
    const duration = 1000;
    function tick(now) {
      const t = Math.min((now - start) / duration, 1);
      const ease = t * (2 - t); // ease-out
      boundaryLine.setAttribute('stroke-dashoffset', lineLen * (1 - ease));
      if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateBoundary();
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });
  observer.observe(container);
}


/* =========================================================================
   4. BAYES FORMULA COLOR-CODED  (#viz-bayes)
   ========================================================================= */

function renderBayes(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const wrapper = document.createElement('div');
  wrapper.style.cssText = 'max-width:600px;margin:0 auto;padding:16px;background:#fff;border-radius:8px;font-family:Inter,system-ui,sans-serif;overflow:hidden;';
  wrapper.setAttribute('role', 'img');
  wrapper.setAttribute('aria-label', 'Bayes theorem formula with color-coded terms: P(Fraud|Data) in gold, P(Data|Fraud) in red, P(Fraud) in blue, P(Data) in green');

  // The formula as structured HTML
  wrapper.innerHTML = `
    <div class="bayes-formula" style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:4px;font-size:clamp(16px,3.5vw,24px);font-weight:700;line-height:1.6;">
      <span class="bayes-term" data-order="1" style="opacity:0;transform:translateY(10px);transition:opacity 0.5s ease,transform 0.5s ease;">
        <span style="color:${VIZ_COLORS.gold};text-shadow:0 0 1px rgba(0,0,0,0.1);">P(Fraud|Data)</span>
      </span>
      <span class="bayes-term" data-order="2" style="opacity:0;transform:translateY(10px);transition:opacity 0.5s ease 0.3s,transform 0.5s ease 0.3s;font-weight:400;font-size:0.9em;color:#616161;">
        =
      </span>
      <span class="bayes-term" data-order="3" style="opacity:0;transform:translateY(10px);transition:opacity 0.5s ease 0.6s,transform 0.5s ease 0.6s;">
        <span style="display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;">
          <span style="padding:0 8px 4px;border-bottom:2.5px solid #616161;">
            <span style="color:${VIZ_COLORS.red};">P(Data|Fraud)</span>
            <span style="color:#616161;font-weight:400;margin:0 3px;">&times;</span>
            <span style="color:${VIZ_COLORS.primary};">P(Fraud)</span>
          </span>
          <span style="padding:4px 8px 0;">
            <span style="color:${VIZ_COLORS.secondary};">P(Data)</span>
          </span>
        </span>
      </span>
    </div>
    <div class="bayes-labels" style="display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin-top:20px;">
      <div class="bayes-label-item" data-order="1" style="opacity:0;transform:translateY(8px);transition:opacity 0.4s ease 0.9s,transform 0.4s ease 0.9s;text-align:center;min-width:100px;">
        <div style="width:28px;height:4px;border-radius:2px;background:${VIZ_COLORS.gold};margin:0 auto 6px;"></div>
        <div style="font-size:11px;font-weight:600;color:${VIZ_COLORS.gold};">How suspicious?</div>
        <div style="font-size:9px;color:#9e9e9e;margin-top:2px;">Posterior</div>
      </div>
      <div class="bayes-label-item" data-order="2" style="opacity:0;transform:translateY(8px);transition:opacity 0.4s ease 1.1s,transform 0.4s ease 1.1s;text-align:center;min-width:100px;">
        <div style="width:28px;height:4px;border-radius:2px;background:${VIZ_COLORS.red};margin:0 auto 6px;"></div>
        <div style="font-size:11px;font-weight:600;color:${VIZ_COLORS.red};">How typical of fraud?</div>
        <div style="font-size:9px;color:#9e9e9e;margin-top:2px;">Likelihood</div>
      </div>
      <div class="bayes-label-item" data-order="3" style="opacity:0;transform:translateY(8px);transition:opacity 0.4s ease 1.3s,transform 0.4s ease 1.3s;text-align:center;min-width:100px;">
        <div style="width:28px;height:4px;border-radius:2px;background:${VIZ_COLORS.primary};margin:0 auto 6px;"></div>
        <div style="font-size:11px;font-weight:600;color:${VIZ_COLORS.primary};">How rare is fraud?</div>
        <div style="font-size:9px;color:#9e9e9e;margin-top:2px;">Prior</div>
      </div>
      <div class="bayes-label-item" data-order="4" style="opacity:0;transform:translateY(8px);transition:opacity 0.4s ease 1.5s,transform 0.4s ease 1.5s;text-align:center;min-width:100px;">
        <div style="width:28px;height:4px;border-radius:2px;background:${VIZ_COLORS.secondary};margin:0 auto 6px;"></div>
        <div style="font-size:11px;font-weight:600;color:${VIZ_COLORS.secondary};">How normal is this data?</div>
        <div style="font-size:9px;color:#9e9e9e;margin-top:2px;">Evidence</div>
      </div>
    </div>
  `;

  container.appendChild(wrapper);

  // Animate on scroll into view
  const allTerms = wrapper.querySelectorAll('.bayes-term, .bayes-label-item');
  const reduced = prefersReducedMotion();

  if (reduced) {
    allTerms.forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    });
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        allTerms.forEach(el => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });
  observer.observe(container);
}


/* =========================================================================
   5. COSINE SIMILARITY  (#viz-cosine)
   ========================================================================= */

function renderCosine(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const W = 400, H = 400;
  const pad = { top: 30, right: 30, bottom: 45, left: 55 };
  const plotW = W - pad.left - pad.right;
  const plotH = H - pad.top - pad.bottom;
  const maxVal = 6;

  function toX(v) { return pad.left + (v / maxVal) * plotW; }
  function toY(v) { return pad.top + plotH - (v / maxVal) * plotH; }
  function fromX(sx) { return ((sx - pad.left) / plotW) * maxVal; }
  function fromY(sy) { return ((pad.top + plotH - sy) / plotH) * maxVal; }

  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`, width: '100%',
    style: 'max-width:400px;display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;touch-action:none;',
    role: 'img',
    'aria-label': 'Cosine similarity visualization with two draggable vectors showing the angle between them and the similarity score',
  });

  svg.appendChild(svgEl('rect', { x: 0, y: 0, width: W, height: H, fill: VIZ_COLORS.surface, rx: 8 }));
  svg.appendChild(svgEl('rect', { x: pad.left, y: pad.top, width: plotW, height: plotH, fill: VIZ_COLORS.mathBg, rx: 4 }));

  // Grid
  for (let v = 1; v <= 5; v++) {
    svg.appendChild(svgEl('line', {
      x1: toX(v), y1: pad.top, x2: toX(v), y2: pad.top + plotH,
      stroke: VIZ_COLORS.border, 'stroke-width': 0.5,
    }));
    svg.appendChild(svgEl('line', {
      x1: pad.left, y1: toY(v), x2: pad.left + plotW, y2: toY(v),
      stroke: VIZ_COLORS.border, 'stroke-width': 0.5,
    }));
  }

  // Axes
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: pad.top + plotH, x2: pad.left + plotW, y2: pad.top + plotH,
    stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: pad.top, x2: pad.left, y2: pad.top + plotH,
    stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));

  // Axis labels
  const xLabel = svgEl('text', {
    x: pad.left + plotW / 2, y: H - 5, 'text-anchor': 'middle',
    fill: VIZ_COLORS.textLight, 'font-size': '11',
  });
  xLabel.textContent = 'Savings Interest';
  svg.appendChild(xLabel);

  const yLabel = svgEl('text', {
    x: 12, y: pad.top + plotH / 2, 'text-anchor': 'middle',
    fill: VIZ_COLORS.textLight, 'font-size': '11',
    transform: `rotate(-90, 12, ${pad.top + plotH / 2})`,
  });
  yLabel.textContent = 'Risk Tolerance';
  svg.appendChild(yLabel);

  // Tick labels
  [0, 1, 2, 3, 4, 5].forEach(v => {
    const tx = svgEl('text', {
      x: toX(v), y: pad.top + plotH + 14, 'text-anchor': 'middle',
      fill: VIZ_COLORS.textLight, 'font-size': '8',
    });
    tx.textContent = v;
    svg.appendChild(tx);
    const ty = svgEl('text', {
      x: pad.left - 6, y: toY(v) + 3, 'text-anchor': 'end',
      fill: VIZ_COLORS.textLight, 'font-size': '8',
    });
    ty.textContent = v;
    svg.appendChild(ty);
  });

  // State
  const vecA = { x: 4, y: 3 };
  let vecB = { x: 3, y: 4 };

  // Angle arc
  const arcPath = svgEl('path', { fill: 'rgba(255,143,0,0.15)', stroke: VIZ_COLORS.accent, 'stroke-width': 1 });
  svg.appendChild(arcPath);

  // Vector A
  const lineA = svgEl('line', { stroke: VIZ_COLORS.primary, 'stroke-width': 2.5, 'marker-end': 'url(#arrowA)' });
  const lineB = svgEl('line', { stroke: VIZ_COLORS.secondary, 'stroke-width': 2.5, 'marker-end': 'url(#arrowB)' });

  // Arrowhead markers
  const defs = svgEl('defs');
  [{ id: 'arrowA', color: VIZ_COLORS.primary }, { id: 'arrowB', color: VIZ_COLORS.secondary }].forEach(({ id, color }) => {
    const marker = svgEl('marker', {
      id, viewBox: '0 0 10 10', refX: 8, refY: 5,
      markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse',
    });
    marker.appendChild(svgEl('path', { d: 'M 0 0 L 10 5 L 0 10 z', fill: color }));
    defs.appendChild(marker);
  });
  svg.appendChild(defs);
  svg.appendChild(lineA);
  svg.appendChild(lineB);

  // Labels
  const labelA = svgEl('text', { fill: VIZ_COLORS.primary, 'font-size': '10', 'font-weight': '700' });
  labelA.textContent = 'A (You)';
  svg.appendChild(labelA);

  const labelB = svgEl('text', { fill: VIZ_COLORS.secondary, 'font-size': '10', 'font-weight': '700' });
  labelB.textContent = 'B (Friend)';
  svg.appendChild(labelB);

  const thetaLabel = svgEl('text', { fill: VIZ_COLORS.accent, 'font-size': '9', 'font-weight': '600' });
  svg.appendChild(thetaLabel);

  // Score readout
  const scoreBox = svgEl('rect', { rx: 6, fill: VIZ_COLORS.mathBg, stroke: VIZ_COLORS.border, 'stroke-width': 1 });
  svg.appendChild(scoreBox);
  const scoreText = svgEl('text', { 'font-size': '11', 'font-weight': '700', 'text-anchor': 'middle' });
  svg.appendChild(scoreText);

  // Draggable endpoint for B
  const dragCircle = svgEl('circle', {
    r: 10, fill: VIZ_COLORS.secondary, opacity: 0.3, style: 'cursor:grab;',
  });
  svg.appendChild(dragCircle);

  function cosineSim(a, b) {
    const dot = a.x * b.x + a.y * b.y;
    const magA = Math.sqrt(a.x * a.x + a.y * a.y);
    const magB = Math.sqrt(b.x * b.x + b.y * b.y);
    return magA === 0 || magB === 0 ? 0 : dot / (magA * magB);
  }

  function updateViz() {
    const ox = toX(0), oy = toY(0);
    lineA.setAttribute('x1', ox); lineA.setAttribute('y1', oy);
    lineA.setAttribute('x2', toX(vecA.x)); lineA.setAttribute('y2', toY(vecA.y));
    lineB.setAttribute('x1', ox); lineB.setAttribute('y1', oy);
    lineB.setAttribute('x2', toX(vecB.x)); lineB.setAttribute('y2', toY(vecB.y));

    labelA.setAttribute('x', toX(vecA.x) + 8);
    labelA.setAttribute('y', toY(vecA.y) - 6);
    labelB.setAttribute('x', toX(vecB.x) + 8);
    labelB.setAttribute('y', toY(vecB.y) - 6);

    dragCircle.setAttribute('cx', toX(vecB.x));
    dragCircle.setAttribute('cy', toY(vecB.y));

    // Angle arc
    const angleA = Math.atan2(vecA.y, vecA.x);
    const angleB = Math.atan2(vecB.y, vecB.x);
    const radius = 35;
    // SVG arc angles are clockwise from positive-x, but our Y is flipped
    const svgAngleA = -angleA;
    const svgAngleB = -angleB;
    const startAngle = Math.min(svgAngleA, svgAngleB);
    const endAngle = Math.max(svgAngleA, svgAngleB);
    const sweep = endAngle - startAngle;

    const arcStartX = ox + radius * Math.cos(startAngle);
    const arcStartY = oy + radius * Math.sin(startAngle);
    const arcEndX = ox + radius * Math.cos(endAngle);
    const arcEndY = oy + radius * Math.sin(endAngle);
    const largeArc = sweep > Math.PI ? 1 : 0;

    arcPath.setAttribute('d',
      `M ${ox} ${oy} L ${arcStartX} ${arcStartY} A ${radius} ${radius} 0 ${largeArc} 1 ${arcEndX} ${arcEndY} Z`
    );

    const midAngle = (startAngle + endAngle) / 2;
    thetaLabel.setAttribute('x', ox + (radius + 14) * Math.cos(midAngle));
    thetaLabel.setAttribute('y', oy + (radius + 14) * Math.sin(midAngle) + 3);
    const thetaDeg = Math.abs(angleA - angleB) * (180 / Math.PI);
    thetaLabel.textContent = '\u03B8=' + thetaDeg.toFixed(0) + '\u00B0';

    // Score
    const sim = cosineSim(vecA, vecB);
    const simText = sim.toFixed(2);
    let desc = '';
    if (sim > 0.9) desc = 'Very similar!';
    else if (sim > 0.7) desc = 'Similar';
    else if (sim > 0.4) desc = 'Somewhat similar';
    else if (sim > 0.0) desc = 'Different';
    else desc = 'Opposite';

    const boxW = 200, boxH = 26;
    const boxX = pad.left + plotW / 2 - boxW / 2;
    const boxY = pad.top + 4;
    scoreBox.setAttribute('x', boxX);
    scoreBox.setAttribute('y', boxY);
    scoreBox.setAttribute('width', boxW);
    scoreBox.setAttribute('height', boxH);
    scoreText.setAttribute('x', pad.left + plotW / 2);
    scoreText.setAttribute('y', boxY + 17);
    scoreText.setAttribute('fill', sim > 0.7 ? VIZ_COLORS.secondary : (sim > 0.3 ? VIZ_COLORS.accent : VIZ_COLORS.red));
    scoreText.textContent = `cos(\u03B8) = ${simText} \u2014 ${desc}`;
  }

  updateViz();

  // Drag interaction
  let dragging = false;

  function getSVGPoint(evt) {
    const pt = svg.createSVGPoint();
    const touch = evt.touches ? evt.touches[0] : evt;
    pt.x = touch.clientX;
    pt.y = touch.clientY;
    return pt.matrixTransform(svg.getScreenCTM().inverse());
  }

  function startDrag(e) {
    e.preventDefault();
    dragging = true;
    dragCircle.style.cursor = 'grabbing';
  }
  function moveDrag(e) {
    if (!dragging) return;
    e.preventDefault();
    const pt = getSVGPoint(e);
    const bx = clamp(fromX(pt.x), 0.2, maxVal);
    const by = clamp(fromY(pt.y), 0.2, maxVal);
    vecB = { x: bx, y: by };
    updateViz();
  }
  function endDrag() {
    dragging = false;
    dragCircle.style.cursor = 'grab';
  }

  dragCircle.addEventListener('mousedown', startDrag);
  dragCircle.addEventListener('touchstart', startDrag, { passive: false });
  svg.addEventListener('mousemove', moveDrag);
  svg.addEventListener('touchmove', moveDrag, { passive: false });
  svg.addEventListener('mouseup', endDrag);
  svg.addEventListener('touchend', endDrag);
  svg.addEventListener('mouseleave', endDrag);

  container.appendChild(svg);
}


/* =========================================================================
   6. DOT PRODUCT  (#viz-dotproduct)
   ========================================================================= */

function renderDotProduct(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const wrapper = document.createElement('div');
  wrapper.style.cssText = 'max-width:500px;margin:0 auto;padding:20px;background:#fff;border-radius:8px;font-family:Inter,system-ui,sans-serif;overflow:hidden;';
  wrapper.setAttribute('role', 'img');
  wrapper.setAttribute('aria-label', 'Dot product visualization showing vectors A=[4,2,5] and B=[3,5,1] being multiplied element-wise and summed to 27');

  const A = [4, 2, 5];
  const B = [3, 5, 1];
  const products = A.map((a, i) => a * B[i]);
  const total = products.reduce((s, v) => s + v, 0);

  // Build the rows
  wrapper.innerHTML = `
    <div style="text-align:center;margin-bottom:16px;">
      <span style="font-weight:700;color:${VIZ_COLORS.primary};font-size:14px;">A = [${A.join(', ')}]</span>
      <span style="margin:0 12px;color:#9e9e9e;">&middot;</span>
      <span style="font-weight:700;color:${VIZ_COLORS.secondary};font-size:14px;">B = [${B.join(', ')}]</span>
    </div>
    <div id="dp-steps" style="display:flex;flex-direction:column;gap:10px;align-items:center;">
      ${A.map((a, i) => `
        <div class="dp-row" data-step="${i}" style="display:flex;align-items:center;gap:8px;opacity:0;transform:translateX(-20px);transition:opacity 0.4s ease ${i * 0.5}s, transform 0.4s ease ${i * 0.5}s;">
          <div style="display:flex;align-items:center;gap:6px;min-width:180px;justify-content:center;">
            <span style="display:inline-flex;align-items:center;justify-content:center;width:40px;height:36px;border-radius:6px;background:rgba(26,35,126,0.1);color:${VIZ_COLORS.primary};font-weight:700;font-size:18px;">${a}</span>
            <span style="color:#9e9e9e;font-size:16px;">&times;</span>
            <span style="display:inline-flex;align-items:center;justify-content:center;width:40px;height:36px;border-radius:6px;background:rgba(0,137,123,0.1);color:${VIZ_COLORS.secondary};font-weight:700;font-size:18px;">${B[i]}</span>
            <span style="color:#9e9e9e;font-size:16px;">=</span>
            <span style="display:inline-flex;align-items:center;justify-content:center;width:40px;height:36px;border-radius:6px;background:rgba(255,143,0,0.12);color:${VIZ_COLORS.accent};font-weight:700;font-size:18px;">${products[i]}</span>
          </div>
        </div>
      `).join('')}
    </div>
    <div id="dp-sum" style="margin-top:16px;text-align:center;opacity:0;transform:translateY(10px);transition:opacity 0.5s ease ${A.length * 0.5 + 0.3}s, transform 0.5s ease ${A.length * 0.5 + 0.3}s;">
      <div style="display:inline-flex;align-items:center;gap:6px;padding:8px 20px;background:linear-gradient(135deg,rgba(255,215,0,0.15),rgba(255,143,0,0.1));border-radius:8px;border:2px solid ${VIZ_COLORS.gold};">
        <span style="font-size:13px;color:#616161;">${products.join(' + ')} =</span>
        <span style="font-size:24px;font-weight:700;color:${VIZ_COLORS.gold};">${total}</span>
      </div>
      <div style="margin-top:10px;font-size:13px;font-weight:600;color:${VIZ_COLORS.textLight};">
        Similarity Score: <span style="color:${VIZ_COLORS.gold};font-size:16px;">${total}</span>
      </div>
    </div>
  `;

  container.appendChild(wrapper);

  // Animate on scroll
  const rows = wrapper.querySelectorAll('.dp-row');
  const sumEl = wrapper.querySelector('#dp-sum');
  const reduced = prefersReducedMotion();

  if (reduced) {
    rows.forEach(r => { r.style.opacity = '1'; r.style.transform = 'none'; });
    sumEl.style.opacity = '1';
    sumEl.style.transform = 'none';
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        rows.forEach(r => { r.style.opacity = '1'; r.style.transform = 'translateX(0)'; });
        sumEl.style.opacity = '1';
        sumEl.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });
  observer.observe(container);
}


/* =========================================================================
   7. LINEAR REGRESSION  (#viz-regression)
   ========================================================================= */

function renderRegression(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const W = 500, H = 350;
  const pad = { top: 20, right: 30, bottom: 45, left: 60 };
  const plotW = W - pad.left - pad.right;
  const plotH = H - pad.top - pad.bottom;

  // Axis ranges
  const xRange = [0, 25];
  const yRange = [500, 850];

  // Regression: y = 12x + 580
  const m = 12, b = 580;

  function toX(v) { return pad.left + ((v - xRange[0]) / (xRange[1] - xRange[0])) * plotW; }
  function toY(v) { return pad.top + (1 - (v - yRange[0]) / (yRange[1] - yRange[0])) * plotH; }

  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`, width: '100%',
    style: 'max-width:500px;display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;',
    role: 'img',
    'aria-label': 'Linear regression scatter plot with a best-fit line showing y = 12x + 580 for credit score prediction based on years of credit history',
  });

  svg.appendChild(svgEl('rect', { x: 0, y: 0, width: W, height: H, fill: VIZ_COLORS.surface, rx: 8 }));
  svg.appendChild(svgEl('rect', { x: pad.left, y: pad.top, width: plotW, height: plotH, fill: VIZ_COLORS.mathBg, rx: 4 }));

  // Grid
  [5, 10, 15, 20].forEach(x => {
    svg.appendChild(svgEl('line', {
      x1: toX(x), y1: pad.top, x2: toX(x), y2: pad.top + plotH,
      stroke: VIZ_COLORS.border, 'stroke-width': 0.5,
    }));
  });
  [550, 600, 650, 700, 750, 800].forEach(y => {
    svg.appendChild(svgEl('line', {
      x1: pad.left, y1: toY(y), x2: pad.left + plotW, y2: toY(y),
      stroke: VIZ_COLORS.border, 'stroke-width': 0.5,
    }));
  });

  // Axes
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: pad.top + plotH, x2: pad.left + plotW, y2: pad.top + plotH,
    stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));
  svg.appendChild(svgEl('line', {
    x1: pad.left, y1: pad.top, x2: pad.left, y2: pad.top + plotH,
    stroke: VIZ_COLORS.text, 'stroke-width': 1.5,
  }));

  // Axis labels
  const xLabel = svgEl('text', {
    x: pad.left + plotW / 2, y: H - 5, 'text-anchor': 'middle',
    fill: VIZ_COLORS.textLight, 'font-size': '11',
  });
  xLabel.textContent = 'Years of Credit History';
  svg.appendChild(xLabel);

  const yAxisLabel = svgEl('text', {
    x: 14, y: pad.top + plotH / 2, 'text-anchor': 'middle',
    fill: VIZ_COLORS.textLight, 'font-size': '11',
    transform: `rotate(-90, 14, ${pad.top + plotH / 2})`,
  });
  yAxisLabel.textContent = 'Credit Score';
  svg.appendChild(yAxisLabel);

  // Tick labels
  [0, 5, 10, 15, 20, 25].forEach(x => {
    const t = svgEl('text', {
      x: toX(x), y: pad.top + plotH + 14, 'text-anchor': 'middle',
      fill: VIZ_COLORS.textLight, 'font-size': '8',
    });
    t.textContent = x;
    svg.appendChild(t);
  });
  [500, 550, 600, 650, 700, 750, 800, 850].forEach(y => {
    const t = svgEl('text', {
      x: pad.left - 6, y: toY(y) + 3, 'text-anchor': 'end',
      fill: VIZ_COLORS.textLight, 'font-size': '8',
    });
    t.textContent = y;
    svg.appendChild(t);
  });

  // Generate data points
  function seededRandom(seed) {
    let s = seed;
    return function () {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
  }
  const rand = seededRandom(77);

  const data = [];
  for (let i = 0; i < 18; i++) {
    const x = 1 + rand() * 22;
    const noise = (rand() - 0.5) * 60;
    const y = m * x + b + noise;
    data.push({ x, y: clamp(y, yRange[0], yRange[1]) });
  }

  // Draw data points
  data.forEach(p => {
    svg.appendChild(svgEl('circle', {
      cx: toX(p.x), cy: toY(p.y), r: 5,
      fill: VIZ_COLORS.secondary, opacity: 0.8,
    }));
  });

  // Residual lines for a few points
  [2, 5, 9, 13, 16].forEach(idx => {
    if (idx >= data.length) return;
    const p = data[idx];
    const predicted = m * p.x + b;
    svg.appendChild(svgEl('line', {
      x1: toX(p.x), y1: toY(p.y), x2: toX(p.x), y2: toY(predicted),
      stroke: VIZ_COLORS.red, 'stroke-width': 1, 'stroke-dasharray': '3,2', opacity: 0.6,
    }));
  });

  // Best-fit line
  const lineX1 = xRange[0], lineX2 = xRange[1];
  const lineY1 = m * lineX1 + b, lineY2 = m * lineX2 + b;

  const regLine = svgEl('line', {
    x1: toX(lineX1), y1: toY(lineY1), x2: toX(lineX2), y2: toY(lineY2),
    stroke: VIZ_COLORS.primary, 'stroke-width': 2.5,
  });

  // Animate draw-in
  const linePxLen = Math.sqrt(
    Math.pow(toX(lineX2) - toX(lineX1), 2) + Math.pow(toY(lineY2) - toY(lineY1), 2)
  );
  regLine.setAttribute('stroke-dasharray', linePxLen);
  regLine.setAttribute('stroke-dashoffset', linePxLen);
  svg.appendChild(regLine);

  // Equation label on the line
  const eqX = 14, eqPredicted = m * eqX + b;
  const eqLabel = svgEl('text', {
    x: toX(eqX) + 6, y: toY(eqPredicted) - 10,
    fill: VIZ_COLORS.primary, 'font-size': '11', 'font-weight': '700',
    opacity: 0,
  });
  eqLabel.textContent = `y = ${m}x + ${b}`;
  svg.appendChild(eqLabel);

  container.appendChild(svg);

  // Animate on scroll
  const reduced = prefersReducedMotion();

  function animateLine() {
    if (reduced) {
      regLine.setAttribute('stroke-dashoffset', 0);
      eqLabel.setAttribute('opacity', 1);
      return;
    }
    const start = performance.now();
    const duration = 1200;
    function tick(now) {
      const t = Math.min((now - start) / duration, 1);
      const ease = t * (2 - t);
      regLine.setAttribute('stroke-dashoffset', linePxLen * (1 - ease));
      if (t > 0.6) {
        eqLabel.setAttribute('opacity', Math.min(1, (t - 0.6) / 0.4));
      }
      if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateLine();
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });
  observer.observe(container);
}


/* =========================================================================
   INIT -- call all renderers on DOMContentLoaded
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
  renderSigmoid('viz-sigmoid');
  renderBellCurve('viz-bellcurve');
  renderScatter('viz-scatter');
  renderBayes('viz-bayes');
  renderCosine('viz-cosine');
  renderDotProduct('viz-dotproduct');
  renderRegression('viz-regression');
});
