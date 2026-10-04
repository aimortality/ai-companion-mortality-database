# Audit contract: `scripts/audit-surfaces.py`

`audit-surfaces.py` is the deploy gate. Netlify runs it after `build.py`; any FAIL keeps the
site on its last good build. This file is the contract a redesign has to respect: what each
check asserts, which surfaces it reads, and which markup it leans on.

Run it: `python3 scripts/audit-surfaces.py --base <ref>` (builds `dist/` first; `--no-build`
audits the existing `dist/`; `--links` also probes every external URL). Tests for the audit's
own logic: `.venv/bin/pytest -q` (set up with `pip install -r requirements-dev.txt`).

## Redesign rules

1. **Content assertions are never weakened.** A check that fails because the page is wrong is
   fixed by fixing the page. A check that fails on correct content (a false positive) is
   narrowed, with a pytest case that reproduces the false positive written first.
2. **Structural selectors may change only in the same PR as the markup they select**, with the
   reason in the commit message. The two checks marked "structure-coupled" below are the ones
   to expect this for.
3. **Surfaces are derived, not listed.** Every `.html` page in `dist/` is audited (via
   `site_pages()`), except `EXEMPT_PAGES` and the `dist/data/` and `dist/docs/` publish copies
   (those are covered by `check_publish_copies`). A new page is gated from its first build.
   Markdown surfaces are listed in `MARKDOWN_SURFACES`.
4. **Agreement checks fail only on a wrong value**, so they run on every surface. **Presence
   checks** (headline totals, masthead) run only where the page is meant to carry them
   (`HEADLINE_SURFACES`, `index-academic.html`).

## Checks

Surface key: *every page* = `site_pages()` + `MARKDOWN_SURFACES`. Expected values are always
derived from `data/mortality-data.json`; stale values from the same file at `--base`.

| check | asserts | surfaces | markup it depends on | redesign rule |
|---|---|---|---|---|
| `check_headline` | `total_fatalities`, `total_incidents`, `ai_users_deceased` each appear at least once as a whole-number token | `HEADLINE_SURFACES`: `dist/index.html`, `dist/index-academic.html`, `dist/report.html`, `dist/methodology.html`, `README.md`, `docs/methodology.md` | none (plain-text token match) | Keep the three totals visible on those pages. Other pages are not required to carry them. |
| `check_period` | Every "Between March 2023 and X" (also lowercase "between March 2023 and X", as in the report Conclusions), "Mar 2023–X", "March 2023 — X", "Period: March 2023 — X", "March 2023 to X" string names the `time_range.end` month; in `docs/methodology.md` and `dist/methodology.html` (the page rendered from it), also "through X, no deaths". On `dist/index.html`, JSON-LD `temporalCoverage` equals `start/end` | every page (JSON-LD clause: `dist/index.html`) | The phrasing patterns in `PERIOD_RE` / `PERIOD_THROUGH_RE`; on `dist/methodology.html`, the "through <Month YYYY>, no deaths" sentence must be a single text run in the rendered HTML (no bold, link or other tag inside it, or the regex stops seeing it); the `"temporalCoverage": "YYYY-MM/YYYY-MM"` JSON-LD key | Rephrasing a period string outside those patterns hides it from the check; keep the patterns or extend them in the same PR. |
| `check_version` | Any `Version: x.y.z`, `· vx.y.z`, or `version: "x.y.z"` equals `metadata.version` | every page | `VERSION_RE` forms | New version-string formats need a `VERSION_RE` alternative. |
| `check_updated` | Any "Last updated / Data current as of / Database last updated: Month D, YYYY" equals `metadata.last_updated` | every page | `UPDATED_RE` forms | A document's own revision date must not be labelled "Last updated"; that phrase means the database date and is audited. Use another label, e.g. "Standards last revised". |
| `check_pathways` | Any "relational / cognitive / instrumental (pathway) ... N" with N > 1 equals the canonical pathway count | every page | `PATHWAY_RE`: the pathway word, optional "pathway", optional `</strong>`, then `:` and the number | Keep the word and number adjacent. |
| `check_stale` | Values that changed between `--base` and canonical (old version, date, period, totals, per-platform deaths, pathway counts) do not survive in any line, except lines tagged as history (corrected / raised from / "as of <date>" snapshots / etc.) | every page | Literal probe strings such as `"{N} fatalities"`, `"{p} ({N}"`, `"{Name}: {N} user deaths"` | Prose reworded away from these literals escapes the probes; prefer deriving figures from canonical. |
| `check_masthead` | **Structure-coupled.** The academic page's journal-header issue month equals the coverage-end month | `dist/index-academic.html` | `<header class="journal-header">` ... `<span>Month YYYY</span></header>`, matched with a single regex | If the masthead markup changes, change this regex in the same PR and say why in the commit message. The assertion (issue month = coverage end) stays. |
| `check_duration_statements` | Every "Duration known for N of M cases" equals canonical | every page | the literal sentence | Charts that return as generated output bring their own check. |
| `check_sources` | **Structure-coupled.** Each canonical incident has a "Verification Sources" line in `report.html`; no marquee outlet (AP, Reuters, BBC, Guardian, NYT, WaPo) appears there unless it is in the canonical `sources`; at least `total_incidents` case sections are compared | `dist/report.html` | `<h3...>CASE #N: <name>` headers, and `<strong>Verification Sources</strong>:` ... `</p>`, with `;`-separated outlets | If the case-section markup changes, change the splitter/matcher in the same PR. The assertion (rendered sources are a subset of canonical sources, no embellishment) stays. Fewer than `total_incidents` sections found is a FAIL, so a restructure cannot silently turn the check off. |
| `check_exports` | `data/platform-analysis.csv`, `data/incidents.csv`, `data/timeline.json` equal what `build-data-exports.py` generates now (the audit restores the files afterward) | those three files | none | Regenerate exports after any canonical change. |
| `check_relative_links` | Every relative `href` / `src` resolves to a file inside `dist/` | every built page | `href=` / `src=` attribute (and `href:` / `src:` in script) forms | Links are resolved against `dist/`, so write `name.html`, not a source path. |
| `check_publish_copies` | `dist/data/` and `dist/docs/` are exact, un-nested copies of `data/` and `docs/` | `dist/data`, `dist/docs` | none | None. |
| `check_sitemap` | `dist/sitemap.xml` exists; lists every `site_pages()` URL (except `404.html`) exactly once and nothing else (`dist/index.html` -> `/`, `dist/x.html` -> `/x`); every `<lastmod>` equals `metadata.last_updated`. A missing file is a FAIL | `dist/sitemap.xml` | `<loc>` / `<lastmod>` elements (written by `build.py` `write_sitemap`) | The sitemap is generated, never hand-edited. A page excluded from it needs an entry in `SITEMAP_EXCLUDED`, with a reason. |
| `check_meta` | Every built page has exactly one non-empty `<title>`, one `rel="canonical"` equal to its expected extensionless URL, one `og:title`, `og:description`, `og:url` (equal to the canonical), one `name="twitter:card"`, one non-empty `description`, and no `twitter:*` tag using `property=` | every page from `site_pages()` | `<title>`, `<link rel="canonical">`, `<meta property="og:...">`, `<meta name="twitter:...">` in the head (emitted by `templates/base.html.j2` from `build.py` `PAGES_META`) | A page must not hand-type these tags: add it to `PAGES_META` and the base head supplies them. |
| `check_inline_scripts` | Every `<script>` without a `src` is `type="application/ld+json"` (a data block, never executed), and no element carries an `on*=` event-handler attribute. Fails closed on an empty page list | every page from `site_pages()` | `<script>` elements and element attributes, parsed (not regex) | Pages must not carry inline executable scripts or handlers: the CSP in `netlify.toml` has no `'unsafe-inline'` in `script-src`. Put script in `src/assets/*.js` and load it with `<script src>`. A new third-party script host needs a deliberate CSP change in `netlify.toml`. |
| `check_links` (`--links` only) | Every external URL in the pages and Markdown surfaces answers 2xx | every page | none | Not part of the Netlify gate. |

## URL contract

Netlify's Pretty URLs serve /page for page.html and rewrite internal "page.html" links to "/page" at deploy, so dist/ links say page.html while the live site says /page; both forms return 200. New pages: emit name.html, link name.html. Canonical URLs are extensionless (`https://aimortality.org/report`); `/` for the index.

Pretty URLs is set explicitly in `netlify.toml` (PR #92) rather than left to the site default.
