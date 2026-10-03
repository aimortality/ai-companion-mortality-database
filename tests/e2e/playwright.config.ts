import { defineConfig } from '@playwright/test';
// BASE_URL unset: serve the local build. Set BASE_URL=https://deploy-preview-N--aimortality.netlify.app
// to run the same specs against a Netlify deploy preview (real headers, redirects, pretty URLs).
const local = !process.env.BASE_URL;
export default defineConfig({
  testDir: '.',
  use: { baseURL: process.env.BASE_URL ?? 'http://127.0.0.1:8765' },
  webServer: local
    ? { command: 'python3 -m http.server 8765 --directory ../../dist', url: 'http://127.0.0.1:8765/index.html', reuseExistingServer: true, stderr: 'ignore' }
    : undefined,
  projects: [{ name: 'chromium', use: { browserName: 'chromium' } }],
});
