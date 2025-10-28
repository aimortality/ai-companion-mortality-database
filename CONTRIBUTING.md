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
  "verification_level": "Court documents|Government acknowledged|Multiple news sources"
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

### Level 1: Confirmed (Highest)
- Court documents
- Government acknowledgment
- Congressional/parliamentary testimony

### Level 2: Highly Probable
- 3+ major news outlets
- Family public statements
- Company acknowledgment

### Level 3: Under Investigation
- 2 news sources
- Ongoing investigation
- Partial documentation

**Note**: Only Level 1 and 2 cases are included in the main database.

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
### Email: hnshokrian@gmail.com
### Issues: Use GitHub Issues for all contributions

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