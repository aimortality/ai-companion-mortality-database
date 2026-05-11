---
name: USF Tampa Murders — Zamil Limon & Nahida Bristy (Tampa, Florida)
description: Two Bangladeshi doctoral students at USF murdered by roommate who allegedly searched ChatGPT for body disposal before the killings; Florida AG criminal investigation expanded to encompass this case
type: new-case-candidate
tier: tier-1
surfaced_by: weekly-triage-2026-05-11
labels: new-case-candidate, tier-1
---

## Candidate record

```json
{
  "id": "2026-04-US-001",
  "name": "Zamil Limon",
  "name_type": "real",
  "age": null,
  "date": "2026-04-16",
  "location": {
    "city": "Tampa",
    "state": "Florida",
    "country": "USA"
  },
  "platform": "ChatGPT",
  "chatbot_name": "ChatGPT",
  "interaction_duration": "Single pre-crime session (April 13, 2026, three days before disappearances)",
  "outcome": "Murder (two victims: Zamil Limon and Nahida Bristy)",
  "mechanism_type": "instrumental_pathway",
  "mechanism_subtype": "violence_planning_body_disposal_research",
  "outcome_target": "violence_against_others",
  "perpetrator": {
    "name": "Hisham Abugharbieh",
    "age": null,
    "relationship": "Roommate",
    "status": "Charged with two counts of first-degree murder; in custody"
  },
  "victims": [
    {"name": "Zamil Limon", "age_approximate": "doctoral student", "nationality": "Bangladeshi", "affiliation": "University of South Florida"},
    {"name": "Nahida Bristy", "age_approximate": "doctoral student", "nationality": "Bangladeshi", "affiliation": "University of South Florida"}
  ],
  "key_factors": [
    "Suspect Hisham Abugharbieh allegedly searched ChatGPT on April 13, 2026: 'What happens if a human is put in a black garbage bag and thrown in a dumpster?'",
    "ChatGPT query preceded victims' disappearances by three days (April 16, 2026)",
    "Limon's body found April 24 in a black trash bag on the Howard Franklin Bridge, Tampa Bay",
    "Bristy's decomposed remains found April 26",
    "Florida AG James Uthmeier expanded criminal investigation into OpenAI to include this case on April 27, 2026",
    "Case charged as two counts of first-degree murder"
  ],
  "legal_action": "Criminal charges: two counts of first-degree murder against Hisham Abugharbieh. Florida AG criminal investigation (expanded April 27, 2026) seeking to assess OpenAI's liability for ChatGPT's response to the body-disposal query.",
  "sources": [
    "WUSF: https://www.wusf.org/courts-law/2026-04-29/how-suspect-killing-two-usf-students-used-chatgpt",
    "CNN (multiple articles)",
    "NBC News: https://www.nbcnews.com/news/us-news/suspect-murder-florida-college-students-asked-chatgpt-putting-person-d-rcna342211",
    "Washington Post",
    "Axios Tampa Bay: https://www.axios.com/local/tampa-bay/2026/04/27/florida-ag-openai-chatgpt-usf-murders-ai-accountability-debate"
  ],
  "verification_level": "Tier 1 Juridical"
}
```

## Summary

Zamil Limon and Nahida Bristy, Bangladeshi doctoral students at the University of South Florida, disappeared on April 16, 2026. Limon's body was found on April 24 in a black trash bag on the Howard Franklin Bridge over Tampa Bay; Bristy's decomposed remains were found on April 26. Their roommate Hisham Abugharbieh has been charged with two counts of first-degree murder.

Prosecutors allege that on April 13, 2026 — three days before the victims disappeared — Abugharbieh asked ChatGPT: "What happens if a human is put in a black garbage bag and thrown in a dumpster?" He also made other violence-related ChatGPT searches. Investigators used this search history as evidence of premeditation.

On April 27, 2026, Florida Attorney General James Uthmeier expanded his criminal investigation into OpenAI — originally opened April 21 over the FSU shooting — to include this case. This is the second AI-platform-linked murder investigation brought by the Florida AG, and the first to involve post-crime as well as pre-crime AI use.

This case follows the same *instrumental pathway* taxonomy as the FSU shooting (April 2025), the Tumbler Ridge mass shooting (February 2026), and the DeepSeek/Roberts case (Wales, October 2025): the perpetrator used ChatGPT as a research tool in planning. It is distinct in that the AI query apparently addressed body disposal specifically rather than weapon selection or attack planning.

**Note:** This incident is outside the May 4–11, 2026 search window (murders occurred April 16–17; bodies discovered April 24–26; FL AG expansion April 27). It is flagged here because it is not yet in `data/mortality-data.json` and constitutes a significant gap given its Tier 1 evidence and direct connection to the Florida AG investigation already tracked in the database.

## Sources (tiered)

### Tier 1 — Juridical
- Criminal charges filed against Hisham Abugharbieh (two counts first-degree murder) — confirmed by multiple major outlets
- Florida AG official expansion of criminal investigation, April 27, 2026: https://www.myfloridalegal.com/newsrelease/attorney-general-james-uthmeier-launches-criminal-investigation-openai-chatgpt (Florida AG press office)
- Arrest and arraignment records (Hillsborough County, Florida — exact case number not confirmed in available public sources; check Hillsborough County Clerk)

### Tier 2 — Journalistic
- WUSF (NPR member station, primary investigative reporting): https://www.wusf.org/courts-law/2026-04-29/how-suspect-killing-two-usf-students-used-chatgpt
- NBC News: https://www.nbcnews.com/news/us-news/suspect-murder-florida-college-students-asked-chatgpt-putting-person-d-rcna342211
- CNN (multiple independent articles)
- Washington Post (independent)
- Axios Tampa Bay: https://www.axios.com/local/tampa-bay/2026/04/27/florida-ag-openai-chatgpt-usf-murders-ai-accountability-debate

### Tier 3 — Preliminary
- None needed; Tier 1 and Tier 2 coverage is sufficient

## Verification status

- [x] Case not already present in `data/mortality-data.json` — confirmed; no entry for Limon, Bristy, or April 2026 Tampa/USF murders
- [x] Multiple independent sources cross-referenced — WUSF, NBC, CNN, Washington Post, Axios (5+ independent outlets)
- [ ] Primary court filing reviewed — Hillsborough County criminal case number not yet confirmed; charge details come from news reporting; direct court access needed
- [x] Adult victims — names used as they have been publicly identified in major news coverage
- [x] US jurisdiction — standard English-language media access

## Open questions

1. **Hillsborough County criminal case number** — Exact docket reference for the Abugharbieh murder charges should be confirmed via the Hillsborough County Clerk's office.
2. **ChatGPT response to the query** — Available reporting does not specify what ChatGPT answered to the body-disposal query. If ChatGPT provided useful information (analogous to the DeepSeek/Roberts "hammer recommendation"), that would significantly affect the causal analysis. If it refused, the case is more analogous to "attempted instrumental use."
3. **Victims' ages** — Specific ages of Limon and Bristy are not confirmed in available English-language reporting.
4. **Additional AI queries** — Reporting mentions "other violence-related searches" but does not detail them; primary court documents would clarify scope of ChatGPT involvement.
5. **Florida AG scope** — Whether the AG is investigating OpenAI's response to the body-disposal query specifically, or the broader pattern of violent AI use, will determine how this case is framed in the database.
6. **OpenAI statement** — No public statement from OpenAI specifically regarding this case has been found. OpenAI generally stated it cooperates with law enforcement.

## Three-question gate (methodology.md:157–163)

1. *Would the families of the deceased recognize this entry as accurate and respectful?* — Victim names and identities are taken from verified reporting and court proceedings; framing is factual without sensationalism. **Yes.**
2. *Would the platform's lawyers find it defensible as factual reporting?* — All claims sourced to court records and official FL AG statements. The ChatGPT query is attributed to prosecution allegations in active criminal proceedings. **Yes.**
3. *Would a researcher cite it without peer-review issues?* — Tier 1 (criminal charges filed, FL AG expansion) and five-outlet Tier 2 cross-referencing. **Yes.**

**All three: Yes. Recommend Tier 1 publication pending Hillsborough County case number confirmation.**

## Recommended next step

1. Confirm Hillsborough County criminal docket number for State v. Abugharbieh.
2. Obtain charging documents to verify exact ChatGPT query language and what response (if any) ChatGPT gave.
3. If ChatGPT's response materially assisted, add to `data/mortality-data.json` under a new record; if it did not respond helpfully, note this as mitigating context.
4. Coordinate with the Florida AG investigation record already in the database (FSU shooting) — this case may warrant a new FL AG investigation sub-entry.

---

*If you are struggling, please call or text 988 (US Suicide and Crisis Lifeline). International resources: findahelpline.com*
