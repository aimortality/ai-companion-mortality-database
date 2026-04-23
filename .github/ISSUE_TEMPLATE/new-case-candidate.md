---
name: New case candidate
about: Submit a newly surfaced fatality or severe harm for evaluation against the
  database's verification tiers
title: 'New case candidate: <name or event>'
labels: new-case-candidate
assignees: ''
---

<!--
Thanks for contributing. Please fill out as much of this as you can. An empty
field is better than a guess — verification tier classification depends on
evidence quality, and we would rather hold a case in Tier 3 (monitoring)
than publish an unverified detail.

See docs/methodology.md and docs/verification-standards.md for the rubric.
Crisis resources: Call or text 988 (US) if you or someone you know is struggling.
-->

## Candidate record

```json
{
  "id": "YYYY-MM-CC-###",
  "name": "Full Name or Pseudonym",
  "name_type": "real | pseudonym | event",
  "age": null,
  "date": "YYYY-MM-DD",
  "location": {
    "city": "",
    "state": "",
    "country": ""
  },
  "platform": "",
  "chatbot_name": "",
  "interaction_duration": "",
  "outcome": "Death by suicide | Death | Survived attempt | Mass shooting | Murder | Murder-suicide",
  "mechanism_type": "relational_pathway | cognitive_pathway | instrumental_pathway",
  "outcome_target": "self_harm | violence_against_others",
  "key_factors": [
    ""
  ],
  "legal_action": "",
  "sources": [
    ""
  ],
  "verification_level": "Tier 1 Juridical | Tier 2 Journalistic | Tier 3 Preliminary"
}
```

## Sources (tiered)

List every source you have. Group by tier per `docs/verification-standards.md`.

### Tier 1 — Juridical
<!-- Court filings, government statements, coroner findings, congressional testimony. -->
-

### Tier 2 — Journalistic
<!-- 3+ independent outlets OR primary-source reporting by a single major outlet OR platform acknowledgment. Wire reprints do not count as independent. -->
-

### Tier 3 — Preliminary
<!-- Single source, social media, forum posts. Will be tracked but not published unless escalated. -->
-

## Verification status

- [ ] Case not already present in `data/mortality-data.json`
- [ ] Multiple independent sources cross-referenced (or explicit Tier 1 document attached)
- [ ] Primary documents reviewed where available
- [ ] Minor? Pseudonym used unless family has publicly identified
- [ ] Non-English / non-US jurisdiction? Access gaps noted

## Open questions

<!-- Anything unresolved: ambiguous dates, disputed ages, unclear platform attribution, pending court rulings, etc. -->

## Recommended next step

<!-- Pick one: Promote to published tier | Hold for second source | Hold pending docket update | Reject with reason -->
