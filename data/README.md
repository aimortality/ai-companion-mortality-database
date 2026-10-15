# Data

Five files. One is canonical; four are derived from it.

| File | What it is | Use it for |
|---|---|---|
| `mortality-data.json` | **Canonical record.** Every incident with sources, legal status, mechanism classification, key factors, and victim details; platform records; regulatory responses; derived statistics; metadata (version, coverage period, definitions). | Anything you'll cite. |
| `platform-analysis.csv` | Per-platform summary: user deaths, third-party fatalities, survived attempts, safety features and when they were added. | Spreadsheets, quick comparisons. |
| `incidents.csv` | One row per incident: date and its precision, name, age, fatalities, survived-attempt victims, tier, platform, location, mechanism, outcome, verification level, legal status, sources. | Spreadsheet analysis of the cases themselves. |
| `people.csv` | One row per person: the AI user, each third-party victim, and any perpetrator, with role, outcome (died / survived / uninjured), age and how precise it is. | Any chart or statistic about *people* (ages, minors, victims vs. users). The incident-level `Age` column cannot do this: it is null for multi-victim events and mixes users with perpetrators. |
| `timeline.json` | Incidents in chronological order with fatalities, survived-attempt victims, outcome, legal status, mechanism, tier and date precision. | Time-series views. |

The derived files are regenerated from the JSON by `scripts/build-data-exports.py` and checked against it by `scripts/audit-surfaces.py`; if they ever disagree, the JSON is right.

**24 incidents, 35 fatalities — not the same number, on purpose.** `total_incidents` counts *occurrences of harm*; `total_fatalities` counts *people who died*. Most incidents have one victim, but Tumbler Ridge (8 killed by the same shooter, who also died) and the FSU, USF, and Kim Seoul cases (2 killed each) are one incident apiece with multiple victims — see *On What Counts as an Incident* in the methodology. `incidents.csv`'s `Fatalities` column makes this arithmetic checkable directly in a spreadsheet: `SUM(Fatalities)` equals `total_fatalities` (35); `SUM(Survived-Attempt Victims)` equals `total_attempts` (2, both inside incidents that also had fatalities: Kim Seoul's first, December-2025 victim, and Nina's incident, which is 0 fatalities / 1 survived).

## Scope and definitions

This is a register of deaths associated with **conversational AI systems** — chatbots and LLM assistants — in which the interaction was alleged as a contributing factor in court filings, official government statements, or multiple independent news sources. It is not a register of all AI-related deaths: autonomous vehicles, clinical ML, industrial automation, weapons, and recommender systems are out of scope. The database makes no independent claim of causation.

Before analysing the data, read [`docs/methodology.md`](../docs/methodology.md) — in particular *On What Counts as an Incident* (survived attempts are incidents; one incident may have several victims; pathway counts need not sum to incident counts), the rule for counting third-party victims, the adjudicated-status rule for how killings are described, and *Limitations and Uncertainties*. Verification tiers and sub-labels are in [`docs/verification-standards.md`](../docs/verification-standards.md).

Key fields in `mortality-data.json`:

- `metadata` — `version`, `last_updated`, `time_range` (coverage period; the end is the sweep date, not the last incident), headline totals, `mechanism_definitions`.
- `incidents[]` — one record per incident. `mechanism_type` is one of `relational_pathway`, `cognitive_pathway`, `instrumental_pathway`; `outcome_target` is `self_harm` or `violence_against_others`; `legal_status_category` is a free-text category defined by its values; `sources[]` are the outlets and documents actually relied on.
  - `tier` (1, 2 or 3, per `docs/verification-standards.md`), `sub_labels[]` (hyphenated; currently only `jurisdictional-verification-limited`) and `tier_basis` (which sources justify the tier). `verification_level` is the older free-text description and is kept for continuity; `tier` is the field to filter on.
  - `date` and `date_precision` (`day`, `month`, `year`). Where only a month is known the `date` carries `-01` as a placeholder day; `date_precision: month` says so. Ceccanti (`2025-XX-US-001`) is known only to the year; the ID is kept because it is cited.
  - `age` is the AI user's age where the incident has a single user, and null for multi-victim events; `people[]` is the per-person record and should be preferred for any age statistic.
  - `people[]` — one entry per person named or counted in the incident: `role` (`user`: the person who interacted with the AI, including users who then killed others; `third_party`: a person killed or harmed by an AI user; `perpetrator` is reserved for a killer who was not the AI user and is unused so far), `outcome` (`died`; `survived`, a counted survived attempt; `wounded`; `uninjured`), `name` (exactly as published elsewhere in this record, or null), `name_type` (`real`, `pseudonym`, `unnamed`), `age`, `age_precision` (`exact`, `approximate`, `unknown`), `age_source`, and an optional `note`. The `died` entries sum to `total_fatalities`; `survived` entries sum to `total_attempts`; `scripts/validate_data.py` checks both and the per-incident counts. `people[]` enumerates the dead, the counted survived attempts, the AI user, and the wounded wherever canonical states a count (the FSU and Tumbler Ridge wounded, Whittemore's mother); wounded entries are unnamed with unknown ages unless canonical says otherwise, and they are excluded from the fatality and attempt sums.
- `platforms[]` — per-platform `deaths` (AI users), `third_party_fatalities`, and documented safety responses.
- `statistics` — `incidents_by_year` (incidents, by the year of the index event; this key was misnamed `deaths_by_year` before v4.0.0), `deaths_by_year` (people who died, same keying; sums to `total_fatalities`), age distribution, platform shares, with notes on any estimates.
- `metadata.schema_version` — `2.0.0` introduced `tier`, `sub_labels`, `date_precision`, `people[]` and the `incidents_by_year` rename. Earlier releases (schema 1) have none of these fields.

## Versions and citation

The JSON carries its version in `metadata.version`. Each released version is archived on Zenodo; cite the version you used.

```
Karman, H. (2026). AI Companion Mortality Database: Documented Deaths
Associated with Conversational AI Systems (2023–2026). Version 3.5.9.
Zenodo. https://doi.org/10.5281/zenodo.23115481
```

`10.5281/zenodo.22062862` is the concept DOI and always resolves to the latest version; each version also has its own DOI on its Zenodo page.

## License and contact

The data is licensed [CC BY 4.0](LICENSE) — reuse freely with attribution (cite the version you used, above). The repository's code is MIT ([`../LICENSE`](../LICENSE)). Questions, corrections, and requests about a documented person: **contact@aimortality.org** — a person reads it.
