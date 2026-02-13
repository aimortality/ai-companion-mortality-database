# AI Companion Mortality Database - Development Guide

## Project Overview

Public research database tracking verified deaths associated with AI chatbot interactions. Static HTML site deployed on Netlify at **aimortality.org**. Also accessible via ai-death.com and chatbotdeaths.org (redirects).

## Architecture

Static site using vanilla HTML/CSS with React 18 loaded via CDN (esm.sh). No build step - files in `src/` are served directly.

## Key Files & Data Flow

**Data is duplicated across multiple files.** When adding or updating cases, ALL of these must be updated:

| File | What it contains |
|------|-----------------|
| `data/mortality-data.json` | **Canonical data source.** Full incident records, platform stats, regulatory info. Update this first. |
| `src/index.html` | Main page. Has inline React component with **its own copy** of all case data, SVG charts, stat boxes, demographic tables, and meta tags. |
| `src/report.html` | Research report. Individual case sections with detailed narratives, legal proceedings, and summary stats. |
| `src/index-academic.html` | Academic-style page. Has abstract, key findings, and dates that mirror index.html. |
| `src/export.js` | Data export utilities. Has **another copy** of case data plus a mock API with hardcoded stats. |
| `README.md` | GitHub-facing. Has badges, case table, platform comparison, key findings. |

## Adding a New Case - Checklist

1. **Verify the case** through court documents, multiple news sources, or government acknowledgment before adding
2. Update `data/mortality-data.json` (add incident, update metadata counts, platform deaths)
3. Update `src/index.html`:
   - Meta tags (description, OG, Twitter, schema.org JSON-LD)
   - `.meta` line (deaths count, cases count, period)
   - Abstract text and key findings list
   - React `data.platforms` array (add case object)
   - Stat boxes (death count, minors count if applicable)
   - SVG visualizations (age distribution, platform bars, cumulative chart)
   - Temporal distribution table (deaths by year)
   - Demographic tables (add age row, recalculate percentages)
   - Footer date
4. Update `src/report.html` (add case section, update executive summary, stats, conclusions)
5. Update `src/index-academic.html` (abstract, key findings, dates)
6. Update `src/export.js` (case array, death counts, stats)
7. Update `README.md` (badge, case table, platform comparison, key findings)

## Stats to Recalculate

When death count changes, recalculate:
- Minors percentage (deaths under 18 / total deaths)
- Average age
- Deaths by year
- Platform death counts and percentages
- Age distribution buckets (13-17, 18-35, 36-54, 55+) and their percentages
- Cases count (deaths + survived attempts)
- Duration note denominator ("Duration known for X of Y cases")

## Verification Standards

Cases require at least ONE of:
- Court documents or legal filings
- Multiple independent news sources (3+)
- Official government acknowledgment
- Congressional testimony
- Public statements by verified family members

**Important:** LLM-generated research (from Gemini, ChatGPT, etc.) should always be independently verified through web searches before adding to the database. LLMs can hallucinate cases, dates, and details.

## Platforms Tracked

Currently 7: ChatGPT, Character.AI, Chai AI, Meta AI, Gemini, Claude, Replika

## Content Sensitivity

This database documents real deaths. Maintain:
- Crisis resources (988 hotline) on every page
- Respectful, factual tone
- No speculation about causation beyond what's documented
- Verification level noted for each case

## Deployment

- **Host:** Netlify (auto-deploys from main branch)
- **Domain:** aimortality.org
- **Analytics:** Google Analytics (G-SS2VTGZ004)
- No build step required - push to main and it's live

## Style Conventions

- Monospace font throughout (SF Mono / Menlo / Monaco / Courier New)
- Brutalist aesthetic with light/dark theme toggle
- All dates in format: "Month DD, YYYY" or "Month YYYY"
- Sources linked with "View source ->" text
