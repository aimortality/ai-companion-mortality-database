---
name: Docket update — A.F. v. Character Technologies (2:24-cv-01014, E.D. Tex.) — correction: case appears to have joined settlement track
description: ⚠️ 48h-rule breach — January 6, 2026 joint motion to stay deadlines indicates A.F. case joined the Character.AI/Google settlement negotiations; previously characterized in database as NOT part of the settlement
type: docket-update
case: A.F. v. Character Technologies, Inc. (2:24-cv-01014, E.D. Tex.)
---

# ⚠️ 48h-rule breach — A.F. Case Appears to Have Joined Settlement Track (January 6, 2026)

**Development date:** January 6, 2026 (joint motion to stay filed by all defendants)
**Document type:** Joint motion to stay all deadlines; notice of settlement
**Court:** U.S. District Court, Eastern District of Texas (Magistrate Judge Roy S. Payne)
**48h-rule status:** ⚠️ BREACH — filing is approximately 125 days old at time of this run. The database characterizes A.F. as "NOT" part of the January 2026 settlement; this appears to be incorrect.

## Substance

The database currently states: *"A.F. v. Character Technologies (2:24-cv-01014 EDTX) was not included [in the settlement]; that case remains active."*

This characterization requires correction based on new docket information from CourtListener and TechPolicy.Press:

On **January 6, 2026** — one day before the January 7, 2026 public settlement announcement — defendants (Character Technologies, Google/Alphabet, Noam Shazeer, Daniel De Freitas) filed a **joint motion to stay all deadlines and notice of settlement** in the A.F. case. This is the same type of motion filed in the Garcia and Peralta/Montoya cases when they were settled.

On March 19, 2026, Magistrate Judge Roy S. Payne ordered a telephone conference to address the settlement status.

**Current status is uncertain:** No dismissal order has been confirmed in publicly available sources. It is possible that:
1. The A.F. settlement is still being finalized (similar to the Garcia situation — see `docket-garcia-settlement-collapsed.md`)
2. The A.F. settlement finalized but was not publicly announced separately
3. The A.F. case is on a parallel settlement track that is still ongoing

**The injunctive relief element** — A.F. sought an order requiring Character.AI to cease operations until safety defects were cured, which no monetary settlement can fully resolve — may complicate settlement finalization.

**Practical implication:** The database should not characterize A.F. as an actively litigated case heading to trial without verifying the current status. The January 6 joint motion suggests the parties intend to settle; whether they have successfully done so requires direct PACER access to confirm.

## Sources

- CourtListener docket 2:24-cv-01014: https://www.courtlistener.com/docket/69450881/af-on-behalf-of-jf-v-character-technologies-inc/
- TechPolicy.Press tracker: https://www.techpolicy.press/tracker/af-et-al-v-character-technologies-et-al/
- JurisCase.org docket entry

## Database updates required

- `data/mortality-data.json`, Character.AI platform entry: Update `legal_status` note — A.F. case (EDTX) appears to be in settlement negotiations as of January 6, 2026; remove or caveat the statement that it "was NOT included" in the settlement.
- `docs/sources/court-documents.md`, A.F. section: Update status to "settlement negotiations entered January 6, 2026; formal dismissal unconfirmed as of May 11, 2026."
- **Action required:** Obtain current PACER docket for 2:24-cv-01014 to confirm whether case has been dismissed or remains pending.

---

*If you are struggling, please call or text 988 (US). International: findahelpline.com*
