---
name: Gangbuk Motel Serial Murders — Kim Soyoung (Seoul, South Korea)
description: 21-year-old woman indicted for drugging and killing two men in Seoul motel rooms; police cited ChatGPT history researching lethal doses as evidence of intent
type: new-case-candidate
tier: tier-1
surfaced_by: weekly-triage-2026-05-11
labels: new-case-candidate, tier-1, jurisdictional-verification-limited
---

## Candidate record

```json
{
  "id": "2026-01-KR-001",
  "name": "Gangbuk Motel Serial Murders (two victims unnamed in available English sources)",
  "name_type": "event",
  "age": null,
  "date": "2026-01-28",
  "location": {
    "city": "Gangbuk-gu, Seoul",
    "state": null,
    "country": "South Korea"
  },
  "platform": "ChatGPT",
  "chatbot_name": "ChatGPT",
  "interaction_duration": "Single session (three days before first killing)",
  "outcome": "Murder (two men killed; one man survived earlier December 2025 attempt)",
  "mechanism_type": "instrumental_pathway",
  "mechanism_subtype": "violence_planning_lethality_research",
  "outcome_target": "violence_against_others",
  "perpetrator": {
    "name": "Kim Soyoung",
    "age": 21,
    "relationship": "Stranger (met victims via apps/dating channels)",
    "status": "Indicted March 10, 2026 on charges of murder, aggravated assault, and narcotics violations"
  },
  "key_factors": [
    "Kim Soyoung allegedly drugged and killed two men in their 20s in Gangbuk-gu motel rooms (January 28 and February 9, 2026); a third man survived a December 2025 attempt",
    "Police found her ChatGPT search history asked 'What happens if you take a lot of sleeping pills?' and 'Could it kill someone?' three days before the first killing",
    "Police characterised the ChatGPT searches as establishing premeditation and described them as 'the smoking gun'",
    "Victims' drinks spiked with benzodiazepines",
    "Indicted March 10, 2026; charges include murder, aggravated assault, narcotics law violations"
  ],
  "legal_action": "Indictment filed March 10, 2026 (South Korean criminal court, Gangbuk jurisdiction)",
  "sources": [
    "Korea Herald (English): https://www.koreaherald.com/article/10678557",
    "Fortune: https://fortune.com/2026/03/02/seoul-south-korea-woman-chatgpt-two-murders/",
    "South China Morning Post: https://www.scmp.com/week-asia/people/article/3345411/south-korean-drink-spike-killer-quizzed-chatgpt-lethal-doses-police-say",
    "Korea-language: Newdaily, Nate News, Daum/Korea Daily (Korean original source)"
  ],
  "verification_level": "Tier 1 Juridical"
}
```

## Summary

Kim Soyoung, 21, was indicted on March 10, 2026 for the murders of two men in their 20s in Gangbuk-gu motel rooms in Seoul, South Korea. The killings occurred on January 28 and February 9, 2026; a third man survived an earlier attempt in December 2025.

According to police, Kim Soyoung spiked the victims' drinks with benzodiazepines. Investigators recovered her ChatGPT search history, which included the queries "What happens if you take a lot of sleeping pills?" and "Could it kill someone?" — searched three days before the first killing. Police publicly described the ChatGPT history as the "smoking gun" establishing premeditation.

This case follows the same *instrumental pathway* taxonomy as the DeepSeek/Roberts case (Wales, October 2025) and the FSU shooting (April 2025): the perpetrator used an AI system as a research tool in pre-attack planning, not as a relational companion. It would be the first instrumental-pathway case involving a female perpetrator and the first case originating in South Korea.

The two victims are two men in their 20s whose names have not been published in available English-language sources. Korean-language reporting (Korea Herald, Newdaily, Nate News) may carry full names — see Open Questions below.

## Sources (tiered)

### Tier 1 — Juridical
- Indictment filed March 10, 2026 in South Korean criminal court (confirmed via multiple independent news reports citing prosecution; primary court document in Korean — see Open Questions)

### Tier 2 — Journalistic
- Korea Herald (English-language South Korean outlet with editorial standards): https://www.koreaherald.com/article/10678557
- Fortune (US major outlet): https://fortune.com/2026/03/02/seoul-south-korea-woman-chatgpt-two-murders/
- South China Morning Post (regional major outlet, independent): https://www.scmp.com/week-asia/people/article/3345411/south-korean-drink-spike-killer-quizzed-chatgpt-lethal-doses-police-say
- Asia Business Daily (indictment confirmation, Korean-language)
- Newdaily, Nate News, Daum/Korea Daily (Korean-language; primary domestic coverage)

### Tier 3 — Preliminary
- None needed; Tier 1 and Tier 2 evidence is sufficient

## Verification status

- [x] Case not already present in `data/mortality-data.json` — confirmed
- [x] Multiple independent sources cross-referenced — Korea Herald, Fortune, SCMP (three independent outlets minimum); Korean-language corroboration
- [ ] Primary Korean court document reviewed — Korean criminal docket access required; English-language reporting is consistent across outlets but indictment text has not been directly obtained
- [x] Adult victims (men in their 20s) — pseudonyms may apply once victim names are confirmed; perpetrator name (Kim Soyoung) is public via indictment
- [x] Non-US jurisdiction gap noted — label `jurisdictional-verification-limited` applied

## Open questions

1. **Victim names** — Available English-language reporting does not name the two murder victims. Korean-language sources may identify them; their families' preferences regarding publication should be researched before adding names.
2. **Primary court document** — The indictment text and specific charges are reported in Korean; direct access to the Gangbuk District Court filing would confirm exact charge language and victim details.
3. **Mechanism specificity** — Whether Kim Soyoung used ChatGPT to determine benzodiazepine lethal doses specifically, or had a broader research session, is unclear from English-language sources. Korean reporting may be more granular.
4. **Survivor (December 2025 attempt)** — The third victim who survived is not named or described in available sources. This attempt may constitute a "Survived attempt" sub-record.
5. **Scoping question** — This is an instrumental pathway case where AI was used to research lethality before killings; the AI involvement is analogous to the DeepSeek/Roberts case (weapon-selection research). Confirm that this meets the database's "significant, documented factor" threshold before publishing.
6. **OpenAI / ChatGPT response** — No public statement from OpenAI regarding this case has been found.

## Three-question gate (methodology.md:157–163)

1. *Would the family of the deceased recognize this entry as accurate and respectful?* — The two murder victims are described factually based on police and prosecution statements. Victim identities are not yet named in English sources. Entry is accurate to available information and respectful in framing. **Yes, pending victim name verification.**
2. *Would the platform's lawyers find it defensible as factual reporting?* — The ChatGPT history is attributed to police and prosecution; the indictment is a public record. All claims are sourced to official proceedings. **Yes.**
3. *Would a researcher cite it without peer-review issues?* — Tier 1 (indictment) plus three-outlet Tier 2 cross-referencing including the Korea Herald as the primary domestic outlet. **Yes.**

**All three: Yes. Recommend Tier 1 publication pending victim name verification and Korean court document review.**

## Recommended next step

1. Obtain Korean court indictment (Gangbuk District Court) to confirm victim names and charge details.
2. Research Korean-language coverage (Nate News, Newdaily) for victim names and their families' public statements.
3. If victims are named publicly and families have not requested non-publication, add to `data/mortality-data.json` as `2026-01-KR-001` (first killing January 28) and/or `2026-02-KR-001` (second killing February 9), or as a single event record.
4. Contact OpenAI for statement.

---

*If you are struggling, please call or text 988 (US Suicide and Crisis Lifeline). International resources: findahelpline.com*
