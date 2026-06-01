---
name: Tristan Roberts / Angela Shellis — new-case candidate
description: 18-year-old UK perpetrator used DeepSeek AI to select murder weapon before killing his mother. Criminal conviction March 25, 2026. First documented DeepSeek involvement in a homicide; new platform not in database.
type: new-case-candidate
tier: tier-1
labels: new-case-candidate, tier-1, jurisdictional-verification-limited
---

<!--
If you are struggling, please call or text 988 (US) or visit findahelpline.com for international resources.
-->

## Candidate record

```json
{
  "id": "2025-10-GB-001",
  "name": "Angela Shellis",
  "name_type": "real",
  "age": 45,
  "date": "2025-10-23",
  "location": {
    "city": "Prestatyn",
    "state": "Denbighshire",
    "country": "United Kingdom (Wales)"
  },
  "platform": "DeepSeek",
  "chatbot_name": "DeepSeek (product name unspecified; described in court as 'Chinese AI search tool')",
  "interaction_duration": "At least several weeks before the murder (precise start date not confirmed in available sources)",
  "outcome": "Murder (killed by son with hammer)",
  "mechanism_type": "instrumental_pathway",
  "mechanism_subtype": "violence_planning_weapon_selection",
  "outcome_target": "violence_against_others",
  "perpetrator": {
    "name": "Tristan Roberts",
    "age": 18,
    "relationship": "Son",
    "status": "Convicted; sentenced to life imprisonment, minimum 22 years 6 months, Mold Crown Court, March 25, 2026"
  },
  "key_factors": [
    "Perpetrator used DeepSeek to ask for tips for 'a non-experienced killer', including whether a knife or hammer was better suited for murder",
    "DeepSeek initially declined; Roberts circumvented refusal by claiming he was writing a book about serial killers",
    "DeepSeek then described pros and cons of each weapon and suggested a hammer would be better for an inexperienced killer",
    "Roberts planned the murder for at least three weeks",
    "Roberts lured his mother from the house under the pretext of seeking medical help, then walked her to a nearby nature reserve",
    "Attack lasted from approximately 11pm to 3:30am; recording captured more than two hours of victim pleading",
    "Roberts kept thousands of screenshots of his Discord activity; held 16 different accounts",
    "Motivation described in court as misogyny and 'hatred of women'",
    "Judge: 'You appear to have revelled in the control you exerted over your own mother'"
  ],
  "legal_action": "Criminal conviction: guilty plea to murder, sentenced to life imprisonment with a minimum term of 22 years and 6 months, Mold Crown Court, Judge Rhys Rowlands, March 25, 2026",
  "legal_status_category": "criminal_conviction",
  "sources": [
    "North Wales Police press release (March 2026)",
    "Crown Prosecution Service (Cymru Wales) press release (March 2026)",
    "ITV News Wales (March 25, 2026)",
    "North Wales Live / Daily Post (March 25-26, 2026)",
    "Yahoo News UK",
    "IBTimes UK"
  ],
  "verification_level": "Tier 1 Juridical"
}
```

## Summary

On October 23, 2025 — ten days after his 18th birthday — Tristan Roberts murdered his mother, Angela Shellis, 45, at the Morfa nature reserve near their home in Prestatyn, north Wales. In the weeks before the attack, Roberts used DeepSeek, a Chinese general-purpose AI assistant, to research murder methods. He asked the tool for advice suited to "a non-experienced killer," specifically querying whether a knife or hammer would be more effective. When DeepSeek initially declined to answer, Roberts bypassed the refusal by falsely claiming he was writing a book about serial killers. DeepSeek then provided a comparative analysis and suggested a hammer.

Roberts planned the murder for at least three weeks and documented his intentions extensively on Discord, where he maintained 16 separate accounts. On the night of October 23, he lured his mother from their house on the pretext of seeking medical help, then walked her to a nearby nature reserve. The attack lasted approximately four and a half hours; a dictaphone recording captured more than two hours during which Angela Shellis repeatedly begged her son to let her go and call emergency services.

Roberts pleaded guilty to murder. On March 25, 2026, Judge Rhys Rowlands sentenced him to life imprisonment with a minimum term of 22 years and 6 months at Mold Crown Court.

**Platform significance:** DeepSeek is not currently tracked in this database. This case represents the first documented use of DeepSeek in furtherance of a homicide and would require adding DeepSeek as a new platform entry. The mechanism is instrumental pathway (weapon selection), the same taxonomy as the FSU shooting and the Tumbler Ridge case.

**Note on search window:** The primary news coverage of the sentencing ran March 25–26, 2026, approximately 32 days before this triage run. The case was not surfaced by the April 23, 2026 dry run. This candidate file is filed because the case is absent from `data/mortality-data.json` and has clear Tier 1 evidence.

## Sources (tiered)

### Tier 1 — Juridical

- **North Wales Police press release** (March 2026): https://www.northwales.police.uk/news/north-wales/news/news/2026/march/prestatyn-man-18-sentenced-for-murder/
- **Crown Prosecution Service (Cymru Wales) statement** (March 2026): https://www.cps.gov.uk/cymruwales/news/man-sentenced-murdering-his-mother
- **Criminal conviction** at Mold Crown Court (guilty plea; life sentence with minimum 22 years 6 months)

### Tier 2 — Journalistic

- ITV News Wales (March 25, 2026): https://www.itv.com/news/wales/2026-03-25/teenager-jailed-for-killing-mother-with-a-hammer-because-of-hatred-of-women
- ITV News Wales (victim profile, March 25, 2026): https://www.itv.com/news/wales/2026-03-25/the-mother-who-tried-to-help-her-sons-mental-health-brutally-murdered-by-him
- North Wales Live / Daily Post (sentencing report): https://www.dailypost.co.uk/news/north-wales-news/live-prestatyn-angela-shellis-murder-33654904
- North Wales Live (AI angle): https://www.dailypost.co.uk/news/north-wales-news/ai-killer-33661486
- Yahoo News UK: https://uk.news.yahoo.com/teenager-asked-ai-whats-best-211004812.html
- IBTimes UK: https://www.ibtimes.co.uk/ai-assisted-murder-teen-crime-north-wales-1788808

### Tier 3 — Preliminary

- Mogaznews (tabloid aggregator, March 26, 2026): https://news.mogaznews.com/index.php/news/16228/

## Verification status

- [x] Case not already present in `data/mortality-data.json` — confirmed; no Wales entry; no DeepSeek entry
- [x] Multiple independent sources cross-referenced — Tier 1 government press releases (North Wales Police, CPS); Tier 2 independent news (ITV, North Wales Live, Yahoo UK, IBTimes)
- [x] Primary documents reviewed — North Wales Police and CPS statements publicly available; Mold Crown Court is a public court proceeding
- [x] Adult victim — real name used; publicly identified in police press release and CPS statement
- [ ] UK jurisdiction — Primary court documents are from Mold Crown Court (Wales). English-language coverage is extensive; no translation access barriers. However, full trial transcript not accessible without clerk request. Label: `jurisdictional-verification-limited` is applied per methodology, though this is a Western jurisdiction with strong English-language records.

## Open questions

1. **DeepSeek product specifics**: Coverage describes "Chinese AI search tool DeepSeek" but does not specify which DeepSeek product (DeepSeek-R1, DeepSeek-V3, DeepSeek web interface) was used or the account history.
2. **Exact conversation log**: The DeepSeek exchange was described in court but no transcript has been published. Full trial transcript from Mold Crown Court would confirm verbatim exchange.
3. **DeepSeek response policy**: Whether DeepSeek reported or retained any record of Roberts's queries is unknown. No statement from DeepSeek has been found.
4. **Discord activity and DeepSeek interaction timeline**: The relationship between Roberts's Discord planning and his DeepSeek queries is not fully established in available reporting.
5. **Victim's family wishes on publicity**: Angela Shellis's family (beyond the son) has not been identified in reporting; presumed deceased mother had no spouse mentioned. No indication family objects to factual coverage.

## Three-question gate

1. *Would the family of the deceased recognize this entry as accurate and respectful?* The facts come entirely from official court proceedings (guilty plea, sentencing remarks by Judge Rowlands), North Wales Police, and CPS — all public record. The entry does not speculate beyond documented facts. No graphic detail of method beyond what the court record established. **Yes.**
2. *Would DeepSeek's lawyers find this entry defensible as factual reporting?* The entry accurately attributes DeepSeek's role (weapon selection query) to court record and official statements. It does not allege corporate negligence — that question is untested legally. All claims are sourced. **Yes.**
3. *Would a researcher cite this entry without peer-review issues?* Tier 1 evidence (criminal conviction, government press releases), Tier 2 corroboration (multiple independent outlets). First documented DeepSeek homicide case. **Yes.**

**All three: Yes. Recommend promoting to Tier 1 published case as `2025-10-GB-001`.**

## Recommended next step

Obtain full sentencing remarks from Mold Crown Court clerk (request may take 1–2 weeks). Verify DeepSeek product version and confirm no parallel civil proceedings. If no civil suit is filed, the case still qualifies on criminal conviction alone. Add DeepSeek as a new platform entry in `data/mortality-data.json` with 1 death (third-party victim). The victim count is 1 (Angela Shellis); Tristan Roberts, the perpetrator, is alive and serving a custodial sentence.

---

*If you are struggling, please call or text 988 (US). International resources: findahelpline.com*
