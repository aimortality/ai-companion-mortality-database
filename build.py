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
import posixpath
import re
from datetime import date
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
from validate_data import validate  # noqa: E402

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markdown_it import MarkdownIt
from markupsafe import Markup
from mdit_py_plugins.anchors import anchors_plugin

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
CANON = os.path.join(ROOT, "data", "mortality-data.json")

# Pages rendered from templates/, all extending base.html.j2. Everything else under src/ is copied through unchanged.
TEMPLATED = {
    "index.html": "index.html.j2",
    "report.html": "report.html.j2",
    "index-academic.html": "index-academic.html.j2",
    "methodology.html": "doc.html.j2",
    "verification-standards.html": "doc.html.j2",
}
# The two pages rendered from Markdown (output file -> repo-relative source). Both use doc.html.j2;
# render_markdown() turns the source into HTML here, in Python, never in the template.
DOC_SOURCES = {
    "methodology.html": "docs/methodology.md",
    "verification-standards.html": "docs/verification-standards.md",
}
# Which nav item is current. Passed to the shared nav partial as page_key.
PAGE_KEYS = {
    "index.html": "index",
    "report.html": "report",
    "index-academic.html": "academic",
    "methodology.html": "methodology",
    "verification-standards.html": "verification-standards",
}
SITE_URL = "https://aimortality.org"
SITE_NAME = "AI Companion Mortality Database"
# Zenodo DOI of the RELEASED version (the concept DOI, 10.5281/zenodo.22062862, always resolves to the
# latest and lives in the footer and README). Bumped by hand in the release checklist (CLAUDE.md
# "Releasing a version", step 3), after Zenodo mints it -- it cannot come from canonical data.
VERSION_DOI = "10.5281/zenodo.22428187"

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
    "verification-standards.html": {
        "title": "Verification Standards \u2014 AI Companion Mortality Database",
        "description": ("Verification standards for the AI Companion Mortality Database: the three evidence tiers "
                        "(juridical, journalistic, preliminary), what qualifies for each, and which are published."),
        "path": "/verification-standards", "og_type": "article", "ld_type": "WebPage",
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


# ── Markdown documents ───────────────────────────────────────────────────────────────────────
# Where a link in a document should point once the document is a page at the site root. The
# Markdown sources stay byte-identical (dist/docs/*.md must be exact copies); links are rewritten
# at render time only.
REPO_URL = "https://gitlab.com/aimortality/ai-companion-mortality-database"
PUBLISHED_ROOTS = ("docs", "data")          # copied whole into dist/ by assemble()
DOC_PAGE_PATHS = {src: "/" + out for out, src in DOC_SOURCES.items()}     # docs/x.md -> /x.html
_SCHEME = re.compile(r"^(?:[a-z][a-z0-9+.\-]*:|//)", re.I)


def rewrite_doc_link(href, doc_dir="docs"):
    """The href a link written in a document under `doc_dir` should have on the built site.

    External, mailto: and #fragment links are untouched. A relative link is resolved against the
    document's own folder, then: another rendered document -> its page; a file under docs/ or
    data/ (published) -> its root-absolute path; any other repository file -> its page on the
    repository host. A link to a file that does not exist raises, so a dead link fails the build."""
    if not href or href.startswith("#") or _SCHEME.match(href):
        return href
    target, hash_, frag = href.partition("#")
    target = target.partition("?")[0]
    repo_path = posixpath.normpath(posixpath.join(doc_dir, target))
    if repo_path.startswith("..") or not os.path.isfile(os.path.join(ROOT, *repo_path.split("/"))):
        raise ValueError(f"link {href!r} in {doc_dir}/ points at no file in the repository")
    if repo_path in DOC_PAGE_PATHS:
        new = DOC_PAGE_PATHS[repo_path]
    elif repo_path.split("/")[0] in PUBLISHED_ROOTS:
        new = "/" + repo_path
    else:
        new = f"{REPO_URL}/-/blob/main/{repo_path}"
    return new + hash_ + frag


def _inline_text(inline):
    return "".join(c.content for c in inline.children if c.type in ("text", "code_inline"))


def render_markdown(rel_path):
    """Render one Markdown document (repo-relative path) to (html, toc). `toc` lists (id, text)
    for each h2. CommonMark plus tables; raw HTML in the source stays disabled. h2/h3 get stable
    ids and a permalink with an accessible name. Linkify is limited to bare e-mail addresses
    (the client-side renderer this replaces autolinked them, and contact@ must stay a link)."""
    md = (MarkdownIt("commonmark", {"html": False, "linkify": True}).enable(["table", "linkify"])
          .use(anchors_plugin, min_level=2, max_level=3, permalink=True))
    md.linkify.set({"fuzzy_link": False, "fuzzy_email": True})
    with open(os.path.join(ROOT, *rel_path.split("/")), encoding="utf-8") as f:
        tokens = md.parse(f.read())
    doc_dir = posixpath.dirname(rel_path)
    toc = []
    for i, tok in enumerate(tokens):
        if tok.type == "heading_open" and tok.tag == "h2":
            toc.append((tok.attrGet("id"), _inline_text(tokens[i + 1]).strip()))
        if tok.type != "inline":
            continue
        for c in tok.children:
            if c.type == "link_open":
                if c.attrGet("class") == "header-anchor":
                    c.attrSet("aria-label", "Link to this section: " + _inline_text(tok).strip())
                else:
                    c.attrSet("href", rewrite_doc_link(c.attrGet("href"), doc_dir))
    return md.renderer.render(tokens, md.options, {}), toc


def doc_context(out):
    html, toc = render_markdown(DOC_SOURCES[out])
    return {"doc_html": Markup(html), "doc_toc": toc, "doc_source": DOC_SOURCES[out]}


def render(ctx):
    env = Environment(
        loader=FileSystemLoader(os.path.join(ROOT, "templates")),
        undefined=StrictUndefined,          # a missing value fails the build; it never renders blank
        autoescape=True,
        keep_trailing_newline=True,
    )
    for out, tpl in TEMPLATED.items():
        extra = doc_context(out) if out in DOC_SOURCES else {}
        html = env.get_template(tpl).render(**ctx, **extra, page_key=PAGE_KEYS[out], page=ctx["pages"][out])
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
