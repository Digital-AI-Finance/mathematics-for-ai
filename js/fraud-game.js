/**
 * fraud-game.js
 * "Spot the Fraud" -- interactive game widget for the Mathematics for AI site.
 *
 * Renders three scenario cards into #fraud-game-container.
 * Each card presents a transaction; the user votes Fraud or Legit,
 * then sees whether they were right plus a Bayesian explanation.
 *
 * Vanilla JS, no dependencies. ~280 lines.
 */

(function () {
  'use strict';

  /* ── Scenario data ──────────────────────────────────────────────────── */

  var SCENARIOS = [
    {
      id: 1,
      name: 'Alex',
      text: 'Alex, 17, buys a \u20ac900 electric guitar from an online shop in Berlin. Alex lives in Munich and has never bought anything over \u20ac100 before.',
      answer: 'legit',
      explanation: 'High amount + new merchant + different city = suspicious. But Alex saved birthday money for months. The AI flagged it, a human approved it. That is the system working.',
      bayesian: 'P(Fraud|unusual purchase) is higher, but P(birthday gift\u2011buying) is also plausible.'
    },
    {
      id: 2,
      name: 'Tomoko',
      text: 'Tomoko\u2019s card is used to buy 50 identical \u20ac25 gift cards at 3:00\u202fAM from a convenience store.',
      answer: 'fraud',
      explanation: '50 identical purchases + 3\u202fAM + gift cards = textbook fraud pattern. Stolen cards are often used to buy gift cards because they are untraceable. The AI would catch this in seconds.',
      bayesian: 'P(Fraud|50 gift cards at 3\u202fAM) \u2248 very high.'
    },
    {
      id: 3,
      name: 'Karla',
      text: 'Karla, a university student, has 4 small charges (\u20ac2\u20135 each) from 4 different countries in the same hour.',
      answer: 'fraud',
      explanation: 'Multiple countries in one hour is physically impossible. Small test charges are how criminals verify a stolen card before making big purchases. The AI catches this pattern instantly.',
      bayesian: 'P(Fraud|4 countries in 1 hour) \u2248 near certain.'
    }
  ];

  /* ── Inject scoped styles ───────────────────────────────────────────── */

  function injectStyles() {
    if (document.getElementById('fraud-game-styles')) return;
    var style = document.createElement('style');
    style.id = 'fraud-game-styles';
    style.textContent = [
      /* wrapper */
      '.fg-wrap{max-width:720px;margin:0 auto;font-family:var(--font-body,Inter,sans-serif)}',

      /* progress */
      '.fg-progress{text-align:center;font-size:.85rem;font-weight:600;color:var(--color-text-light,#616161);margin-bottom:var(--space-md,1rem)}',

      /* card */
      '.fg-card{background:var(--color-surface,#fff);border-radius:var(--radius-lg,16px);box-shadow:var(--shadow-md,0 4px 12px rgba(0,0,0,.1));overflow:hidden;margin-bottom:var(--space-lg,2rem);transition:opacity .35s ease,transform .35s ease}',
      '.fg-card.fg-hidden{display:none}',

      /* card header */
      '.fg-card-header{padding:var(--space-md,1rem) var(--space-lg,2rem);background:linear-gradient(135deg,var(--color-primary,#1a237e),var(--color-primary-light,#283593));color:#fff}',
      '.fg-card-header h3{margin:0;font-size:1.05rem;font-weight:700}',

      /* card body */
      '.fg-card-body{padding:var(--space-lg,2rem)}',
      '.fg-scenario-text{font-size:.95rem;line-height:1.65;color:var(--color-text,#212121);margin-bottom:var(--space-lg,2rem)}',

      /* buttons row */
      '.fg-buttons{display:flex;gap:var(--space-md,1rem);justify-content:center;flex-wrap:wrap}',
      '.fg-btn{padding:.65rem 2rem;border:none;border-radius:999px;font-size:.95rem;font-weight:700;cursor:pointer;transition:background .2s ease,transform .15s ease,box-shadow .2s ease;color:#fff;letter-spacing:.02em}',
      '.fg-btn:focus-visible{outline:2px solid var(--color-secondary,#00897b);outline-offset:3px}',
      '.fg-btn:active{transform:scale(.97)}',
      '.fg-btn-legit{background:#00897b}',
      '.fg-btn-legit:hover{background:#00796b;box-shadow:0 4px 14px rgba(0,137,123,.35)}',
      '.fg-btn-fraud{background:#e74c3c}',
      '.fg-btn-fraud:hover{background:#c0392b;box-shadow:0 4px 14px rgba(231,76,60,.35)}',

      /* disabled state after vote */
      '.fg-btn[disabled]{opacity:.45;cursor:default;transform:none;box-shadow:none}',
      '.fg-btn.fg-selected{opacity:1;box-shadow:0 0 0 3px rgba(255,255,255,.6),0 4px 14px rgba(0,0,0,.18);transform:scale(1.05)}',

      /* result card */
      '.fg-result{margin-top:var(--space-lg,2rem);padding:var(--space-lg,2rem);border-radius:var(--radius-md,8px);animation:fgFadeIn .4s ease both}',
      '.fg-result-correct{background:rgba(0,137,123,.08);border-left:4px solid #00897b}',
      '.fg-result-wrong{background:rgba(231,76,60,.08);border-left:4px solid #e74c3c}',

      '.fg-result-icon{font-size:1.6rem;margin-bottom:var(--space-sm,.5rem)}',
      '.fg-result-label{font-weight:700;font-size:1rem;margin-bottom:var(--space-sm,.5rem)}',
      '.fg-result-label.fg-correct-label{color:#00897b}',
      '.fg-result-label.fg-wrong-label{color:#e74c3c}',
      '.fg-result-explain{font-size:.9rem;line-height:1.6;color:var(--color-text-light,#616161);margin-bottom:var(--space-sm,.5rem)}',
      '.fg-result-bayesian{font-size:.8rem;font-style:italic;color:var(--color-text-light,#616161);opacity:.85}',

      /* next button */
      '.fg-next-row{text-align:center;margin-top:var(--space-md,1rem)}',
      '.fg-btn-next{padding:.55rem 2rem;border:none;border-radius:999px;font-size:.9rem;font-weight:700;cursor:pointer;color:#fff;background:var(--color-primary,#1a237e);transition:background .2s ease}',
      '.fg-btn-next:hover{background:var(--color-primary-light,#283593)}',

      /* summary card */
      '.fg-summary{text-align:center;padding:var(--space-xl,4rem) var(--space-lg,2rem);background:var(--color-surface,#fff);border-radius:var(--radius-lg,16px);box-shadow:var(--shadow-md,0 4px 12px rgba(0,0,0,.1));animation:fgFadeIn .5s ease both}',
      '.fg-summary-score{font-size:2rem;font-weight:700;color:var(--color-primary,#1a237e);margin-bottom:var(--space-sm,.5rem)}',
      '.fg-summary-msg{font-size:1rem;color:var(--color-text-light,#616161);line-height:1.5;margin-bottom:var(--space-lg,2rem)}',
      '.fg-btn-restart{padding:.55rem 2rem;border:none;border-radius:999px;font-size:.9rem;font-weight:700;cursor:pointer;color:#fff;background:var(--color-secondary,#00897b);transition:background .2s ease}',
      '.fg-btn-restart:hover{background:var(--color-secondary-light,#26a69a)}',

      /* animation */
      '@keyframes fgFadeIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}'
    ].join('\n');
    document.head.appendChild(style);
  }

  /* ── Helpers ─────────────────────────────────────────────────────────── */

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === 'className') { node.className = attrs[k]; }
        else if (k === 'textContent') { node.textContent = attrs[k]; }
        else if (k === 'innerHTML') { node.innerHTML = attrs[k]; }
        else { node.setAttribute(k, attrs[k]); }
      });
    }
    if (children) {
      children.forEach(function (c) { if (c) node.appendChild(c); });
    }
    return node;
  }

  /* ── Main init ──────────────────────────────────────────────────────── */

  function initFraudGame(containerId) {
    var container = document.getElementById(containerId);
    if (!container) return;
    injectStyles();

    var state = { current: 0, score: 0, voted: false };
    var wrap = el('div', { className: 'fg-wrap' });
    container.appendChild(wrap);

    render();

    /* ── Render current view ───────────────────────────────────────── */

    function render() {
      wrap.innerHTML = '';

      if (state.current >= SCENARIOS.length) {
        renderSummary();
        return;
      }

      var sc = SCENARIOS[state.current];

      /* Progress indicator */
      var progress = el('div', {
        className: 'fg-progress',
        textContent: 'Scenario ' + (state.current + 1) + ' of ' + SCENARIOS.length
      });
      wrap.appendChild(progress);

      /* Card */
      var card = el('div', { className: 'fg-card' });

      var header = el('div', { className: 'fg-card-header' }, [
        el('h3', { textContent: 'Scenario ' + sc.id + ': ' + sc.name })
      ]);
      card.appendChild(header);

      var body = el('div', { className: 'fg-card-body' });
      body.appendChild(el('p', { className: 'fg-scenario-text', textContent: sc.text }));

      /* Vote buttons */
      var btnLegit = el('button', { className: 'fg-btn fg-btn-legit', textContent: 'LEGIT', 'aria-label': 'Vote Legit' });
      var btnFraud = el('button', { className: 'fg-btn fg-btn-fraud', textContent: 'FRAUD', 'aria-label': 'Vote Fraud' });

      var buttonsRow = el('div', { className: 'fg-buttons' }, [btnLegit, btnFraud]);
      body.appendChild(buttonsRow);

      /* Result placeholder */
      var resultSlot = el('div');
      body.appendChild(resultSlot);

      card.appendChild(body);
      wrap.appendChild(card);

      /* If already voted (back from browser cache), skip interaction */
      if (state.voted) return;

      /* Click handlers */
      function vote(choice) {
        state.voted = true;
        var correct = choice === sc.answer;
        if (correct) state.score++;

        /* Disable buttons, highlight chosen */
        btnLegit.disabled = true;
        btnFraud.disabled = true;
        if (choice === 'legit') btnLegit.classList.add('fg-selected');
        else btnFraud.classList.add('fg-selected');

        /* Build result card */
        var resultClass = correct ? 'fg-result fg-result-correct' : 'fg-result fg-result-wrong';
        var iconText = correct ? '\u2713' : '\u2717';
        var labelText = correct ? 'Correct!' : 'Not quite!';
        var labelClass = correct ? 'fg-result-label fg-correct-label' : 'fg-result-label fg-wrong-label';

        var result = el('div', { className: resultClass }, [
          el('div', { className: 'fg-result-icon', textContent: iconText }),
          el('div', { className: labelClass, textContent: labelText }),
          el('p', { className: 'fg-result-explain', textContent: sc.explanation }),
          el('p', { className: 'fg-result-bayesian', innerHTML: '<strong>Bayesian hint:</strong> ' + sc.bayesian })
        ]);
        resultSlot.appendChild(result);

        /* Next / finish button */
        var isLast = state.current >= SCENARIOS.length - 1;
        var nextBtn = el('button', {
          className: 'fg-btn-next',
          textContent: isLast ? 'See Results' : 'Next Scenario \u2192'
        });
        var nextRow = el('div', { className: 'fg-next-row' }, [nextBtn]);
        resultSlot.appendChild(nextRow);

        nextBtn.addEventListener('click', function () {
          state.current++;
          state.voted = false;
          render();
        });
      }

      btnLegit.addEventListener('click', function () { vote('legit'); });
      btnFraud.addEventListener('click', function () { vote('fraud'); });
    }

    /* ── Summary screen ────────────────────────────────────────────── */

    function renderSummary() {
      var total = SCENARIOS.length;
      var s = state.score;

      var msg;
      if (s === total) {
        msg = 'Perfect score! You have serious fraud-detection instincts.';
      } else if (s >= 2) {
        msg = 'You got ' + s + '/' + total + ' \u2014 not bad! Even AI gets fooled sometimes.';
      } else if (s === 1) {
        msg = 'You got ' + s + '/' + total + ' \u2014 tricky, right? That is exactly why we need Bayesian reasoning.';
      } else {
        msg = 'You got ' + s + '/' + total + ' \u2014 do not worry, these are genuinely hard. The AI trains on millions of examples.';
      }

      var restartBtn = el('button', { className: 'fg-btn-restart', textContent: 'Play Again' });

      var summary = el('div', { className: 'fg-summary' }, [
        el('div', { className: 'fg-summary-score', textContent: s + ' / ' + total }),
        el('p', { className: 'fg-summary-msg', textContent: msg }),
        restartBtn
      ]);

      wrap.appendChild(summary);

      restartBtn.addEventListener('click', function () {
        state.current = 0;
        state.score = 0;
        state.voted = false;
        render();
      });
    }
  }

  /* ── Expose globally ────────────────────────────────────────────────── */
  window.initFraudGame = initFraudGame;

  /* ── Auto-init on DOMContentLoaded ──────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      if (document.getElementById('fraud-game-container')) {
        initFraudGame('fraud-game-container');
      }
    });
  } else {
    /* DOM already ready (script loaded with defer or at bottom) */
    if (document.getElementById('fraud-game-container')) {
      initFraudGame('fraud-game-container');
    }
  }

})();
