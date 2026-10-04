import AxeBuilder from '@axe-core/playwright';
import { test, expect } from './fixtures';
import { PAGES } from './pages';

// Accessibility floor: WCAG 2.1 AA, verified by axe in BOTH colour schemes on every page, plus the
// behaviours axe cannot see (skip link, visible focus, 44px targets, no page-level horizontal scroll).
// axe is run with no disabled rules and no exclusions.
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'];

for (const scheme of ['light', 'dark'] as const) {
  for (const path of PAGES) {
    test(`${path} axe clean (${scheme})`, async ({ page }) => {
      await page.emulateMedia({ colorScheme: scheme });
      await page.goto(path);
      const r = await new AxeBuilder({ page }).withTags(TAGS).analyze();
      expect(r.violations.map((v) => `${v.id}: ${v.nodes.length}`)).toEqual([]);
    });
  }
}

for (const path of PAGES) {
  test.describe(path, () => {
    test('structure: one skip link first in body, one main#main-content it targets', async ({ page }) => {
      await page.goto(path);
      await expect(page.locator('a.skip-link')).toHaveCount(1);
      await expect(page.locator('a.skip-link')).toHaveAttribute('href', '#main-content');
      // The skip link is the first element in <body>, before the crisis bar and everything else.
      expect(await page.evaluate(() => document.body.firstElementChild?.matches('a.skip-link'))).toBe(true);
      await expect(page.locator('main')).toHaveCount(1);
      await expect(page.locator('main#main-content')).toHaveCount(1);
    });

    test('at 320px: no page scroll, 44px targets', async ({ page }) => {
      await page.setViewportSize({ width: 320, height: 640 });
      await page.goto(path);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
      for (const sel of ['.crisis-bar a[href="tel:988"]', '#theme-toggle']) {
        const box = await page.locator(sel).boundingBox();
        expect(box!.height, sel).toBeGreaterThanOrEqual(44);
        expect(box!.width, sel).toBeGreaterThanOrEqual(44);
      }
    });

    test('keyboard: skip link is first tab stop and visible on focus; skip moves focus into main', async ({ page }) => {
      await page.goto(path);
      await page.keyboard.press('Tab');
      const skip = page.locator(':focus');
      await expect(skip).toHaveText(/Skip to main content/);
      const style = await skip.evaluate((e) => {
        const s = getComputedStyle(e);
        const r = e.getBoundingClientRect();
        return { outline: s.outlineStyle, left: r.left, top: r.top, w: r.width, h: r.height };
      });
      expect(style.outline).not.toBe('none');
      // Focused, it is on screen (not parked off-canvas).
      expect(style.left).toBeGreaterThanOrEqual(0);
      expect(style.top).toBeGreaterThanOrEqual(0);
      expect(style.w).toBeGreaterThan(0);
      await page.keyboard.press('Enter');
      expect(await page.evaluate(() => location.hash)).toBe('#main-content');
    });

    test('keyboard: every focusable element shows a focus indicator', async ({ page }) => {
      await page.goto(path);
      const bad: string[] = [];
      for (let i = 0; i < 12; i++) {
        await page.keyboard.press('Tab');
        const r = await page.locator(':focus').evaluate((e) => {
          const s = getComputedStyle(e);
          return { desc: e.tagName + (e.id ? '#' + e.id : '') + '.' + e.className, none: s.outlineStyle === 'none' || parseFloat(s.outlineWidth) < 1 };
        });
        if (r.none) bad.push(r.desc);
      }
      expect(bad).toEqual([]);
    });

    test('readable without JS', async ({ browser }) => {
      const ctx = await browser.newContext({ javaScriptEnabled: false });
      const page = await ctx.newPage();
      await page.goto(path);
      expect((await page.locator('main').innerText()).length).toBeGreaterThan(500);
      await ctx.close();
    });

    test('every table is inside a labelled, keyboard-scrollable region (labels unique)', async ({ page }) => {
      await page.goto(path);
      const labels: string[] = [];
      for (const t of await page.locator('table').all()) {
        const wrap = t.locator('xpath=..');
        await expect(wrap).toHaveClass(/table-scroll/);
        await expect(wrap).toHaveAttribute('role', 'region');
        await expect(wrap).toHaveAttribute('tabindex', '0');
        const label = (await wrap.getAttribute('aria-label')) ?? '';
        expect(label.trim().length).toBeGreaterThan(0);
        labels.push(label);
      }
      expect(new Set(labels).size).toBe(labels.length);
    });

    test('motion: smooth scrolling only without a reduced-motion preference', async ({ page }) => {
      await page.emulateMedia({ reducedMotion: 'reduce' });
      await page.goto(path);
      expect(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior)).toBe('auto');
      await page.emulateMedia({ reducedMotion: 'no-preference' });
      expect(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior)).toBe('smooth');
    });

    test('focused theme toggle shows a >= 2px ring in both states', async ({ page }) => {
      await page.emulateMedia({ colorScheme: 'light' });
      await page.goto(path);
      const btn = page.locator('#theme-toggle');
      for (const pressed of ['false', 'true']) {
        if ((await btn.getAttribute('aria-pressed')) !== pressed) await btn.click();
        await expect(btn).toHaveAttribute('aria-pressed', pressed);
        await page.mouse.move(0, 0);
        await btn.focus();
        await page.keyboard.press('Shift+Tab');
        await page.keyboard.press('Tab'); // arrive by keyboard so :focus-visible matches
        await expect(btn).toBeFocused();
        const o = await btn.evaluate((e) => {
          const s = getComputedStyle(e);
          return { style: s.outlineStyle, width: parseFloat(s.outlineWidth) };
        });
        expect(o.style, `pressed=${pressed}`).not.toBe('none');
        expect(o.width, `pressed=${pressed}`).toBeGreaterThanOrEqual(2);
      }
    });
  });
}

test('academic page: links are distinguishable from text without colour', async ({ page }) => {
  await page.goto('/index-academic.html');
  const links = page.locator('article p a, article li a, article footer a');
  expect(await links.count()).toBeGreaterThan(0);
  for (const a of await links.all()) {
    expect(await a.evaluate((e) => getComputedStyle(e).textDecorationLine)).toContain('underline');
  }
});
