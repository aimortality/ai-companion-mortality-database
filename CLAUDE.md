# AI Companion Mortality Database - Development Guide

## Project Overview

Public research database tracking verified deaths associated with AI chatbot interactions. Static HTML site deployed on Netlify at **aimortality.org**. Also accessible via ai-death.com and chatbotdeaths.org (redirects).

## Architecture

Static site built by `build.py` (Python 3.12 + Jinja2) into `dist/`, which Netlify publishes. `build.py` validates canonical (`scripts/validate_data.py`) and refuses to build from invalid data, renders `templates/index.html.j2` to static HTML (no runtime JavaScript is needed to read the page), and copies the other pages from `src/` plus `data/` and `docs/`. **Never edit `dist/`** — it is not in git and is rebuilt on every deploy. Change the template or the data and run `python3 build.py`.

## Key Files & Data Flow

**Data is duplicated across multiple files.** When adding or updating cases, ALL of these must be updated:

| File | What it contains |
|------|-----------------|
| `data/mortality-data.json` | **Canonical data source.** Full incident records, platform stats, regulatory info. Update this first. |
| `templates/index.html.j2` | Main page, rendered to `dist/index.html` by `build.py`. Static HTML. Still carries hand-typed values (case rows, meta tags, prose figures) until they are derived from canonical. |
| `src/report.html` | Research report. Individual case sections with detailed narratives, legal proceedings, and summary stats. |
| `src/index-academic.html` | Academic-style page. Has abstract, key findings, and dates that mirror index.html. |
| `README.md` | Repo-facing (GitLab: aimortality/ai-companion-mortality-database; also uploaded to Zenodo). Has badges, case table, platform comparison, key findings. |

## Adding a New Case - Checklist

1. **Verify the case** through court documents, multiple news sources, or government acknowledgment before adding. For non-English-jurisdiction cases, run a primary-language source sweep and apply the **jurisdictional-verification-limited** Tier 2 sub-label where appropriate. See `docs/verification-standards.md`.
2. Update `data/mortality-data.json` (add incident record, update metadata counts, update relevant platform record including `third_party_fatalities` where applicable, update `statistics.instrumental_pathway_casualties` if instrumental)
3. Update `templates/index.html.j2`:
   - Meta tags (description, OG, Twitter, schema.org JSON-LD — both the `variableMeasured` values AND the description strings)
   - `.meta` line (Deaths, Incidents, Period — *not* `Cases` as an additive total; see `docs/methodology.md` "On What Counts as an Incident")
   - Abstract text and key findings list
   - Case table row (in `<div id="cases">`)
   - Key Findings cards (`card-grid`) — prose that carries derived figures
   - Footer date
   - *No charts or statistics tables on this page.* They were removed 2026-09-29 and return only as output generated from canonical, never hand-drawn. The deaths-by-year, platform, and age tables live on the academic page (Tables 1–3).
4. Update `src/report.html` (add case section, update executive summary near top AND Summary Statistics near bottom — there are two stat blocks, both need attention; update Lawsuits section, Regulatory section, Conclusions)
5. Update `src/index-academic.html` (abstract, key findings, stats grid, Table 1 deaths-by-year, Table 2 platform distribution, Table 3 age distribution, Table 4 case list, masthead date)
6. Update `README.md` (badge, case table, platform comparison, key findings, last-updated)
7. Regenerate the derived exports: `python3 scripts/build-data-exports.py` (`data/platform-analysis.csv`, `data/timeline.json`). They are a sixth surface; the audit fails if they drift from canonical. Missed after v3.5.1/3.5.2 and shipped stale to Zenodo.
8. Run the audit grep (see "Verification grep" below) before declaring done.

## Releasing a version (Zenodo DOI)

Every released version is archived on Zenodo under concept DOI `10.5281/zenodo.22062862` (always resolves to the latest version). The README badge uses the concept DOI; citation strings use the *version* DOI.

1. Bump the version in all five places: `data/mortality-data.json` `metadata.version`, `src/index-academic.html` (masthead + footer citation), `README.md` (sub line + citation), `docs/methodology.md` citation, `data/README.md` citation. Regenerate exports. Audit green. Merge.
2. Zenodo → the latest record → **New version** (or API: `POST /api/deposit/depositions/{id}/actions/newversion` with `$ZENODO_TOKEN`), upload the files from the merged `main` (`data/mortality-data.json`, `data/incidents.csv`, `data/platform-analysis.csv`, `data/timeline.json`, `data/LICENSE`, `docs/methodology.md`, `docs/verification-standards.md`, `README.md`, `LICENSE`), set `version` and `license: cc-by-4.0` (data license; code is MIT in-repo), publish.
3. Put the new version DOI into the three citation strings (academic footer, methodology, README, data/README) in a follow-up PR. The concept-DOI badge needs no change.

Publishing is permanent; the maintainer confirms it. Never upload derived exports that the audit has not just verified against canonical.

## Stats to Recalculate

When the death count, incident count, or platform tally changes, recalculate:
- Minors percentage (deaths under 18 / total deaths)
- Average age (note any estimated ages — e.g., the Kim Seoul Korean victims at midpoint 25 — in `statistics.average_age_note`)
- Deaths by year
- Platform death counts and percentages
- Per-platform totals that *aggregate* user deaths + third-party victims — these are the values that were *correct before the change* and silently go stale after (e.g., `ChatGPT total = N`). Re-derive each one rather than relying on grep for the new headline number.
- Age distribution buckets (13-17, 18-35, 36-54, 55+) and their percentages — the bucket counts must sum to the total fatalities
- Duration note denominator ("Duration known for X of Y cases")
- **The coverage period (`metadata.time_range.end` and every rendered "Period: March 2023 — <Month YYYY>" / "Mar 2023–<Mon YYYY>" / "Between March 2023 and <Month YYYY>" string).** `time_range.end` tracks the *sweep date* (coverage-through), not the last index event — bump it on every sweep. It surfaces in: the `.meta` line, all three meta descriptions, JSON-LD `temporalCoverage`, abstract + key findings (index and index-academic), the README badge + key findings, `docs/methodology.md` p7 and the zero-deaths claim, and `report.html` exec summary + Conclusions prose. Missed in v3.5.0; caught on the live site.
- The three pathway counts (relational, cognitive, instrumental) — note that these classify *death mechanism* and need not sum to total incidents; survived-attempt incidents have no death mechanism.

## Presentation lag classes — locations easy to miss

Five classes of locations have caused presentation-vs-data drift in prior sweeps. Check each explicitly:

1. **Same-page duplicate stats in different rhetorical positions.** A single HTML page may carry the same statistic in the Key Findings bullets, the abstract, a card-meta tooltip, the schema.org JSON-LD, and the meta description tags. Updating one and missing the others creates *internal* inconsistency on a single page. Past misses: pathway counts split between two rhetorical sections of the index page.
2. **SVG `<desc>` accessibility text.** Each chart has both visible labels and a `<desc>` element that screen readers announce. They are independent strings. Past misses: the index page's engagement-duration desc and platform-deaths desc carrying outdated totals.
3. **Decorative header dates that are not `last_updated`.** Pages can carry "as of [date]" text in cosmetic header banners that is technically separate from the `last_updated` metadata. Past misses: `src/index-academic.html` `<header class="journal-header">` masthead date.
4. **Derived subtotals that were CORRECT before the sweep but go stale after.** This is the subtle one. When a top-line total changes, *derived* subtotals (a platform's own total like "ChatGPT: 23 fatalities", a "general-purpose assistants accounted for 26 fatalities" prose sentence, a code comment carrying the prior figure, an SVG `<desc>` reciting the prior platform total) silently become wrong. Grepping only for the headline old value misses these because the stale token is a *different* number that nobody thinks to search for. Before declaring done, enumerate every per-platform and per-category subtotal that the changed total feeds into, and search each old value.
5. **Mid-paragraph prose.** The worst misses hide in flowing sentences ("...accounted for 26 fatalities...") that no stat-box-focused check looks at. `docs/methodology.md` paragraph-7 numbers, the `index-academic.html` Platform Distribution intro, and the long-form `report.html` Conclusions block are particularly exposed.

## Verification grep — run before declaring a sweep done

**Run the scripts first — they derive every expected and stale value from canonical, so they cannot rot:**

```bash
python3 scripts/validate_data.py                 # JSON invariants
python3 scripts/audit-surfaces.py --base main    # builds dist/, then checks the BUILT pages vs canonical + stale probes (use the pre-sweep ref as --base)
```

Then the manual grep below for anything the script cannot classify (prose subtotals, code comments), and the `/credibility-audit` skill for the judgment calls (source integrity via independent subagent, allegation framing, dated snapshots).

Grep all five canonical files (`data/mortality-data.json`, `templates/index.html.j2`, `src/index-academic.html`, `src/report.html`, `README.md`), plus `docs/methodology.md` (which carries headline numbers in prose) and the project CLAUDE.md, for *every* pre-change value: headline totals, per-platform subtotals, derived percentages, period-end dates, and the version string.

- Use **case-insensitive** matching (`grep -ri`). A capital-I "Incidents" header has previously evaded a case-sensitive pass.
- Check `<desc id="...-desc">` elements explicitly.
- Check decorative header bands and page-banner spans, not just `last_updated`.
- Check prose mid-paragraph, not just stat boxes and tables.
- Check code comments — they're cosmetic but often quoted as authoritative downstream.

## Sourcing integrity — non-negotiable

When citing sources for a case, **copy source names verbatim from the canonical record's `sources` array**. Never embellish a source list with marquee outlets that did not cover the case. A prior sweep rendered "(including AP, Reuters, BBC)" in the Kim Seoul verification note while omitting the actual cited outlets (Korea Herald, Fortune, NBC News, South China Morning Post) — an integrity failure that is worst-of-all in a Tier 2 / jurisdictional-verification-limited case, where source provenance is the defining caveat.

## Verification Standards

Cases require at least ONE of:
- Court documents or legal filings
- Multiple independent news sources (3+)
- Official government acknowledgment
- Congressional testimony
- Public statements by verified family members

**Important:** LLM-generated research (from Gemini, ChatGPT, etc.) should always be independently verified through web searches before adding to the database. LLMs can hallucinate cases, dates, and details.

## Platforms Tracked

Currently 8: ChatGPT, Character.AI, Chai AI, Meta AI, Gemini, DeepSeek, Claude, Replika. Six of these have documented fatalities (all except Claude and Replika). DeepSeek was added in April 2026 following the Roberts/Shellis homicide (Wales, October 2025) — the first non-Western corporate AI to appear in the database.

## Content Sensitivity

**This repository is public.** Tier 3 leads, unpromoted candidates, weekly-triage drafts, and the living-room brief live in the private repo `closestfriend/aimortality-triage` (sibling checkout `../triage`) and must never be committed here — `drafts/` is gitignored and was purged from history on 2026-08-25. Anything that names a person the database has not published belongs there, not here.

This database documents real deaths. Maintain:
- Crisis resources (988 hotline) on every page
- Respectful, factual tone
- No speculation about causation beyond what's documented
- Verification level noted for each case

## Deployment

- **Host:** Netlify (auto-deploys from main branch)
- **Domain:** aimortality.org
- **Analytics:** Google Analytics (G-SS2VTGZ004)
- Netlify runs `pip install -r requirements.txt && python3 build.py && python3 scripts/audit-surfaces.py --no-build`. Any audit FAIL fails the deploy, and the site stays on its last good build. Deploy previews run the same gate on every PR.

## Style Conventions

- Monospace font throughout (SF Mono / Menlo / Monaco / Courier New)
- Brutalist aesthetic with light/dark theme toggle
- All dates in format: "Month DD, YYYY" or "Month YYYY"
- Sources linked with "View source ->" text
