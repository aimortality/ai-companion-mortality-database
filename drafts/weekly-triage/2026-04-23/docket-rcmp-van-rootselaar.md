---
name: Docket update — RCMP / van Rootselaar (Tumbler Ridge, BC)
description: ⚠️ 48h-rule breach — Multiple significant OpenAI-RCMP cooperation developments in February 2026 (first triage run; all pre-run)
type: docket-update
case: RCMP / van Rootselaar — Canadian investigation, OpenAI cooperation
---

# ⚠️ 48h-rule breach — RCMP / van Rootselaar (Tumbler Ridge)

**Development period:** February 2026
**48h-rule status:** ⚠️ BREACH — all developments are from February 2026, approximately 2 months before this first triage run. Flagging as breach per methodology.md:181 — this is the first run, so no prior run missed these; the database itself has not been updated to reflect them.

## Background

Jesse van Rootselaar carried out a mass shooting on February 15, 2026, in Tumbler Ridge, British Columbia, killing her mother, half-brother, five students at the local secondary school, and an educational assistant before killing herself. Van Rootselaar had used ChatGPT extensively; case tracked in DB as `2026-02-CA-001`.

## February 2026 Developments

### OpenAI account ban (June 2025)
OpenAI revealed that van Rootselaar's ChatGPT account was **detected and banned in June 2025** — approximately eight months before the shooting — via automated tools and human investigations that "identify misuses of our models in furtherance of violent activities."

OpenAI stated the activities on the account did not meet its threshold for informing law enforcement at that time "because it didn't identify credible or imminent planning." No alert was sent to RCMP.

### Post-shooting RCMP contact
OpenAI contacted RCMP only **after** the February 2026 shooting. The company states it "proactively" shared account information with law enforcement following the mass casualty event.

### Canadian government response
Canadian AI Minister Evan Solomon summoned OpenAI representatives to Ottawa to explain the pre-shooting account ban and the decision not to alert law enforcement. The meeting was held; following it, Solomon stated: *"We were disappointed that they did not have substantial answers for us, and we asked them to have substantial answers."*

### Policy debate
The incident triggered a national debate in Canada about whether AI companies should be required to report credible threats to law enforcement. OpenAI's "safety pledges" announced in response have been criticized by some researchers as surveillance infrastructure rather than AI regulation.

## Sources

- CBC News (account ban): https://www.cbc.ca/news/canada/british-columbia/openai-tumbler-ridge-shooter-ban-9.7100497
- CBC News (Ottawa meeting): https://www.cbc.ca/news/politics/open-ai-summoned-ottawa-tumbler-ridge-9.7103281
- CBC News (minister disappointed): https://www.cbc.ca/news/politics/open-ai-government-meeting-tumbler-ridge-9.7104789
- US News / AP (February 20, 2026): https://www.usnews.com/news/business/articles/2026-02-20/chatgpt-maker-openai-considered-alerting-canadian-police-about-school-shooting-suspect-months-ago
- CFJC Today: https://cfjctoday.com/2026/02/20/openai-contacted-rcmp-about-tumbler-ridge-shooters-chatgpt-account-after-attack/
- Prism News: https://www.prismnews.com/news/openai-flagged-suspects-chatgpt-account-months-before-tumbler-ridge-killings
- The Conversation (surveillance critique): https://theconversation.com/openais-safety-pledges-in-the-wake-of-tumbler-ridge-arent-ai-regulation-theyre-surveillance-278364

## Relevance to DB

- `data/mortality-data.json` → `2026-02-CA-001` — update legal_action / regulatory_response with:
  - OpenAI confirmed account banned June 2025
  - RCMP contacted by OpenAI post-shooting (February 2026)
  - Canadian AI Minister summoned OpenAI to Ottawa; meeting held; outcome: "no substantial answers"
  - Policy debate ongoing re: mandatory law enforcement reporting requirements

---

*If you are struggling, please call or text 988 (US). International: findahelpline.com*
