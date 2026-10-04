// Google Analytics (GA4) configuration. Loaded right after the async gtag.js loader tag in
// templates/partials/analytics.html. It is a file, not an inline <script>, so the
// Content-Security-Policy in netlify.toml can keep script-src free of 'unsafe-inline'.
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-SS2VTGZ004');
