---
name: Docket update — JCCP 5431 (ChatGPT Product Liability Cases) coordination confirmed; case numbers updated
description: ⚠️ 48h-rule breach — February 3, 2026 coordination order consolidated seven CA state-court OpenAI wrongful death cases into JCCP 5431 in San Francisco Superior Court; case numbers now confirmed for Enneking, Lacey, Fox
type: docket-update
case: JCCP 5431 — ChatGPT Product Liability Cases (San Francisco Superior Court)
---

# ⚠️ 48h-rule breach — JCCP 5431 Coordination Order (February 3, 2026)

**Development date:** February 3, 2026 (JCCP coordination order)
**Document type:** Order Granting Petition for Coordination
**Court:** California Judicial Council / San Francisco Superior Court
**48h-rule status:** ⚠️ BREACH — coordination order is approximately 97 days old at time of this run (May 11, 2026). No earlier triage run captured this.

## Substance

On February 3, 2026, the California Judicial Council granted a petition to coordinate seven related wrongful death and harm cases against OpenAI in a single Judicial Council Coordination Proceeding, designated **JCCP 5431 ("ChatGPT Product Liability Cases")**, in San Francisco Superior Court.

**Cases consolidated under JCCP 5431:**

| Case | Plaintiff | Victim | Prior case number | Confirmed SF Superior No. |
|------|-----------|--------|-------------------|--------------------------|
| Raine v. OpenAI | Matt & Maria Raine | Adam Raine (16) | SF Superior | CGC-25-628528 |
| Enneking v. OpenAI | Family | Joshua Enneking (26) | SF Superior | CGC-25-630809 |
| Lacey v. OpenAI | Cedric Lacey | Amaurie Lacey (17) | SF Superior | CGC-25-630808 |
| Fox v. OpenAI (Ceccanti) | Jennifer "Kate" Fox | Joe Ceccanti (48) | LA Superior (transferred) | 25STCV32379 |
| Shamblin v. OpenAI | Alicia & Kirk Shamblin | Zane Shamblin (23) | LA Superior (transferred) | 25STCV32382 |
| Irwin v. OpenAI | — | — | — | Confirmed in JCCP |
| Madden v. OpenAI | — | — | — | Confirmed in JCCP |

*Note: Irwin and Madden cases are included in the JCCP but are not currently in `data/mortality-data.json`. They should be monitored for identification.*

**Coordination document:** Order Granting Petition for Coordination — JCCP 5431 (February 3, 2026), available via Tech Justice Law Project: https://techjusticelaw.org/wp-content/uploads/2026/03/OAI_JCCP_Order_re_Petition_for_Coordination_-_5431.pdf

**Effect on case management:** Scheduling, discovery, and pre-trial motions for all coordinated cases are now managed at the JCCP level, not individually. Any significant JCCP rulings will apply across multiple cases simultaneously.

**Gray v. OpenAI (26STCV00988):** It is not confirmed whether the Austin Gordon case (filed January 13, 2026, LA County Superior) has been consolidated into JCCP 5431. This should be verified.

**Adams v. OpenAI (SF Superior, December 11, 2025):** The state court Adams/Soelberg case is not confirmed as part of JCCP 5431 (it may be proceeding independently given its distinctive nature as a homicide case rather than a suicide case).

## Sources

- Order Granting Petition for Coordination: https://techjusticelaw.org/wp-content/uploads/2026/03/OAI_JCCP_Order_re_Petition_for_Coordination_-_5431.pdf
- Tech Justice Law Project: https://techjusticelaw.org/2025/12/03/seven-ai-delusional-disorder-cases-shamblin-irwin-fox-enneking-madden-brooks-and-lacey-v-openai-et-al/
- Social Media Victims Law Center (SMVLC): confirmed case numbers via press releases
- Transparency Coalition AI litigation tracker

## Database updates required

- `data/mortality-data.json`, incidents for Raine (2025-04-US-001), Enneking (2024-08-US-001), Lacey (2025-06-US-001), Ceccanti (2025-XX-US-001), Shamblin (2025-07-US-001): Update `legal_action` fields to add confirmed case numbers and note JCCP 5431 coordination.
- `docs/sources/court-documents.md`: Add JCCP 5431 section; update individual case sections with confirmed case numbers.
- Monitor for Irwin and Madden case identities — these are named plaintiffs in JCCP but not yet in the database.

---

*If you are struggling, please call or text 988 (US). International: findahelpline.com*
