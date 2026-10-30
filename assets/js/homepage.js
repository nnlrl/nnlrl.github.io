/* Progressive enhancement: all profile content is readable without JavaScript. */
(() => {
  const root = document.documentElement;
  const navLinks = [...document.querySelectorAll('.primary-nav a[href^="#"]')];
  const themeButton = document.querySelector('#theme-toggle');
  const motionButton = document.querySelector('#motion-toggle');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const save = (key, value) => {
    try { localStorage.setItem(key, value); } catch { /* Keep the controls usable without storage. */ }
  };

  function setTheme(theme) {
    const dark = theme === 'dark';
    root.dataset.theme = theme;
    themeButton.textContent = dark ? '☼ Day' : '☾ Night';
    themeButton.setAttribute('aria-pressed', String(dark));
    themeButton.setAttribute('aria-label', dark ? 'Switch to day theme' : 'Switch to night theme');
    document.querySelector('meta[name="theme-color"]').content = dark ? '#202322' : '#f6f7f6';
  }
  setTheme(root.dataset.theme);
  themeButton.addEventListener('click', () => {
    setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
    save('jing-wang-theme', root.dataset.theme);
  });

  function setMotion(enabled) {
    const active = enabled && !reducedMotion.matches;
    root.dataset.motion = active ? 'on' : 'off';
    motionButton.textContent = active ? 'Motion on' : 'Motion off';
    motionButton.setAttribute('aria-pressed', String(active));
    motionButton.disabled = reducedMotion.matches;
  }
  setMotion(root.dataset.motion !== 'off');
  motionButton.addEventListener('click', () => {
    setMotion(root.dataset.motion !== 'on');
    save('jing-wang-motion', root.dataset.motion);
  });
  reducedMotion.addEventListener('change', () => setMotion(!reducedMotion.matches));

  // The fixed background uses small opacity-only stars, with no external assets or animation library.
  const starField = document.querySelector('.stars');
  const stars = document.createDocumentFragment();
  let seed = 0x4a57;
  const random = () => {
    seed = (1664525 * seed + 1013904223) >>> 0;
    return seed / 4294967296;
  };
  for (let index = 0; index < 192; index++) {
    const star = document.createElement('i');
    star.className = 'star';
    star.style.setProperty('--x', `${(random() * 100).toFixed(3)}%`);
    star.style.setProperty('--y', `${(random() * 100).toFixed(3)}%`);
    star.style.setProperty('--duration', `${(4 + random() * 4).toFixed(2)}s`);
    star.style.setProperty('--delay', `${(-random() * 8).toFixed(2)}s`);
    stars.append(star);
  }
  starField?.append(stars);
  document.addEventListener('visibilitychange', () => {
    root.dataset.visibility = document.hidden ? 'hidden' : 'visible';
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
  const sections = [...document.querySelectorAll('.section-card')];
  let navigationFrame = null;
  function updateActiveSection() {
    navigationFrame = null;
    const readingLine = document.querySelector('.terminal-nav').getBoundingClientRect().bottom + 36;
    const current = sections.filter(section => section.getBoundingClientRect().top <= readingLine).pop();
    markActive(current?.id || 'about');
  }
  function queueNavigationUpdate() {
    if (navigationFrame === null) navigationFrame = requestAnimationFrame(updateActiveSection);
  }
  window.addEventListener('scroll', queueNavigationUpdate, { passive: true });
  window.addEventListener('resize', queueNavigationUpdate);
  window.addEventListener('pageshow', queueNavigationUpdate);
  queueNavigationUpdate();

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
