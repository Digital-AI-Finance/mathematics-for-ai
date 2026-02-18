/**
 * bankbot.js
 * Inline SVG generation for the BankBot character -- 8 emotional variants.
 *
 * BankBot: simple geometric robot mascot for "Mathematics for AI" talk.
 *   - Round head (circle), rectangular body, thin stick limbs
 *   - Amber tie (#ff8f00, site accent), XKCD-inspired line-art style
 *   - Dark stroke (#1a237e, site primary), white body, no other fills
 *   - ViewBox 0 0 120 180, scales to any requested pixel size
 *
 * Public API:
 *   createBankBot(state, size)  -- returns an SVG string
 *   injectBankBots()            -- replaces data-bankbot elements with SVGs
 */

/* eslint-disable max-len */
(function () {
  'use strict';

  // ── Design tokens (match style.css :root) ──────────────────────────────────
  var STROKE   = '#1a237e';
  var SW       = 2.5;          // stroke-width for all outlines
  var FILL_BODY = '#ffffff';
  var FILL_TIE  = '#ff8f00';   // var(--color-accent)
  var FILL_NONE = 'none';

  // ── Shared SVG building blocks ─────────────────────────────────────────────

  /** Open the <svg> tag with correct viewBox and requested size. */
  function svgOpen(size) {
    return '<svg xmlns="http://www.w3.org/2000/svg" ' +
      'viewBox="0 0 120 180" ' +
      'width="' + size + '" height="' + Math.round(size * 1.5) + '" ' +
      'role="img" aria-label="BankBot character">';
  }

  /** Shared stroke attributes string. */
  function s(extra) {
    return ' stroke="' + STROKE + '" stroke-width="' + SW + '" stroke-linecap="round" stroke-linejoin="round"' + (extra || '');
  }

  // ── Body parts (reusable across states) ────────────────────────────────────

  /** Head: circle at (60, 38) r=24. */
  function head() {
    return '<circle cx="60" cy="38" r="24" fill="' + FILL_BODY + '"' + s() + '/>';
  }

  /** Body: rounded rect from y=64 to y=120. */
  function body() {
    return '<rect x="38" y="64" width="44" height="56" rx="6" fill="' + FILL_BODY + '"' + s() + '/>';
  }

  /** Tie: small triangle hanging from the neckline. */
  function tie() {
    return '<polygon points="55,66 65,66 60,84" fill="' + FILL_TIE + '"' + s() + '/>';
  }

  /** Left leg: line from body bottom to foot. */
  function leftLeg() {
    return '<line x1="50" y1="120" x2="42" y2="160"' + s(' fill="' + FILL_NONE + '"') + '/>' +
           '<line x1="42" y1="160" x2="34" y2="160"' + s(' fill="' + FILL_NONE + '"') + '/>';
  }

  /** Right leg: line from body bottom to foot. */
  function rightLeg() {
    return '<line x1="70" y1="120" x2="78" y2="160"' + s(' fill="' + FILL_NONE + '"') + '/>' +
           '<line x1="78" y1="160" x2="86" y2="160"' + s(' fill="' + FILL_NONE + '"') + '/>';
  }

  /** Both legs (default neutral stance). */
  function legs() {
    return leftLeg() + rightLeg();
  }

  /** Neutral left arm: hangs down from shoulder. */
  function leftArmDown() {
    return '<line x1="38" y1="72" x2="22" y2="105"' + s(' fill="' + FILL_NONE + '"') + '/>';
  }

  /** Neutral right arm: hangs down from shoulder. */
  function rightArmDown() {
    return '<line x1="82" y1="72" x2="98" y2="105"' + s(' fill="' + FILL_NONE + '"') + '/>';
  }

  /** Both arms neutral. */
  function armsDown() {
    return leftArmDown() + rightArmDown();
  }

  /** Simple round eye at position (cx, cy). */
  function eye(cx, cy, r) {
    return '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r || 3.5) + '" fill="' + STROKE + '" stroke="none"/>';
  }

  /** Eye with visible pupil (white outer, dark inner). */
  function eyeWithPupil(cx, cy, outerR, pupilCx, pupilCy, pupilR) {
    return '<circle cx="' + cx + '" cy="' + cy + '" r="' + outerR + '" fill="' + FILL_BODY + '"' + s() + '/>' +
           '<circle cx="' + pupilCx + '" cy="' + pupilCy + '" r="' + pupilR + '" fill="' + STROKE + '" stroke="none"/>';
  }

  // ── State renderers ────────────────────────────────────────────────────────
  // Each returns the inner SVG elements (no outer <svg> tag).

  var states = {};

  // ─── 1. CONFIDENT ──────────────────────────────────────────────────────────
  // Big smile, eyes wide open, one arm raised in a wave, slight head tilt.
  states.confident = function () {
    return '' +
      // Slight head tilt via transform
      '<g transform="rotate(-4, 60, 38)">' +
        head() +
        // Wide open eyes
        eye(50, 35, 4) + eye(70, 35, 4) +
        // Big smile arc
        '<path d="M48,45 Q60,56 72,45" fill="' + FILL_NONE + '"' + s() + '/>' +
      '</g>' +
      body() + tie() +
      // Left arm raised waving
      '<line x1="38" y1="72" x2="16" y2="52"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      '<line x1="16" y1="52" x2="10" y2="42"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      // Right arm relaxed
      rightArmDown() +
      legs();
  };

  // ─── 2. COCKY ──────────────────────────────────────────────────────────────
  // Smirk (half-smile), one eyebrow raised (one eye higher), arms crossed.
  states.cocky = function () {
    return '' +
      head() +
      // Left eye normal, right eye slightly higher (raised brow)
      eye(50, 36, 3.5) +
      eye(70, 33, 3.5) +
      // Raised eyebrow line above right eye
      '<line x1="65" y1="27" x2="76" y2="25"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      // Smirk: asymmetric half-smile
      '<path d="M52,46 Q58,46 64,44 Q68,42 72,44" fill="' + FILL_NONE + '"' + s() + '/>' +
      body() + tie() +
      // Arms crossed over body
      '<line x1="38" y1="74" x2="72" y2="88"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      '<line x1="82" y1="74" x2="48" y2="88"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      legs();
  };

  // ─── 3. STRESSED ───────────────────────────────────────────────────────────
  // Wide eyes (bigger circles), wavy mouth, sweat drops, arms up.
  states.stressed = function () {
    return '' +
      head() +
      // Wide alarmed eyes
      eye(50, 35, 5) + eye(70, 35, 5) +
      // Tiny white highlights in eyes
      '<circle cx="48" cy="33" r="1.5" fill="' + FILL_BODY + '" stroke="none"/>' +
      '<circle cx="68" cy="33" r="1.5" fill="' + FILL_BODY + '" stroke="none"/>' +
      // Wavy worried mouth
      '<path d="M48,48 Q52,44 56,48 Q60,52 64,48 Q68,44 72,48" fill="' + FILL_NONE + '"' + s() + '/>' +
      // Sweat drops (light blue)
      '<circle cx="86" cy="28" r="2.5" fill="#64b5f6" stroke="none"/>' +
      '<circle cx="90" cy="38" r="2" fill="#64b5f6" stroke="none"/>' +
      body() + tie() +
      // Arms raised in panic
      '<line x1="38" y1="72" x2="14" y2="56"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      '<line x1="82" y1="72" x2="106" y2="56"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      legs();
  };

  // ─── 4. LEARNING ───────────────────────────────────────────────────────────
  // One hand on chin, eyes looking up-right, neutral mouth, thought bubbles.
  states.learning = function () {
    return '' +
      head() +
      // Eyes looking up-right (pupils offset)
      eyeWithPupil(50, 35, 4, 52, 33, 2) +
      eyeWithPupil(70, 35, 4, 72, 33, 2) +
      // Neutral slight mouth
      '<line x1="52" y1="47" x2="68" y2="47"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      // Thought bubble dots above head
      '<circle cx="82" cy="12" r="2" fill="' + STROKE + '" stroke="none"/>' +
      '<circle cx="88" cy="6" r="2.5" fill="' + STROKE + '" stroke="none"/>' +
      '<circle cx="96" cy="2" r="3" fill="' + STROKE + '" stroke="none"/>' +
      body() + tie() +
      // Left arm: hand on chin
      '<path d="M38,72 L26,62 L40,52" fill="' + FILL_NONE + '"' + s() + '/>' +
      // Right arm relaxed
      rightArmDown() +
      legs();
  };

  // ─── 5. HUMBLED ────────────────────────────────────────────────────────────
  // Small mouth (dot), eyes looking down, slight body slump, hands together.
  states.humbled = function () {
    return '' +
      // Slight downward tilt
      '<g transform="rotate(3, 60, 38)">' +
        head() +
        // Downcast eyes (pupils low)
        eyeWithPupil(50, 36, 3.5, 50, 38, 2) +
        eyeWithPupil(70, 36, 3.5, 70, 38, 2) +
        // Small dot mouth
        '<circle cx="60" cy="48" r="1.5" fill="' + STROKE + '" stroke="none"/>' +
      '</g>' +
      // Body shifted slightly down (slumped)
      '<g transform="translate(0, 2)">' +
        body() + tie() +
        // Hands together in front
        '<line x1="38" y1="74" x2="52" y2="100"' + s(' fill="' + FILL_NONE + '"') + '/>' +
        '<line x1="82" y1="74" x2="68" y2="100"' + s(' fill="' + FILL_NONE + '"') + '/>' +
        // Small clasped hands indicator
        '<circle cx="60" cy="102" r="3" fill="' + FILL_BODY + '"' + s() + '/>' +
      '</g>' +
      legs();
  };

  // ─── 6. OBSERVANT ──────────────────────────────────────────────────────────
  // Holding magnifying glass, small focused pupils, slight lean forward.
  states.observant = function () {
    return '' +
      // Slight lean forward
      '<g transform="rotate(-3, 60, 120)">' +
        head() +
        // Focused eyes: small centered pupils
        eyeWithPupil(50, 36, 4, 50, 36, 1.5) +
        eyeWithPupil(70, 36, 4, 70, 36, 1.5) +
        // Neutral focused mouth
        '<line x1="54" y1="47" x2="66" y2="47"' + s(' fill="' + FILL_NONE + '"') + '/>' +
        body() + tie() +
        // Left arm down
        leftArmDown() +
        // Right arm holding magnifying glass up
        '<line x1="82" y1="72" x2="100" y2="58"' + s(' fill="' + FILL_NONE + '"') + '/>' +
        // Magnifying glass: circle + handle
        '<circle cx="108" cy="48" r="10" fill="' + FILL_NONE + '"' + s() + '/>' +
        '<line x1="101" y1="55" x2="96" y2="60"' + s(' fill="' + FILL_NONE + '"') + '/>' +
        // Lens glint
        '<path d="M104,42 Q106,40 108,42" fill="' + FILL_NONE + '" stroke="' + STROKE + '" stroke-width="1.5" stroke-linecap="round"/>' +
      '</g>' +
      legs();
  };

  // ─── 7. CRITICAL ───────────────────────────────────────────────────────────
  // Arms crossed, one eyebrow up, straight-line mouth, skeptical head tilt.
  states.critical = function () {
    return '' +
      // Skeptical head tilt
      '<g transform="rotate(5, 60, 38)">' +
        head() +
        // Left eye normal
        eye(50, 36, 3.5) +
        // Right eye slightly narrowed (ellipse)
        '<ellipse cx="70" cy="36" rx="4" ry="2.5" fill="' + STROKE + '" stroke="none"/>' +
        // Raised left eyebrow
        '<line x1="44" y1="28" x2="56" y2="27"' + s(' fill="' + FILL_NONE + '"') + '/>' +
        // Straight skeptical mouth
        '<line x1="50" y1="47" x2="70" y2="47"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      '</g>' +
      body() + tie() +
      // Arms crossed (same as cocky but tighter)
      '<line x1="38" y1="76" x2="74" y2="90"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      '<line x1="82" y1="76" x2="46" y2="90"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      legs();
  };

  // ─── 8. WISE ───────────────────────────────────────────────────────────────
  // Graduation cap, gentle smile, one hand raised palm-up, confident posture.
  states.wise = function () {
    return '' +
      head() +
      // Graduation cap (mortarboard)
      '<rect x="36" y="13" width="48" height="4" rx="1" fill="' + STROKE + '" stroke="none"/>' +
      '<polygon points="60,6 36,17 84,17" fill="' + STROKE + '" stroke="none"/>' +
      // Tassel: line from right side of cap + small circle
      '<line x1="78" y1="15" x2="86" y2="24" stroke="' + FILL_TIE + '" stroke-width="2" stroke-linecap="round"/>' +
      '<circle cx="86" cy="26" r="2" fill="' + FILL_TIE + '" stroke="none"/>' +
      // Calm confident eyes
      eye(50, 36, 3) + eye(70, 36, 3) +
      // Gentle smile
      '<path d="M50,45 Q60,52 70,45" fill="' + FILL_NONE + '"' + s() + '/>' +
      body() + tie() +
      // Left arm down
      leftArmDown() +
      // Right arm raised, palm up (presenting)
      '<line x1="82" y1="72" x2="100" y2="60"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      '<line x1="100" y1="60" x2="108" y2="58"' + s(' fill="' + FILL_NONE + '"') + '/>' +
      // Open palm indicator
      '<path d="M106,54 Q110,56 108,60 Q106,62 102,62" fill="' + FILL_NONE + '"' + s() + '/>' +
      legs();
  };

  // ── Public API ─────────────────────────────────────────────────────────────

  /**
   * Create BankBot SVG string for a given emotional state.
   *
   * @param  {string} state - One of: confident, cocky, stressed, learning,
   *                          humbled, observant, critical, wise
   * @param  {number} [size=120] - Width in pixels (height = size * 1.5)
   * @return {string} Complete <svg> element as a string
   */
  function createBankBot(state, size) {
    size = size || 120;
    var key = String(state).toLowerCase().trim();
    var renderer = states[key];

    if (!renderer) {
      // Fallback: show confident if unknown state requested
      renderer = states.confident;
    }

    return svgOpen(size) + renderer() + '</svg>';
  }

  /**
   * Find every element with a `data-bankbot` attribute and replace its
   * innerHTML with the matching BankBot SVG.
   *
   * Reads `data-bankbot` for the emotional state and optional
   * `data-bankbot-size` for the width in pixels (default 120).
   */
  function injectBankBots() {
    var targets = document.querySelectorAll('[data-bankbot]');
    for (var i = 0; i < targets.length; i++) {
      var el    = targets[i];
      var state = el.getAttribute('data-bankbot');
      var size  = parseInt(el.getAttribute('data-bankbot-size'), 10) || 120;
      el.innerHTML = createBankBot(state, size);
    }
  }

  // ── Expose globally ────────────────────────────────────────────────────────
  window.createBankBot  = createBankBot;
  window.injectBankBots = injectBankBots;

  // ── Auto-inject on page load ───────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectBankBots);
  } else {
    // DOM already ready (script loaded with defer or at bottom of body)
    injectBankBots();
  }

})();
