/* Progressive enhancement: all profile content is readable without JavaScript. */
(() => {
  const toggle = document.querySelector('#menu-toggle');
  const menu = document.querySelector('#navbarResponsive');
  const navLinks = [...document.querySelectorAll('.navbar-nav a[href^="#"]')];

  function closeMenu() {
    menu?.classList.remove('is-open');
    toggle?.setAttribute('aria-expanded', 'false');
  }

  toggle?.addEventListener('click', () => {
    const opened = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(opened));
  });
  navLinks.forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.classList.contains('is-open')) {
      closeMenu();
      toggle.focus();
    }
  });

  // Preserve the current section when switching between the static language pages.
  const languageLink = document.querySelector('.language-switch');
  languageLink?.addEventListener('click', () => {
    const next = new URL(languageLink.href);
    next.hash = window.location.hash;
    languageLink.href = next.href;
  });

  function markActive(id) {
    navLinks.forEach(link => {
      const active = link.hash === `#${id}`;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  markActive(window.location.hash.slice(1) || 'about');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) markActive(entry.target.id);
      }
    }, { rootMargin: '-80px 0px -55% 0px', threshold: 0 });
    document.querySelectorAll('.section-card').forEach(section => observer.observe(section));
  }

  // Expand the complete publication list for the browser's Print / Save PDF action.
  let previouslyClosed = [];
  window.addEventListener('beforeprint', () => {
    previouslyClosed = [...document.querySelectorAll('details:not([open])')];
    previouslyClosed.forEach(details => { details.open = true; });
  });
  window.addEventListener('afterprint', () => {
    previouslyClosed.forEach(details => { details.open = false; });
    previouslyClosed = [];
  });
  document.querySelectorAll('[data-print]').forEach(button => {
    button.addEventListener('click', () => window.print());
  });
})();
