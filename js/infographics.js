/**
 * infographics.js
 * Mathematics for AI — Animated infographic visualizations
 *
 * Infographic 1: Morning Timeline  →  #viz-morning-timeline
 * Infographic 2: Career Constellation  →  #viz-career-constellation
 */

(function () {
  'use strict';

  // ─── SHARED HELPERS ────────────────────────────────────────────────────────

  /** Create an SVG element with optional attributes. */
  function svgEl(tag, attrs) {
    const NS = 'http://www.w3.org/2000/svg';
    const node = document.createElementNS(NS, tag);
    if (attrs) {
      Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v));
    }
    return node;
  }

  /** Create an HTML element with optional attributes and children. */
  function el(tag, attrs, ...children) {
    const node = document.createElement(tag);
    if (attrs) {
      Object.entries(attrs).forEach(([k, v]) => {
        if (k === 'style' && typeof v === 'object') Object.assign(node.style, v);
        else node[k] = v;
      });
    }
    children.forEach(c => {
      if (c == null) return;
      node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    });
    return node;
  }

  /** Inject a <style> block once, identified by id. */
  function injectStyles(id, css) {
    if (document.getElementById(id)) return;
    const s = document.createElement('style');
    s.id = id;
    s.textContent = css;
    document.head.appendChild(s);
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // INFOGRAPHIC 1 — MORNING TIMELINE
  // ═══════════════════════════════════════════════════════════════════════════

  const TIMELINE_STATIONS = [
    {
      time:  '6:30',
      label: 'Alarm',
      callout: 'Smart alarm adjusted based on sleep pattern',
      icon: 'alarm',
    },
    {
      time:  '6:45',
      label: 'Phone Check',
      callout: '12 notifications ranked by predicted importance',
      icon: 'phone',
    },
    {
      time:  '7:00',
      label: 'Social Scroll',
      callout: 'Content feed reordered 47 times in 5 minutes',
      icon: 'social',
    },
    {
      time:  '7:30',
      label: 'Buy Coffee',
      callout: 'Payment authorized in 0.3s — fraud check passed',
      icon: 'coffee',
    },
    {
      time:  '8:15',
      label: 'Bank Balance',
      callout: 'Balance prediction: You might overspend this week',
      icon: 'bank',
    },
  ];

  // Counter values shown after each station reveals
  const COUNTER_VALUES = [1, 5, 12, 37, '50–200'];

  // ─── SVG ICON PATHS ───────────────────────────────────────────────────────
  // Each icon fits a 32×32 viewBox centered at (0,0).

  function buildIcon(type, color) {
    const g = svgEl('g');

    if (type === 'alarm') {
      // Clock circle + hands + two bell bumps
      g.appendChild(Object.assign(svgEl('circle', { cx: 0, cy: 0, r: 11, fill: 'none', stroke: color, 'stroke-width': 2 })));
      g.appendChild(svgEl('line', { x1: 0, y1: 0, x2: 0, y2: -7, stroke: color, 'stroke-width': 2, 'stroke-linecap': 'round' }));
      g.appendChild(svgEl('line', { x1: 0, y1: 0, x2: 5, y2: 3,  stroke: color, 'stroke-width': 2, 'stroke-linecap': 'round' }));
      // Bell bumps
      g.appendChild(svgEl('circle', { cx: -8,  cy: -9,  r: 2, fill: color }));
      g.appendChild(svgEl('circle', { cx:  8,  cy: -9,  r: 2, fill: color }));

    } else if (type === 'phone') {
      // Rounded rect phone body
      const body = svgEl('rect', { x: -6, y: -12, width: 12, height: 22, rx: 2, ry: 2,
        fill: 'none', stroke: color, 'stroke-width': 2 });
      g.appendChild(body);
      // Screen lines (notifications)
      [-5, -1, 3].forEach(yy => {
        g.appendChild(svgEl('line', { x1: -3, y1: yy, x2: 3, y2: yy,
          stroke: color, 'stroke-width': 1.5, 'stroke-linecap': 'round' }));
      });
      // Home button dot
      g.appendChild(svgEl('circle', { cx: 0, cy: 7, r: 1.5, fill: color }));

    } else if (type === 'social') {
      // Speech bubble + heart
      const bubble = svgEl('path', {
        d: 'M -10 -10 Q -10 -3 0 -3 Q 10 -3 10 -10 Q 10 -16 0 -16 Q -10 -16 -10 -10 Z',
        fill: 'none', stroke: color, 'stroke-width': 2,
      });
      g.appendChild(bubble);
      // Bubble tail
      g.appendChild(svgEl('path', { d: 'M -4 -3 L -6 2 L 2 -3', fill: 'none', stroke: color, 'stroke-width': 2 }));
      // Heart below
      g.appendChild(svgEl('path', {
        d: 'M 0 8 C 0 8 -8 2 -8 -1 C -8 -4 -5 -6 0 -2 C 5 -6 8 -4 8 -1 C 8 2 0 8 0 8 Z',
        fill: color, opacity: 0.8,
      }));

    } else if (type === 'coffee') {
      // Cup body
      g.appendChild(svgEl('path', { d: 'M -7 -4 L -5 10 L 5 10 L 7 -4 Z',
        fill: 'none', stroke: color, 'stroke-width': 2, 'stroke-linejoin': 'round' }));
      // Handle
      g.appendChild(svgEl('path', { d: 'M 7 0 Q 13 0 13 5 Q 13 10 7 10',
        fill: 'none', stroke: color, 'stroke-width': 2 }));
      // Saucer
      g.appendChild(svgEl('ellipse', { cx: 0, cy: 11, rx: 9, ry: 2,
        fill: 'none', stroke: color, 'stroke-width': 1.5 }));
      // Steam
      [-3, 0, 3].forEach((xx, i) => {
        const d = `M ${xx} -5 Q ${xx + 2} -9 ${xx} -13`;
        g.appendChild(svgEl('path', { d, fill: 'none', stroke: color, 'stroke-width': 1.5,
          'stroke-linecap': 'round', opacity: 0.6 }));
      });

    } else if (type === 'bank') {
      // Columns (pillars)
      [-6, 0, 6].forEach(xx => {
        g.appendChild(svgEl('rect', { x: xx - 1.5, y: -7, width: 3, height: 13,
          fill: color }));
      });
      // Roof triangle
      g.appendChild(svgEl('polygon', { points: '-11,-7 11,-7 0,-15', fill: color }));
      // Base
      g.appendChild(svgEl('rect', { x: -11, y: 6, width: 22, height: 3, rx: 1, fill: color }));
      // Foundation
      g.appendChild(svgEl('rect', { x: -13, y: 9, width: 26, height: 3, rx: 1, fill: color }));
    }

    return g;
  }

  // ─── STYLES ───────────────────────────────────────────────────────────────

  const TIMELINE_CSS = `
    .mt-root {
      font-family: var(--font-body, 'Inter', sans-serif);
      position: relative;
      padding: 24px 0 16px;
    }
    .mt-counter-wrap {
      position: absolute;
      top: 0;
      right: 0;
      text-align: right;
    }
    .mt-counter-label {
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--text-secondary, #6b7280);
    }
    .mt-counter-value {
      font-size: 2rem;
      font-weight: 800;
      color: #ff8f00;
      font-variant-numeric: tabular-nums;
      line-height: 1.1;
      transition: opacity 0.25s;
    }
    /* ── Desktop: horizontal ── */
    .mt-svg-wrap {
      width: 100%;
      overflow-x: auto;
    }
    .mt-svg-wrap svg {
      display: block;
      width: 100%;
    }
    /* Station node */
    .mt-station-g {
      opacity: 0;
      transition: opacity 0.4s ease, transform 0.4s ease;
    }
    .mt-station-g.mt-visible {
      opacity: 1;
    }
    /* Callout bubble */
    .mt-callout-g {
      opacity: 0;
      transform-origin: center bottom;
      transition: opacity 0.35s ease 0.15s;
    }
    .mt-callout-g.mt-visible {
      opacity: 1;
    }
    /* ── Mobile: vertical stack ── */
    @media (max-width: 767px) {
      .mt-svg-wrap { display: none; }
      .mt-mobile-list {
        display: flex;
        flex-direction: column;
        gap: 0;
        position: relative;
        padding-left: 40px;
        margin-top: 8px;
      }
      .mt-mobile-item {
        display: flex;
        flex-direction: column;
        position: relative;
        padding-bottom: 24px;
        opacity: 0;
        transform: translateX(-12px);
        transition: opacity 0.4s ease, transform 0.4s ease;
      }
      .mt-mobile-item.mt-visible {
        opacity: 1;
        transform: translateX(0);
      }
      /* Vertical connecting line */
      .mt-mobile-item::before {
        content: '';
        position: absolute;
        left: -26px;
        top: 20px;
        bottom: 0;
        width: 2px;
        background: #e0e0e0;
      }
      .mt-mobile-item:last-child::before { display: none; }
      /* Station dot */
      .mt-mobile-item::after {
        content: '';
        position: absolute;
        left: -30px;
        top: 12px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #616161;
        border: 2px solid #fff;
        box-shadow: 0 0 0 2px #616161;
      }
      .mt-mobile-time {
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--text-secondary, #6b7280);
        margin-bottom: 2px;
      }
      .mt-mobile-label {
        font-size: 0.9rem;
        font-weight: 700;
        color: var(--text-primary, #1a1a2e);
        margin-bottom: 4px;
      }
      .mt-mobile-callout {
        font-size: 0.78rem;
        background: #e74c3c;
        color: #fff;
        border-radius: 8px;
        padding: 6px 10px;
        display: inline-block;
        max-width: 280px;
      }
    }
    @media (min-width: 768px) {
      .mt-mobile-list { display: none; }
    }
  `;

  // ─── RENDER FUNCTION ──────────────────────────────────────────────────────

  function renderMorningTimeline(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    injectStyles('mt-styles', TIMELINE_CSS);

    const root = el('div', { className: 'mt-root' });

    // ── Counter (top-right) ────────────────────────────────────────────────
    const counterWrap = el('div', { className: 'mt-counter-wrap' });
    const counterLabel = el('div', { className: 'mt-counter-label' }, 'AI decisions so far');
    const counterValue = el('div', { className: 'mt-counter-value' }, '0');
    counterWrap.appendChild(counterLabel);
    counterWrap.appendChild(counterValue);
    root.appendChild(counterWrap);

    // ── Desktop SVG ────────────────────────────────────────────────────────
    const N = TIMELINE_STATIONS.length;
    const SVG_W = 900;
    const SVG_H = 220;
    const PAD_X = 70;
    const STATION_Y = 140;
    const CALLOUT_H = 80;   // height of callout bubble area above line
    const CALLOUT_W = 130;
    const ICON_R = 20;

    const svgWrap = el('div', { className: 'mt-svg-wrap' });
    const svg = svgEl('svg', {
      viewBox: `0 0 ${SVG_W} ${SVG_H}`,
      preserveAspectRatio: 'xMidYMid meet',
      'aria-hidden': 'true',
    });

    // Track line
    const trackLine = svgEl('line', {
      x1: PAD_X, y1: STATION_Y, x2: SVG_W - PAD_X, y2: STATION_Y,
      stroke: '#e0e0e0', 'stroke-width': 3,
    });
    svg.appendChild(trackLine);

    // Station x positions
    const xs = TIMELINE_STATIONS.map((_, i) =>
      PAD_X + i * ((SVG_W - 2 * PAD_X) / (N - 1))
    );

    const stationGs = [];
    const calloutGs = [];

    TIMELINE_STATIONS.forEach((station, i) => {
      const x = xs[i];

      // ── Station group ──
      const sg = svgEl('g', { class: 'mt-station-g', transform: `translate(${x},${STATION_Y})` });

      // Station circle
      sg.appendChild(svgEl('circle', { cx: 0, cy: 0, r: ICON_R + 4, fill: '#f5f5f5', stroke: '#e0e0e0', 'stroke-width': 2 }));

      // Icon (scaled to fit within circle)
      const iconG = buildIcon(station.icon, '#616161');
      iconG.setAttribute('transform', 'scale(0.9)');
      sg.appendChild(iconG);

      // Time label below station
      const timeText = svgEl('text', {
        x: 0, y: ICON_R + 18,
        'text-anchor': 'middle',
        'font-size': 11, 'font-weight': 700,
        fill: '#ff8f00',
        'font-family': "var(--font-body, 'Inter', sans-serif)",
      });
      timeText.textContent = station.time;
      sg.appendChild(timeText);

      // Station label
      const labelText = svgEl('text', {
        x: 0, y: ICON_R + 32,
        'text-anchor': 'middle',
        'font-size': 11, 'font-weight': 500,
        fill: '#444',
        'font-family': "var(--font-body, 'Inter', sans-serif)",
      });
      labelText.textContent = station.label;
      sg.appendChild(labelText);

      svg.appendChild(sg);
      stationGs.push(sg);

      // ── Callout group ──
      const cg = svgEl('g', { class: 'mt-callout-g' });

      // Stem line from station top to bubble
      cg.appendChild(svgEl('line', {
        x1: x, y1: STATION_Y - ICON_R - 4,
        x2: x, y2: STATION_Y - CALLOUT_H + 10,
        stroke: '#e74c3c', 'stroke-width': 2, 'stroke-dasharray': '4 3',
      }));

      // Bubble rect
      const bx = Math.min(Math.max(x - CALLOUT_W / 2, 4), SVG_W - CALLOUT_W - 4);
      const by = STATION_Y - CALLOUT_H - 2;
      cg.appendChild(svgEl('rect', {
        x: bx, y: by, width: CALLOUT_W, height: CALLOUT_H - 12,
        rx: 8, ry: 8, fill: '#e74c3c',
      }));

      // Callout text (word-wrapped via two lines)
      const words  = station.callout.split(' ');
      const mid    = Math.ceil(words.length / 2);
      const line1  = words.slice(0, mid).join(' ');
      const line2  = words.slice(mid).join(' ');
      const textY1 = by + 22;
      const textY2 = by + 38;

      [line1, line2].forEach((txt, li) => {
        const t = svgEl('text', {
          x: bx + CALLOUT_W / 2,
          y: li === 0 ? textY1 : textY2,
          'text-anchor': 'middle',
          'font-size': 10, fill: '#fff',
          'font-family': "var(--font-body, 'Inter', sans-serif)",
          'font-weight': 500,
        });
        t.textContent = txt;
        cg.appendChild(t);
      });

      svg.appendChild(cg);
      calloutGs.push(cg);
    });

    svgWrap.appendChild(svg);
    root.appendChild(svgWrap);

    // ── Mobile list ────────────────────────────────────────────────────────
    const mobileList = el('div', { className: 'mt-mobile-list' });
    const mobileItems = [];

    TIMELINE_STATIONS.forEach(station => {
      const item = el('div', { className: 'mt-mobile-item' });
      item.appendChild(el('div', { className: 'mt-mobile-time' }, station.time + ' AM'));
      item.appendChild(el('div', { className: 'mt-mobile-label' }, station.label));
      item.appendChild(el('div', { className: 'mt-mobile-callout' }, station.callout));
      mobileList.appendChild(item);
      mobileItems.push(item);
    });

    root.appendChild(mobileList);
    container.appendChild(root);

    // ── Animation (IntersectionObserver) ──────────────────────────────────
    let revealed = 0;

    function revealStation(idx) {
      if (idx >= N) return;
      stationGs[idx].classList.add('mt-visible');
      mobileItems[idx].classList.add('mt-visible');

      setTimeout(() => {
        calloutGs[idx].classList.add('mt-visible');

        // Update counter
        counterValue.style.opacity = '0';
        setTimeout(() => {
          counterValue.textContent = COUNTER_VALUES[idx];
          counterValue.style.opacity = '1';
        }, 120);

        revealed = idx + 1;
        // Cascade to next station after a short delay
        setTimeout(() => revealStation(idx + 1), 450);
      }, 300);
    }

    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            obs.disconnect();
            revealStation(0);
          }
        });
      },
      { threshold: 0.15 }
    );
    observer.observe(root);
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // INFOGRAPHIC 2 — CAREER CONSTELLATION
  // ═══════════════════════════════════════════════════════════════════════════

  const CAREER_NODES = [
    { id: 'data',    label: 'Data Scientist',   icon: 'chart',   desc: 'Find patterns in financial data',         salary: '€€€',      color: '#00897b' },
    { id: 'quant',   label: 'Quant Analyst',    icon: 'trending',desc: 'Build mathematical trading models',        salary: '€€€€',     color: '#ff8f00' },
    { id: 'ethics',  label: 'AI Ethics Officer',icon: 'scale',   desc: 'Ensure AI is fair and transparent',       salary: '€€€',      color: '#00897b' },
    { id: 'fintech', label: 'Fintech Founder',  icon: 'rocket',  desc: 'Build the next banking app',              salary: '€–€€€€€',  color: '#ff8f00' },
    { id: 'risk',    label: 'Risk Analyst',     icon: 'shield',  desc: 'Predict and prevent financial disasters', salary: '€€€',      color: '#00897b' },
    { id: 'ml',      label: 'ML Engineer',      icon: 'robot',   desc: 'Build and deploy AI systems',             salary: '€€€€',     color: '#ff8f00' },
  ];

  // ─── CAREER ICON BUILDERS ─────────────────────────────────────────────────

  function buildCareerIcon(type, color) {
    const g = svgEl('g');

    if (type === 'chart') {
      // Bar chart
      [[- 6, 8], [0, 2], [6, 5]].forEach(([bx, top]) => {
        g.appendChild(svgEl('rect', { x: bx - 3, y: top - 10, width: 5, height: 10 - top + 8,
          fill: color, rx: 1 }));
      });
      g.appendChild(svgEl('line', { x1: -10, y1: -2, x2: 10, y2: -2,
        stroke: color, 'stroke-width': 1.5 }));

    } else if (type === 'trending') {
      // Upward trending line with arrow
      g.appendChild(svgEl('polyline', {
        points: '-9,6 -3,0 3,-4 9,-8',
        fill: 'none', stroke: color, 'stroke-width': 2.5, 'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
      }));
      g.appendChild(svgEl('polyline', {
        points: '5,-8 9,-8 9,-4',
        fill: 'none', stroke: color, 'stroke-width': 2.5, 'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
      }));

    } else if (type === 'scale') {
      // Balance scales
      g.appendChild(svgEl('line', { x1: 0, y1: -10, x2: 0, y2: 9,
        stroke: color, 'stroke-width': 2 }));
      g.appendChild(svgEl('line', { x1: -9, y1: -6, x2: 9, y2: -6,
        stroke: color, 'stroke-width': 2 }));
      // Left pan
      g.appendChild(svgEl('path', { d: 'M -9 -6 L -12 0 L -6 0 Z',
        fill: 'none', stroke: color, 'stroke-width': 1.5 }));
      // Right pan (slightly lower)
      g.appendChild(svgEl('path', { d: 'M 9 -6 L 6 1 L 12 1 Z',
        fill: 'none', stroke: color, 'stroke-width': 1.5 }));
      g.appendChild(svgEl('line', { x1: -4, y1: 9, x2: 4, y2: 9,
        stroke: color, 'stroke-width': 2 }));

    } else if (type === 'rocket') {
      // Rocket body
      g.appendChild(svgEl('path', {
        d: 'M 0 -12 C 4 -8 5 -2 5 4 L -5 4 C -5 -2 -4 -8 0 -12 Z',
        fill: 'none', stroke: color, 'stroke-width': 2,
      }));
      // Fins
      g.appendChild(svgEl('path', { d: 'M -5 4 L -9 10 L -5 8 Z', fill: color }));
      g.appendChild(svgEl('path', { d: 'M  5 4 L  9 10 L  5 8 Z', fill: color }));
      // Window
      g.appendChild(svgEl('circle', { cx: 0, cy: -3, r: 2.5, fill: 'none', stroke: color, 'stroke-width': 1.5 }));
      // Flame
      g.appendChild(svgEl('path', {
        d: 'M -3 8 Q 0 14 3 8',
        fill: 'none', stroke: color, 'stroke-width': 2, 'stroke-linecap': 'round',
      }));

    } else if (type === 'shield') {
      g.appendChild(svgEl('path', {
        d: 'M 0 -12 L 10 -7 L 10 2 Q 10 10 0 14 Q -10 10 -10 2 L -10 -7 Z',
        fill: 'none', stroke: color, 'stroke-width': 2, 'stroke-linejoin': 'round',
      }));
      // Checkmark inside
      g.appendChild(svgEl('polyline', {
        points: '-5,1 -1,6 6,-4',
        fill: 'none', stroke: color, 'stroke-width': 2.5, 'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
      }));

    } else if (type === 'robot') {
      // Head
      g.appendChild(svgEl('rect', { x: -7, y: -11, width: 14, height: 10, rx: 2, fill: 'none', stroke: color, 'stroke-width': 2 }));
      // Eyes
      g.appendChild(svgEl('circle', { cx: -3, cy: -7, r: 1.5, fill: color }));
      g.appendChild(svgEl('circle', { cx:  3, cy: -7, r: 1.5, fill: color }));
      // Antenna
      g.appendChild(svgEl('line', { x1: 0, y1: -11, x2: 0, y2: -14, stroke: color, 'stroke-width': 1.5 }));
      g.appendChild(svgEl('circle', { cx: 0, cy: -15, r: 1.5, fill: color }));
      // Body
      g.appendChild(svgEl('rect', { x: -8, y: -1, width: 16, height: 12, rx: 2, fill: 'none', stroke: color, 'stroke-width': 2 }));
      // Arms
      g.appendChild(svgEl('line', { x1: -8, y1: 3, x2: -12, y2: 3, stroke: color, 'stroke-width': 2 }));
      g.appendChild(svgEl('line', { x1:  8, y1: 3, x2:  12, y2: 3, stroke: color, 'stroke-width': 2 }));
    }

    return g;
  }

  // ─── STYLES ───────────────────────────────────────────────────────────────

  const CONSTELLATION_CSS = `
    .cc-root {
      font-family: var(--font-body, 'Inter', sans-serif);
      position: relative;
    }
    .cc-svg-wrap {
      width: 100%;
      overflow: hidden;
    }
    .cc-svg-wrap svg {
      display: block;
      width: 100%;
    }
    /* Pulsing connection lines */
    @keyframes cc-pulse {
      0%, 100% { opacity: 0.35; }
      50%       { opacity: 0.7;  }
    }
    .cc-line {
      stroke: #cfd8dc;
      stroke-width: 2;
      animation: cc-pulse 3s ease-in-out infinite;
    }
    .cc-line.cc-highlight {
      stroke: #00897b;
      stroke-width: 3;
      animation: none;
      opacity: 1;
    }
    /* Career node circles */
    .cc-node {
      cursor: pointer;
      transition: transform 0.2s;
      transform-origin: center center;
    }
    .cc-node:hover, .cc-node.cc-active {
      transform: scale(1.12);
    }
    /* Hover/click tooltip */
    .cc-tooltip {
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.2s;
    }
    .cc-tooltip.cc-visible {
      opacity: 1;
    }
    /* Mobile vertical list */
    @media (max-width: 767px) {
      .cc-svg-wrap { display: none; }
      .cc-mobile-list {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-top: 12px;
      }
      .cc-mobile-item {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        background: var(--card-bg, #fff);
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        padding: 14px 16px;
        border-left: 4px solid currentColor;
      }
      .cc-mobile-icon {
        flex-shrink: 0;
        width: 36px;
        height: 36px;
      }
      .cc-mobile-text { flex: 1; }
      .cc-mobile-label {
        font-size: 0.92rem;
        font-weight: 700;
        margin-bottom: 2px;
      }
      .cc-mobile-desc {
        font-size: 0.78rem;
        color: var(--text-secondary, #6b7280);
        margin-bottom: 4px;
      }
      .cc-mobile-salary {
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.03em;
      }
      .cc-mobile-connector {
        width: 3px;
        align-self: stretch;
        background: #e0e0e0;
        border-radius: 2px;
        display: block;
      }
    }
    @media (min-width: 768px) {
      .cc-mobile-list { display: none; }
    }
  `;

  // ─── RENDER FUNCTION ──────────────────────────────────────────────────────

  function renderCareerConstellation(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    injectStyles('cc-styles', CONSTELLATION_CSS);

    const root = el('div', { className: 'cc-root' });

    // ── Desktop SVG ────────────────────────────────────────────────────────
    const SVG_W  = 700;
    const SVG_H  = 500;
    const CX     = SVG_W / 2;
    const CY     = SVG_H / 2;
    const RADIUS = 175;        // distance from center to career nodes
    const HUB_R  = 52;
    const NODE_R = 36;

    const svgWrap = el('div', { className: 'cc-svg-wrap' });
    const svg = svgEl('svg', {
      viewBox: `0 0 ${SVG_W} ${SVG_H}`,
      preserveAspectRatio: 'xMidYMid meet',
      'aria-hidden': 'true',
    });

    // Pre-compute node positions (evenly spaced on circle, starting top)
    const positions = CAREER_NODES.map((_, i) => {
      const angle = (i / CAREER_NODES.length) * 2 * Math.PI - Math.PI / 2;
      return {
        x: CX + RADIUS * Math.cos(angle),
        y: CY + RADIUS * Math.sin(angle),
      };
    });

    // ── Defs: hub gradient ──
    const defs = svgEl('defs');
    const grad = svgEl('linearGradient', { id: 'cc-hub-grad', x1: '0%', y1: '0%', x2: '100%', y2: '100%' });
    const stop1 = svgEl('stop', { offset: '0%',   'stop-color': 'var(--primary, #1a237e)' });
    const stop2 = svgEl('stop', { offset: '100%', 'stop-color': 'var(--secondary, #00897b)' });
    grad.appendChild(stop1);
    grad.appendChild(stop2);
    defs.appendChild(grad);
    svg.appendChild(defs);

    // ── Connection lines ──
    const lineEls = [];
    positions.forEach((pos, i) => {
      const line = svgEl('line', {
        class: 'cc-line',
        x1: CX,  y1: CY,
        x2: pos.x, y2: pos.y,
        style: `animation-delay: ${i * 0.5}s`,
      });
      svg.appendChild(line);
      lineEls.push(line);
    });

    // ── Central hub ──
    const hubG = svgEl('g');
    hubG.appendChild(svgEl('circle', {
      cx: CX, cy: CY, r: HUB_R + 6,
      fill: 'rgba(26,35,126,0.08)',
    }));
    hubG.appendChild(svgEl('circle', {
      cx: CX, cy: CY, r: HUB_R,
      fill: 'url(#cc-hub-grad)',
    }));
    // Hub label (two lines)
    ['Math + AI', '+ Finance'].forEach((txt, li) => {
      const t = svgEl('text', {
        x: CX, y: CY + (li === 0 ? -7 : 10),
        'text-anchor': 'middle',
        'font-size': 12, 'font-weight': 800,
        fill: '#fff',
        'font-family': "var(--font-body, 'Inter', sans-serif)",
        'pointer-events': 'none',
      });
      t.textContent = txt;
      hubG.appendChild(t);
    });
    svg.appendChild(hubG);

    // ── Career nodes ──
    let activeIdx = null;

    CAREER_NODES.forEach((career, i) => {
      const { x, y } = positions[i];

      const nodeG = svgEl('g', { class: 'cc-node', tabindex: '0', role: 'button',
        'aria-label': career.label });
      nodeG.setAttribute('transform', `translate(${x},${y})`);

      // Shadow circle
      nodeG.appendChild(svgEl('circle', { cx: 0, cy: 0, r: NODE_R + 4,
        fill: 'rgba(0,0,0,0.06)' }));

      // Main circle
      nodeG.appendChild(svgEl('circle', { cx: 0, cy: 0, r: NODE_R,
        fill: '#fff', stroke: career.color, 'stroke-width': 2.5 }));

      // Icon
      const iconG = buildCareerIcon(career.icon, career.color);
      iconG.setAttribute('transform', 'scale(0.85)');
      nodeG.appendChild(iconG);

      // Label below node
      const labelY = NODE_R + 15;
      const labelT = svgEl('text', {
        x: 0, y: labelY,
        'text-anchor': 'middle',
        'font-size': 10.5, 'font-weight': 700,
        fill: '#333',
        'font-family': "var(--font-body, 'Inter', sans-serif)",
      });
      labelT.textContent = career.label;
      nodeG.appendChild(labelT);

      // Salary tag
      const salaryT = svgEl('text', {
        x: 0, y: labelY + 14,
        'text-anchor': 'middle',
        'font-size': 9.5, 'font-weight': 600,
        fill: career.color,
        'font-family': "var(--font-body, 'Inter', sans-serif)",
      });
      salaryT.textContent = career.salary;
      nodeG.appendChild(salaryT);

      svg.appendChild(nodeG);

      // ── Tooltip (desc) ──
      // Positioned toward center from the node
      const tx = CX + (x - CX) * 0.52;
      const ty = CY + (y - CY) * 0.52;
      const TOOLTIP_W = 140;
      const TOOLTIP_H = 38;

      const tipG = svgEl('g', { class: 'cc-tooltip' });
      tipG.appendChild(svgEl('rect', {
        x: tx - TOOLTIP_W / 2,
        y: ty - TOOLTIP_H / 2,
        width: TOOLTIP_W, height: TOOLTIP_H,
        rx: 7, ry: 7,
        fill: career.color, opacity: 0.93,
      }));

      // Wrap description into two lines
      const dwords = career.desc.split(' ');
      const dmid   = Math.ceil(dwords.length / 2);
      [dwords.slice(0, dmid).join(' '), dwords.slice(dmid).join(' ')].forEach((txt, li) => {
        const t = svgEl('text', {
          x: tx, y: ty - 7 + li * 15,
          'text-anchor': 'middle',
          'font-size': 9.5, fill: '#fff', 'font-weight': 500,
          'font-family': "var(--font-body, 'Inter', sans-serif)",
          'pointer-events': 'none',
        });
        t.textContent = txt;
        tipG.appendChild(t);
      });

      svg.appendChild(tipG);

      // ── Interaction ──
      function activate() {
        // Deactivate previous
        if (activeIdx !== null && activeIdx !== i) {
          svg.querySelectorAll('.cc-node')[activeIdx].classList.remove('cc-active');
          lineEls[activeIdx].classList.remove('cc-highlight');
          svg.querySelectorAll('.cc-tooltip')[activeIdx].classList.remove('cc-visible');
        }
        const wasActive = nodeG.classList.contains('cc-active');
        nodeG.classList.toggle('cc-active');
        lineEls[i].classList.toggle('cc-highlight', !wasActive);
        tipG.classList.toggle('cc-visible', !wasActive);
        activeIdx = wasActive ? null : i;
      }

      nodeG.addEventListener('click', activate);
      nodeG.addEventListener('mouseenter', () => {
        nodeG.classList.add('cc-active');
        lineEls[i].classList.add('cc-highlight');
        tipG.classList.add('cc-visible');
      });
      nodeG.addEventListener('mouseleave', () => {
        if (activeIdx !== i) {
          nodeG.classList.remove('cc-active');
          lineEls[i].classList.remove('cc-highlight');
          tipG.classList.remove('cc-visible');
        }
      });
      nodeG.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(); }
      });
    });

    svgWrap.appendChild(svg);
    root.appendChild(svgWrap);

    // ── Mobile list ────────────────────────────────────────────────────────
    const mobileList = el('div', { className: 'cc-mobile-list' });

    CAREER_NODES.forEach(career => {
      const item = el('div', { className: 'cc-mobile-item',
        style: { color: career.color, borderLeftColor: career.color } });

      // Mini SVG icon
      const iconSvg = svgEl('svg', { viewBox: '-16 -16 32 32', width: 36, height: 36 });
      const iconG = buildCareerIcon(career.icon, career.color);
      iconSvg.appendChild(iconG);
      const iconWrap = el('div', { className: 'cc-mobile-icon' });
      iconWrap.appendChild(iconSvg);

      const text = el('div', { className: 'cc-mobile-text' });
      text.appendChild(el('div', { className: 'cc-mobile-label', style: { color: career.color } },
        career.label));
      text.appendChild(el('div', { className: 'cc-mobile-desc' }, career.desc));
      text.appendChild(el('div', { className: 'cc-mobile-salary', style: { color: career.color } },
        career.salary));

      item.appendChild(iconWrap);
      item.appendChild(text);
      mobileList.appendChild(item);
    });

    root.appendChild(mobileList);
    container.appendChild(root);
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // AUTO-INIT
  // ═══════════════════════════════════════════════════════════════════════════

  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('viz-morning-timeline')) {
      renderMorningTimeline('viz-morning-timeline');
    }
    if (document.getElementById('viz-career-constellation')) {
      renderCareerConstellation('viz-career-constellation');
    }
  });

  // Expose for manual / deferred init
  window.renderMorningTimeline    = renderMorningTimeline;
  window.renderCareerConstellation = renderCareerConstellation;

}());
