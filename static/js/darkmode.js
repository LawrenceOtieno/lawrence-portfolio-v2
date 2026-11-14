(function () {
  const stored = localStorage.getItem('darkMode');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initial = stored === 'enabled' || (stored === null && prefersDark);

  if (initial) document.documentElement.classList.add('dark');

  function toggle() {
    const on = document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', on ? 'enabled' : 'disabled');
  }

  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('dark-toggle');
    if (btn) btn.addEventListener('click', toggle);

    const menu = document.getElementById('mobile-menu');
    const openBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('menu-close');

    if (menu && openBtn) {
      openBtn.addEventListener('click', () => {
        menu.classList.remove('hidden');
        menu.classList.add('flex');
        openBtn.setAttribute('aria-expanded', 'true');
      });
    }
    if (menu && closeBtn) {
      closeBtn.addEventListener('click', () => {
        menu.classList.add('hidden');
        menu.classList.remove('flex');
        openBtn.setAttribute('aria-expanded', 'false');
      });
    }
    document.querySelectorAll('.mobile-link').forEach(a => {
      a.addEventListener('click', () => {
        menu.classList.add('hidden');
        menu.classList.remove('flex');
        openBtn.setAttribute('aria-expanded', 'false');
      });
    });
  });
})();