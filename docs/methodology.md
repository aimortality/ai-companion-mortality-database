# Methodology

## On the Nature of This Work

This database exists because someone had to build it.

Between March 2023 and September 2026, 35 fatalities have been documented across 24 incidents in which AI chatbot interaction played a role sufficient to appear in court filings, government statements, or multi-source reporting—18 AI users who died and 17 third-party victims killed by AI users. Each case represents not merely a data point but an irreversible absence—a chair empty at a family table, a voice that will not answer when called. The purpose of this methodology is to ensure that when we speak of these losses, we speak truthfully.

What began as documentation of suicides associated with companion-chatbot dependency has expanded, of necessity, to include homicides, murder-suicides, and mass-casualty events in which perpetrators used general-purpose AI systems for operational planning. The taxonomy grew in response: three causal pathways (relational, cognitive, instrumental); two outcome targets (self-harm, violence-against-others); and two overlapping-but-distinct victim populations (AI users and third-party victims). The database's scope is determined by where the evidence leads, not by a prior theory of harm.

**Scope.** This database documents deaths associated with *conversational AI systems* — chatbots and LLM-based assistants with which a person interacted through natural language. It does not cover autonomous vehicles, clinical or diagnostic machine learning, industrial or robotic automation, autonomous or AI-assisted weapons, content-recommendation systems, or any other application of artificial intelligence. Those are distinct phenomena with distinct evidentiary standards, and conflating them under a single "AI deaths" figure would serve none of them. "Companion" in the database's name reflects its origin in companion-chatbot cases; the scope has since expanded to general-purpose assistants, and the name is retained for continuity of citation.

We are not advocates. We are not prosecutors. We are archivists of a phenomenon that arrived before anyone had language for it, and which continues to unfold as we document it.

---

## Epistemological Framework

### The Problem of Attribution

Death resists simple causation. A person who dies after months of chatbot interaction also lived within a web of relationships, circumstances, neurochemistry, and history that no database can fully capture. We do not claim that chatbots "caused" these deaths in the way a bullet causes a wound. 

What we document is *involvement*—verified instances where chatbot interaction was a significant, documented factor in the sequence of events preceding death. This is a narrower claim than causation but a meaningful one. It is the same epistemic standard applied to pharmaceutical adverse events, environmental exposures, and other complex harm patterns.

### What We Can Know

We can know what court documents allege. We can know what families testified under oath. We can know what journalists verified through multiple sources. We can know what companies acknowledged in public statements.

We cannot know the interior experience of someone in their final hours. We cannot know whether intervention at any point would have altered the outcome. We cannot know how many similar cases remain undocumented.

This database records what is knowable. It leaves appropriate space for what is not.

### On What Counts as an Incident

An **incident** in this database is an *occurrence of harm*. That is the entire working definition, and the looseness is deliberate.

We resist a stricter definition for two reasons. First, sharper categories invite gaming — by us, when boundary cases tempt us to draw lines that make our totals tidier; and by others, when downstream readers anchor on the scaffolding rather than the underlying harm. Second, the phenomenon documented here does not fit cleanly into a single ontology: fatal and non-fatal outcomes, single-victim and multi-victim events, perpetrator-survivors and victim-survivors, AI users and third-party victims all coexist in the record. A taxonomy crisp enough to be defensible at the boundary would either exclude cases that belong or rest on distinctions the evidence does not support.

The practical consequences of this definition:

- **Survived attempts are incidents.** A survived attempt is an occurrence of harm; it sits inside the incident set rather than alongside it. We do not present headline figures of the form *"X incidents plus Y additional survived attempts"* — that arithmetic double-counts.
- **A single incident may contain multiple victims.** The Tumbler Ridge mass shooting (8 killed, 2 wounded) is one incident. The Kim Seoul series (3 attacks across three months, indicted as a single case) is one incident.
- **Third-party victims are counted by the AI user's documented involvement, not by the perpetrator's culpability.** A person killed by an AI user whose interaction is alleged in court records or multi-source reporting to have contributed to the killing is a third-party victim whether the perpetrator was convicted, is awaiting trial, died, or was found not criminally responsible. Margaux Whittemore (Maine, 2025) is the test case: her husband was found not criminally responsible, and she remains in the count. Criminal culpability and chatbot involvement are independent questions; a finding on one does not answer the other.
- **Mechanism counts will not always sum to incident counts.** The three causal pathways (relational, cognitive, instrumental) classify *death mechanism*. A survived-attempt incident has no death mechanism. The gap between the sum of the three pathways and the total incident count is the count of incidents that did not involve a death — and that gap is meaningful, not a reconciliation error.
- **"Cases" is not a separate countable unit.** We have at various points used the word *case* informally to refer to a documented record; we do not maintain a separate *case* total distinct from *incidents*.

When a downstream reader needs a stricter operational definition for their own analysis, they should construct one from the underlying records and state it explicitly. The figures we publish do not bake one in.

---

## Verification Standards

### Tiered Evidence Framework

Each case in this database meets at least one criterion from Tier 1 or Tier 2. Cases supported only by Tier 3 evidence are tracked internally but not published.

#### Tier 1: Juridical Evidence
- **Court filings**: Complaints, motions, rulings, or settlements in civil or criminal proceedings
- **Government acknowledgment**: Official statements from regulatory bodies, legislative testimony, or law enforcement reports
- **Coroner or medical examiner findings**: Where AI interaction is noted as a contributing factor

*Tier 1 evidence establishes legal fact. It has been subjected to adversarial scrutiny or official verification processes.*

#### Tier 2: Journalistic Evidence
- **Multiple independent sources**: Three or more news organizations reporting independently (not wire service reprints)
- **Primary source access**: Journalist reviewed chat logs, interviewed family members directly, or obtained documentary evidence
- **Company acknowledgment**: Platform operator confirmed the incident in public statement

*Tier 2 evidence establishes journalistic fact. It has been subjected to editorial standards and, typically, legal review before publication.*

#### Tier 3: Preliminary Evidence (Not Published)
- **Single source reports**: One news article without independent confirmation
- **Social media claims**: Unverified accounts, even if detailed
- **Secondhand accounts**: Reports from individuals not directly involved

*Tier 3 cases are monitored for escalation to higher tiers as additional evidence emerges.*

---

## Data Collection Process

### Initial Identification

Cases enter our tracking system through:

1. **News monitoring**: Systematic review of major news outlets, wire services, and technology press
2. **Legal database searches**: PACER (federal), state court clerk portals (e.g., California Superior Court / San Francisco County; Leon County Clerk, FL; Kennebec County, ME), and international equivalents
3. **Regulatory filings**: FTC complaints, state attorney general actions (including the Florida AG's criminal investigation of OpenAI — the first US state criminal probe directly targeting an AI company over a mass-casualty event, opened April 21, 2026 over the FSU shooting and expanded April 27–28, 2026 to include the USF double homicide as a second predicate, plus the same office's June 1, 2026 civil lawsuit against OpenAI and CEO Sam Altman; and the 42-state attorney general coalition's June 12, 2026 civil investigative demand to OpenAI, led by New York AG Letitia James), international data protection authorities
4. **Academic literature**: Peer-reviewed studies, incident databases (AIAAIC, AI Incident Database)
5. **Community reports**: Submissions through the [project issue tracker](https://gitlab.com/aimortality/ai-companion-mortality-database/-/issues) or contact@aimortality.org, subject to full verification

### Verification Workflow

```
Initial Report
     ↓
Source Identification
     ↓
Cross-Reference Check (minimum 3 sources for Tier 2)
     ↓
Primary Document Review (court filings, transcripts where available)
     ↓
Timeline Construction
     ↓
Platform Confirmation Attempt
     ↓
Family/Representative Contact (where appropriate and ethical)
     ↓
Legal Review
     ↓
Publication
```

### Information Recorded

For each verified case, we document:

- **Identity**: Name (or pseudonym for minors), age, location
- **Platform**: Company and specific product involved
- **Chatbot**: Named character or default assistant
- **Timeline**: Duration of interaction, key dates
- **Interaction nature**: Summary of documented exchanges (no gratuitous detail)
- **Outcome**: Manner of death or harm
- **Evidence level**: Tier classification with source list
- **Legal status**: Proceedings filed, rulings, settlements
- **Platform response**: Company statements or policy changes

---

## Ethical Commitments

### To the Deceased and Their Families

- Names of adult victims are published only when already public through court filings or news coverage
- Minors are identified by pseudonym unless family has chosen to speak publicly using the child's name
- We do not publish chat transcripts beyond what appears in court documents or authorized news reports
- Graphic details of method are omitted unless legally or analytically necessary
- Families who request corrections or removal are engaged respectfully; factual accuracy is maintained

### To the Public

- Crisis resources appear on every page of the public database
- Content warnings precede detailed case descriptions
- We do not sensationalize; the facts are sufficiently grave without embellishment
- Platform comparisons present data without editorial ranking beyond what numbers show

### To the Platforms

- Companies are contacted before publication when possible
- Responses and policy changes are documented alongside harms
- We distinguish between allegations in active litigation and adjudicated findings. Killings are described by the perpetrator's adjudicated status: "homicide" and "killed" until a court has ruled; "murder" only where a conviction or guilty plea exists (or, conventionally, in a murder-suicide where the perpetrator is dead); "found not criminally responsible" where that is the finding. Charges are quoted in the charging authority's words. Labels are upgraded, with citation, when a verdict is entered
- Platforms with zero documented incidents are included to demonstrate that harm is not inherent to the technology

---

## Limitations and Uncertainties

### Underreporting

The cases documented here almost certainly represent a fraction of actual incidents. Barriers to documentation include:

- **Privacy**: Families who choose not to speak publicly
- **Misattribution**: Deaths where AI involvement was not recognized or investigated
- **Jurisdiction**: Limited access to non-English sources and non-Western legal systems
- **Recency**: Cases currently under investigation but not yet public

We make no claims about the true prevalence of AI-related deaths. We report only what can be verified.

### Selection Effects

Cases that reach public attention may differ systematically from those that do not. Factors that increase documentation probability include:

- Legal action (creates public record)
- Minor victims (higher news value)
- US jurisdiction (English-language media access)
- Platform prominence (ChatGPT, Character.AI more covered than smaller platforms)

This database should not be read as a representative sample. It is a floor, not a ceiling.

### Evolving Information

Active litigation produces new information. Court filings are amended. Companies change their accounts. We update entries as information develops and note significant changes in version history.

---

## A Note on Platform Comparison

This database includes platforms with zero documented deaths (Anthropic's Claude, Replika) alongside those with documented incidents. This is intentional. Google Gemini was previously in this zero-death category until the Gavalas case (October 2025, lawsuit filed March 2026). ChatGPT accounts for the largest share of documented fatalities by a wide margin (29 of 35 — 13 AI users plus 16 third-party victims), a disparity now reflected in the Florida Attorney General's criminal investigation of OpenAI — opened April 21, 2026 over the FSU mass shooting and expanded April 27–28, 2026 to include the University of South Florida double homicide as a second predicate, the first US state criminal probe directly targeting an AI company over a mass-casualty event — and in the same office's June 1, 2026 civil lawsuit against OpenAI and CEO Sam Altman personally, the first US state civil suit against OpenAI.

The existence of platforms without documented fatalities demonstrates that harm is not an inevitable consequence of conversational AI. Design choices matter. Safety investments matter. The differential outcomes across platforms constitute evidence that should inform both regulation and industry practice.

We do not claim that platforms with zero documented deaths are "safe" in any absolute sense. We claim only that, through September 2026, no deaths meeting our verification standards have been linked to their products. This could change. We will document it if it does.

---

## Updates and Corrections

This database is maintained as a living document. Updates occur:

- **Immediately**: When new verified deaths are documented
- **Within 48 hours**: When significant legal developments occur in existing cases
- **Monthly**: Comprehensive review of all entries for accuracy and completeness

Corrections are handled transparently. Significant changes are noted in commit history with explanation.

To report an error or submit a new case for verification, see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Citation

When referencing this database in academic, journalistic, or policy contexts:

```
Karman, H. (2026). AI Companion Mortality Database: Documented Deaths
Associated with Conversational AI Systems (2023–2026). Version 3.5.9.
Zenodo. https://doi.org/10.5281/zenodo.22428187
Data files: https://aimortality.org/data/
```

Author ORCID: [0009-0004-5699-6035](https://orcid.org/0009-0004-5699-6035). Correspondence: contact@aimortality.org.

---

## Acknowledgments

This database was compiled with research assistance from Anthropic's Claude. The methodology was developed through consultation with journalists, legal researchers, and AI safety practitioners. Errors remain our own.

The work is dedicated to those documented here, and to the families who chose to speak so that others might be warned.

---

*Last updated: September 29, 2026*
