// Apply appearance before the stylesheet paints; task and media state are untouched.
(() => {
  let selected;
  try { selected = localStorage.getItem('genjustsu.theme'); } catch {}
  document.documentElement.dataset.theme = ['light', 'dark'].includes(selected)
    ? selected : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
})();
