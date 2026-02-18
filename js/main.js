/**
 * main.js
 * Mathematics for AI — Interactive slide companion
 *
 * Features:
 *   1. Mobile navigation toggle
 *   2. Scroll spy (IntersectionObserver)
 *   3. Smooth scroll with fixed-nav offset
 *   4. Scroll-triggered reveal animations
 *   5. Navbar background on scroll
 *   6. KaTeX auto-render initialization
 */

document.addEventListener('DOMContentLoaded', () => {

  // ─── 1. MOBILE NAVIGATION TOGGLE ───────────────────────────────────────────

  const navToggle = document.querySelector('.nav-toggle');
  const navLinks  = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    // Toggle menu open/closed on hamburger click
    navToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('active');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Close menu when any nav link is clicked
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });

    // Close menu when clicking outside the nav
    document.addEventListener('click', (e) => {
      const navbar = document.querySelector('#navbar');
      if (navbar && !navbar.contains(e.target)) {
        navLinks.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }


  // ─── 2. SCROLL SPY ─────────────────────────────────────────────────────────
  // Highlights the nav link corresponding to the section currently in view.

  const spyLinks = navLinks
    ? Array.from(navLinks.querySelectorAll('a[href^="#"]'))
    : [];

  const setActiveLink = (id) => {
    spyLinks.forEach(link => {
      if (link.getAttribute('href') === `#${id}`) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  };

  if (spyLinks.length > 0) {
    // Collect all sections that have a matching nav link
    const spySections = spyLinks
      .map(link => document.querySelector(link.getAttribute('href')))
      .filter(Boolean);

    const spyObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setActiveLink(entry.target.id);
          }
        });
      },
      { threshold: 0.3 }
    );

    spySections.forEach(section => spyObserver.observe(section));
  }


  // ─── 3. SMOOTH SCROLL WITH FIXED-NAV OFFSET ────────────────────────────────
  // Intercepts anchor clicks and scrolls with a ~64 px offset for the fixed nav.

  const NAV_HEIGHT = 64; // px — matches #navbar height in CSS

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (!targetId || targetId === '#') return;

      const target = document.querySelector(targetId);
      if (!target) return;

      e.preventDefault();

      const targetTop = target.getBoundingClientRect().top + window.scrollY - NAV_HEIGHT;

      window.scrollTo({ top: targetTop, behavior: 'smooth' });

      // Close mobile menu after navigation
      if (navLinks) {
        navLinks.classList.remove('active');
        if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  });


  // ─── 4. SCROLL-TRIGGERED REVEAL ANIMATIONS ─────────────────────────────────
  // Adds .visible to .scroll-reveal elements when they enter the viewport.
  // Each element animates only once.

  const revealElements = document.querySelectorAll('.scroll-reveal');

  if (revealElements.length > 0) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target); // animate once
          }
        });
      },
      { threshold: 0.1 }
    );

    revealElements.forEach(el => revealObserver.observe(el));
  }


  // ─── 5. NAVBAR BACKGROUND ON SCROLL ────────────────────────────────────────
  // Adds .scrolled to #navbar once the user scrolls past 50 % of the hero.

  const navbar = document.querySelector('#navbar');
  const hero   = document.querySelector('#hero');

  if (navbar && hero) {
    let ticking = false;

    const updateNavbar = () => {
      const heroThreshold = hero.offsetHeight * 0.5;
      if (window.scrollY > heroThreshold) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
      ticking = false;
    };

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(updateNavbar);
        ticking = true;
      }
    }, { passive: true });

    // Run once on load in case the page starts mid-scroll
    updateNavbar();
  }


  // ─── 6. KATEX AUTO-RENDER ──────────────────────────────────────────────────
  // Renders all $…$ and $$…$$ math in the document using KaTeX auto-render.

  if (typeof renderMathInElement === 'function') {
    renderMathInElement(document.body, {
      delimiters: [
        { left: '$$', right: '$$', display: true  },
        { left: '$',  right: '$',  display: false }
      ],
      throwOnError: false   // degrade gracefully if a formula is malformed
    });
  }

});
