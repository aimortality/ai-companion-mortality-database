import { test as fixtureTest, expect as fixtureExpect } from './fixtures';
import { test as rawTest, expect, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { PAGES } from './pages';

// The policy under test is read from netlify.toml, so the repo has one source of truth and these
// tests exercise exactly the string Netlify will send.
const toml = readFileSync(join(__dirname, '..', '..', 'netlify.toml'), 'utf8');
const match = toml.match(/^\s*Content-Security-Policy\s*=\s*"([^"]+)"/m);
if (!match) throw new Error('netlify.toml has no Content-Security-Policy header line');
const CSP = match[1];

// Netlify deploy previews (and only previews; production does not do this) inject
// <script async src="/.netlify/scripts/cdp">, which frames https://app.netlify.com for the preview
// toolbar. Our policy blocks that frame, correctly: the policy is not widened for a tool that never
// reaches production. So the collectors ignore exactly that one violation: effective directive
// frame-src AND blocked origin https://app.netlify.com. Nothing broader.
const NETLIFY_TOOLBAR_ORIGIN = 'https://app.netlify.com';
const isToolbarFrame = (effectiveDirective: string, blockedURI: string): boolean => {
  let origin = '';
  try { origin = new URL(blockedURI).origin; } catch { /* not a URL (e.g. "inline"): not the toolbar */ }
  return effectiveDirective === 'frame-src' && origin === NETLIFY_TOOLBAR_ORIGIN;
};
// Chromium's console text for the same event: "Framing 'https://app.netlify.com/' violates ...
// 'frame-src' was not explicitly set, so 'default-src' is used as a fallback."
const isToolbarFrameMessage = (text: string): boolean => {
  const m = text.match(/^Framing '([^']+)' violates/);
  return !!m && /'frame-src'/.test(text) && isToolbarFrame('frame-src', m[1]);
};

// Two independent collectors: the console message Chromium prints for a violation, and the
// securitypolicyviolation DOM event (which carries the directive and the blocked URI).
async function collectViolations(page: Page): Promise<string[]> {
  const violations: string[] = [];
  page.on('console', (m) => {
    const text = m.text();
    if (/Content Security Policy/i.test(text) && !isToolbarFrameMessage(text)) violations.push(`console: ${text}`);
  });
  await page.addInitScript(() => {
    (window as any).__cspViolations = [];
    document.addEventListener('securitypolicyviolation', (e) => {
      (window as any).__cspViolations.push({ effective: e.effectiveDirective, violated: e.violatedDirective, blocked: e.blockedURI });
    });
  });
  return violations;
}

async function domViolations(page: Page): Promise<string[]> {
  const raw: { effective: string; violated: string; blocked: string }[] =
    await page.evaluate(() => (window as any).__cspViolations ?? []);
  return raw.filter((v) => !isToolbarFrame(v.effective, v.blocked)).map((v) => `${v.violated} blocked ${v.blocked}`);
}

// (a) Runs locally and on previews: the local server sends no headers, so attach the policy to the
// document response ourselves. Subresources are then judged by the browser under that policy.
fixtureTest.describe('CSP enforced on every page (header attached by the test)', () => {
  for (const path of PAGES) {
    fixtureTest(`${path}: zero violations, theme toggle still works`, async ({ page }) => {
      await page.route('**/*', async (route) => {
        if (route.request().resourceType() !== 'document') return route.fallback();
        const response = await route.fetch();
        await route.fulfill({ response, headers: { ...response.headers(), 'content-security-policy': CSP } });
      });
      const violations = await collectViolations(page);
      await page.emulateMedia({ colorScheme: 'light' });
      const response = await page.goto(path);
      // Positive control: the document the page actually received carries the policy, so a
      // route.fulfill that stopped attaching it cannot leave this test passing vacuously.
      fixtureExpect(response!.headers()['content-security-policy']).toBe(CSP);
      await page.waitForLoadState('load');
      const btn = page.locator('#theme-toggle');
      await fixtureExpect(btn).toHaveAttribute('aria-pressed', 'false');
      await btn.click();
      await fixtureExpect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
      // analytics.js ran under the policy: its gtag('js') and gtag('config') calls are queued.
      fixtureExpect(await page.evaluate(() => (window as any).dataLayer?.length ?? 0)).toBeGreaterThanOrEqual(2);
      fixtureExpect([...violations, ...(await domViolations(page))]).toEqual([]);
    });
  }
});

// (b) Netlify only: the real header, and Google Analytics left unaborted to prove the policy
// does not break it.
rawTest.describe('CSP as served by Netlify', () => {
  // Same switch playwright.config.ts uses: no BASE_URL means the local server, which sends no headers.
  rawTest.skip(!process.env.BASE_URL, 'headers only exist on Netlify');

  for (const path of PAGES) {
    rawTest(`${path}: header equals netlify.toml, zero violations`, async ({ page }) => {
      const violations = await collectViolations(page);
      const response = await page.goto(path);
      await page.waitForLoadState('networkidle');
      expect(response!.headers()['content-security-policy']).toBe(CSP);
      expect([...violations, ...(await domViolations(page))]).toEqual([]);
    });
  }

  rawTest('analytics still reaches Google under the policy', async ({ page }) => {
    const collect = page.waitForRequest(
      (r) => {
        const u = new URL(r.url());
        return /google-analytics\.com|analytics\.google\.com/.test(u.hostname) && u.pathname.includes('/collect');
      },
      { timeout: 15_000 },
    );
    await page.goto('/index.html');
    await collect;
  });
});
