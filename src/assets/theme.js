// Theme toggle. Static label ("Dark theme"); state lives in aria-pressed. Storage may be blocked
// (private mode, blocked site data): every access is guarded so the toggle still works per page.
(function () {
  var KEY = 'theme';
  var root = document.documentElement;
  var toggle = document.getElementById('theme-toggle');
  if (!toggle) return;
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function system() { return media && media.matches ? 'dark' : 'light'; }
  function stored() {
    try { var v = localStorage.getItem(KEY); return v === 'dark' || v === 'light' ? v : null; } catch (e) { return null; }
  }
  function current() { return root.dataset.theme || system(); }
  function sync() { toggle.setAttribute('aria-pressed', current() === 'dark' ? 'true' : 'false'); }
  toggle.addEventListener('click', function () {
    var next = current() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem(KEY, next); } catch (e) {}
    sync();
  });
  if (media && media.addEventListener) media.addEventListener('change', function () { if (!stored()) sync(); });
  window.addEventListener('storage', function (e) {      // another tab changed it
    if (e.key !== KEY) return;
    if (e.newValue === 'dark' || e.newValue === 'light') root.dataset.theme = e.newValue;
    else delete root.dataset.theme;
    sync();
  });
  sync();
})();
