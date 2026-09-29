---
name: credibility-audit
description: Use before opening or merging any PR that touches data values, case records, source attributions, dates, or rendered prose on aimortality.org; after a stat-propagation sweep or new-case promotion; before replying to a contributor who reported a factual or link error; and as quarterly maintenance for link rot and decorative-date drift. Scoped to what a citing academic, journalist, or regulator would notice.
---

# Credibility Audit (aimortality.org)

## Overview

The database is cited by researchers, regulators, and journalists. Its truth is spread across five files that duplicate the same facts (`data/mortality-data.json` is canonical; `templates/index.html.j2` (built to `dist/index.html`), `src/index-academic.html`, `src/report.html`, `README.md` derive from it; `docs/methodology.md` carries headline numbers in prose). When they disagree, the database is silently lying. This audit catches drift before it ships.

**Core principle: evidence before claims.** Every finding cites `file:line` or fresh command output from *this* pass. If you did not run the command in this pass, you cannot say it passes.

**Mechanical checks live in code, not in this document.** `scripts/audit-surfaces.py` derives every expected value from canonical and every *stale* value from canonical at a git base ref, so the receipts cannot rot the way a hardcoded checklist does. This skill covers the run plus the judgment calls the script cannot make.

## The run

```bash
python3 scripts/validate_data.py                   # JSON internal invariants
python3 scripts/audit-surfaces.py --base main      # five surfaces vs canonical; stale probes vs main
python3 scripts/audit-surfaces.py --links          # add on quarterly passes or after source edits
```

`--base` is the ref whose canonical JSON supplies the *pre-change* values (use `HEAD~1` or the pre-sweep commit when auditing a merged sweep). The script checks: headline totals; coverage-period strings (`Period: … — <Month YYYY>`, `Between March 2023 and …`, `Mar 2023–…`, the three meta descriptions, JSON-LD `temporalCoverage`, methodology's zero-deaths claim); version and last-updated strings incl. the index-academic masthead; pathway counts; `index.html` age buckets summing to fatalities, duration denominator, and every chart `<desc>` against its data; `report.html` Verification Sources against canonical `sources` (marquee outlet not in canonical = FAIL; any other unmatched outlet = WARN); stale pre-change values surviving anywhere. Exit 0 = no FAIL.

Then **render it**: serve `dist/` (`python3 -m http.server -d dist`), open `index.html` headless, confirm zero console errors and that the page shows canonical values. The script reads the built pages' markup; it cannot see a chart clipping its own label.

## What the script cannot judge — do these by hand or by subagent

| Category | How |
|---|---|
| **Source integrity on a case you just wrote** | You are anchored. Dispatch an independent subagent: *"Do NOT trust any prior 'clean' assessment. For case X, list canonical `sources`, then every rendered outlet; flag any outlet not in canonical and any quoted fact, date, or name that differs."* Mandatory for Tier 2 / jurisdictional-verification-limited cases, where provenance is the defining caveat. |
| **Allegation framing** | Every chatbot-behavior claim in new prose carries "complaint alleges" / "allegedly" / "reportedly". Crisis resources (988) present on every page. |
| **Dated status snapshots** | "as of May 2026", "no ruling as of…", "at least N lawsuits" — the script ignores these on purpose. They are findings only if a newer docket item in the private triage repo (`closestfriend/aimortality-triage`, sibling checkout `../triage/weekly-triage/`) supersedes them; otherwise they are honest history. |
| **Derived subtotals in prose** | Per-platform totals, "general-purpose assistants accounted for N", lawsuit tallies with their own arithmetic. Re-derive each from canonical; do not grep for the headline number. |
| **`docs/verification-standards.md`** | Must define every Tier sub-label canonical uses (`jurisdictional-verification-limited`). |
| **WARN lines** | A WARN on source attribution is a real gap in canonical or a real embellishment in the report — decide which, and say so in the report. Never close a pass with unexplained WARNs. |

**Conventions to preserve, not "fix":** ChatGPT's third-party count is 16 on index/report/methodology and 15 + Margaux footnote on README (the validator encodes this as a documented exception). Reconciling it is a canonical data decision for the maintainer, not an audit fix. Record it as a known inconsistency in the report.

## Past misses — the institutional memory this skill exists for

| Miss | Where it hid | Now caught by |
|---|---|---|
| "(including AP, Reuters, BBC)" on the Kim Seoul case — outlets that never covered it | `report.html` Verification Sources | `audit-surfaces.py` marquee check + subagent dispatch |
| "ChatGPT: 23 fatalities (11 + 12)" after the total changed | Derived subtotal, exec summary | `--base` stale probes |
| Coverage period left at "May 2026" through an August sweep — `time_range.end` is the *sweep date*, not the last death | `.meta` line, 3 meta descriptions, JSON-LD, abstract, README badge, methodology, Conclusions prose | period checks (all forms) |
| Cognitive-pathway count "4" on four surfaces while canonical said 6 | Key findings, Summary Statistics | pathway check |
| Version "3.0" and masthead "May 2026" on the academic page | `<header class="journal-header">` | version / updated checks |
| `<desc>` screen-reader text reciting a prior platform total | SVG accessibility strings | `<desc>` vs chart-data checks |
| Cumulative chart points that never matched canonical dates | `index.html` SVG polyline | rendering check + manual re-derivation |

## Red flags — you are rationalizing

| Thought | Reality |
|---|---|
| "The new cases fall inside the period, so it's unchanged" | The period is coverage-through. It moves on every sweep. |
| "grep came back clean" | The script greps source. Prose, charts, and judgment live elsewhere. Render it; dispatch for sources. |
| "I wrote the sweep, I know it's complete" | That is precisely why an independent pass is required. |
| "WARN isn't FAIL" | A WARN on a Tier 2 case's sources is a finding. Explain it or fix it. |
| "That number is a dated snapshot, leave it" | Only if nothing in the private triage repo supersedes it. Check `../triage/weekly-triage/`. |

## Report format

```
## Credibility Audit — <date> · base <ref>
**Recommendation:** Clean to ship | Minor revisions | Major revisions before ship

### Major      <finding> — file:line — evidence — why it matters — fix
### Minor      <finding> — file:line — evidence
### Known inconsistencies preserved   (e.g., Margaux 15/16)
### What checks out                   (script summary line, link counts, render result)
### Receipts   | Check | Command | Result |
```

## `--fix` mode

When invoked as `/credibility-audit --fix`, apply only unambiguous fixes after the report: verified replacement URLs, stale derived values where canonical is authoritative, decorative dates behind `last_updated`. Never auto-apply classification changes, case-status changes needing source verification, convention reconciliations, or anything where canonical itself is suspect. Re-run the script after every fix; no completion claim without fresh output.

## Related

- `CLAUDE.md` — "Stats to Recalculate" and the five presentation-lag classes; this skill is their enforcement.
- `scripts/validate_data.py` — JSON invariants. `scripts/audit-surfaces.py` — surface consistency. Both must be green to ship.
- Memory: `feedback_presentation_lag_patterns`, `feedback_adversarial_subagent_review`, `project_third_party_margaux_inconsistency`, `project_definition_of_incident`.
