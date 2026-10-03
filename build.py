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


def derive(d):
    """Every value a template shows that comes from data. Templates must not compute.
    Date formats match scripts/audit-surfaces.py, which checks the rendered strings -- so a
    formatting drift between the two fails the audit rather than shipping."""
    m = d["metadata"]
    start, end = m["time_range"]["start"], m["time_range"]["end"]
    return {
        "meta": m,
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
        html = env.get_template(tpl).render(**ctx, page_key=PAGE_KEYS[out])
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


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    ctx = derive(load())
    render(ctx)
    assemble()
    print(f"built dist/: {sum(len(f) for _, _, f in os.walk(DIST))} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
