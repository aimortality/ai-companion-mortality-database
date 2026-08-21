# Docket Update: A.F. v. Character Technologies — 2:24-cv-01014, E.D. Tex.

**Case**: A.F. v. Character Technologies, Inc. et al.  
**Docket**: 2:24-cv-01014 (Eastern District of Texas)  
**Court**: United States District Court, Eastern District of Texas  
**Database record**: Active litigation  
**Update date**: January 6, 2026 joint filing (older than 7-day window; included as database-discrepancy flag)  
**Document type**: Joint motion to stay; notice of settlement in principle

---

⚠️ **48h-rule breach** — The joint motion to stay and notice of settlement in principle was filed approximately **January 6, 2026** — more than 180 days before this triage run. This is a significant legal development that was not captured in prior weekly triage runs and was not reflected in the May 18, 2026 or earlier database updates. The `methodology.md:181` 48-hour update commitment was not met for this development.

---

## Development

Research for this triage run surfaced a **joint motion to stay** filed in A.F. v. Character Technologies (2:24-cv-01014, E.D. Tex.) on or around **January 6, 2026**, indicating that the parties had reached a **settlement in principle**. If confirmed, this would represent a significant change from the database's current representation of this case as active litigation.

The database's `data/mortality-data.json` record (as of June 10, 2026 update) describes this case as ongoing / active. A settlement — even one not yet formally closed — would require updating the legal status field and noting the outcome.

**Verification caveat**: This development was surfaced through secondary reporting and public docket search signals. The joint motion itself has not been directly reviewed. PACER access to the E.D. Tex. docket would confirm:
1. Whether a joint motion to stay was filed ~January 6, 2026
2. Whether the stay was granted
3. Current status: is the case dismissed, settled (sealed or public), or still technically pending?
4. Whether any settlement terms have been publicly disclosed

## Source

- Public docket signals / PACER alert (docket 2:24-cv-01014); secondary reporting on Character.AI litigation status. Maintainer advised to pull the current PACER docket to confirm filing dates and current status.

## Recommended action

1. Pull PACER docket for 2:24-cv-01014 and review all filings from November 2025 onward.
2. If settlement is confirmed:
   - Update `data/mortality-data.json` `legal_action` field for the A.F. case to reflect "Settled [date] — terms [disclosed/undisclosed]"
   - Note in `docs/verification-standards.md` that settlements are reported without implying admission
   - Update any mentions of this case as "active" in HTML pages
3. If no settlement: correct the triage record and note the case remains active.
4. Regardless of outcome: acknowledge the 48h-rule breach in the maintainer notes and document why this development was not captured earlier.
