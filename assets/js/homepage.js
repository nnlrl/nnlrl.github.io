/* Progressive enhancement: all profile content is readable without JavaScript. */
(() => {
  document.querySelector('.language-link').addEventListener('click', function() {
    const next = new URL(this.href);
    next.hash = location.hash;
    this.href = next.href;
  });
  document.querySelector('[data-print]').addEventListener('click', () => window.print());
  let closed = [];
  addEventListener('beforeprint', () => {
    closed = [...document.querySelectorAll('details:not([open])')];
    closed.forEach(item => item.open = true);
  });
  addEventListener('afterprint', () => {
    closed.forEach(item => item.open = false);
    closed = [];
  });
  const sections = [...document.querySelectorAll('main section[id]')];
  const links = [...document.querySelectorAll('.page-nav a[href^="#"]')];
  let frame;
  function update() {
    frame = null;
    const threshold = document.querySelector('.topbar').getBoundingClientRect().bottom + 40;
    const active = sections.filter(section => section.getBoundingClientRect().top <= threshold).pop()?.id || 'about';
    links.forEach(link => {
      if(link.hash === '#' + active) link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    });
  }
  function queue() { if(frame == null) frame = requestAnimationFrame(update); }
  addEventListener('scroll',queue,{passive:true});
  addEventListener('resize',queue);
  addEventListener('pageshow',queue);
  queue();
})();
