## Candidate record

```json
{
  "id": "2026-01-KR-001",
  "name": "Kim So-young",
  "name_type": "real",
  "age": 20,
  "date": "2026-01-28",
  "location": {
    "city": "Seoul (Gangbuk-gu)",
    "state": null,
    "country": "South Korea"
  },
  "platform": "ChatGPT",
  "chatbot_name": "ChatGPT",
  "interaction_duration": "At least from December 2025 through February 2026",
  "outcome": "Murder (2 third-party victims killed; 1 seriously injured)",
  "mechanism_type": "instrumental_pathway",
  "mechanism_subtype": "violence_planning_weapon_selection",
  "outcome_target": "violence_against_others",
  "key_factors": [
    "Kim asked ChatGPT 'What happens if you take sleeping pills with alcohol?' and 'How much is dangerous?' before the first attack",
    "After the first victim survived, Kim consulted ChatGPT about lethal dosages and increased the amount for subsequent attacks",
    "ChatGPT search history forensically extracted from Kim's phone and used by Seoul Gangbuk Police as evidence of premeditated intent",
    "Three attacks in Seoul motel rooms (Gangbuk-gu district) between December 2025 and February 2026: Dec 2025 (victim survived, serious injury), Jan 28 2026 (victim died), Feb 9 2026 (victim died)",
    "Kim laced drinks with benzodiazepines she was prescribed for a mental illness",
    "Identity of perpetrator publicly disclosed by Seoul Northern District Prosecutors' Office on March 9, 2026",
    "Charges upgraded from 'inflicting bodily injury resulting in death' (Feb 11 arrest) to two counts of murder"
  ],
  "legal_action": "Arrested February 11, 2026 (Seoul Gangbuk Police). Charges upgraded to 2 counts of murder. Sent to prosecutor by Seoul Gangbuk Police on murder charges. Seoul Northern District Prosecutors' Office conducting prosecution.",
  "sources": [
    "The Korea Herald (https://www.koreaherald.com/article/10678557)",
    "Fortune (https://fortune.com/2026/03/02/seoul-south-korea-woman-chatgpt-two-murders/)",
    "NBC News (https://www.nbcnews.com/tech/tech-news/chatgpt-advised-south-korea-woman-3-men-poison-police-say-rcna344063)",
    "South China Morning Post",
    "Vice",
    "TechRadar",
    "Mothership.SG (https://mothership.sg/2026/02/seoul-woman-murder-chatgpt/)",
    "Controverity (https://controverity.com/2026/02/27/chatgpt-searches-cited-in-south-korea-double-murder-case/)",
    "Evrimagaci / Grand Pinnacle Tribune",
    "AOL/Yahoo News"
  ],
  "verification_level": "Tier 2 Journalistic"
}
```

## Summary

Kim So-young (20), a South Korean woman, conducted a series of drug-poisoning attacks against men she met through dates at hotels in Seoul's Gangbuk-gu district between December 2025 and February 2026. She used ChatGPT to research the lethality of combining sleeping pills (benzodiazepines) with alcohol before the first attack; after that victim survived, she queried ChatGPT again about lethal dosages and adjusted the amount for the second and third attacks, both of which killed their victims.

The Seoul Gangbuk Police forensically extracted ChatGPT conversations from Kim's phone and are using them as direct evidence of premeditated intent — a legally significant development noted by prosecutors as "highly noteworthy" because it represents one of the first uses of ChatGPT conversations as direct murder-intent evidence in a criminal proceeding. Kim's identity was publicly disclosed by the Seoul Northern District Prosecutors' Office on March 9, 2026.

The case constitutes the first documented instrumental-pathway chatbot case outside the English-speaking world and the first in East Asia in this database, and the first involving ChatGPT as a weapon-selection/method-refinement tool in a serial poisoning context.

**Note on timing:** The incident dates from December 2025–February 2026; primary English-language reporting broke on approximately February 27–March 2, 2026. This case was not captured by the April 23 or May 4 triage runs. It surfaced during the May 18 sweep via multilingual search (Korean: Korea Herald; Chinese: SCMP) and was confirmed across 10+ independent English-language outlets. It is not represented in `data/mortality-data.json`.

**Caution re victim count:** Three attacks are documented. The two January 28 and February 9 victims died. The December 2025 victim survived with serious injury. Only the two confirmed deaths should count toward the fatality total. Third-party victims, not AI users.

## Sources (tiered)

### Tier 1 — Juridical
- Seoul Gangbuk Police Station investigation and charge upgrade (February 11, 2026 arrest; murder charges sent to prosecutors)
- Seoul Northern District Prosecutors' Office — public disclosure of Kim's identity (March 9, 2026); ongoing prosecution

### Tier 2 — Journalistic
- The Korea Herald: "Suspect used ChatGPT in planning drug killings: police" (Korean domestic outlet, editorial standards, police-sourced)
- Fortune: "'Could it kill someone?' A Seoul woman allegedly used ChatGPT to carry out two murders in South Korean motels" (March 2, 2026)
- NBC News: "A woman turned to ChatGPT before poisoning 3 men in South Korea, police say"
- South China Morning Post: "South Korean drink-spike killer quizzed ChatGPT for lethal doses, police say"
- Vice: "Woman Accused of Using ChatGPT to Plot Murders of Two Men"
- TechRadar: "ChatGPT search trail becomes central evidence in South Korea double murder probe"
- Mothership.SG: "Woman, 21, charged with murder of 2 men in Seoul, allegedly asked ChatGPT about lethality of mixing sedatives & alcohol" (February 2026)
- Controverity, Evrimagaci, Yahoo News, AOL (additional independent English outlets)

*Ten or more independent outlets reporting the same core facts. Wire service reprints do not explain the count — Korea Herald is a domestic Korean source; SCMP is Hong Kong-based; NBC News and Fortune independently reported on the same facts. Cross-regional agreement on core facts (ChatGPT queries forensically extracted, two murders, one injury, murder charges) satisfies the Tier 2 three-outlet minimum.*

### Tier 3 — Preliminary
- None relied upon.

## Verification status

- [x] Case not already present in `data/mortality-data.json`
- [x] Multiple independent sources cross-referenced (10+)
- [x] Police confirmation of ChatGPT conversation extraction
- [x] Prosecutor involvement documented (Seoul Northern District)
- [ ] Primary court documents obtained (criminal case in Korean courts; PACER equivalent not publicly accessible in English; label `jurisdictional-verification-limited` applies)
- [x] Victims are adults (not minors); real name of perpetrator publicly disclosed by prosecutors

## Open questions

1. **Jurisdictional access**: Full Korean criminal case documents are not accessible in English. The Korea Herald and SCMP report is the primary non-English documentation. `jurisdictional-verification-limited` applies.
2. **Victim identities**: Victims are identified only as "men in their 20s" in English reporting; Korean-language sources may contain names. If named, names should be used; pseudonyms required for minors (not applicable here — all adults).
3. **December victim status**: The December 2025 attack resulted in serious injury (not death). This victim should not be counted in the fatality total but may be referenced in the harm count.
4. **Perpetrator age discrepancy**: Sources vary between "20" and "21" — Mothership.SG reported 21 at time of arrest (February 2026); Seoul NDO disclosure in March 2026 reported age 20. Use 20 as the more recent official figure.
5. **OpenAI / ChatGPT response**: No public statement from OpenAI regarding this case has been located.
6. **Trial date / further proceedings**: No trial date yet published in English-language sources.
7. **Database ID**: Suggested ID `2026-01-KR-001` (for the January 28 first death; the incident series began December 2025, but the first confirmed death is January 28). Alternatively, `2026-KR-001` if the date prefix follows incident series rather than first fatality.

## Recommended next step

**Promote to Tier 2 publication** pending:
1. Human maintainer review of quality gate (all three questions from `verification-standards.md:157-163`):
   - *Family recognition*: Victim identities not yet established in English sources — cannot confirm yet; Korean-language sources should be consulted.
   - *Platform defensibility*: Multiple police-sourced independent reports; ChatGPT conversations entered as forensic evidence. Defensible as journalistic fact.
   - *Researcher citeability*: Korea Herald + Fortune + NBC News + SCMP cross-confirmation satisfies standard. Yes.
2. Label `jurisdictional-verification-limited` to be added to the weekly issue.
3. If promoted: add as a new incident in `data/mortality-data.json` with platform ChatGPT; mechanism `instrumental_pathway`; outcome_target `violence_against_others`; note two third-party fatalities.

*If maintainer prefers to hold pending Korean-language source confirmation of victim names and trial filing, hold at Tier 3 under `jurisdictional-verification-limited`.*

---

*If you are in crisis: Call or text 988 (US Suicide & Crisis Lifeline) · Text HOME to 741741 · International: findahelpline.com*
