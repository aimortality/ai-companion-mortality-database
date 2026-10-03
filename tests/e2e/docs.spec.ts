import { test, expect } from './fixtures';

// The two documents are rendered to static HTML at build time, so they must read without JavaScript.
const DOCS: [string, string, string][] = [
  ['/methodology.html', 'Methodology', 'Methodology'],
  ['/verification-standards.html', 'Verification Standards', 'Verification Standards'],
];

test.describe('no JavaScript', () => {
  test.use({ javaScriptEnabled: false });
  for (const [path, h1, title] of DOCS) {
    test(`${path} readable without JS`, async ({ page }) => {
      await page.goto(path);
      await expect(page.locator('main h1')).toHaveText(h1);
      await expect(page).toHaveTitle(new RegExp(title));
      await expect(page.locator('main h2').first()).toBeVisible();
      await expect(page.locator('main')).not.toContainText('Loading');
    });
  }
});

for (const [path] of DOCS) {
  test(`${path}: landmarks, contents and switch`, async ({ page }) => {
    await page.goto(path);
    await expect(page.locator('main#main-content')).toHaveCount(1);
    await expect(page.locator('body > footer, footer')).toHaveCount(1);       // the shared site footer only
    await expect(page.locator('main footer')).toHaveCount(0);
    await expect(page.locator('main p.doc-source a[href^="/docs/"]')).toBeVisible();
    const toc = page.locator('nav[aria-label="On this page"]');
    await expect(toc).toHaveCount(1);
    const first = toc.locator('a').first();
    const target = (await first.getAttribute('href'))!;
    await first.click();
    await expect(page.locator(target)).toBeInViewport();
    const sw = page.locator('nav[aria-label="Document"] a');
    await expect(sw).toHaveText(['Methodology', 'Verification Standards']);
    await expect(sw.nth(0)).toHaveAttribute('href', '/methodology.html');
    await expect(sw.nth(1)).toHaveAttribute('href', '/verification-standards.html');
    await expect(page.locator('nav[aria-label="Document"] [aria-current="page"]')).toHaveAttribute('href', path);
  });
}

test('the two documents link to each other and to the repository, never to a raw markdown path', async ({ page }) => {
  await page.goto('/verification-standards.html');
  await expect(page.locator('main a[href="/methodology.html"]')).toHaveCount(1);
  await page.goto('/methodology.html');
  await expect(page.locator('main a[href^="https://gitlab.com/aimortality/ai-companion-mortality-database/-/blob/main/CONTRIBUTING.md"]')).toHaveCount(1);
  await expect(page.locator('main a[href$=".md"][href^="../"], main a[href="methodology.md"], main a[href="verification-standards.md"]')).toHaveCount(0);
});

test('old citation URLs land on Verification Standards', async ({ page, baseURL }) => {
  test.skip(baseURL!.includes('127.0.0.1'), 'redirects only exist on Netlify — run with BASE_URL=<deploy preview>');
  for (const u of ['/methodology?doc=verification-standards', '/methodology.html?doc=verification-standards']) {
    await page.goto(u);
    await expect(page).toHaveURL(/verification-standards/);
    await expect(page.locator('main h1')).toHaveText('Verification Standards');
  }
});

test('new route resolves under both URL forms', async ({ page, baseURL }) => {
  test.skip(baseURL!.includes('127.0.0.1'), 'pretty URLs only exist on Netlify');
  for (const u of ['/verification-standards', '/verification-standards.html']) {
    expect((await page.goto(u))!.status()).toBe(200);
  }
});
