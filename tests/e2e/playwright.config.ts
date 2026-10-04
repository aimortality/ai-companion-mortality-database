import { defineConfig } from '@playwright/test';
// BASE_URL unset: build dist/ from the current checkout, then serve it. Set
// BASE_URL=https://deploy-preview-N--aimortality.netlify.app to run the same specs against a Netlify
// deploy preview (real headers, redirects, pretty URLs); no local server is started then.
//
// The local server is hermetic: it always builds first (the suite must test THIS checkout, not whatever
// dist/ was left behind) and never reuses a server it did not start (another worktree's server on the
// same port would silently serve a different tree). If port 8765 is taken, the run fails loudly.
const local = !process.env.BASE_URL;
export default defineConfig({
  testDir: '.',
  use: { baseURL: process.env.BASE_URL ?? 'http://127.0.0.1:8765' },
  webServer: local
    ? {
        command: "sh -c 'cd ../.. && .venv/bin/python build.py && exec python3 -m http.server 8765 --directory dist'",
        url: 'http://127.0.0.1:8765/index.html',
        reuseExistingServer: false,
        stderr: 'ignore',
      }
    : undefined,
  projects: [{ name: 'chromium', use: { browserName: 'chromium' } }],
});
