import AxeBuilder from '@axe-core/playwright';
import { test, expect } from './fixtures';
import { linkTo } from './pages';

// The 404 page (dist/404.html, served by Netlify for any unknown path) and the print stylesheet.
// /404.html is deliberately NOT in PAGES: the other specs assume every PAGES entry has a current nav
// item and a canonical URL, and the error page has neither.
const NAV = ['Database', 'Research Report', 'Academic Summary', 'Methodology', 'Verification Standards', 'Data files'];
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'];

test.describe('/404.html', () => {
  test('content, chrome, and no claim to be an indexable page', async ({ page }) => {
    await page.goto('/404.html');
    await expect(page.locator('h1')).toHaveText('Page not found');
    await expect(page.locator('main#main-content')).toContainText("This page doesn't exist.");
    const crisis = page.locator('.crisis-bar');
    await expect(crisis).toContainText('Crisis resources available 24/7');
    await expect(crisis.locator('a[href="tel:988"]')).toBeVisible();
    await expect(page.locator('nav[aria-label="Site"] li a')).toHaveText(NAV);
    await expect(page.locator('nav[aria-label="Site"] [aria-current]')).toHaveCount(0);
    const inMain = (sel: string) => sel.split(', ').map((s) => `main ${s}`).join(', ');
    await expect(page.locator(inMain(linkTo('/report.html')))).toHaveText('Research report');
    await expect(page.locator('main a[href="/"]')).toHaveText('Database');
    await expect(page.locator('footer.site-footer a[href="tel:988"]')).toBeVisible();
    await expect(page.locator('meta[name="robots"][content="noindex"]')).toHaveCount(1);
    await expect(page.locator('link[rel="canonical"]')).toHaveCount(0);
  });

  for (const scheme of ['light', 'dark'] as const) {
    test(`axe clean (${scheme})`, async ({ page }) => {
      await page.emulateMedia({ colorScheme: scheme });
      await page.goto('/404.html');
      const r = await new AxeBuilder({ page }).withTags(TAGS).analyze();
      expect(r.violations.map((v) => `${v.id}: ${v.nodes.length}`)).toEqual([]);
    });
  }
});

// Netlify-only: the local static server has no 404 fallback, and only Netlify serves 404.html at any depth.
test.describe('unknown paths (Netlify only)', () => {
  test.skip(!process.env.BASE_URL, 'needs Netlify: the local static server does not serve 404.html for unknown paths');
  for (const path of ['/no-such-page', '/a/b/c/no-such-page']) {
    test(`${path} returns 404 with the page, the crisis bar, and the shared stylesheet`, async ({ page }) => {
      const res = await page.goto(path);
      expect(res!.status()).toBe(404);
      await expect(page.locator('h1')).toHaveText('Page not found');
      const crisis = page.locator('.crisis-bar');
      await expect(crisis).toBeVisible();
      await expect(crisis.locator('a[href="tel:988"]')).toBeVisible();
      // Not transparent proves /assets/base.css resolved at this depth (root-absolute URLs).
      expect(await crisis.evaluate((e) => getComputedStyle(e).backgroundColor)).not.toBe('rgba(0, 0, 0, 0)');
    });
  }
});

// Print: emulated with a dark colour scheme, the case that used to print dark.
for (const path of ['/report.html', '/index.html']) {
  test.describe(`print: ${path}`, () => {
    test.beforeEach(async ({ page }) => {
      await page.emulateMedia({ media: 'print', colorScheme: 'dark' });
      await page.goto(path);
    });

    test('theme toggle and site nav are not printed', async ({ page }) => {
      await expect(page.locator('#theme-toggle')).toBeHidden();
      await expect(page.locator('nav[aria-label="Site"]')).toBeHidden();
    });

    test('the crisis bar prints, with the 988 line', async ({ page }) => {
      const crisis = page.locator('.crisis-bar');
      await expect(crisis).toBeVisible();
      await expect(crisis).toContainText('988');
      const c = await crisis.evaluate((e) => { const s = getComputedStyle(e); return { bg: s.backgroundColor, fg: s.color }; });
      expect(c.fg).toBe('rgb(0, 0, 0)');
      expect(c.bg).toBe('rgb(255, 255, 255)');
    });

    test('white ground, black text, even in a dark scheme', async ({ page }) => {
      const c = await page.evaluate(() => ({ body: getComputedStyle(document.body).backgroundColor,
        html: getComputedStyle(document.documentElement).backgroundColor, text: getComputedStyle(document.body).color }));
      expect(c).toEqual({ body: 'rgb(255, 255, 255)', html: 'rgb(255, 255, 255)', text: 'rgb(0, 0, 0)' });
    });

    test('wide tables are not clipped', async ({ page }) => {
      for (const t of await page.locator('.table-scroll').all()) {
        expect(await t.evaluate((e) => getComputedStyle(e).overflowX)).toBe('visible');
      }
    });
  });
}

test('print: /index.html has scroll regions to un-clip (the table check is not vacuous)', async ({ page }) => {
  await page.goto('/index.html');
  expect(await page.locator('.table-scroll').count()).toBeGreaterThan(0);
});

test('print: external links in main show their URL; sources are not hidden', async ({ page }) => {
  await page.emulateMedia({ media: 'print' });
  await page.goto('/report.html');
  const link = page.locator('main a[href^="http"]').first();
  const after = await link.evaluate((e) => getComputedStyle(e, '::after').content);
  expect(after).toContain((await link.getAttribute('href'))!);
});

test('print: heading permalink glyphs are hidden; on screen they exist (the check is not vacuous)', async ({ page }) => {
  await page.goto('/methodology.html');
  const anchors = page.locator('a.header-anchor');
  expect(await anchors.count()).toBeGreaterThan(0);
  await expect(anchors.first()).toBeVisible();
  await page.emulateMedia({ media: 'print' });
  for (const a of await anchors.all()) {
    expect(await a.evaluate((e) => getComputedStyle(e).display)).toBe('none');
  }
});
