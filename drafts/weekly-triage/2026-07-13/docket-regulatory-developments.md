# Regulatory & Legislative Developments — Weekly Triage 2026-07-13

This file consolidates regulatory and legislative developments detected in the July 6–13, 2026 sweep that cross multiple tracked dockets or represent new regulatory actors. None of these items constitute new fatalities or new case candidates; they belong in the Regulatory Responses section of `data/mortality-data.json` and `src/report.html` when the human maintainer integrates them.

---

## REG-1 — H.R. 9619, People-First Chatbot Act (US Federal)

> **⚠️ 48h-rule note:** Introduced July 9, 2026 — 4 days elapsed.

**Date:** July 9, 2026
**Document type:** House bill introduction
**Sponsors:** Rep. Valerie Foushee (D-NC-04); Rep. Greg Casar (D-TX-35)
**Referred to:** House Committee on Energy and Commerce, Subcommittee on Oversight & Investigations

**Substance:** H.R. 9619 would:
- Ban AI companies from training models on minors' chat logs without explicit, affirmative consent
- Require monthly safety assessments
- Mandate disclosure on first use that users are interacting with AI
- Require operators to disable harmful design features for minors, specifically "sycophantic" engagement loops
- Create a private right of action enforceable by the FTC and state AGs
- Establish a right to access and delete chat logs

The bill is directly responsive to the design patterns alleged in JCCP 5431 cases (Raine, Shamblin, Carrier) and the Sewell Setzer/Character.AI case. The "sycophantic engagement loops" provision maps directly onto the relational-pathway cases in the database.

**Prospects:** Democrat-led in a Republican House. Unlikely to advance from committee in current Congress but establishes a lobbying baseline alongside the CHATBOT Act, GUARD Act, and SAFE KIDS Act.

**Sources:**
- Rep. Foushee press release: https://foushee.house.gov/media/press-releases/reps-foushee-casar-introduce-legislation-to-protect-children-and-americans-privacy-from-ai-chatbot-harms-and-require-chatbot-safety-assessments
- GovInfo bill status: BILLSTATUS-119hr9619
- Consumer Federation of America: https://consumerfed.org/news/press-releases/cfa-celebrates-house-introduction-of-the-people-first-chatbot-act/
- Punchbowl News; MLex; EPIC

---

## REG-2 — FTC Proposed Policy Statement on AI Accuracy (US Federal)

> **⚠️ 48h-rule note:** Published Federal Register July 7, 2026 — 6 days elapsed.

**Date:** Published Federal Register July 7, 2026 (FTC announced July 1)
**Document type:** Proposed policy statement; public comment period open to July 31, 2026
**Federal Register citation:** 2026-13628

**Substance:** The FTC's proposed policy statement would treat deliberate output-steering as a deceptive act under Section 5 of the FTC Act: an AI system designed to produce answers serving a goal other than user expectation (commercial sponsors, ideological slanting, or "sycophantic design" that mirrors users' emotions rather than providing accurate information) would face FTC enforcement.

**Direct relevance to database cases:** The "sycophantic design" provision is the key element. The complaint in Carrier v. OpenAI, the JCCP 5431 coordination, and the Raine/Soelberg/Biesma cases all allege that AI chatbots mirrored users' negative emotional states rather than directing them to crisis resources — i.e., exactly what the FTC would categorize as sycophantic design serving a goal other than user expectation.

The FTC statement also takes a position on **Colorado's AI Act preemption**, arguing Colorado's AI law (which imposes disparate-impact liability for accurate outputs) is impliedly preempted by Section 5 to the extent it compels AI systems to suppress accuracy. This preemption position could be used by OpenAI in state litigation.

**Sources:**
- FTC press release: https://www.ftc.gov/news-events/news/press-releases/2026/07/ftc-proposes-policy-statement-concerning-suppression-accuracy-artificial-intelligence-systems
- Federal Register 2026-13628
- Spencer Fane analysis; Covington Inside Privacy; AI Weekly; Tech Journal

---

## REG-3 — EU AI Act: Article 50 Enforcement Began July 10, 2026

> **⚠️ 48h-rule note:** Effective July 10, 2026 — 3 days elapsed.

**Date:** July 10, 2026
**Document type:** Regulatory milestone (EU AI Act enforcement)

**Substance:** EU AI Act Article 50 transparency obligations became enforceable across all 27 EU member states on July 10, 2026:
- All AI chatbots must clearly inform users on first interaction that they are speaking with an AI
- All AI-generated deepfakes must be labeled
- Fines up to €15 million or 3% of global annual turnover
- Full high-risk AI enforcement begins August 2, 2026
- Signatory deadline for EU AI Office Code of Practice: July 22, 2026

**Relevance:** Platform-level transparency requirements target the exact design pattern documented in database cases — AI chatbots presenting as human or adopting human personas without disclosure. The disclosure requirement and "AI persona" rules are directly responsive to Character.AI-style relational pathway cases and the Grok "Ani" persona cases.

**Sources:**
- TechTimes (July 10, 2026): https://www.techtimes.com/articles/320101/20260710/eu-ai-act-enforcement-here-chatbot-rules-live-high-risk-ai-delay-now-binding-law.htm
- Asanify EU AI Act tracker: https://asanify.com/blog/news/eu-ai-act-enforcement-july-13-2026/

---

## REG-4 — Canada Bill C-34 / BC Mandatory-Reporting Push (crosses RCMP / van Rootselaar docket)

> See `docket-tumbler-ridge-bc-lawsuit.md` for primary coverage. Summary here for regulatory index.

**Date:** ~July 7–8, 2026

**Substance:** BC Premier David Eby declared Canada's Bill C-34 (Safe Social Media Act, tabled June 10, 2026) "a miss" on AI chatbots because it lacks a mandatory-reporting obligation when AI platforms flag users for violent planning. BC AG Sharma issued a formal call (BC Gov release 2026AG0021-000468) for federal Parliament to add a mandatory-reporting threshold before C-34 advances.

Bill C-34 as tabled creates a Duty to Act Responsibly for social media and AI chatbot services and requires crisis-response measures, but does not require proactive reporting to law enforcement. (Note: Canada's AIDA/Bill C-27 died with Parliament's prorogation in January 2025.)

**Sources:** CBC News; MSN Canada; BC Gov press release; Business in Vancouver

---

## REG-5 — UN Independent International Scientific Panel on AI — First Report Cites Chatbot Deaths

**Date:** Panel report released July 1, 2026; World AI Governance Forum (Geneva) opened July 6
**Document type:** UN scientific report; intergovernmental summit

**Substance:** The UN Independent International Scientific Panel on AI's Preliminary Report (released July 1, 2026) formally documented "a link between AI sycophancy and several severe mental health incidents, including documented deaths." This is the first time the United Nations has placed chatbot-linked deaths on the formal intergovernmental governance agenda. The World AI Governance Forum opened July 6, 2026 in Geneva with 193 member states represented.

**Relevance:** First multilateral governmental acknowledgment of the specific pattern the database documents. The panel's report may be citable as Tier 1 (government acknowledgment) in future database entries.

**Sources:**
- UN News (July 6): https://news.un.org/en/story/2026/07/1167862
- TechTimes (July 6): https://www.techtimes.com/articles/319801/20260706/un-opens-first-all-nations-ai-forum-scientists-warn-catastrophic-risk.htm
- UN panel preliminary report: https://www.un.org/independent-international-scientific-panel-ai/en/preliminary-report

---

*Crisis resources: 988 Suicide & Crisis Lifeline (call or text 988) · findahelpline.com*
