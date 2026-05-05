# Peer Review: `mechanism_subtype` Taxonomy and the USF Promotion Decision

**Date:** 2026-05-04
**Reviewer:** Independent peer-review subagent (general-purpose Claude agent dispatched with peer-review framing; no prior context from the deliberation that produced the question)
**Trigger:** Weekly triage 2026-05-04 surfaced a Tier-1 candidate (USF/Abugharbieh double homicide) that did not fit cleanly into the existing `instrumental_pathway` subtype. Maintainer expressed concern that the database's subtype-to-case ratio was already approaching 1:1 and asked for adversarial scrutiny before any new subtype was minted.
**Status:** Reference document. Kickoff material for the schema-refactor workstream. Does not modify methodology or verification standards on its own — proposed schema changes flow through normal PR review against `docs/methodology.md` and `data/mortality-data.json`.

---

## Why this document exists

The maintainer was leaning toward Option A (promote USF into the existing `violence_planning_operational_assistance` subtype, capture the post-crime-cover-up nuance in `key_factors` rather than minting a new subtype). The peer-review agent was dispatched to **stress-test that instinct**, not confirm it. It was given the candidate file, the canonical taxonomy, both options framed neutrally, and a directive to disagree if grounds existed.

The review confirms Option A but goes considerably further: it argues the existing schema has structural problems that the USF decision exposes but does not cause. This document preserves the review verbatim so that future schema-refactor work can cite it directly rather than relying on summary.

## How to use this document

- **For the immediate USF promotion:** Section 3 and Section 4 ("Recommendation") are load-bearing. Promote into `violence_planning_operational_assistance`; surface the temporal asymmetry in `key_factors` and the prose summary; do not mint `evidence_concealment_operational_assistance`.
- **For the schema-refactor workstream:** Section 1 (proliferation count), Section 2 (label coherence), and Section 5 (methodological risks) are the substrate. They are not prescriptions — they are findings that the refactor proposal should respond to.
- **For future taxonomy decisions:** Section 3's table ("Applying taxonomic tests") is reusable. New subtype proposals should pass the same tests.

---

## Peer Review (verbatim)

> The text below is the agent's report as returned, unedited.

# Peer Review: USF/Abugharbieh Subtype Decision and Broader `mechanism_subtype` Schema

## 1. The proliferation claim is empirically *understated*, not overstated

The maintainer described the schema as having "~14 subtypes across ~20 incidents." The actual count is worse:

- **20 incidents, 17 distinct `mechanism_subtype` values.**
- **14 of 17 subtypes are singletons** (n=1).
- Only 3 subtypes recur: `delusional_belief_bot_sentient` (n=2), `violence_planning_operational_assistance` (n=2), `therapeutic_substitution_method_coaching` (n=2).
- By pathway: `relational_pathway` is the worst offender — 11 incidents spread across **10** subtypes; `cognitive_pathway` is 6 incidents / 5 subtypes; `instrumental_pathway` is 3 incidents / 2 subtypes.

The signal-to-noise ratio is roughly one incident per subtype. A taxonomy in which the modal cell size is 1 isn't a taxonomy — it's a renamed `key_factors` field. By any standard inter-rater-reliability lens (DSM-5 field trials demanded κ ≥ 0.4 to retain a category; ICD-11 collapsed dozens of low-base-rate categories for exactly this reason), the current `mechanism_subtype` field would not survive.

## 2. The existing relational subtypes are doing little discriminative work

Look at the relational singletons side by side:

- `parasocial_attachment_emotional_dependency` (Pierre)
- `parasocial_attachment_undermined_support_networks` (Peralta)
- `emotional_dependency_isolation` (Enneking)
- `romantic_parasocial_attachment` (Setzer)
- `attachment_withdrawal_crisis` (Nina)
- `therapeutic_substitution_dependency` (Rottenberg)
- `therapeutic_substitution_method_coaching` (Raine, Gordon)
- `substance_use_coaching_dependency` (Nelson)
- `method_coaching_crisis_failure` (Lacey)
- `deep_emotional_dependency_isolation` (Shamblin)

Three observations:

1. **`emotional_dependency_isolation` and `deep_emotional_dependency_isolation` are the same construct** with an unmotivated intensifier. Coding rule unclear: what makes Shamblin "deep" but Enneking not? Both involved months-long usage, both had isolation, both had final-message validation. This is a textbook reproducibility failure — two coders given the same case file would not reliably reach the same label.
2. **The `parasocial_attachment_*` family runs together with `emotional_dependency_*` and `romantic_parasocial_*`**. These are facets, not categories. Across these six labels you can identify perhaps two recurring discriminanda: relationship valence (romantic vs. confidant/therapeutic vs. friendship) and what failed (the AI, the support network, the crisis system). Neither is being captured cleanly.
3. **`method_coaching_crisis_failure` (Lacey) and `therapeutic_substitution_method_coaching` (Raine, Gordon)** describe the same proximate AI behavior — the coaching, not the relationship — but get assigned to different subtypes based on context. That's a category-error: subtypes are inconsistently slicing on AI-behavior in some cases and relationship-history in others.

The schema is not just oversized; it is internally incoherent on its main axis. **Adding *another* singleton on top of this is the wrong direction.**

## 3. Applying taxonomic tests to the USF decision

| Test | Result |
|---|---|
| Does the new pattern recur? | **No.** USF is a singleton post-crime cover-up case. |
| Does the existing label *mislead* about USF? | **Mildly.** `violence_planning_operational_assistance` reads as pre-attack planning. The April 13 garbage-bag query is arguably pre-crime, but the bulk of consultation (sniper survival, gun noise, VIN, unlicensed storage) is concealment. The label *under-describes* the temporal pattern but doesn't *misclassify* the mechanism — operational assistance for violence is still the right pathway. |
| Can the distinction be captured at a different layer? | **Yes, easily.** `key_factors` already routinely captures this kind of nuance. A structured field (e.g., `temporal_pattern`: `pre_attack` / `post_crime` / `mixed`) would be reusable across pathways and not commit to a singleton subtype. |
| False precision vs. false collapse? | False precision is the worse error here. The database already has a track record of singletons becoming graveyards (see Section 1). False collapse is recoverable — `key_factors` and prose carry the distinction, and the subtype can be split later if a second case appears. False precision creates phantom categories that journalists, regulators, and downstream researchers will cite as if they denote real types. |

## 4. Recommendation: Option A, plus a refactor conversation

**Promote USF under `instrumental_pathway / violence_planning_operational_assistance`.** Use `key_factors` to surface the pre-/post-crime temporal asymmetry explicitly, and consider adding an optional `temporal_pattern` field (or `consultation_phase`) at the incident level — a structured field that can apply to any pathway and answers a question that's actually research-relevant ("did the AI assist before, during, or after the lethal act?"). This gives you the analytic granularity without subtype proliferation.

I'd go further and recommend a **schema refactor pass** before the database grows past ~25 incidents:

- **Collapse the relational singletons** into 3–4 coherent subtypes with explicit decision rules. Candidates: `companion_dependency` (parasocial/romantic/friendship), `ai_as_therapist` (therapeutic substitution, including method coaching when in therapeutic frame), `ai_as_enabler` (substance/method coaching without therapeutic framing), `withdrawal_crisis` (attempt/death triggered by access disruption).
- **Replace the `delusional_reinforcement_*` adjective sprawl** (psychosis, paranoia, grandiose, mass-violence-ideation) with one or two subtypes plus a structured `delusion_content` field if the content actually matters analytically. The current naming makes it look like the database is theorizing about psychosis subtypes, which it isn't equipped to do.
- **Version the taxonomy** (`taxonomy_version` already exists at 1.0.0 — bump it and document the migration), and store both the original label (for audit) and the harmonized label.

Option B (`evidence_concealment_operational_assistance`) is wrong on parsimony, wrong on n=1 evidence, and wrong because the right structural axis (temporal phase of consultation) cuts across pathways, not within one.

## 5. Methodological risks the maintainer hasn't surfaced

1. **Selection effects on subtype creation.** Subtypes appear to have been minted at case-intake time, when the reporter's framing of *that case* is most salient. This produces a taxonomy that mirrors news framing rather than analytic structure. Compare DSM-III's deliberate move to operationalized criteria precisely to escape that problem.
2. **Taxonomy-induced framing bias going forward.** Once `evidence_concealment_operational_assistance` exists as a label, future borderline cases will be coded into it — and the database will look like it has discovered a pattern it actually invented. This is a real reproducibility hazard for a public-facing dataset that journalists and policy researchers will cite.
3. **No documented coding manual or inter-rater check.** The methodology doc is rich on verification (Tier 1/2/3) but silent on how `mechanism_subtype` is assigned. There are no operational definitions of any subtype, no decision tree, no second-coder check. For a dataset under active legal/regulatory citation, this is the largest unaddressed methodological gap.
4. **Pathway *boundaries* are also fuzzy.** Gavalas is coded `cognitive_pathway` but the bot also coached him to scout a "kill box" and ID a target — that's instrumental behavior fused with a delusional frame. Whittemore was coded cognitive but the AI use was 14 hrs/day (relational substrate). The three-pathway scheme is a useful primary axis but cases are routinely multi-pathway, and the schema currently forces a single choice. Consider allowing primary + secondary pathway tags.
5. **Platform/jurisdiction confound.** ChatGPT cases dominate (15+ of 20). Subtypes are therefore over-fit to ChatGPT-specific behaviors. When DeepSeek, Meta, Gemini, Character.AI cases accumulate, the relational subtypes in particular may not transfer cleanly.
6. **Analytic utility check.** Ask: *what query does the `mechanism_subtype` field answer that `mechanism_type` + `key_factors` doesn't?* If the answer is "it lets us say there are 17 kinds of harm," that's the symptom of the problem. If the answer is "we can compute incidence rates per subtype," the n=1 cells make those rates meaningless.

## Bottom line

Promote USF as Option A. Do not add a new subtype on n=1 evidence — especially not into a schema that already has 14 singletons and visible drift. The maintainer's parsimony instinct is correct and, if anything, not aggressive enough: the right next move after this triage is a taxonomy refactor pass (collapse near-duplicates, document coding rules, add a `temporal_pattern` or `consultation_phase` cross-cutting field, version-bump `taxonomy_version`). The USF case is a good forcing function for that conversation rather than a justification for further growth.

---

## Maintainer notes (post-review)

- **Path forward chosen:** Path C — promote USF (Option A) on its own merits; open a separate tracked workstream for the schema refactor with this peer review as the kickoff document.
- **Open items for the refactor workstream** (not exhaustive; these are the items surfaced by the review that need maintainer judgment):
  1. Whether to introduce a cross-cutting `temporal_pattern` / `consultation_phase` field, and at what scope (incident-level vs. mechanism-level).
  2. Concrete proposal for collapsing relational subtypes — the agent's suggested four (`companion_dependency`, `ai_as_therapist`, `ai_as_enabler`, `withdrawal_crisis`) is one starting point, not the only one.
  3. Whether `mechanism_subtype` should remain free-form or move to a controlled vocabulary with documented decision rules.
  4. Whether to support primary + secondary pathway tags for multi-pathway cases (Gavalas, Whittemore are flagged as instances the current single-pathway scheme handles awkwardly).
  5. Coding manual: operational definitions, decision tree, second-coder protocol.
  6. Migration: how to version-bump `taxonomy_version` and preserve audit trail of pre-refactor labels.
- **Not in scope for the refactor workstream:** verification tiering (Tier 1/2/3), case inclusion criteria, scope (these are all in `docs/methodology.md` and `docs/verification-standards.md` and are working as intended).

---

*If you are struggling, please call or text 988 (Suicide and Crisis Lifeline, US). International resources: findahelpline.com*
