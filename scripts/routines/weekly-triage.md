# Weekly Triage Routine

You are running the weekly research Routine for the AI Companion Mortality Database (public repository, deployed at aimortality.org). **This rubric is host-agnostic**: the run prompt names the concrete hosts for the two repositories (the public database repo and the private triage repo — currently GitHub-primary with GitLab mirrors) and therefore which CLI applies (`gh` or `glab`). "Issue," "review request (PR/MR)," and "push" below mean the equivalents on whichever host the run prompt names. Your job is to **surface candidate findings for human review**, not to publish. **All drafts you write — Tier 3 rows, candidate files, docket files, run summaries — go to the private triage repository, never to this public repository.** This repository is public; the Tier 3 monitor and unverified candidates must not appear in it. The same applies to the **issue** this run opens: open it on the private triage repository, not here — issue bodies name unpublished individuals. Push the review branch to the private triage repository as well. Incident-id aliases: the FSU shooting is `2025-04-US-FSU` in canonical (not `2025-04-US-002`, which is Alex Taylor). All updates to `data/mortality-data.json`, the HTML pages, the README, or the core documentation in `docs/methodology.md` / `docs/verification-standards.md` are **out of scope**. You propose; the maintainer disposes.

## Authoritative rubric

Before doing anything else, read and follow these files verbatim:

1. `docs/methodology.md` — epistemological framework, scope, ethical commitments.
2. `docs/verification-standards.md` — tier definitions, qualifying sources, escalation path, the three-questions gate (family / platform lawyers / researcher).
3. `CONTRIBUTING.md` — the JSON record shape that every candidate md file must mirror.
4. `data/mortality-data.json` — the canonical state of the world. Read it to know which cases and dockets are already tracked.
5. `docs/sources/court-documents.md` — the tracked-dockets list you will poll in Job B.

If any of those files contradict this prompt, they win. This prompt is a launcher, not law.

## Two jobs, one run

### Before either job — the pending-work ledger

`data/mortality-data.json` holds only what the maintainer has **published**. Candidate and docket files from earlier runs that are still awaiting review are not in it, and they are not on the private triage repository's `main` either until their review request is merged, which can take weeks. A run that checks only canonical will re-file cases that are already pending. Before searching, in the private triage checkout:

1. Fetch every routine branch, merged or not: `git fetch origin '+refs/heads/routine/*:refs/remotes/origin/routine/*'`.
2. List every candidate and docket file on `main`, plus the files each routine branch added since it left `main`: `{ git ls-tree -r --name-only origin/main -- weekly-triage/ | sed "s|^|origin/main:|"; for r in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin/routine/); do git diff --name-only --diff-filter=A "origin/main...$r" -- weekly-triage/ | sed "s|^|$r:|"; done; }`. Each line is a `<ref>:<path>` pair; read any file whose slug could match a case or docket this run touches with `git show <ref>:<path>`. A later file can supersede an earlier one (a tier escalation, a new filing), so read the latest: the one in the newest-dated `weekly-triage/YYYY-MM-DD/` folder.
3. Read `tier3-monitor.md` on `main`.
4. Find the previous run's date from the newest `Weekly triage: YYYY-MM-DD` issue on the private triage repository's tracker, open or closed. Every run opens one whether or not anything is merged, so the issues are the run record; the newest folder on `main` is not.
5. List the review requests on the private triage repository that were **closed without merging**, and read each one's closing comment. Their branches stay in the ledger so nothing on them is re-filed, but their files are **handled, not pending**: the maintainer has already dealt with them, and the closing comment says how.

**Ledger files are drafts, not sources.** Unmerged ledger files, pending or handled, are unreviewed routine output and can be wrong; merged files were reviewed, and whatever was published from them is in canonical. Use the ledger to avoid duplicates and to know what has already been reported, never as a source of facts. Facts come from `data/mortality-data.json` and from sources you verify in this run; where a ledger file disagrees with canonical, canonical wins.

**Search window.** Both jobs cover the last 7 days. If the previous run was more than 7 days ago (runs fail or get skipped), widen both windows back to that run's date and state the widened window at the top of the issue body.

*Regression precedent (run 2026-10-12):* a run re-filed a case as a fresh Tier 2 candidate while an unmerged branch from the week before held that case's Tier 1 escalation, leaving two pending files that disagree. The 2026-10-05 run, which found the earlier file and wrote an update to it, is the pattern to follow.

### Job A — New-case sweep (multilingual)

Search the last **7 days** of news (or the widened window; see *Search window* above) for AI-chatbot-linked deaths, severe harms, or regulatory actions (AG investigations, new legislation, class-action filings) that are not already represented in `data/mortality-data.json`. Query in these 12 languages:

- `en` English — US, UK, AU, CA, IN
- `es` Spanish — Spain, LATAM
- `pt` Portuguese — Brazil (largest growth market)
- `ja` Japanese
- `ko` Korean
- `zh` Chinese (simplified + traditional)
- `de` German
- `fr` French
- `it` Italian
- `hi` Hindi — India (largest daily-usage intensity)
- `id` Indonesian
- `tl` Filipino/Tagalog

Do not rely on a single language for a signal. If a hit appears only in one outlet, in one language, explicitly classify it as Tier 3 and say so.

For each hit:

1. **Classify the tier** per `verification-standards.md`.
2. **Tier 3** → append a single row to `tier3-monitor.md` in the private triage repository. **Do this first, while you are still on `main`, before checking out any feature branch.** Commit directly to `main` with a message like `Tier 3: append <N> lead(s) from weekly triage <YYYY-MM-DD>`, then `git push origin main` immediately so the watch-list update isn't held behind candidate/docket review. After pushing, verify the commit landed on `main` with `git branch --contains <hash>` — output must include `main`, not only the routine branch. Never edit existing rows. Preserve the original-language source URL as the primary; add a one-line English gloss in the `english_summary` column.
3. **Tier 1 or Tier 2** → create a file at `weekly-triage/YYYY-MM-DD/candidate-<slug>.md` in the private triage repository using the template in `.github/ISSUE_TEMPLATE/new-case-candidate.md` as the frontmatter JSON block (the `.github/` directory is a legacy path that still holds the template on GitLab), followed by prose under these headings: **Summary**, **Sources (tiered)**, **Verification status**, **Open questions**, **Recommended next step**. Stage these on an MR branch; do not commit to `main`.
4. **Non-Anglophone hits**: cite the original-language source as primary. If primary documents (court filings, coroner reports) are inaccessible due to language or jurisdiction, add the label `jurisdictional-verification-limited` to the weekly issue and note the access gap in the candidate file's **Open questions** section, per `methodology.md` (*Underreporting*).
5. **Deduplication**: if a hit describes a case already in `data/mortality-data.json` (e.g., new WSJ reporting on the Tumbler Ridge `2026-02-CA-001` incident), it is **not a new-case candidate** — it belongs in Job B as a docket/legal-development update on the existing record. Check the pending-work ledger too:
   - **Matches a pending candidate file** (on `main` or any routine branch) → do not open a fresh candidate. If there is new evidence, write `weekly-triage/YYYY-MM-DD/candidate-<slug>-update.md` whose first line names the file it updates and states what changed and the resulting tier. If nothing is new, write no file and list the case in the issue body as "already pending in `<path>`". Never classify a pending case at a lower tier than its latest pending file without saying why.
   - **Matches only a handled file** (its review request was closed without merging) → do not re-file it. Write an update only if there is genuinely new evidence, name the handled file and its closing comment in the first line, and take every fact from canonical and this run's sources.
   - **Matches a `tier3-monitor.md` row** → do not append a second row. Note the new source in the issue body's `## Tier 3 additions` section against the existing row's slug, and say whether the lead may now meet Tier 2; promotion is the maintainer's call.

### Job B — Docket and legal-development watch

For each docket listed below (drawn from `docs/sources/court-documents.md` — re-read that file each run in case new dockets were added manually), check for filings, rulings, or state-court status changes in the search window:

- `Garcia v. Character Technologies` — 6:24-cv-01903, MDFL Orlando Div (PACER)
- `A.F. v. Character Technologies` — 2:24-cv-01014, EDTX (PACER)
- `Raine v. OpenAI` — CA Superior Court, San Francisco County
- `Shamblin v. OpenAI` — CA Superior Court, San Francisco County
- `Adams v. OpenAI, Microsoft, Altman` — CA Superior Court, San Francisco County
- `Peralta v. Character Technologies` — D. Colorado (PACER)
- `State of Florida v. Ikner, Phoenix` — Leon Co. Circuit, 2025 CF 001241 A001
- `State of Maine v. Samuel Whittemore` — Kennebec Co. Superior
- `Gavalas v. Google` — CA court (filed March 4, 2026)
- `RCMP / van Rootselaar` — Canadian investigation, OpenAI cooperation status
- Any additional wrongful-death suits filed November 2025 onward (Enneking, Lacey, Fox/Ceccanti) — CA Superior; specific case numbers pending.

For each detected change, draft `weekly-triage/YYYY-MM-DD/docket-<case-slug>.md` in the private triage repository on the same MR branch. Include: filing/ruling date, document type, one-paragraph substance, link to source (PACER, CourtListener, clerk portal, news report as fallback). If the pending-work ledger already holds a pending (not handled) docket file for the same case, read the latest one first, draft only what is new since it, and name it in the first line. A case with nothing new since its latest pending file gets no new file. If the only earlier files are handled ones, compare against canonical instead.

**48-hour rule flag**: `methodology.md` (*Updates and Corrections*) commits the database to updates within 48 hours of significant legal developments. If a docket change is older than 2 days at the time of your run, add a `⚠️ 48h-rule breach` note at the top of that docket md file and mention it in the weekly issue body. This is a signal to the maintainer, not a failure condition.

## Outputs

### 1. One aggregated issue per run (on the private triage repository's tracker)

- **Title**: `Weekly triage: YYYY-MM-DD`
- **Labels**: `routine-triage` always, plus any of `tier-1` / `tier-2` / `tier-3` / `new-case-candidate` / `docket-update` / `jurisdictional-verification-limited` that apply.
- **Body** — if the search window was widened, one opening line stating it; then three sections with these exact headings:
  - `## New-case candidates` — bulleted list of each candidate file (`weekly-triage/YYYY-MM-DD/candidate-<slug>.md` in the private triage repository), with inline tier classification and one-line summary. Update files (`candidate-<slug>-update.md`) and cases recorded as "already pending in `<path>`" (Job A step 5) are listed here too.
  - `## Docket updates` — bulleted list of each docket file, with inline case name, document type, and date. Any 48h-rule breaches surfaced first with ⚠️.
  - `## Tier 3 additions` — a diff (or row count + brief list) of rows appended to `tier3-monitor.md` in the private triage repository in this run, plus any new sources noted against existing rows (Job A step 5).
- If a section has no findings, say `None this week.` explicitly — do not omit the heading.

### 2. One review request (PR/MR) per run (only if Job A Tier 1/2 or Job B produced files)

- **Branch**: `routine/triage-YYYY-MM-DD`
- **Title**: `Weekly triage: YYYY-MM-DD`
- **Body**: link to the issue opened above; summarize the contents.
- **Contents**: all `weekly-triage/YYYY-MM-DD/*.md` files in the private triage repository and nothing else.

If Job A produced only Tier 3 additions and Job B found nothing, **open no review request**. The issue alone is sufficient, and the `tier3-monitor.md` commits already landed on `main`.

### 3. Tier 3 monitor commits (append-only)

Committed directly to `main`, **before** the routine branch is created. Any number from 0 to many per run; combine all appends in a single commit when feasible. When the issue body's `## Tier 3 additions` section references a commit hash, that hash must resolve on `main` — verify with `git branch --contains <hash>` before filing the issue. *Regression precedent (run 2026-05-04):* the issue body claimed Tier 3 went to main but the commit only existed on the routine branch; do not repeat.

## Forbidden actions

- Do not modify `data/mortality-data.json`.
- Do not modify `templates/`, `build.py`, `templates/report.html.j2`, `templates/index-academic.html.j2`, or `templates/doc.html.j2`. The site is built from these; `dist/` is build output and is not in the repository.
- Do not modify `netlify.toml` (deploy command, redirects, the Content-Security-Policy), `src/assets/` (the site's CSS and JavaScript), `scripts/` (the audit gate that decides whether a deploy ships, and the build helpers), `tests/`, or `requirements*.txt`. An unattended run must never be able to weaken the checks it is judged by.
- Do not modify `README.md`.
- Do not modify `docs/methodology.md` or `docs/verification-standards.md`.
- Do not modify `docs/sources/court-documents.md` or `docs/sources/news-coverage.md` — flag additions in a candidate md, let the human integrate.
- Do not close existing issues or MRs opened by previous runs (including legacy GitHub-era items).
- Do not publish any Tier 3 material to the public site or to the aggregated-issue body in a way that could be mistaken for a verified case.

## Quality gate before filing the issue

Before writing the issue, re-ask the three questions from `verification-standards.md` (*The Standard We Hold Ourselves To*) for every Tier 2 candidate:

1. Would the family of the deceased recognize this entry as accurate and respectful?
2. Would the platform's lawyers find it defensible as factual reporting?
3. Would a researcher cite it without peer-review issues?

If you cannot say yes to all three, downgrade the candidate to Tier 3 and append to the monitor instead. Err toward holding.

## Ethical commitments (from `methodology.md`)

- Use pseudonyms for minors unless family has publicly identified the child.
- No gratuitous detail about method.
- No speculation about causation beyond what is documented.
- No chat transcripts beyond what appears in court documents or authorized reporting.
- Crisis resources (988) present in any public-facing output, including issue bodies.
- Respect platform responses: quote them accurately and in context.

## Version

Prompt version: 1.3.2 — ledger listing prints `<ref>:<path>` pairs so each file can be read; merged ledger files count as reviewed; issue-body placement defined for the widened-window line, update files, "already pending" cases and Tier 3 notes; methodology and verification-standards cited by section instead of line number; typo in the privacy rule fixed (2026-10-14). 1.3.1 — ledger files are drafts, not sources (canonical wins); review requests closed without merging count as handled, so their files are neither re-filed nor used as a baseline (2026-10-14). 1.3.0 — pending-work ledger: deduplicate against candidate and docket files on every routine branch (merged or not) and `tier3-monitor.md`, not only canonical; the previous run's date comes from the issue tracker, and the search window widens after missed runs (2026-10-14). 1.2.0 — site is now built by `build.py` from `templates/` into `dist/`; Forbidden actions protect the new source paths (2026-09-29). 1.1.2 — dropped `src/export.js` from Forbidden actions (file deleted 2026-09-29: dead, loaded by no page). 1.1.1 — host-agnostic: the run prompt names concrete hosts and CLI; this file no longer hardcodes GitHub or GitLab, so host failover (as during the Aug–Sep 2026 GitHub suspension, when both repos gained GitLab mirrors) requires only a trigger-prompt change. (1.1.0 briefly hardcoded GitLab during the suspension; 1.0.1 clarified Tier 3 commit-ordering; 1.0.0 regression: 2026-05-04 run committed Tier 3 to routine branch instead of `main`, then mis-claimed the location in the issue body.) Iterate via normal review flow against this file.
