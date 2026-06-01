---
name: Surat India Dual Suicide — Roshni Shirsat & Jyotsna Chaudhary (Gujarat, India)
description: Two college students (18 and 20) died by suicide in a temple washroom in Surat, Gujarat; police confirmed both had searched ChatGPT for suicide methods before the incident
type: new-case-candidate
tier: tier-2
surfaced_by: weekly-triage-2026-05-11
labels: new-case-candidate, tier-2, jurisdictional-verification-limited
---

## Candidate record

```json
{
  "id": "2026-03-IN-001",
  "name": "Roshni Shirsat",
  "name_type": "real",
  "age": 18,
  "date": "2026-03-06",
  "location": {
    "city": "Surat (Saniya village, Swaminarayan Temple)",
    "state": "Gujarat",
    "country": "India"
  },
  "platform": "ChatGPT",
  "chatbot_name": "ChatGPT",
  "interaction_duration": "Unknown (single or recent-prior session)",
  "outcome": "Death by suicide (two victims: Roshni Shirsat, 18, and Jyotsna Chaudhary, 20)",
  "mechanism_type": "relational_pathway",
  "mechanism_subtype": "method_research_without_intervention",
  "outcome_target": "self_harm",
  "key_factors": [
    "Both victims searched ChatGPT for suicide methods and drugs before the incident",
    "Police confirmed ChatGPT queries during investigation",
    "Anaesthetic syringes and suspected poison recovered at scene",
    "Victims found dead in washroom of Swaminarayan Temple, Saniya village, Surat",
    "Roshni Shirsat aged 18; Jyotsna Chaudhary aged 20 — both college students"
  ],
  "legal_action": "None confirmed (police investigation ongoing as of available reporting)",
  "sources": [
    "The Print (India): https://theprint.in/india/two-women-found-dead-in-temple-bathroom-anaesthesia-injections-chatgpt-query-point-to-suicide/2872744/",
    "NewsX: https://www.newsx.com/regionals/surat-shock-two-college-girls-found-dead-in-temple-washroom-after-injecting-anaesthetic-drugs-police-say-they-searched-chatgpt-for-how-to-die-watch-video-179473/",
    "ISH News (video report)",
    "StartupNews.fyi (English-language Indian tech press)"
  ],
  "verification_level": "Tier 2 Journalistic"
}
```

## Summary

On March 6, 2026, two college students — Roshni Shirsat (18) and Jyotsna Chaudhary (20) — were found dead in the washroom of Swaminarayan Temple, Saniya village, Surat, Gujarat, India. Police confirmed both had searched ChatGPT for suicide methods and drugs before the incident. Anaesthetic syringes and suspected poison were recovered at the scene.

This is believed to be the first documented dual-fatality incident linked to ChatGPT in India, and the first documented AI-related death case in India meeting this database's verification threshold.

Police confirmation of the ChatGPT queries places this at Tier 2 (police statement as a qualifying source approaching Tier 1, multiple Indian news outlets confirming). Court filings or a coroner's report mentioning AI interaction would upgrade this to Tier 1.

**Mechanism note:** This case differs from the method-coaching cases (Amaurie Lacey, Adam Raine) in that the AI apparently answered research queries about suicide methods without a documented extended relational dynamic. The interaction is most analogous to a search-engine-style query rather than a companion relationship. The taxonomy should be confirmed once primary documents are available.

**Note:** This incident is outside the May 4–11, 2026 search window (date of deaths: March 6, 2026). It is flagged here because it is not in `data/mortality-data.json` and constitutes a significant gap: two deaths, police-confirmed AI involvement, and multiple independent Indian news sources.

## Sources (tiered)

### Tier 1 — Juridical
- Police confirmation of ChatGPT searches (Surat Police, Gujarat) — cited in multiple news reports as the basis for identifying AI involvement. Primary police report has not been directly obtained.

### Tier 2 — Journalistic
- The Print (major independent Indian news outlet): https://theprint.in/india/two-women-found-dead-in-temple-bathroom-anaesthesia-injections-chatgpt-query-point-to-suicide/2872744/
- NewsX (Indian television news outlet): https://www.newsx.com/regionals/surat-shock-two-college-girls-found-dead-in-temple-washroom-after-injecting-anaesthetic-drugs-police-say-they-searched-chatgpt-for-how-to-die-watch-video-179473/
- ISH News (video news outlet, India)
- StartupNews.fyi (English-language Indian tech/startup press)

### Tier 3 — Preliminary
- Social media coverage circulating the story without additional primary sourcing

## Verification status

- [x] Case not already present in `data/mortality-data.json` — confirmed; no India entry
- [x] Multiple independent sources cross-referenced — The Print, NewsX, ISH News, StartupNews.fyi (four independent outlets; The Print and NewsX are editorially independent major Indian outlets)
- [ ] Primary police report reviewed — Surat Police document not directly obtained; police attribution comes via news reporting
- [ ] Coroner or medical examiner report — not available in English-language sources
- [x] Adult and minor victim: Jyotsna Chaudhary (20) — adult name as publicly reported. Roshni Shirsat (18) — legal adult in India; name reported publicly. Both names are public via major Indian news outlets.
- [x] Non-US / non-English jurisdiction gap noted — label `jurisdictional-verification-limited` applied; Indian legal documents not directly obtained

## Open questions

1. **Surat Police report** — Primary police document confirming ChatGPT queries should be obtained (or verified directly with the Surat City Police or Gujarat Police digital division) before publication.
2. **ChatGPT response content** — Unknown what ChatGPT provided in response to the queries. If it gave specific suicide method information, this strengthens causal connection; if it deflected to crisis resources, that is material context.
3. **Mechanism clarification** — The interaction appears to be method-research rather than a sustained relational engagement; taxonomy should be `relational_pathway / method_research_without_intervention` or potentially a new sub-type. The methodology team should consider whether a single ChatGPT query for method information constitutes the same "significant documented factor" standard as the multi-month companion relationships in other cases.
4. **Family consent** — Families of both victims have not been publicly identified in available sources as having spoken to media; verify before publishing victim names in a US-based database.
5. **Hindi-language coverage** — Hindi-language Indian press coverage should be checked for additional primary sourcing; the current sources are English-language Indian outlets.
6. **OpenAI response** — No public statement from OpenAI regarding this case has been found.

## Three-question gate (methodology.md:157–163)

1. *Would the families of the deceased recognize this entry as accurate and respectful?* — Victim names are publicly reported in major Indian outlets; entry is factual and respectful. Caveated on family wishes not having been verified. **Conditionally yes — verify family preference before publishing.**
2. *Would the platform's lawyers find it defensible as factual reporting?* — Claims sourced to police statement and multiple Indian news outlets; connection attributed to ChatGPT use is factual per police. **Yes, with appropriate "police allege" framing.**
3. *Would a researcher cite it without peer-review issues?* — Multiple independent outlets plus police statement; methodology note on mechanism type clearly labeled. **Yes.**

**All three: Conditionally yes. Recommend hold for one additional action (verify family preferences and/or obtain Surat Police report), then promote to Tier 2.**

## Recommended next step

1. Verify Surat Police report directly or through Gujarat Police RTI/press office to confirm ChatGPT search details.
2. Check Hindi-language Indian press for additional sourcing.
3. Clarify what ChatGPT returned in response to the queries.
4. Confirm family preferences regarding publication of names.
5. If confirmed, add to `data/mortality-data.json` as a dual-fatality event, possibly with two separate incident records (`2026-03-IN-001` and `2026-03-IN-002`) or a single event record.

---

*If you are struggling, please call or text 988 (US Suicide and Crisis Lifeline). India: iCall 9152987821. International resources: findahelpline.com*
