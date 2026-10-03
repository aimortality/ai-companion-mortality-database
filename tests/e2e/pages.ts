export const PAGES = ['/index.html', '/report.html', '/index-academic.html', '/methodology.html', '/verification-standards.html'];

// Netlify's Pretty URLs rewrites internal "x.html" links to "/x" in the served HTML, and both forms
// resolve (see the URL contract in netlify.toml). A link assertion must accept either form while still
// pinning WHICH page it points at: '/methodology.html' -> /^\/methodology(\.html)?$/.
export const hrefBoth = (htmlPath: string): RegExp =>
  new RegExp('^' + htmlPath.replace(/\.html$/, '').replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&') + '(\\.html)?$');
// The same, as a CSS selector for locating links by target.
export const linkTo = (htmlPath: string): string => {
  const bare = htmlPath.replace(/\.html$/, '');
  return `a[href="${bare}.html"], a[href="${bare}"]`;
};
