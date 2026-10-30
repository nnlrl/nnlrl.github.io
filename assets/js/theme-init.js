// Apply the saved theme before the first paint. Reading storage may fail in private browsing.
(() => {
  const root = document.documentElement;
  try {
    root.dataset.theme = localStorage.getItem('jing-wang-theme') === 'light' ? 'light' : 'dark';
    root.dataset.motion = localStorage.getItem('jing-wang-motion') === 'off' ? 'off' : 'on';
  } catch {
    root.dataset.theme = 'dark';
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) root.dataset.motion = 'off';
})();
