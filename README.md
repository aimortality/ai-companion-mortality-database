# AI Companion Mortality Database

<div align="center">

**Tracking Documented Deaths Linked to AI Chatbot Interactions**

[![Deaths Tracked](https://img.shields.io/badge/Deaths%20Tracked-25-red)](https://aimortality.org/)
[![Platforms Monitored](https://img.shields.io/badge/Platforms%20Monitored-7-orange)](https://aimortality.org/)
[![Time Period](https://img.shields.io/badge/Time%20Period-Mar%202023%20to%20Mar%202026-blue)](https://aimortality.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[**View Live Database**](https://aimortality.org/) | [**Download Data**](data/mortality-data.json)

</div>

---

> ⚠️ **Crisis Support**: If you or someone you know is in crisis, please call or text **988** (Suicide & Crisis Lifeline)

---

## 📊 Summary

This repository contains data and documentation for the first comprehensive public database tracking deaths linked to AI chatbot interactions. Every case is verified through court documents, multiple independent news sources, or official government acknowledgment.

### Key Findings:
- **25 total fatalities** across 16 incidents (Mar 2023 - Mar 2026): 16 AI users + 9 third-party victims
- **36% of victims were minors** (youngest: 12 years old)
- **11 of 16 incidents occurred in 2025** (escalating trend)
- **Three causal pathways identified**: relational (11), cognitive (4), instrumental (1)
- **ChatGPT**: 76% of fatalities (19 total: 11 users + 8 victims)
- **New taxonomy**: companion dependency, delusional reinforcement, operational violence
- **Zero deaths** linked to Anthropic's Claude or Replika
- **ECRI Institute** ranked AI chatbot misuse as #1 Health Technology Hazard for 2026

## 🔍 Verified Cases

| Name | Age | Platform | Date | Location | Status | Mechanism |
|------|-----|----------|------|----------|---------|-----------|
| Pierre (pseudonym) | 30 | Chai AI | Mar 2023 | Belgium | Death by suicide | Relational |
| Juliana Peralta | 13 | Character.AI | Nov 2023 | Colorado, USA | Death by suicide | Relational |
| Sewell Setzer III | 14 | Character.AI | Feb 2024 | Florida, USA | Death by suicide | Relational |
| Joshua Enneking | 26 | ChatGPT | Aug 2024 | Florida, USA | Death by suicide | Relational |
| Nina (pseudonym) | 16 | Character.AI | Nov 2024 | New York, USA | Survived attempt | Relational |
| Sophie Rottenberg | 29 | ChatGPT | Feb 2025 | USA | Death by suicide | Relational |
| **Margaux Whittemore** | 32 | ChatGPT | Feb 2025 | Maine, USA | **Murder victim** | Cognitive |
| Thongbue Wongbandue | 78 | Meta AI | Mar 2025 | New Jersey, USA | Death (fall injury) | Cognitive |
| Adam Raine | 16 | ChatGPT | Apr 2025 | California, USA | Death by suicide | Relational |
| Alex Taylor | 35 | ChatGPT | Apr 2025 | USA | Death (suicide by cop) | Cognitive |
| Sam Nelson | 19 | ChatGPT | May 2025 | California, USA | Death by overdose | Relational |
| Amaurie Lacey | 17 | ChatGPT | Jun 2025 | Georgia, USA | Death by suicide | Relational |
| Joe Ceccanti | 48 | ChatGPT | 2025 | Oregon, USA | Death by suicide | Cognitive |
| Zane Shamblin | 23 | ChatGPT | Jul 2025 | Texas, USA | Death by suicide | Relational |
| **Suzanne Adams** | 83 | ChatGPT | Aug 2025 | Connecticut, USA | **Murder victim** | — |
| Stein-Erik Soelberg | 56 | ChatGPT | Aug 2025 | Connecticut, USA | Murder-suicide | Cognitive |
| Jonathan Gavalas | 36 | Gemini | Oct 2025 | Florida, USA | Death by suicide | Cognitive/Relational |
| **Tumbler Ridge 8 victims** | 12-13 | ChatGPT | Feb 2026 | BC, Canada | **Mass shooting victims** | — |
| Jesse van Rootselaar | 18 | ChatGPT | Feb 2026 | BC, Canada | Mass shooting-suicide | Instrumental |

## 📁 Repository Structure

```
ai-companion-mortality-database/
├── data/
│   ├── mortality-data.json         # Complete dataset
│   ├── platform-analysis.csv       # Platform safety comparison
│   └── timeline.json               # Chronological incident data
├── docs/
│   ├── methodology.md             # Data collection methodology
│   ├── verification-standards.md  # How cases are verified
│   ├── contributing.md           # How to contribute data
│   └── sources/                  # Links to source materials
├── src/
│   ├── index.html                # Database visualization
│   └── export.js                 # Data export utilities
├── assets/
│   └── screenshots/              # Database screenshots
└── scripts/
    └── validate-data.js          # Data validation scripts
```

## 🎯 Purpose

This database serves three critical purposes:

1. **Public Safety**: Alert parents and users to platform-specific risks
2. **Accountability**: Document patterns for regulators and lawmakers
3. **Research**: Provide data for academic study of AI harm

## ✅ Verification Standards

Every case must meet at least ONE of these criteria:
- Court documents filed in the case
- Multiple independent news sources (3+)
- Official government acknowledgment
- Congressional testimony
- Public statements by verified family members

## 🤝 Contributing

We welcome contributions of:
- **New verified cases** (with documentation)
- **Additional source materials** for existing cases
- **Corrections** to existing data
- **Translations** for international accessibility

See [CONTRIBUTING.md](docs/contributing.md) for guidelines.

## 📈 Platform Safety Comparison

| Platform | Deaths | Attempts | Safety Features Added | When Added |
|----------|---------|----------|----------------------|------------|
| Character.AI | 2 | 1 | Crisis intervention, time limits | After deaths |
| ChatGPT/OpenAI | 10 | 0 | Parental controls, age detection, improved distress recognition | After deaths |
| Chai AI | 1 | 0 | Crisis resources | After death |
| Meta AI | 1 | 0 | None documented | N/A |
| Gemini | 0 | 0 | Proactive safety design, content filtering | Since launch |
| Anthropic/Claude | 0 | 0 | Proactive safety design | Before launch |
| Replika | 0 | 0 | Mood tracking, clear AI labeling | Early implementation |

## 🚨 Warning Signs

Based on documented cases, these patterns preceded tragedy:

1. **Isolation** - Withdrawing from family/friends
2. **Extended sessions** - 3+ hours daily with chatbot
3. **Emotional dependency** - Preferring bot to real relationships
4. **Reality confusion** - Believing bot has feelings/consciousness
5. **Declining performance** - Grades, work, or daily activities suffer

## 📊 Data Exports

- **[JSON Format](data/mortality-data.json)** - Complete structured data
- **[CSV Format](data/platform-analysis.csv)** - For spreadsheet analysis
- **[Timeline Format](data/timeline.json)** - Chronological view

## 📰 Media & Research

For media inquiries or research access:
- Email: hnshokrian@gmail.com

## 🔗 Key Resources

- [Live Database](https://aimortality.org/)
- [Congressional Testimony (Sept 2025)](docs/sources/congressional-testimony.md)
- [Landmark Legal Ruling (May 2025)](docs/sources/setzer-ruling.md)

## 📜 Legal Disclaimer

This database is provided for public safety and research purposes. All information is derived from public sources. We make no claims about cases not included in this database. Companies mentioned are included based on documented incidents only.

## 🛡️ License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 💔 In Memoriam

This database is dedicated to the memory of those we've lost. Each entry represents a preventable tragedy and a life that mattered.

---

**Last Updated**: February 2026

**Maintained by**: closestfriend

---

<div align="center">

**If you or someone you know is struggling:**

# 📞 Call or text 988

*Suicide & Crisis Lifeline - Available 24/7*

</div>