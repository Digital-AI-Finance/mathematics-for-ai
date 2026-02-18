/**
 * use-skip.js
 * Mathematics for AI — "USE IT or SKIP IT" interactive exercise
 *
 * Renders into a container with id="use-skip-container".
 * Call: initUseSkip('use-skip-container')
 */

(function () {
  'use strict';

  // ─── DATA ────────────────────────────────────────────────────────────────────

  const DATA_CATEGORIES = [
    {
      name: 'Income',
      icon: '💰',
      description: 'How much money you earn',
      bankVerdict: 'USE IT',
      bankLabel: 'Most banks',
      ethicsVerdict: 'USE IT',
      ethicsNote: 'Generally fair'
    },
    {
      name: 'Payment History',
      icon: '🧾',
      description: 'Whether you pay bills on time',
      bankVerdict: 'USE IT',
      bankLabel: 'Most banks',
      ethicsVerdict: 'USE IT',
      ethicsNote: 'Fair'
    },
    {
      name: 'Social Media Friends',
      icon: '👥',
      description: 'How many friends / followers you have',
      bankVerdict: 'USE IT',
      bankLabel: 'Some companies have tried',
      ethicsVerdict: 'SKIP IT',
      ethicsNote: 'Unfair — not related to creditworthiness'
    },
    {
      name: 'Zip Code',
      icon: '📮',
      description: 'Where you live',
      bankVerdict: 'USE IT',
      bankLabel: 'Many banks',
      ethicsVerdict: 'SKIP IT',
      ethicsNote: 'Controversial — can encode racial bias'
    },
    {
      name: 'GPA',
      icon: '🎓',
      description: 'Your school grades',
      bankVerdict: 'USE IT',
      bankLabel: 'Some lenders',
      ethicsVerdict: 'SKIP IT',
      ethicsNote: 'Debatable'
    },
    {
      name: 'Shopping Habits',
      icon: '🛍️',
      description: 'What you buy (luxury vs. budget)',
      bankVerdict: 'USE IT',
      bankLabel: 'Some AI models',
      ethicsVerdict: 'SKIP IT',
      ethicsNote: 'Very controversial'
    },
    {
      name: 'Family Wealth',
      icon: '🏠',
      description: 'How much your parents have',
      bankVerdict: 'SKIP IT',
      bankLabel: 'Not legal in most countries',
      ethicsVerdict: 'SKIP IT',
      ethicsNote: 'Unfair'
    },
    {
      name: 'Age',
      icon: '🎂',
      description: 'How old you are',
      bankVerdict: 'USE IT',
      bankLabel: 'Used indirectly',
      ethicsVerdict: 'SKIP IT',
      ethicsNote: 'Protected characteristic'
    }
  ];

  // ─── STYLES ──────────────────────────────────────────────────────────────────

  const CSS = `
    .us-wrapper {
      font-family: inherit;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1.5rem;
      padding: 1rem 0 2rem;
    }
    .us-progress {
      font-size: 0.85rem;
      color: #888;
      letter-spacing: 0.05em;
    }
    .us-stage {
      position: relative;
      width: 100%;
      max-width: 420px;
      min-height: 220px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .us-card {
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.10);
      padding: 2rem 2rem 1.75rem;
      width: 100%;
      max-width: 420px;
      text-align: center;
      transition: transform 0.45s cubic-bezier(.4,0,.2,1),
                  opacity 0.45s ease,
                  box-shadow 0.3s ease;
      position: absolute;
      top: 0; left: 0;
      box-sizing: border-box;
    }
    .us-card.exit-right {
      transform: translateX(120%) rotate(12deg);
      opacity: 0;
      box-shadow: 0 0 32px rgba(0,137,123,0.45);
    }
    .us-card.exit-down {
      transform: translateY(100%) rotate(-8deg) scale(0.85);
      opacity: 0;
    }
    .us-card .us-icon {
      font-size: 3rem;
      line-height: 1;
      margin-bottom: 0.6rem;
    }
    .us-card .us-name {
      font-size: 1.35rem;
      font-weight: 700;
      color: #1a1a2e;
      margin: 0 0 0.4rem;
    }
    .us-card .us-desc {
      font-size: 0.95rem;
      color: #555;
      margin: 0;
      line-height: 1.5;
    }
    .us-buttons {
      display: flex;
      gap: 1rem;
      justify-content: center;
    }
    .us-btn {
      flex: 1;
      max-width: 160px;
      padding: 0.85rem 1rem;
      border: none;
      border-radius: 10px;
      font-size: 1rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      cursor: pointer;
      transition: transform 0.15s ease, box-shadow 0.15s ease, opacity 0.15s ease;
      outline: none;
    }
    .us-btn:active {
      transform: scale(0.96);
    }
    .us-btn-use {
      background: #00897b;
      color: #fff;
      box-shadow: 0 4px 14px rgba(0,137,123,0.35);
    }
    .us-btn-use:hover {
      background: #00796b;
      box-shadow: 0 6px 18px rgba(0,137,123,0.45);
      transform: translateY(-2px);
    }
    .us-btn-skip {
      background: #e74c3c;
      color: #fff;
      box-shadow: 0 4px 14px rgba(231,76,60,0.32);
    }
    .us-btn-skip:hover {
      background: #c0392b;
      box-shadow: 0 6px 18px rgba(231,76,60,0.42);
      transform: translateY(-2px);
    }
    .us-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }
    /* ── Summary ── */
    .us-summary {
      width: 100%;
      max-width: 480px;
      display: none;
      flex-direction: column;
      gap: 1.25rem;
      animation: usFadeIn 0.5s ease;
    }
    .us-summary.visible { display: flex; }
    @keyframes usFadeIn {
      from { opacity: 0; transform: translateY(16px); }
      to   { opacity: 1; transform: none; }
    }
    .us-summary-title {
      font-size: 1.2rem;
      font-weight: 700;
      color: #1a1a2e;
      text-align: center;
    }
    .us-columns {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }
    .us-col {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.08);
      padding: 1rem;
    }
    .us-col-header {
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin-bottom: 0.6rem;
    }
    .us-col-use .us-col-header  { color: #00897b; }
    .us-col-skip .us-col-header { color: #e74c3c; }
    .us-col ul {
      list-style: none;
      margin: 0; padding: 0;
      display: flex; flex-direction: column; gap: 0.3rem;
    }
    .us-col li {
      font-size: 0.85rem;
      color: #333;
      display: flex; align-items: center; gap: 0.35rem;
    }
    .us-comparison-section {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.08);
      padding: 1rem 1.25rem;
    }
    .us-comp-title {
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #888;
      margin-bottom: 0.7rem;
    }
    .us-comp-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.85rem;
      padding: 0.3rem 0;
      border-bottom: 1px solid #f0f0f0;
      gap: 0.5rem;
    }
    .us-comp-row:last-child { border-bottom: none; }
    .us-comp-name { color: #444; flex: 1; }
    .us-badge {
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.2em 0.55em;
      border-radius: 20px;
      white-space: nowrap;
    }
    .us-badge-use  { background: #e0f2f1; color: #00897b; }
    .us-badge-skip { background: #fdecea; color: #e74c3c; }
    .us-badge-match    { background: #e8f5e9; color: #388e3c; }
    .us-badge-mismatch { background: #fff3e0; color: #e65100; }
    .us-score-box {
      background: #1a1a2e;
      color: #fff;
      border-radius: 12px;
      padding: 1rem 1.25rem;
      text-align: center;
    }
    .us-score-box .us-score-num {
      font-size: 2rem;
      font-weight: 800;
    }
    .us-score-box .us-score-label {
      font-size: 0.9rem;
      color: #aab;
      margin-top: 0.2rem;
    }
    .us-bankbot {
      background: linear-gradient(135deg, #e0f2f1 0%, #f0f4ff 100%);
      border-left: 4px solid #00897b;
      border-radius: 10px;
      padding: 0.9rem 1.1rem;
      font-size: 0.9rem;
      color: #333;
      line-height: 1.55;
    }
    .us-bankbot strong { color: #00897b; }
    .us-restart-btn {
      align-self: center;
      background: transparent;
      border: 2px solid #1a1a2e;
      color: #1a1a2e;
      border-radius: 8px;
      padding: 0.55rem 1.4rem;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s, color 0.2s;
    }
    .us-restart-btn:hover {
      background: #1a1a2e;
      color: #fff;
    }
  `;

  // ─── INIT ────────────────────────────────────────────────────────────────────

  function initUseSkip(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Inject CSS once
    if (!document.getElementById('use-skip-style')) {
      const style = document.createElement('style');
      style.id = 'use-skip-style';
      style.textContent = CSS;
      document.head.appendChild(style);
    }

    renderGame(container);
  }

  // ─── GAME RENDERER ───────────────────────────────────────────────────────────

  function renderGame(container) {
    container.innerHTML = '';

    const userChoices = []; // array of { category, verdict: 'USE IT'|'SKIP IT' }
    let currentIndex = 0;
    let busy = false;

    // Wrapper
    const wrapper = el('div', 'us-wrapper');

    // Progress
    const progress = el('div', 'us-progress');
    updateProgress();

    // Stage (card slot)
    const stage = el('div', 'us-stage');

    // Buttons
    const btnRow = el('div', 'us-buttons');
    const btnUse  = el('button', 'us-btn us-btn-use',  'USE IT ✓');
    const btnSkip = el('button', 'us-btn us-btn-skip', 'SKIP IT ✗');
    btnRow.appendChild(btnUse);
    btnRow.appendChild(btnSkip);

    // Summary (hidden initially)
    const summary = el('div', 'us-summary');

    btnUse.addEventListener('click',  () => handleChoice('USE IT'));
    btnSkip.addEventListener('click', () => handleChoice('SKIP IT'));

    wrapper.appendChild(progress);
    wrapper.appendChild(stage);
    wrapper.appendChild(btnRow);
    wrapper.appendChild(summary);
    container.appendChild(wrapper);

    showCard(currentIndex, true);

    // ── helpers ──────────────────────────────────────────────────────────────

    function updateProgress() {
      progress.textContent = `Card ${Math.min(currentIndex + 1, DATA_CATEGORIES.length)} of ${DATA_CATEGORIES.length}`;
    }

    function showCard(index, instant) {
      // Remove any old card
      const old = stage.querySelector('.us-card');
      if (old && !instant) old.remove();
      if (old && instant) old.remove();

      if (index >= DATA_CATEGORIES.length) return;

      const cat = DATA_CATEGORIES[index];
      const card = el('div', 'us-card');
      card.innerHTML = `
        <div class="us-icon">${cat.icon}</div>
        <div class="us-name">${cat.name}</div>
        <p class="us-desc">${cat.description}</p>
      `;
      // Start off-screen if not instant, then animate in
      if (!instant) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(24px) scale(0.97)';
        stage.appendChild(card);
        // Trigger reflow then animate
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            card.style.transition = 'transform 0.35s cubic-bezier(.4,0,.2,1), opacity 0.35s ease';
            card.style.opacity = '1';
            card.style.transform = 'none';
          });
        });
      } else {
        stage.appendChild(card);
      }
    }

    function handleChoice(verdict) {
      if (busy) return;
      busy = true;
      setButtonsDisabled(true);

      userChoices.push({ category: DATA_CATEGORIES[currentIndex], verdict });

      const card = stage.querySelector('.us-card');
      if (card) {
        if (verdict === 'USE IT') {
          card.classList.add('exit-right');
        } else {
          card.classList.add('exit-down');
        }
      }

      currentIndex++;
      updateProgress();

      setTimeout(() => {
        if (currentIndex < DATA_CATEGORIES.length) {
          showCard(currentIndex, false);
          busy = false;
          setButtonsDisabled(false);
        } else {
          // Done — hide buttons, show summary
          btnRow.style.display = 'none';
          progress.textContent = 'All done!';
          showSummary(userChoices, summary);
          summary.classList.add('visible');
          busy = false;
        }
      }, 500);
    }

    function setButtonsDisabled(disabled) {
      btnUse.disabled  = disabled;
      btnSkip.disabled = disabled;
    }
  }

  // ─── SUMMARY ─────────────────────────────────────────────────────────────────

  function showSummary(choices, summaryEl) {
    summaryEl.innerHTML = '';

    const used   = choices.filter(c => c.verdict === 'USE IT');
    const skipped = choices.filter(c => c.verdict === 'SKIP IT');

    // Title
    summaryEl.appendChild(el('div', 'us-summary-title', 'Your Choices'));

    // Two-column list
    const cols = el('div', 'us-columns');
    const colUse  = el('div', 'us-col us-col-use');
    const colSkip = el('div', 'us-col us-col-skip');

    colUse.innerHTML  = `<div class="us-col-header">Used (${used.length})</div>`;
    colSkip.innerHTML = `<div class="us-col-header">Skipped (${skipped.length})</div>`;

    const ulUse  = el('ul'); used.forEach(c   => { const li = el('li'); li.innerHTML = `<span>${c.category.icon}</span>${c.category.name}`; ulUse.appendChild(li); });
    const ulSkip = el('ul'); skipped.forEach(c => { const li = el('li'); li.innerHTML = `<span>${c.category.icon}</span>${c.category.name}`; ulSkip.appendChild(li); });

    colUse.appendChild(ulUse);
    colSkip.appendChild(ulSkip);
    cols.appendChild(colUse);
    cols.appendChild(colSkip);
    summaryEl.appendChild(cols);

    // Comparison: what banks do
    summaryEl.appendChild(buildComparison(choices, 'bank'));

    // Comparison: what ethicists recommend
    summaryEl.appendChild(buildComparison(choices, 'ethics'));

    // Score
    let agreementCount = 0;
    choices.forEach(c => {
      if (c.verdict === c.category.ethicsVerdict) agreementCount++;
    });

    const scoreBox = el('div', 'us-score-box');
    scoreBox.innerHTML = `
      <div class="us-score-num">${agreementCount} / ${choices.length}</div>
      <div class="us-score-label">times you agreed with ethicists</div>
    `;
    summaryEl.appendChild(scoreBox);

    // BankBot comment
    const bankbot = el('div', 'us-bankbot');
    bankbot.innerHTML = `<strong>BankBot says:</strong> "Interesting choices. The hard part isn't the math — it's deciding what <em>should</em> go into the math."`;
    summaryEl.appendChild(bankbot);

    // Restart
    const restartBtn = el('button', 'us-restart-btn', 'Try again');
    restartBtn.addEventListener('click', () => {
      const container = summaryEl.closest('[id]');
      if (container) renderGame(container);
    });
    summaryEl.appendChild(restartBtn);
  }

  function buildComparison(choices, mode) {
    const section = el('div', 'us-comparison-section');
    const titleText = mode === 'bank'
      ? 'Compared to: what most banks do'
      : 'Compared to: what ethicists recommend';
    section.appendChild(el('div', 'us-comp-title', titleText));

    choices.forEach(c => {
      const referenceVerdict = mode === 'bank'
        ? c.category.bankVerdict
        : c.category.ethicsVerdict;
      const referenceNote = mode === 'bank'
        ? c.category.bankLabel
        : c.category.ethicsNote;
      const matches = c.verdict === referenceVerdict;

      const row = el('div', 'us-comp-row');

      const namePart = el('span', 'us-comp-name');
      namePart.innerHTML = `${c.category.icon} ${c.category.name}`;

      const refBadge = el('span', `us-badge ${referenceVerdict === 'USE IT' ? 'us-badge-use' : 'us-badge-skip'}`, referenceVerdict);

      const matchBadge = el('span', `us-badge ${matches ? 'us-badge-match' : 'us-badge-mismatch'}`, matches ? '✓ match' : '✗ differ');

      row.appendChild(namePart);
      row.appendChild(refBadge);
      row.appendChild(matchBadge);
      section.appendChild(row);
    });

    return section;
  }

  // ─── UTILITY ─────────────────────────────────────────────────────────────────

  function el(tag, className, textContent) {
    const node = document.createElement(tag);
    if (className)   node.className = className;
    if (textContent) node.textContent = textContent;
    return node;
  }

  // ─── AUTO-INIT ───────────────────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('use-skip-container')) {
      initUseSkip('use-skip-container');
    }
  });

  // Expose globally for manual calls
  window.initUseSkip = initUseSkip;

}());
