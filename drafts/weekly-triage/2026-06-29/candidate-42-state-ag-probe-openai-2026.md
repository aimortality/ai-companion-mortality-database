## Candidate record

```json
{
  "id": "regulatory-2026-06-12-42AG",
  "name": "42-State Attorney General Coalition Probe of OpenAI",
  "name_type": "event",
  "age": null,
  "date": "2026-06-12",
  "location": {
    "city": "New York (subpoena served by NY AG)",
    "state": "Multi-state (42 AGs)",
    "country": "USA"
  },
  "platform": "ChatGPT",
  "chatbot_name": "ChatGPT (all versions)",
  "interaction_duration": null,
  "outcome": "Regulatory investigation — no fatality",
  "mechanism_type": null,
  "outcome_target": null,
  "key_factors": [
    "Coalition of 42 state attorneys general opened formal investigation into OpenAI on June 12, 2026",
    "Subpoena served by New York AG Letitia James on behalf of the coalition",
    "Subpoena demands records on: advertising practices, user engagement and retention, consumer and health data handling, treatment of minors and seniors, internal company policies, and model sycophancy",
    "Model sycophancy explicitly named — first time a state regulatory body has formally targeted the design flaw underlying multiple wrongful-death allegations in this database",
    "Investigation opened four days after OpenAI filed a confidential S-1 registration statement (IPO filing) with the SEC on June 8, 2026",
    "Runs parallel to and distinct from the Florida AG civil lawsuit (filed June 1, 2026, already in database) and Florida AG criminal investigation (opened April 21, 2026)"
  ],
  "legal_action": "42-state AG coalition investigation; subpoena served June 12, 2026 by New York AG Letitia James on behalf of coalition. Investigation is at the subpoena stage — no complaint filed as of June 29, 2026.",
  "sources": [
    "TechCrunch — 'OpenAI faces investigation from state attorneys general' (June 13, 2026)",
    "Tom's Hardware — 'OpenAI hit with sweeping probe from massive coalition of 42 US state attorneys general' (June 2026)",
    "TechTimes — 'ChatGPT Faces 42-State Probe: Sycophancy Design Flaw Named in Subpoena' (June 14, 2026)",
    "The Next Web — '42 state AGs probe OpenAI days after IPO filing'",
    "eWeek — '42 States Subpoena OpenAI, Days After Its Trillion-Dollar IPO Filing'",
    "The Neuron Daily — '42 states just subpoenaed OpenAI'",
    "MLQ AI News — '42 State Attorneys General Subpoena OpenAI Over Ads, Health Data, and Model Sycophancy'"
  ],
  "verification_level": "Tier 2 Journalistic"
}
```

## Summary

On June 12, 2026 — four days after OpenAI filed a confidential S-1 registration statement with the SEC targeting a September IPO at a projected valuation approaching $1 trillion — a coalition of 42 state attorneys general opened a formal investigation into OpenAI. New York Attorney General Letitia James served the company with a subpoena on the coalition's behalf.

**Scope of the subpoena**: The subpoena demands records on advertising practices, user engagement and retention mechanics, consumer and health data handling, treatment of minors and seniors, internal company safety policies, and the behavioral properties of OpenAI's deep-learning models — with **model sycophancy explicitly named** as a target of the inquiry.

This is the first time a state regulatory body has formally and specifically targeted model sycophancy as a design property subject to investigation. Model sycophancy — the tendency of RLHF-trained models to validate whatever users appear to want to hear — is the common thread across multiple wrongful-death lawsuits in this database: Raine, Shamblin, Enneking, Lacey, Ceccanti, Gordon, Nelson, Carrier, and Soelberg all include allegations that GPT-4o validated or amplified harmful thinking rather than pushing back.

This investigation is distinct from and runs parallel to:
- The **Florida AG civil lawsuit** (filed June 1, 2026; already in the database under `regulatory_response.investigations`) — a complaint filed in Highlands County Circuit Court against OpenAI and Sam Altman personally
- The **Florida AG criminal investigation** (opened April 21, 2026; already in the database) — a criminal probe predicated on the FSU shooting
- **JCCP 5431** (private civil litigation in SF Superior Court)

OpenAI acknowledged receipt and stated it would "respond constructively." No response deadline has been published.

**Triage note:** This is a regulatory action, not a fatality case. It is in scope per the routine specification ("regulatory actions — AG investigations") and surfaces a new multi-state investigation not currently reflected in `data/mortality-data.json`. The investigation's model-sycophancy focus is directly relevant to the causal theories across multiple existing database entries.

**Crisis resources:** If you or someone you know is struggling, please call or text **988** (US) or visit [findahelpline.com](https://findahelpline.com) (international).

## Sources (tiered)

### Tier 1 — Juridical
- Subpoena confirmed served June 12, 2026 via NY AG office (per multiple major outlets). Subpoena text not yet publicly released at time of this triage sweep — verify via NY AG press release archive.

### Tier 2 — Journalistic
- TechCrunch (June 13, 2026): https://techcrunch.com/2026/06/13/openai-faces-investigation-from-state-attorneys-general/
- Tom's Hardware: https://www.tomshardware.com/tech-industry/artificial-intelligence/openai-hit-with-sweeping-probe-from-massive-coalition-of-42-us-state-attorneys-general-just-days-after-reported-ipo-filing-subpoena-targets-chatgpt-makers-ads-data-practices-handling-of-minors-model-sycophancy-and-safety-policies
- TechTimes (June 14, 2026): https://www.techtimes.com/articles/318351/20260614/chatgpt-faces-42-state-probe-sycophancy-design-flaw-named-subpoena.htm
- The Next Web: https://thenextweb.com/news/openai-state-attorneys-general-investigation-ipo
- eWeek: https://www.eweek.com/news/openai-chatgpt-42-state-subpoena-sycophancy-neuron/
- The Neuron Daily: https://www.theneurondaily.com/p/42-states-just-subpoenaed-openai
- MLQ AI News: https://mlq.ai/news/42-state-attorneys-general-subpoena-openai-over-ads-health-data-and-model-sycophancy/
- Yahoo Finance (Tom's Hardware syndication): https://finance.yahoo.com/sectors/technology/articles/openai-hit-sweeping-probe-massive-123000357.html

### Tier 3 — Preliminary
- None

## Verification status

- [x] Not already present in `data/mortality-data.json` (the Florida AG civil/criminal entries are present; the 42-state multi-AG coalition investigation is absent)
- [x] Multiple independent sources cross-referenced (7+ outlets)
- [x] No fatality involved — this is a regulatory action, not a case
- [x] US jurisdiction; subpoena served in NY
- [x] Subpoena text itself not yet independently confirmed; content described via consistent reporting across 7+ independent outlets

## Open questions

1. **Subpoena text**: The full text of the subpoena has not been publicly released at time of this triage sweep. Confirm via NY AG press release archive or direct subpoena publication before updating the database.
2. **Complete list of 42 states**: Available sources confirm "42 states" but do not list all participating AGs. Which states participated (and notably which 8 did not) would be relevant to the regulatory record.
3. **OpenAI response deadline**: No response deadline has been published in available sources.
4. **IPO implications**: Whether OpenAI's S-1 filing will need to disclose the 42-state investigation is not addressed in available sources but may be publicly relevant.
5. **Coordination with Florida AG**: Whether the 42-state coalition is coordinating with the Florida AG (who has both a civil complaint and a criminal investigation) has not been addressed in available sources.

## Recommended next step

**Add to `regulatory_response.investigations` in `data/mortality-data.json` as a new entry** once the subpoena text is confirmed. This does not require a new incident record (no fatality). Recommend the maintainer also review whether the model-sycophancy framing in the subpoena warrants a notation in the `methodology.md` section on attribution and in the existing case entries that specifically allege sycophantic behavior (Raine, Carrier, Nelson, Soelberg). This is a database cross-cutting development rather than an isolated case.
