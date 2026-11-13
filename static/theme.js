// Migrate browser preferences once, before the stylesheet paints.
(() => {
  let selected;
  try {
    for (const name of ['theme', 'language', 'lastTask']) {
      const current = 'henge.' + name;
      const legacy = 'genjustsu.' + name;
      if (localStorage.getItem(current) === null && localStorage.getItem(legacy) !== null) {
        localStorage.setItem(current, localStorage.getItem(legacy));
      }
      localStorage.removeItem(legacy);
    }
    selected = localStorage.getItem('henge.theme');
  } catch {}
  document.documentElement.dataset.theme = ['light', 'dark'].includes(selected)
    ? selected : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
})();
