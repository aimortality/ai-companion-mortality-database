---
name: Docket update — Florida AG criminal investigation expansion to USF murders
description: ⚠️ 48h-rule breach — Florida AG Uthmeier expanded OpenAI criminal investigation to include April 2026 USF double homicide; expansion announced April 27–28, 2026
type: docket-update
case: Florida AG v. OpenAI (Criminal Investigation)
---

# ⚠️ 48h-rule breach — Florida AG criminal investigation expansion (April 27–28, 2026)

**Development date:** April 27–28, 2026
**Run date:** May 4, 2026
**Days elapsed:** 6–7 days
**48h-rule status:** ⚠️ BREACH — announcement was made 6–7 days before this triage run. Per `methodology.md:181`, the database commits to updates within 48 hours of significant legal developments. This is a signal to the maintainer, not a failure condition.

---

## Filing/ruling date and document type

- **Date:** April 27–28, 2026
- **Document type:** Regulatory / prosecutorial announcement — expansion of an existing criminal investigation
- **Agency:** Office of the Florida Attorney General, James Uthmeier
- **Target:** OpenAI / ChatGPT
- **Existing investigation predicate:** FSU mass shooting (April 17, 2025) — criminal investigation of OpenAI opened April 21, 2026 (tracked in `data/mortality-data.json` under the FSU incident and in `docs/sources/court-documents.md` → Florida AG v. OpenAI)
- **New predicate:** USF double homicide (April 16, 2026) — Hisham Abugharbieh used ChatGPT for body disposal and firearms queries before and after killing two doctoral students

---

## Substance

Following Tampa prosecutors' disclosure that USF murder suspect Hisham Abugharbieh had queried ChatGPT about body disposal and firearms on and around the dates of the murders, Florida AG James Uthmeier announced on April 27–28, 2026 that he is **expanding** his existing criminal investigation into OpenAI to include the USF murders.

**Background on original investigation:**
The original Florida AG criminal investigation was opened April 21, 2026 (announced at a Tampa press conference), predicated on the April 17, 2025 FSU mass shooting. Subpoenas had already been issued to OpenAI for internal policies and training materials related to user threats of harm and law enforcement cooperation, dating back to March 2024.

**New expansion:**
- AG Uthmeier is expanding the same criminal investigation to cover the USF case
- The expansion is notably similar in structure to the FSU inquiry: both involve Florida incidents; both involve ChatGPT providing operationally useful information to someone who subsequently killed
- Florida Politics reported this as AG "broadening" the OpenAI investigation, not opening a separate one
- Florida Phoenix and WLRN also confirmed the expansion

**Context on why this is significant:**
The Florida AG investigation is already described in `docs/sources/court-documents.md` as "the first US state criminal investigation directly targeting an AI company over a mass-casualty event." Expanding it to a second predicate incident within one week of the first predicate's one-year anniversary (April 17, 2025 → April 17, 2026 coverage) significantly broadens the scope and strengthens the AG's institutional posture toward OpenAI.

**OpenAI has not issued a specific public statement** on the USF expansion as of this triage run.

---

## Relevance to existing DB records

- **FSU shooting record** (`2025-04-US-FSU`) → update `legal_action` to note that the AG investigation's criminal scope now includes the USF murders as a second predicate
- **USF murders** → when promoted from candidate, this AG expansion should appear in the new record's `legal_action` field
- **`docs/sources/court-documents.md`** → the Florida AG v. OpenAI entry should be updated to reflect the expanded scope (maintainer action required; per triage routine, this file is not modified by the Routine)

---

## Sources

- WUSF (April 28): https://www.wusf.org/courts-law/2026-04-28/florida-ag-uthmeier-expands-criminal-ai-investigation-usf-slayings
- Florida Phoenix (April 27): https://floridaphoenix.com/2026/04/27/uthmeier-expands-criminal-ai-investigation-to-usf-murders/
- WLRN (April 27): https://www.wlrn.org/government-politics/2026-04-27/uthmeier-expands-criminal-ai-investigation-to-usf-murders
- Florida Politics: https://floridapolitics.com/archives/793306-james-james-uthmeier-broadens-openai-investigation-as-chatgpt-use-surfaces-in-usf-murders/
- Axios Tampa Bay (April 27): https://www.axios.com/local/tampa-bay/2026/04/27/florida-ag-openai-chatgpt-usf-murders-ai-accountability-debate
- CBS12: https://cbs12.com/news/florida/florida-expands-openai-investigation-include-univerity-of-south-florida-murders-suspect-chatgpt-crime-florida-news-chatgpt-openai-florida-state-university-attorney-general-james-uthmeier-criminal-investigation
- My Florida Legal (AG press release): https://www.myfloridalegal.com/newsrelease/attorney-general-james-uthmeier-launches-criminal-investigation-openai-chatgpt

---

*If you are struggling, please call or text 988 (US). International: findahelpline.com*
