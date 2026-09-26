# Contributing to the AI Companion Mortality Database

Thank you for considering contributing to this critical public safety resource. Your contributions can help save lives.

## 🎯 How You Can Help

### 1. Report New Cases
If you know of a death or serious harm linked to AI chatbots that isn't in our database:

**Required Documentation** (must have at least ONE):
- Court filing or legal document
- 3+ independent news articles
- Government report or statement
- Congressional/parliamentary testimony
- Coroner's report mentioning AI interaction
- Police report (redacted as appropriate)

**Information Needed**:
- Victim name (or pseudonym if minor)
- Age
- Date of incident
- Platform and chatbot involved
- Location (city, state/province, country)
- Duration of interaction
- Links to all sources

### 2. Improve Existing Data
- Add additional sources to existing cases
- Correct any factual errors
- Provide translations for international cases
- Add court document updates

### 3. Technical Contributions
- Improve data visualization
- Add export formats
- Create analysis tools
- Enhance accessibility features

## 📝 Submission Process

### For New Cases:

1. **Check existing data** - Ensure the case isn't already documented
2. **Gather documentation** - Compile all verifiable sources
3. **Create an issue** - Use the "New Case" template
4. **Submit pull request** - Add to `data/mortality-data.json`

### Format for New Cases:

```json
{
  "id": "YYYY-MM-CC-###",
  "name": "Full Name or Pseudonym",
  "name_type": "real|pseudonym",
  "age": 00,
  "date": "YYYY-MM-DD",
  "location": {
    "city": "City Name",
    "state": "State/Province",
    "country": "Country"
  },
  "platform": "Platform Name",
  "chatbot_name": "Bot Name",
  "interaction_duration": "Time period",
  "outcome": "Death by suicide|Death|Survived attempt",
  "key_factors": [
    "Factor 1",
    "Factor 2"
  ],
  "legal_action": "Status or None",
  "sources": [
    "Source 1",
    "Source 2"
  ],
  "verification_level": "Tier 1 Juridical | Tier 2 Journalistic | Tier 3 Preliminary"
}
```

## ⚖️ Ethical Guidelines

### DO:
- Respect victims and families
- Use respectful language
- Focus on facts, not speculation
- Protect minor identities
- Include crisis resources
- Verify all information

### DON'T:
- Include graphic details
- Share chat transcripts without permission
- Speculate about unverified cases
- Blame victims
- Minimize mental health issues
- Make medical diagnoses

## 🔍 Verification Standards

This project uses the **three-tier system** defined in [`docs/verification-standards.md`](docs/verification-standards.md) and [`docs/methodology.md`](docs/methodology.md). Please use this vocabulary when submitting:

### Tier 1: Juridical Evidence (Highest)
- Court filings (complaints, motions, rulings)
- Government acknowledgment (regulatory bodies, state AGs, international DPAs)
- Congressional or parliamentary testimony
- Coroner or medical examiner findings

### Tier 2: Journalistic Evidence
- Three or more independent news outlets reporting the same core facts (wire reprints don't count as independent)
- Primary-source journalism from a single major outlet (reporter reviewed chat logs directly; original family interviews; documentary evidence obtained)
- Platform operator acknowledgment of the incident
- **Sub-label — jurisdictional-verification-limited**: applies when the case meets Tier 2 across multiple outlets but primary court records are not accessible in the publication language. Submitters of non-English-jurisdiction cases should flag this and include at least one primary-language source pass. See [`docs/verification-standards.md`](docs/verification-standards.md#jurisdictional-verification-limits-tier-2-sub-label).

### Tier 3: Preliminary Evidence (Tracked, not published)
- Single-source reports without independent confirmation
- Social media claims, however detailed
- Forum posts or secondhand community reports
- International cases without English-language verification

**Note**: Only Tier 1 and Tier 2 cases are included in the main database. Tier 3 leads are tracked in a private working repository (not published; this repository is public) and monitored for escalation if additional evidence emerges.

## 🚫 What We DON'T Include

- Unverified social media claims
- Single-source reports
- Cases where AI was incidental
- Speculation or rumors
- Cases without documented AI interaction
- Non-fatal self-harm without hospitalization

## 📊 Data Updates

### Monthly Review Process:
1. Check for new court filings
2. Review news for updates
3. Update legal proceedings
4. Add newly verified cases
5. Archive disputed cases

## 🔒 Privacy & Sensitivity

- Use pseudonyms for all minors
- Redact identifying details when appropriate
- Never share personal contact information
- Respect family wishes for privacy
- Follow local privacy laws

## 💬 Communication

### Discord: [Not yet available]
### Email: contact@aimortality.org
### Issues: Use the [GitLab issue tracker](https://gitlab.com/aimortality/ai-companion-mortality-database/-/issues) for all contributions

## 📜 Code of Conduct

This project follows a strict code of conduct:

1. **Compassion First**: Remember these are real people and families
2. **Truth Matters**: Only verifiable facts
3. **No Sensationalism**: We're documenting, not dramatizing
4. **Respectful Debate**: Disagreements about data handled professionally
5. **Privacy Protection**: Especially for minors and families

## 🏆 Recognition

Contributors who provide verified new cases or significant improvements will be acknowledged in:
- README.md contributors section
- Annual report
- Media citations (with permission)

## ❓ Questions?

- Check existing issues first
- Use "Question" label for new issues
- Email for sensitive matters

## 🆘 If You're in Crisis

**This project may contain triggering content.**

If you're struggling:
- **Call or text 988** (US)
- **Text HOME to 741741** (US)
- International: [findahelpline.com](https://findahelpline.com)

---

Thank you for helping make AI safer for everyone.