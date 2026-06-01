---
name: Docket update — Florida AG criminal investigation into OpenAI (expanded to USF murders, April 27, 2026; subpoena deadline May 1, 2026)
description: ⚠️ 48h-rule breach — FL AG expanded criminal investigation to USF student murders on April 27; May 1 subpoena deadline passed without public confirmation of OpenAI compliance
type: docket-update
case: Florida AG v. OpenAI (criminal investigation — FSU + USF expansion)
---

# ⚠️ 48h-rule breach — Florida AG Expands Investigation to USF Murders; Subpoena Deadline Passed

**Development date:** April 27, 2026 (USF expansion announced); May 1, 2026 (subpoena response deadline)
**48h-rule status:** ⚠️ BREACH — USF expansion is 14 days old at time of this run (May 11); subpoena deadline passed 10 days ago.

## Substance

The database currently tracks the Florida AG's criminal investigation into OpenAI as relating to the FSU mass shooting (April 17, 2025). Two significant developments have occurred since the database was last updated (April 23, 2026):

### 1. Expansion to USF Student Murders (April 27, 2026)

On April 27, 2026 — six days after opening the FSU-related criminal probe — AG James Uthmeier expanded the investigation to encompass the April 2026 University of South Florida student murders. Specifically:

- Zamil Limon and Nahida Bristy, Bangladeshi doctoral students at USF, disappeared April 16, 2026.
- Limon's body was found April 24 in a black trash bag on the Howard Franklin Bridge, Tampa Bay; Bristy's remains were found April 26.
- Suspect Hisham Abugharbieh is charged with two counts of first-degree murder.
- Prosecutors allege Abugharbieh asked ChatGPT "What happens if a human is put in a black garbage bag and thrown in a dumpster?" on April 13 — three days before the murders.
- AG Uthmeier expanded the criminal investigation into OpenAI to assess whether ChatGPT's response to this query constitutes criminal liability.

This is the second major instrumental-pathway event the Florida AG is investigating in connection with OpenAI in a single month. It substantially broadens the AG's theory of liability from "violence planning for mass shootings" to "body disposal research."

### 2. Subpoena Response Deadline — May 1, 2026 (passed)

The subpoenas issued to OpenAI as part of the criminal investigation (announced April 21, 2026) carried a response deadline of approximately May 1, 2026. As of the May 11, 2026 run date, no public reporting has confirmed whether:
- OpenAI complied with the subpoenas
- OpenAI challenged the subpoenas (potentially in federal court)
- The AG has taken any enforcement action in response

OpenAI stated publicly on April 21 that it would "cooperate" with the investigation. The silence following the deadline is notable and should be monitored.

## Sources

- Florida AG press release (April 27, 2026 expansion): https://www.myfloridalegal.com/newsrelease/attorney-general-james-uthmeier-launches-criminal-investigation-openai-chatgpt
- WUSF (NPR member station, USF case coverage): https://www.wusf.org/courts-law/2026-04-28/florida-ag-uthmeier-expands-criminal-ai-investigation-usf-slayings
- Florida Phoenix
- Axios Tampa Bay: https://www.axios.com/local/tampa-bay/2026/04/27/florida-ag-openai-chatgpt-usf-murders-ai-accountability-debate
- CNN; NBC News (general USF case coverage)

## Database updates required

- `data/mortality-data.json`, ChatGPT platform entry: Update `legal_status` to reflect expanded FL AG investigation.
- `data/mortality-data.json`, incident `2025-04-US-FSU` (FSU shooting): Update `legal_action` to note USF expansion and subpoena deadline status.
- `data/mortality-data.json`, `regulatory_response.investigations`: Update the Florida AG criminal entry to note USF expansion and subpoena deadline.
- Note: A new incident record for the USF murders (Limon/Bristy) is proposed in `candidate-usf-tampa-murders.md` in this same PR.

---

*If you are struggling, please call or text 988 (US). International: findahelpline.com*
