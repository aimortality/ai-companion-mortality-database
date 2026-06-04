---
name: credibility-audit
description: "Project-scoped credibility audit for aimortality.org. Use when shipping data updates, after weekly-triage merges, periodically as maintenance, or before responding to a contributor report. Verifies load-bearing public-facing claims — headline stats, derived subtotals, URL link health, source-attribution integrity, cross-surface consistency, accessibility text, and per-case staleness — across the six canonical surfaces (data/mortality-data.json, src/index.html, src/index-academic.html, src/report.html, src/export.js, README.md). Scoped to what a citing academic, journalist, or regulator would notice."
allowed-tools: [Read, Write, Edit, Bash, Agent]
---

# Credibility Audit (aimortality.org)

## Overview

The database is cited by academic researchers, regulators, and journalists. Its credibility depends on a narrow set of **load-bearing public-facing claims** staying consistent and correct across six surfaces that hold duplicated data. When any of those claims drift, the database is silently lying — not because anyone is malicious, but because the architecture spreads truth across many files.

This skill is the structured audit pass that catches drift before it ships, and produces a report a reviewer can act on. It is the credibility analogue to `peer-review` — narrower scope, faster cadence, mechanical where possible, subagent-driven where independence matters.

**Core principle:** evidence before claims. Every assertion in the audit report must cite a specific file:line or a verification command's output.

## When to use

Invoke `/credibility-audit` before any of:

- Opening a PR that touches data values, source attributions, or rendered prose
- Replying to a contributor who reported a factual or link issue (audit first, reply with receipts)
- Merging a weekly-triage PR into `main` for the first time after `data/mortality-data.json` has been touched
- Quarterly maintenance — link rot, source rot, and decorative-date drift accumulate silently

Also use after:

- Any sweep that propagates a stat change (`33→34 fatalities` etc.) — the post-sweep audit pass is the last gate
- Adding a new case or platform — verify it reached every surface that needs to render it
- A peer-review pass that surfaced specific items needing propagation — confirm propagation is complete

Do **not** use this skill for: methodology refactors (use the methodology branch), code-only changes that don't touch user-visible claims (use `verify`), or schema changes (those need their own design pass).

## The six canonical surfaces

| File | What it holds | Risk class |
|---|---|---|
| `data/mortality-data.json` | Canonical record. All other surfaces derive from this. | **Source of truth — verify others against it** |
| `src/index.html` | React component with inline `data.platforms` case array, abstract, key findings, SVG charts, demographic tables, meta tags, schema.org JSON-LD | **Highest exposure** — landing page, screen-readable, badged |
| `src/report.html` | Long-form research report — per-case sections + executive summary near top + Summary Statistics near bottom + Lawsuits + Regulatory + Conclusions | **Highest detail surface** — has two duplicate stat blocks; both matter |
| `src/index-academic.html` | Academic page — abstract, Key Findings, Table 1 deaths-by-year, Table 2 platforms, Table 3 age distribution, Table 4 case list | **Cited by researchers** — sentence-level prose drift hides here |
| `src/export.js` | JS data-export utility + mock API with hardcoded stats | **Lowest visibility, easiest to forget** |
| `README.md` | GitHub-facing — badges, case table, platform comparison, key findings | **First impression for new visitors** |

Two project-scoped methodology docs that should also be audited when they carry headline numbers:
- `docs/methodology.md` — paragraph-7 prose carries the headline totals and the FL AG context
- `docs/verification-standards.md` — generally static, but check the last-updated date

## The audit categories

Run each category in order. Where a category prescribes a Bash command, run it fresh — do not rely on memory or earlier output. Per the `verification-before-completion` discipline, *if you haven't run the verification command in this audit pass, you cannot claim it passes*.

### A. Headline stat propagation

The most-cited numbers: `total_fatalities`, `total_incidents`, `ai_users_deceased`, `third_party_victims`, period start/end, `version`, `last_updated`. Each must match canonical in every rendered surface.

**Verification command** (replace the numbers if canonical has changed):

```bash
python3 -c "
import json
m = json.load(open('data/mortality-data.json'))['metadata']
print(f'canonical: {m[\"total_fatalities\"]}/{m[\"total_incidents\"]}/{m[\"ai_users_deceased\"]}/{m[\"third_party_victims\"]} v{m[\"version\"]} ({m[\"last_updated\"]})')
"
# Then for each headline number, check presence per surface:
for f in src/index.html src/index-academic.html src/report.html src/export.js README.md docs/methodology.md; do
  printf '  %-30s ' "$f"
  for n in 33 22 17; do
    c=$(grep -cE "\\b${n}\\b" "$f")
    printf '%s:%s ' "$n" "$c"
  done
  echo
done
```

**What to flag:** zero hits for any headline number in any rendered surface = staleness. The number may be cited multiple times per surface; only a `0` is a finding.

### B. Derived subtotals (the silent-stale class)

This is the most dangerous class because the stale value is a *different number* than the changed total. When `total_fatalities` goes 29→33, **per-platform totals** like `ChatGPT: 23 fatalities` (which was 11 + 12 = 23) silently become wrong because the per-platform composition changed but the prior subtotal text doesn't grep against the new headline.

**Past misses caught by this audit:** v3.4.0 sweep left `report.html:282` saying "ChatGPT/OpenAI: 23 fatalities (11 users died, 12 third-party victims)" and `index-academic.html:537` saying "general-purpose assistants accounted for 26 fatalities ... n=13" — both silently wrong after the canonical change.

**Verification approach:** enumerate every per-platform aggregate, per-mechanism aggregate, and per-category figure that the changed total composes from, and grep each *old* value. The headline grep won't find these — only the per-derived-value grep will.

```bash
# After a stat change, list every derived value the change affected:
# - per-platform totals (ChatGPT, Character.AI, ...)
# - per-mechanism counts (relational, cognitive, instrumental)
# - per-year counts (deaths_by_year)
# - per-age-bucket percentages
# Then grep for each PRIOR value across all six surfaces:
for old_val in '23 fatalities' '12 third-party' '26 fatalities' '19 Incidents' '15 deaths'; do
  echo "--- searching old '$old_val' ---"
  grep -rnE "$old_val" src/ README.md docs/methodology.md 2>/dev/null | grep -v '.DS_Store'
done
```

### C. URL link health

Public-facing URLs decay. Contributor reports (e.g. Elizabeth La Salle, June 2026) typically surface 4xx and 5xx responses on case-source links. This category catches them mechanically.

**Verification command:**

```bash
# Extract all URLs from rendered surfaces, strip JS source-string close-quotes
grep -hoE 'https?://[^"<>) ]+' \
  src/index.html src/report.html src/index-academic.html README.md \
  | tr -d "'\"" | sort -u > /tmp/credibility_urls.txt
echo "URLs to test: $(wc -l < /tmp/credibility_urls.txt)"

# Test each URL. SKIP internal/CDN/badge URLs. Try HEAD first, fall back to GET for 403/405/000.
cat > /tmp/credibility_test_one.sh <<'SH'
#!/bin/bash
url="$1"
if echo "$url" | grep -qE 'img\.shields\.io|esm\.sh|aimortality\.org|creativecommons\.org|schema\.org|googletagmanager\.com'; then
  printf "SKIP    %s\n" "$url"; exit 0
fi
code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 15 -A "Mozilla/5.0 (link-checker)" --head "$url" 2>/dev/null)
if [ "$code" = "405" ] || [ "$code" = "403" ] || [ "$code" = "000" ]; then
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 15 -A "Mozilla/5.0 (link-checker)" -r 0-1024 "$url" 2>/dev/null)
fi
printf "%s   %s\n" "$code" "$url"
SH
chmod +x /tmp/credibility_test_one.sh
xargs -n 1 -P 6 /tmp/credibility_test_one.sh < /tmp/credibility_urls.txt | sort > /tmp/credibility_url_status.txt
echo "status distribution:"
awk '{print $1}' /tmp/credibility_url_status.txt | sort | uniq -c | sort -rn
echo "broken (non-2xx, non-SKIP):"
grep -vE '^(SKIP|2[0-9][0-9])' /tmp/credibility_url_status.txt || echo "  (none)"
```

**Critical gotcha — false pass on macOS:** plain `xargs -d '\n'` is **not portable to BSD xargs** on macOS. The audit will silently fail (zero URLs tested) but the final `grep -v ... || echo "(none)"` will report success. Always confirm `Lines written` equals the URL count, and always `tr -d "'\""` to strip JS source-string close-quotes that trip BSD xargs.

**For each broken URL:** cross-reference to the case it sources via `grep -nF "$broken_url" src/index.html`, then dispatch a replacement-finding subagent (see §H below for the dispatch template).

### D. Source-attribution integrity

When citing sources for a case, **the rendered "Verification Sources" list must match the canonical record's `sources` array**. This is the integrity rule that prevented the Kim Seoul fabricated-AP/Reuters/BBC incident from recurring.

**Verification command:**

```bash
# For each case in canonical, list the sources field, then check that the same outlets appear in report.html's Verification Sources line for that case
python3 << 'PY'
import json, re, sys
d = json.load(open('data/mortality-data.json'))
report = open('src/report.html').read()
for inc in d['incidents']:
    # find the report.html block for this case (best effort match on victim name or case label)
    name = inc.get('name', '')
    canonical_sources = inc.get('sources', [])
    # Find the verification-sources block immediately following the case-section header
    # The skill should call this out as a finding when canonical sources are not all present in the rendered block
    # (This is a structural check; mechanically gating it is tricky because rendered prose summarizes — use as a guide for spot-check, not auto-fail)
    pass
PY
```

In practice this category benefits most from **subagent dispatch** — one subagent per high-stakes case section (Tier 2 / jurisdictional-verification-limited cases especially) to do source-by-source comparison. See §H for the template.

**Red-flag pattern** (introduced by the v3.4.0 sweep, caught by peer review): a rendered "Verification Sources" line that names marquee outlets (AP, Reuters, BBC, The Guardian) **not present in the canonical `sources` array**. This is fabricated provenance — the worst possible failure mode for a Tier 2 / jurisdictional-verification-limited case where source provenance is the defining caveat. The rule:

> Never embellish a source list. Copy outlet names verbatim from `data/mortality-data.json`'s `sources` array. If a marquee outlet didn't appear in the canonical record, it does not appear in the rendered citation.

### E. Cross-surface consistency

Drift hides in three places that no stat-box-focused grep finds (see also `[[feedback_presentation_lag_patterns]]` in memory):

1. **Same-page duplicate stats in different rhetorical positions.** A single HTML page may carry the same statistic in the Key Findings bullets, the abstract, a card-meta tooltip, the schema.org JSON-LD, and the meta description tags. Updating one and missing the others creates *internal* inconsistency on a single page.

2. **SVG `<desc>` accessibility text.** Each chart has both visible labels and a `<desc>` element that screen readers announce. They are independent strings. Updating the visible chart label without updating the `<desc>` means screen-reader users get a different chart than sighted users — both an a11y bug and a research-integrity bug.

```bash
# List every <desc> element with its content for human review:
grep -nE "<desc[^>]*>[^<]+</desc>|'desc'[^,]*,\s*['\"][^'\"]+['\"]" src/index.html
```

3. **Decorative header dates that are not `last_updated`.** Pages can carry "as of [date]" text in cosmetic header banners (e.g., `src/index-academic.html`'s `<header class="journal-header">` masthead date) that is technically separate from the `last_updated` metadata.

```bash
# List every date-shaped string in headers/footers/banners:
grep -nE '(Last updated|as of|Updated:|<span>)[^<]*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^<]*<' \
  src/index.html src/index-academic.html src/report.html README.md docs/methodology.md docs/verification-standards.md
```

4. **Mid-paragraph prose.** The worst misses hide in flowing sentences ("...accounted for 26 fatalities...") that no stat-box-focused check looks at. `docs/methodology.md` paragraph-7 numbers, the `index-academic.html` Platform Distribution intro, and the long-form `report.html` Conclusions block are particularly exposed.

5. **Derived per-case detail.** When a case gains a new docket number, judge, or major filing in canonical, ensure the corresponding case section in `report.html` and the case object in `src/index.html` reflect it. The `Find <case-id> stale rendered details` check:

```bash
# Example: did the Gavalas case# 5:26-cv-01849 reach every surface that needs it?
for token in '5:26-cv-01849' 'Lance Neff' 'JCCP 5431' 'PIPEDA'; do
  printf '  %-25s ' "$token"
  for f in src/index.html src/index-academic.html src/report.html src/export.js README.md data/mortality-data.json; do
    c=$(grep -c "$token" "$f" 2>/dev/null)
    printf '%s:%s ' "$(basename $f | cut -c1-12)" "$c"
  done
  echo
done
```

### F. Per-case staleness drift

Status fields and legal-action prose age fast. A case marked `under_investigation` in canonical may need to become `lawsuit_filed` after a docket update; the same applies to rendered surfaces.

**Checks:**

- For each case whose `legal_status_category` changed in the last 90 days, verify the rendered `status` and `lawsuit` fields in `src/index.html`'s case object and the corresponding `report.html` section both reflect the new state
- Spot-check the README.md case table for stale outcome labels
- Check `index-academic.html` Table 4 case list for stale legal-status cells

**Approach:** dispatch a subagent (see §H) to read the canonical record's `legal_status_category` and `legal_action` for every case modified since the last credibility-audit run, and compare against each rendered surface.

### G. Methodology and reporting-standards drift

The internal docs are part of credibility too. Headline numbers in `docs/methodology.md` should match canonical; `docs/verification-standards.md` should formalize any new Tier sub-labels used in canonical (e.g., `jurisdictional-verification-limited`).

```bash
# Headline numbers in methodology.md paragraph 7:
sed -n '7p' docs/methodology.md
# verification-standards.md should mention every Tier 2 sub-label used in canonical:
python3 -c "
import json
d = json.load(open('data/mortality-data.json'))
sublabels = set()
for inc in d['incidents']:
    ctx = inc.get('additional_context', {})
    if 'tier_at_promotion' in ctx:
        for word in ctx['tier_at_promotion'].split():
            if '-limited' in word or '-verification' in word:
                sublabels.add(word.strip(',;.\"'))
print('sub-labels used in canonical:', sublabels)
"
grep -c 'jurisdictional-verification-limited' docs/verification-standards.md
```

### H. Subagent dispatch — when independence matters

For categories where you are anchored on prior work (e.g., you just wrote the propagation, or you wrote the case narrative being audited), dispatch an independent subagent. From the `[[feedback_adversarial_subagent_review]]` memory: when Claude is anchored on a methodological recommendation, propose adversarial review proactively rather than waiting to be asked.

**Subagent dispatch template — cross-surface consistency:**

```
Subagent type: general-purpose
Description: Map cross-surface consistency for <stat or item>
Prompt skeleton:
  You are doing an independent verification pass on aimortality.org at /Users/hnsk/Projects/ai-companion-mortality-database.
  Do NOT trust any prior "it's clean" assessment.
  Re-derive from scratch.
  Hunt for: <specific stale tokens / fabricated sources / drift class>.
  Report only — do not edit any files.
  Return a punch list with file:line citations.
```

**Subagent dispatch template — broken-link replacement (one per broken URL):**

```
Subagent type: general-purpose
Description: Find replacement for <case> <publisher> link
Prompt skeleton:
  You're sourcing a replacement URL for a research database.
  Case: <victim, platform, date, location, key facts>
  Currently-broken URL: <url> (returns <status>)
  Find ONE replacement URL in priority order:
    1. Wayback Machine snapshot of the original URL
    2. Same-publisher URL on same article (sometimes URL slugs change)
    3. Comparable single-source primary article from a major outlet
  Verification: test your candidate with curl HEAD → GET fallback. Confirm 2xx.
  Report format: REPLACEMENT / STATUS / SOURCE TIER / RATIONALE.
  Do NOT make code changes.
```

For broken-link replacement, dispatch all subagents in parallel (single message, multiple Agent tool blocks). After they return, **independently re-test each candidate** with curl before applying — trust but verify.

## Reporting structure

Produce a report in the peer-review register: structured, citation-backed, with explicit Major / Minor findings.

```
## Credibility Audit — <date>
**Recommendation:** <Clean to ship | Minor revisions | Major revisions before ship>

### Major
1. <Finding> — <file:line> — <evidence: command output or quoted text>
   - Why this matters
   - Suggested fix

### Minor
- <Finding> — <file:line> — <evidence>

### What checks out
- <Category> — <evidence the category passed, e.g., "all 27 URLs in index.html returned 2xx; status distribution 20/200, 7/SKIP">

### Receipts
| Check | Command | Result |
| ... | ... | ... |
```

The Receipts table is the credibility analogue to peer-review's "What checks out" — it's how a reader of the audit can verify the audit itself without re-running every command.

## Apply-fixes mode

When invoked as `/credibility-audit --fix`, after producing the report, attempt to apply unambiguous fixes:

- Broken URLs with a verified replacement → swap (parallel subagent dispatch per §H)
- Stale derived subtotals where canonical is authoritative → propagate the correct value across surfaces
- Decorative dates older than `last_updated` → align to `last_updated`

Do **not** auto-apply: methodological reframings, case-status changes requiring source verification, mechanism-classification changes, or anything where the canonical itself is suspect. Those are flagged in the Major section for Hunter's judgment.

After applying any fix, **run the audit category that the fix targets a second time** to confirm the fix worked. The skill's iron rule is the same as `verification-before-completion`: no completion claim without fresh evidence in this pass.

## When *not* to run this skill

- **In the middle of a sweep** — wait until canonical is committed and pushed, then audit the rendered surfaces against it. Mid-sweep audits produce noise about transient inconsistencies.
- **On a `routine/triage-*` branch** that only adds `drafts/weekly-triage/` files — those don't touch rendered surfaces; running the audit will report no findings.
- **Before a known incomplete update** — if you're 80% through a frontend sweep and know you have items left, audit at the end, not mid-stream.

## Related memory files

These memory entries codify the principles this skill operationalizes. Read them when ambiguity arises during the audit:

- `[[feedback_presentation_lag_patterns]]` — the four/five classes of presentation lag (same-page dupes, SVG `<desc>`, decorative dates, derived subtotals, mid-paragraph prose). This is the canonical source for category E.
- `[[feedback_taxonomy_parsimony]]` — when a propagation question requires inventing a new category, don't.
- `[[feedback_adversarial_subagent_review]]` — when to dispatch a subagent rather than trust your own audit.
- `[[project_definition_of_incident]]` — Hunter's `incident = occurrence of harm` definition; the additive `incidents + attempts` formula is wrong; mechanism counts need not sum to total.
- `[[audience_research_institutions]]` — the database is cited by academic research, which raises the bar for currency, accuracy, and methodology rigor.

## Related project documents

- `CLAUDE.md` — the project's authoritative checklist for `Adding a New Case`, `Stats to Recalculate`, the five presentation lag classes, the verification grep, and sourcing integrity. This skill operationalizes those checklists into a structured audit.
- `docs/methodology.md` — for context on `incident = occurrence of harm` and the verification framework.
- `docs/verification-standards.md` — for context on Tier 1 / Tier 2 / Tier 3 and the `jurisdictional-verification-limited` sub-label.

## Bottom line

Every claim in the audit report must cite a file:line or a fresh command's output. No exceptions. The audit's value is its evidence trail — that's what makes the database citable, and that's what makes the audit itself citable to a contributor like Elizabeth La Salle when she next asks why she should trust your reply.
