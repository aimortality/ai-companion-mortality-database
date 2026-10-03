#!/usr/bin/env python3
"""Build aimortality.org into dist/ from canonical data and templates.

  python3 build.py

Stages: load (validate canonical) -> derive (every computed value) -> render (templates only
interpolate; they do no arithmetic) -> assemble (static pages, data/, docs/). The output is a
deterministic function of the repository: running it twice produces byte-identical files.

dist/ is build output. Never hand-edit it -- change the template or the data and rebuild.
"""
import json
import os
from datetime import date
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
from validate_data import validate  # noqa: E402

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
CANON = os.path.join(ROOT, "data", "mortality-data.json")

# Pages rendered from templates/, all extending base.html.j2. Everything else under src/ is copied through unchanged.
TEMPLATED = {
    "index.html": "index.html.j2",
    "report.html": "report.html.j2",
    "index-academic.html": "index-academic.html.j2",
    "methodology.html": "methodology.html.j2",
}
# Which nav item is current. Passed to the shared nav partial as page_key.
PAGE_KEYS = {
    "index.html": "index",
    "report.html": "report",
    "index-academic.html": "academic",
    "methodology.html": "methodology",
}
SITE_URL = "https://aimortality.org"
SITE_NAME = "AI Companion Mortality Database"
# Zenodo DOI of the RELEASED version (the concept DOI, 10.5281/zenodo.22062862, always resolves to the
# latest and lives in the footer and README). Bumped by hand in the release checklist (CLAUDE.md
# "Releasing a version", step 3), after Zenodo mints it -- it cannot come from canonical data.
VERSION_DOI = "10.5281/zenodo.23115481"

# Per-page head metadata, keyed by output file. `path` is the canonical, extensionless URL path
# (Netlify Pretty URLs serves /report for report.html; "/" for the index). `description` is a
# str.format template: every number, the coverage period and the version come from canonical via
# derive(); nothing here is a figure. `ld_type` Dataset = the index carries its own full block.
PAGES_META = {
    "index.html": {
        "title": "AI Companion Mortality Database",
        "description": ("Public database documenting deaths where AI chatbot interaction was alleged as a "
                        "contributing factor. {fatalities} fatalities ({users} AI users + {third_party} "
                        "third-party victims) across {incidents} incidents from {period_start} to {period_end}."),
        "path": "/", "og_type": "website", "ld_type": "Dataset",
    },
    "report.html": {
        "title": "AI Companion Mortality Database - Complete Research Report",
        "description": ("Complete research report: {fatalities} documented deaths across {incidents} incidents "
                        "({period_start} - {period_end}) in which AI chatbot interaction was alleged as a "
                        "contributing factor, with case narratives, legal proceedings, and verification sources."),
        "path": "/report", "og_type": "article", "ld_type": "Article",
    },
    "index-academic.html": {
        "title": "AI Companion Mortality Database: A Systematic Documentation of Deaths Associated with "
                 "Conversational AI Systems",
        "description": ("Academic summary of the AI Companion Mortality Database: {fatalities} documented deaths "
                        "across {incidents} incidents ({period_start} - {period_end}), verification methodology, "
                        "and tabulated case data. Version {version}, DOI {version_doi}."),
        "path": "/index-academic", "og_type": "article", "ld_type": "Article",
    },
    "methodology.html": {
        "title": "Methodology \u2014 AI Companion Mortality Database",
        "description": ("Methodology and verification standards for the AI Companion Mortality Database: scope, "
                        "incident definition, causal pathways, evidence tiers, ethical commitments, and limitations."),
        "path": "/methodology", "og_type": "article", "ld_type": "WebPage",
    },
}
IGNORE = shutil.ignore_patterns(".DS_Store")


def load():
    """Read canonical and refuse to build from data that fails validation."""
    with open(CANON, encoding="utf-8") as f:
        d = json.load(f)
    _, warns, errors = validate(d)
    for w in warns:
        print(f"  WARN  {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"  FAIL  {e}", file=sys.stderr)
        raise SystemExit(f"build.py: canonical data failed validation ({len(errors)} error(s)); nothing built")
    return d


def month_long(ymd):
    return date(int(ymd[:4]), int(ymd[5:7]), 1).strftime("%B %Y")     # "September 2026"


def month_short(ymd):
    return date(int(ymd[:4]), int(ymd[5:7]), 1).strftime("%b %Y")     # "Sep 2026"


def day_long(ymd):
    y, m, dd = (int(x) for x in ymd.split("-"))
    return f"{date(y, m, dd).strftime('%B')} {dd}, {y}"                 # "September 29, 2026"


def page_meta(out, fields, updated_iso):
    """One page's resolved head metadata: the PAGES_META entry with its description filled from
    canonical-derived `fields`, its absolute URL, and (for non-index pages) its JSON-LD."""
    m = PAGES_META[out]
    url = SITE_URL + m["path"]
    title = m["title"]
    page = {"title": title, "description": m["description"].format(**fields), "url": url,
            "og_type": m["og_type"], "ld_type": m["ld_type"], "json_ld": None}
    if m["ld_type"] != "Dataset":      # the index keeps its own full Dataset block in its head
        page["json_ld"] = {
            "@context": "https://schema.org",
            "@type": m["ld_type"],
            "headline": title,
            "url": url,
            "dateModified": updated_iso,
            "isPartOf": {"@type": "Dataset", "name": SITE_NAME, "url": SITE_URL + "/"},
            "author": {"@type": "Person", "name": "Hunter Karman"},
        }
    return page


def derive(d):
    """Every value a template shows that comes from data. Templates must not compute.
    Date formats match scripts/audit-surfaces.py, which checks the rendered strings -- so a
    formatting drift between the two fails the audit rather than shipping."""
    m = d["metadata"]
    start, end = m["time_range"]["start"], m["time_range"]["end"]
    fields = {
        "fatalities": m["total_fatalities"], "users": m["ai_users_deceased"],
        "third_party": m["third_party_victims"], "incidents": m["total_incidents"],
        "version": m["version"], "version_doi": VERSION_DOI,
        "period_start": month_long(start), "period_end": month_long(end),
    }
    return {
        "meta": m,
        "version_doi": VERSION_DOI,
        "site_name": SITE_NAME,
        "pages": {out: page_meta(out, fields, m["last_updated"]) for out in PAGES_META},
        "updated_long": day_long(m["last_updated"]),
        "updated_iso": m["last_updated"],
        "period_start_long": month_long(start),
        "period_start_short": month_short(start),
        "period_end_long": month_long(end),
        "period_end_short": month_short(end),
        "temporal_coverage": f"{start[:7]}/{end[:7]}",
    }


def render(ctx):
    env = Environment(
        loader=FileSystemLoader(os.path.join(ROOT, "templates")),
        undefined=StrictUndefined,          # a missing value fails the build; it never renders blank
        autoescape=True,
        keep_trailing_newline=True,
    )
    for out, tpl in TEMPLATED.items():
        html = env.get_template(tpl).render(**ctx, page_key=PAGE_KEYS[out], page=ctx["pages"][out])
        with open(os.path.join(DIST, out), "w", encoding="utf-8", newline="\n") as f:
            f.write(html)


def assemble():
    src = os.path.join(ROOT, "src")
    for name in sorted(os.listdir(src)):
        if name in TEMPLATED or name in ("data", "docs") or name == ".DS_Store":
            continue
        p = os.path.join(src, name)
        (shutil.copytree(p, os.path.join(DIST, name), ignore=IGNORE) if os.path.isdir(p)
         else shutil.copy2(p, os.path.join(DIST, name)))
    for sub in ("data", "docs"):
        shutil.copytree(os.path.join(ROOT, sub), os.path.join(DIST, sub), ignore=IGNORE)


def sitemap_url(out):
    return SITE_URL + PAGES_META[out]["path"]


def write_sitemap(pages, lastmod):
    """dist/sitemap.xml: one <url> per page in `pages` (output file names), every <lastmod> the
    canonical last_updated. Generated, so it cannot drift from the pages or the data."""
    rows = "".join(f"  <url><loc>{sitemap_url(p)}</loc><lastmod>{lastmod}</lastmod></url>\n" for p in pages)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>\n')
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    ctx = derive(load())
    render(ctx)
    assemble()
    # 404.html (not built yet) is a page, not a destination: it never belongs in the sitemap.
    write_sitemap([p for p in sorted(TEMPLATED) if p != "404.html"], ctx["updated_iso"])
    print(f"built dist/: {sum(len(f) for _, _, f in os.walk(DIST))} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
