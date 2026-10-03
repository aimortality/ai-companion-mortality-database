import { test as base, expect } from '@playwright/test';

// Shared test fixture. Third-party analytics requests are aborted so runs are deterministic
// and offline-safe. Test-only: the analytics tags on the pages are untouched.
export const test = base.extend({
  page: async ({ page }, use) => {
    await page.route(/googletagmanager|google-analytics/, (r) => r.abort());
    await use(page);
  },
});
export { expect };
