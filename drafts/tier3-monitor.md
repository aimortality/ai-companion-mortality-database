# Tier 3 Monitor

Per `docs/verification-standards.md`, Tier 3 leads are **tracked but not published**. This file is the running ledger. The weekly Routine appends rows here; promotion to Tier 2 or Tier 1 is a human-driven PR that moves the row into a new candidate file under `drafts/weekly-triage/` and, ultimately, into `data/mortality-data.json`.

**Rules:**
- Append-only. Never edit an existing row in place.
- One row per lead, keyed loosely by `case_identifier` (may be a placeholder until a canonical ID is assigned on promotion).
- Preserve the original-language source URL; never substitute a translated summary for the primary source.
- If a lead escalates, add a new row rather than editing the original, and reference the promotion PR in the new row's notes.

## Ledger

| date_first_seen | case_identifier | platform | source_url | source_language | english_summary | tier_classification | promotion_candidate |
|-----------------|-----------------|----------|------------|-----------------|-----------------|---------------------|---------------------|
| <!-- YYYY-MM-DD --> | <!-- slug or pending id --> | <!-- e.g. ChatGPT --> | <!-- primary source URL --> | <!-- ISO 639-1 --> | <!-- one line --> | <!-- tier-3 --> | <!-- no / watching / promoting --> |

<!--
First row above is a template placeholder. The Routine appends new rows below
this line. Do not delete the template row; it documents the expected shape.
-->
