# Data

Three files. One is canonical; two are derived from it.

| File | What it is | Use it for |
|---|---|---|
| `mortality-data.json` | **Canonical record.** Every incident with sources, legal status, mechanism classification, key factors, and victim details; platform records; regulatory responses; derived statistics; metadata (version, coverage period, definitions). | Anything you'll cite. |
| `platform-analysis.csv` | Per-platform summary: user deaths, third-party fatalities, survived attempts, safety features and when they were added. | Spreadsheets, quick comparisons. |
| `incidents.csv` | One row per incident: date, name, age, fatalities, survived-attempt victims, platform, location, mechanism, outcome, verification level, legal status, sources. | Spreadsheet analysis of the cases themselves. |
| `timeline.json` | Incidents in chronological order with fatalities, survived-attempt victims, outcome, legal status, and mechanism. | Time-series views. |

The two derived files are regenerated from the JSON by `scripts/build-data-exports.py` and checked against it by `scripts/audit-surfaces.py`; if they ever disagree, the JSON is right.

**24 incidents, 35 fatalities — not the same number, on purpose.** `total_incidents` counts *occurrences of harm*; `total_fatalities` counts *people who died*. Most incidents have one victim, but Tumbler Ridge (8 killed by the same shooter, who also died) and the FSU, USF, and Kim Seoul cases (2 killed each) are one incident apiece with multiple victims — see *On What Counts as an Incident* in the methodology. `incidents.csv`'s `Fatalities` column makes this arithmetic checkable directly in a spreadsheet: `SUM(Fatalities)` equals `total_fatalities` (35); `SUM(Survived-Attempt Victims)` equals `total_attempts` (2, both inside incidents that also had fatalities: Kim Seoul's first, December-2025 victim, and Nina's incident, which is 0 fatalities / 1 survived).

## Scope and definitions

This is a register of deaths associated with **conversational AI systems** — chatbots and LLM assistants — in which the interaction was alleged as a contributing factor in court filings, official government statements, or multiple independent news sources. It is not a register of all AI-related deaths: autonomous vehicles, clinical ML, industrial automation, weapons, and recommender systems are out of scope. The database makes no independent claim of causation.

Before analysing the data, read [`docs/methodology.md`](../docs/methodology.md) — in particular *On What Counts as an Incident* (survived attempts are incidents; one incident may have several victims; pathway counts need not sum to incident counts), the rule for counting third-party victims, the adjudicated-status rule for how killings are described, and *Limitations and Uncertainties*. Verification tiers and sub-labels are in [`docs/verification-standards.md`](../docs/verification-standards.md).

Key fields in `mortality-data.json`:

- `metadata` — `version`, `last_updated`, `time_range` (coverage period; the end is the sweep date, not the last incident), headline totals, `mechanism_definitions`.
- `incidents[]` — one record per incident. `mechanism_type` is one of `relational_pathway`, `cognitive_pathway`, `instrumental_pathway`; `outcome_target` is `self_harm` or `violence_against_others`; `verification_level` and `legal_status_category` are free-text categories defined by their values; `sources[]` are the outlets and documents actually relied on.
- `platforms[]` — per-platform `deaths` (AI users), `third_party_fatalities`, and documented safety responses.
- `statistics` — deaths by year, age distribution, platform shares, with notes on any estimates.

## Versions and citation

The JSON carries its version in `metadata.version`. Each released version is archived on Zenodo; cite the version you used.

```
Karman, H. (2026). AI Companion Mortality Database: Documented Deaths
Associated with Conversational AI Systems (2023–2026). Version 3.5.5.
Zenodo. https://doi.org/10.5281/zenodo.22076350
```

`10.5281/zenodo.22062862` is the concept DOI and always resolves to the latest version; each version also has its own DOI on its Zenodo page.

## License and contact

The data is licensed [CC BY 4.0](LICENSE) — reuse freely with attribution (cite the version you used, above). The repository's code is MIT ([`../LICENSE`](../LICENSE)). Questions, corrections, and requests about a documented person: **contact@aimortality.org** — a person reads it.
