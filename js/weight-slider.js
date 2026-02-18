/**
 * weight-slider.js
 * Interactive credit score weight slider visualization
 * Mathematics for AI — weighted sum demo widget
 */

(function () {
  'use strict';

  // ─── DATA ─────────────────────────────────────────────────────────────────

  const FACTORS = [
    { label: 'Payment History',    defaultWeight: 35, sampleValue: 90, color: '#1a237e' },
    { label: 'Credit Utilization', defaultWeight: 30, sampleValue: 60, color: '#00897b' },
    { label: 'Length of History',  defaultWeight: 15, sampleValue: 70, color: '#ff8f00' },
    { label: 'New Credit',         defaultWeight: 10, sampleValue: 80, color: '#e74c3c' },
    { label: 'Credit Mix',         defaultWeight: 10, sampleValue: 75, color: '#9c27b0' },
  ];

  const GRADE_FACTORS = [
    { label: 'Final Exam',     weight: 40, color: '#1a237e' },
    { label: 'Homework',       weight: 20, color: '#00897b' },
    { label: 'Participation',  weight: 15, color: '#ff8f00' },
    { label: 'Projects',       weight: 15, color: '#e74c3c' },
    { label: 'Quizzes',        weight: 10, color: '#9c27b0' },
  ];

  // ─── INJECT STYLES ────────────────────────────────────────────────────────

  function injectStyles() {
    if (document.getElementById('weight-slider-styles')) return;
    const style = document.createElement('style');
    style.id = 'weight-slider-styles';
    style.textContent = `
      .ws-root {
        font-family: var(--font-body, 'Inter', sans-serif);
        color: var(--text-primary, #1a1a2e);
      }
      .ws-columns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px;
        margin-bottom: 24px;
      }
      @media (max-width: 700px) {
        .ws-columns { grid-template-columns: 1fr; }
      }
      .ws-card {
        background: var(--card-bg, #ffffff);
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        padding: 20px 24px;
      }
      .ws-card-title {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-secondary, #6b7280);
        margin: 0 0 16px 0;
      }
      .ws-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
      }
      .ws-label {
        flex: 0 0 140px;
        font-size: 0.82rem;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .ws-slider-wrap {
        flex: 1;
        position: relative;
        height: 20px;
        display: flex;
        align-items: center;
      }
      .ws-slider {
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        height: 6px;
        border-radius: 3px;
        background: #e5e7eb;
        outline: none;
        cursor: pointer;
      }
      .ws-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: var(--thumb-color, #1a237e);
        border: 2px solid #fff;
        box-shadow: 0 1px 4px rgba(0,0,0,0.25);
        cursor: grab;
        transition: transform 0.1s;
      }
      .ws-slider:active::-webkit-slider-thumb { transform: scale(1.2); cursor: grabbing; }
      .ws-slider::-moz-range-thumb {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: var(--thumb-color, #1a237e);
        border: 2px solid #fff;
        box-shadow: 0 1px 4px rgba(0,0,0,0.25);
        cursor: grab;
      }
      .ws-pct {
        flex: 0 0 38px;
        text-align: right;
        font-size: 0.82rem;
        font-weight: 700;
        font-variant-numeric: tabular-nums;
      }
      .ws-static-bar {
        height: 8px;
        border-radius: 4px;
        flex: 1;
        overflow: hidden;
        background: #e5e7eb;
      }
      .ws-static-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
      }
      .ws-warning {
        font-size: 0.78rem;
        color: #e74c3c;
        font-weight: 600;
        margin-top: -6px;
        margin-bottom: 8px;
        min-height: 1.2em;
      }
      .ws-stacked-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-secondary, #6b7280);
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }
      .ws-stacked-bar {
        display: flex;
        height: 28px;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 6px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.08);
      }
      .ws-stacked-seg {
        height: 100%;
        transition: width 0.3s ease;
        position: relative;
        min-width: 0;
        overflow: hidden;
      }
      .ws-stacked-seg-label {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 0.65rem;
        font-weight: 700;
        color: #fff;
        white-space: nowrap;
        pointer-events: none;
        text-shadow: 0 1px 2px rgba(0,0,0,0.4);
      }
      .ws-formula-card {
        background: var(--card-bg, #ffffff);
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        padding: 20px 24px;
        margin-top: 0;
      }
      .ws-formula-title {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-secondary, #6b7280);
        margin: 0 0 12px 0;
      }
      .ws-formula-expr {
        font-family: 'Courier New', monospace;
        font-size: 0.88rem;
        background: var(--code-bg, #f3f4f6);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        line-height: 1.7;
        word-break: break-word;
      }
      .ws-score-readout {
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
      }
      .ws-score-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary, #1a237e);
        font-variant-numeric: tabular-nums;
      }
      .ws-score-label {
        font-size: 0.85rem;
        color: var(--text-secondary, #6b7280);
      }
    `;
    document.head.appendChild(style);
  }

  // ─── HELPERS ──────────────────────────────────────────────────────────────

  function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }

  function el(tag, attrs, ...children) {
    const node = document.createElement(tag);
    if (attrs) Object.entries(attrs).forEach(([k, v]) => {
      if (k === 'style' && typeof v === 'object') Object.assign(node.style, v);
      else if (k.startsWith('data-')) node.dataset[k.slice(5)] = v;
      else node[k] = v;
    });
    children.forEach(c => {
      if (c == null) return;
      node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    });
    return node;
  }

  // ─── MAIN INIT ────────────────────────────────────────────────────────────

  function initWeightSlider(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    injectStyles();

    // Mutable state
    const weights = FACTORS.map(f => f.defaultWeight);

    // ── Build DOM ──────────────────────────────────────────────────────────

    const root = el('div', { className: 'ws-root' });

    // Two-column comparison
    const columns = el('div', { className: 'ws-columns' });

    // ── LEFT: Credit Score (interactive) ──────────────────────────────────
    const leftCard = el('div', { className: 'ws-card' });
    leftCard.appendChild(el('p', { className: 'ws-card-title' }, 'Your Credit Score'));

    const sliders = [];
    const pctLabels = [];

    FACTORS.forEach((factor, i) => {
      const row = el('div', { className: 'ws-row' });

      const dot = el('span', {
        style: {
          display: 'inline-block',
          width: '10px', height: '10px',
          borderRadius: '50%',
          background: factor.color,
          flexShrink: '0',
        },
      });

      const label = el('span', { className: 'ws-label' }, factor.label);
      const labelWrap = el('span', {
        style: { display: 'flex', alignItems: 'center', gap: '6px', flex: '0 0 152px' },
      }, dot, label);

      const sliderWrap = el('div', { className: 'ws-slider-wrap' });
      const slider = el('input', {
        type: 'range',
        min: 0, max: 100,
        value: factor.defaultWeight,
        className: 'ws-slider',
        style: { '--thumb-color': factor.color },
      });
      // Inline CSS variable for thumb color (works via style attribute on modern browsers)
      slider.style.setProperty('--thumb-color', factor.color);
      sliderWrap.appendChild(slider);

      const pct = el('span', { className: 'ws-pct', style: { color: factor.color } },
        factor.defaultWeight + '%');

      row.append(labelWrap, sliderWrap, pct);
      leftCard.appendChild(row);

      sliders.push(slider);
      pctLabels.push(pct);
    });

    // Warning line
    const warningEl = el('div', { className: 'ws-warning' });
    leftCard.appendChild(warningEl);

    // Stacked bar (credit)
    leftCard.appendChild(el('div', { className: 'ws-stacked-label' }, 'Weight Composition'));
    const stackedBarLeft = el('div', { className: 'ws-stacked-bar' });
    const leftSegs = FACTORS.map(f => {
      const seg = el('div', { className: 'ws-stacked-seg', style: { background: f.color } });
      const segLabel = el('span', { className: 'ws-stacked-seg-label' });
      seg.appendChild(segLabel);
      stackedBarLeft.appendChild(seg);
      return { seg, segLabel };
    });
    leftCard.appendChild(stackedBarLeft);

    columns.appendChild(leftCard);

    // ── RIGHT: School Grade (static) ──────────────────────────────────────
    const rightCard = el('div', { className: 'ws-card' });
    rightCard.appendChild(el('p', { className: 'ws-card-title' }, 'Your School Grade'));

    GRADE_FACTORS.forEach(gf => {
      const row = el('div', { className: 'ws-row' });

      const dot = el('span', {
        style: {
          display: 'inline-block', width: '10px', height: '10px',
          borderRadius: '50%', background: gf.color, flexShrink: '0',
        },
      });
      const label = el('span', { className: 'ws-label' }, gf.label);
      const labelWrap = el('span', {
        style: { display: 'flex', alignItems: 'center', gap: '6px', flex: '0 0 152px' },
      }, dot, label);

      const barWrap = el('div', { className: 'ws-static-bar' });
      const fill = el('div', {
        className: 'ws-static-fill',
        style: { width: gf.weight + '%', background: gf.color },
      });
      barWrap.appendChild(fill);

      const pct = el('span', { className: 'ws-pct', style: { color: gf.color } }, gf.weight + '%');

      row.append(labelWrap, barWrap, pct);
      rightCard.appendChild(row);
    });

    // Static stacked bar (grade)
    rightCard.appendChild(el('div', { className: 'ws-stacked-label' }, 'Weight Composition'));
    const stackedBarRight = el('div', { className: 'ws-stacked-bar' });
    GRADE_FACTORS.forEach(gf => {
      const seg = el('div', { className: 'ws-stacked-seg', style: { background: gf.color, width: gf.weight + '%' } });
      const segLabel = el('span', { className: 'ws-stacked-seg-label' }, gf.weight + '%');
      seg.appendChild(segLabel);
      stackedBarRight.appendChild(seg);
    });
    rightCard.appendChild(stackedBarRight);

    columns.appendChild(rightCard);
    root.appendChild(columns);

    // ── Formula + Score Card ───────────────────────────────────────────────
    const formulaCard = el('div', { className: 'ws-formula-card' });
    formulaCard.appendChild(el('p', { className: 'ws-formula-title' }, 'Weighted Score Formula'));

    const formulaExpr = el('div', { className: 'ws-formula-expr' });
    formulaCard.appendChild(formulaExpr);

    const scoreReadout = el('div', { className: 'ws-score-readout' });
    const scoreValue   = el('span', { className: 'ws-score-value' });
    const scoreLabel   = el('span', { className: 'ws-score-label' }, 'weighted score (out of 100)');
    scoreReadout.append(scoreValue, scoreLabel);
    formulaCard.appendChild(scoreReadout);

    root.appendChild(formulaCard);
    container.appendChild(root);

    // ── Reactivity ────────────────────────────────────────────────────────

    function computeScore(ws) {
      return ws.reduce((sum, w, i) => sum + (w / 100) * FACTORS[i].sampleValue, 0);
    }

    function buildFormulaHTML(ws) {
      const total = ws.reduce((a, b) => a + b, 0);
      const terms = FACTORS.map((f, i) =>
        `<span style="color:${f.color};font-weight:700">${ws[i]}%</span>×${f.sampleValue}`
      ).join(' + ');
      const score = computeScore(ws);
      return `Score = ${terms}<br>
      = ${ws.map((w, i) => ((w / 100) * FACTORS[i].sampleValue).toFixed(1)).join(' + ')}<br>
      = <strong>${score.toFixed(1)}</strong> &nbsp;(weights total: ${total}%)`;
    }

    function render() {
      const total = weights.reduce((a, b) => a + b, 0);

      // Update slider percentage labels
      weights.forEach((w, i) => {
        pctLabels[i].textContent = w + '%';
      });

      // Warning
      if (total !== 100) {
        warningEl.textContent = `Weights sum to ${total}% — adjust to reach exactly 100%.`;
      } else {
        warningEl.textContent = '';
      }

      // Stacked bar segments (use actual weights, not normalized for visual honesty)
      // Show proportional of total so bar always fills 100% visually
      leftSegs.forEach(({ seg, segLabel }, i) => {
        const pct = total > 0 ? (weights[i] / total) * 100 : 0;
        seg.style.width = pct.toFixed(1) + '%';
        segLabel.textContent = weights[i] > 3 ? weights[i] + '%' : '';
      });

      // Formula + score
      formulaExpr.innerHTML = buildFormulaHTML(weights);
      const score = computeScore(weights);
      scoreValue.textContent = score.toFixed(1);
    }

    // Slider event wiring
    sliders.forEach((slider, changedIdx) => {
      slider.addEventListener('input', () => {
        const newVal = parseInt(slider.value, 10);
        const oldVal = weights[changedIdx];
        const delta  = newVal - oldVal;

        if (delta === 0) return;

        weights[changedIdx] = newVal;

        // Proportionally redistribute delta across other sliders
        const others = FACTORS
          .map((_, i) => i)
          .filter(i => i !== changedIdx);
        const otherTotal = others.reduce((s, i) => s + weights[i], 0);

        if (otherTotal > 0) {
          let remainder = -delta;
          others.forEach((i, pos) => {
            const share = pos < others.length - 1
              ? Math.round((weights[i] / otherTotal) * (-delta))
              : remainder;
            const adjusted = clamp(weights[i] + share, 0, 100);
            remainder -= (adjusted - weights[i]);
            weights[i] = adjusted;
          });
        }

        // Sync slider DOM values
        sliders.forEach((s, i) => { s.value = weights[i]; });

        render();
      });
    });

    // Initial render
    render();
  }

  // ─── AUTO-INIT ────────────────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('weight-slider-container')) {
      initWeightSlider('weight-slider-container');
    }
  });

  // Expose for manual init
  window.initWeightSlider = initWeightSlider;

}());
