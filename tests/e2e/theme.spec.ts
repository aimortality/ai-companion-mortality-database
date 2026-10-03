import { test, expect } from './fixtures';
import { PAGES } from './pages';

for (const path of PAGES) {
  test.describe(path, () => {
    test('toggle works when storage throws', async ({ page }) => {
      await page.addInitScript(() => {
        Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('blocked', 'SecurityError'); } });
      });
      await page.emulateMedia({ colorScheme: 'light' });
      await page.goto(path);
      const btn = page.locator('#theme-toggle');
      await expect(btn).toHaveAttribute('aria-pressed', 'false');
      await btn.click();
      await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
      await expect(btn).toHaveAttribute('aria-pressed', 'true');
    });

    test('saved theme that differs from the OS applies before first paint', async ({ page }) => {
      await page.addInitScript(() => localStorage.setItem('theme', 'dark'));
      await page.addInitScript(() => {
        new MutationObserver((_, obs) => {
          if (document.body) { (window as any).__themeAtBody = document.documentElement.dataset.theme ?? null; obs.disconnect(); }
        }).observe(document, { childList: true, subtree: true });
      });
      await page.emulateMedia({ colorScheme: 'light' });
      await page.goto(path);
      expect(await page.evaluate(() => (window as any).__themeAtBody)).toBe('dark');
    });

    test('button has a static name; state is aria-pressed', async ({ page }) => {
      await page.goto(path);
      await expect(page.getByRole('button', { name: 'Dark theme' })).toBeVisible();
    });

    test('declares color-scheme', async ({ page }) => {
      await page.goto(path);
      await expect(page.locator('meta[name="color-scheme"]')).toHaveAttribute('content', 'light dark');
    });
  });
}

test('choice carries across pages', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'light' });
  await page.goto('/index.html');
  await page.locator('#theme-toggle').click();
  await page.goto('/report.html');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
});
