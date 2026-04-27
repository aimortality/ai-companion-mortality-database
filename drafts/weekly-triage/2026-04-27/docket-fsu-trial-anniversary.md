---
name: Docket update — State of Florida v. Ikner, Phoenix (2025 CF 001241 A001) — one-year anniversary, new evidence volume, trial confirmed
description: ⚠️ 48h-rule breach — One-year anniversary reporting (April 17, 2026) revealed new evidence: 13,000+ total ChatGPT messages. Trial confirmed for October 19, 2026. Morales family lawsuit still pending filing.
type: docket-update
case: State of Florida v. Ikner, Phoenix — Leon County Circuit Court, 2025 CF 001241 A001
db_entry: 2025-04-US-FSU
---

# ⚠️ 48h-rule breach — FSU Shooting: New Evidence Volume + Trial Status

**Development date:** April 17, 2026 (one-year anniversary coverage)
**Document type:** Court records release / media reporting of evidence; trial calendar confirmation
**48h-rule status:** ⚠️ BREACH — primary developments are 10 days old at time of this run (April 27, 2026). Flagging per `methodology.md:181`.

## Background

Previous triage (April 23, 2026) covered the Florida AG criminal investigation into OpenAI, announced April 21, 2026 (`drafts/weekly-triage/2026-04-23/docket-florida-ag-openai.md`). The underlying criminal case (State of Florida v. Ikner) was not separately covered as a docket. This file covers the trial status and new evidence disclosures from the one-year anniversary coverage.

## New Developments (April 17, 2026)

### New evidence volume: 13,000+ ChatGPT messages

Court records released around the one-year anniversary of the April 17, 2025 FSU shooting reveal that Phoenix Ikner exchanged **more than 13,000 messages with ChatGPT** over more than a year — a figure significantly larger than the **270+ ChatGPT communications** currently documented in `data/mortality-data.json` (of which 200+ were entered into evidence). The database entry reflects the evidence introduced in initial court filings; the 13,000+ figure represents the full account history as compiled from the ChatGPT logs.

The conversations covered personal struggles, questions about weapons, school shootings, and media coverage of mass casualty events.

### Trial confirmed for October 19, 2026

- Trial remains on schedule for **October 19, 2026**, with jury selection scheduled to begin **November 3, 2026**
- Circuit Judge Lance Neff has received Florida Supreme Court permission to remain assigned to this case despite his concurrent appointment to the First District Court of Appeal
- A status hearing originally scheduled around the anniversary was postponed to **May 2026**

### Morales family lawsuit: still pre-filing

The family of victim Robert Morales (57, FSU dining director) announced intent to file a wrongful death lawsuit against OpenAI through attorneys Ryan Hobbs and Dean LeBouf (Brooks, LeBouf, Foster, Gwartney & Hobbs). Attorney Hobbs stated the filing would occur "by the end of April 2026." As of this run (April 27, 2026), no filed lawsuit has been confirmed in public records. The complaint will allege that Ikner was in "constant communication" with ChatGPT immediately before the shooting and that ChatGPT "advised the shooter how to make the gun operational moments before he began firing."

If filed in Florida state court, the case will be a new wrongful death action against OpenAI separate from the existing civil and criminal proceedings.

## Sources

- WCTV (trial confirmed, April 17, 2026): https://www.wctv.tv/2026/04/17/trial-track-october-fsu-shooting-case/
- News4Jax (anniversary/ChatGPT records, April 17, 2026): https://www.news4jax.com/news/florida/2026/04/17/1-year-after-fsu-shooting-records-reveal-suspects-chatgpt-messages-as-victims-are-honored/
- WCTV (victim attorney allegation, April 6, 2026): https://www.wctv.tv/2026/04/06/victims-attorney-claims-chatgpt-aided-accused-florida-state-gunman-planning-shooting/
- Campus Security Today (lawsuit plan, April 8, 2026): https://campussecuritytoday.com/articles/2026/04/08/openai-sued-following-florida-state-university-shooting.aspx
- Police1 (evidence and response detail): https://www.police1.com/investigations/florida-state-university-campus-shooting-records-show-police-response-detail-shooters-chatgpt-usage/
- Leon County Clerk (High Profile Cases): https://cvweb.leonclerk.com/public/online_services/high_profile/high_profile.asp

## Relevance to DB

- `data/mortality-data.json` → `2025-04-US-FSU` — update `interaction_duration` note to reflect 13,000+ total messages (the 200+ figure is the evidence subset). Suggested revision: `"interaction_duration": "Over one year; 13,000+ total ChatGPT messages over the period; 200+ entered as evidence per court filings"`
- `data/mortality-data.json` → `2025-04-US-FSU` — update `additional_context.trial_status` to reflect October 19, 2026 confirmed trial date, November 3 jury selection
- `docs/sources/court-documents.md` → FSU section: add note on evidence volume and trial confirmation
- When Morales family lawsuit is filed: add as new docket entry in `docs/sources/court-documents.md` under "OpenAI Wrongful Death Suits"

---

*If you are struggling, please call or text 988 (US). International resources: findahelpline.com*
