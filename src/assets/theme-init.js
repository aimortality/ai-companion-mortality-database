// Applies a SAVED theme before first paint. The OS preference needs no script: each page's CSS
// @media (prefers-color-scheme) rules handle it. Loaded synchronously at the end of <head>; keep it tiny.
(function () {
  try {
    var t = localStorage.getItem('theme');
    if (t === 'dark' || t === 'light') document.documentElement.dataset.theme = t;
  } catch (e) { /* storage blocked: the OS preference applies */ }
})();
