import { test, expect } from '@playwright/test';
import { PAGES } from './pages';

const NAV = ['Database', 'Research Report', 'Academic Summary', 'Methodology', 'Verification Standards', 'Data files'];
const CURRENT: Record<string, string> = { '/index.html': 'Database', '/report.html': 'Research Report',
  '/index-academic.html': 'Academic Summary', '/methodology.html': 'Methodology' };

for (const path of PAGES) {
  test(`${path}: shared chrome`, async ({ page }) => {
    await page.goto(path);
    const crisis = page.locator('.crisis-bar');
    await expect(crisis).toHaveCount(1);
    await expect(crisis).toContainText('Crisis resources available 24/7');
    const tel = crisis.locator('a[href="tel:988"]');
    const box = await tel.boundingBox();
    expect(box!.height).toBeGreaterThanOrEqual(44);
    const links = page.locator('nav[aria-label="Site"] li a');
    await expect(links).toHaveText(NAV);
    await expect(page.locator('nav[aria-label="Site"] [aria-current="page"]')).toHaveText(CURRENT[path]);
    await expect(page.locator('.register-line')).toContainText('Period: March 2023 —');
    await expect(page.locator('footer a[href="mailto:contact@aimortality.org"]').first()).toBeVisible();
  });
}

test('crisis bar text is byte-identical across pages', async ({ page }) => {
  const texts = [];
  for (const p of PAGES) { await page.goto(p); texts.push(await page.locator('.crisis-bar').innerHTML()); }
  expect(new Set(texts).size).toBe(1);
});
