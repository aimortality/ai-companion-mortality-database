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
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
from validate_data import validate  # noqa: E402

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
CANON = os.path.join(ROOT, "data", "mortality-data.json")

# Pages rendered from templates/. Everything else under src/ is copied through unchanged.
TEMPLATED = {"index.html": "index.html.j2"}
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


def derive(d):
    """Every value a template shows that comes from data. Templates must not compute."""
    return {"meta": d["metadata"]}


def render(ctx):
    env = Environment(
        loader=FileSystemLoader(os.path.join(ROOT, "templates")),
        undefined=StrictUndefined,          # a missing value fails the build; it never renders blank
        autoescape=True,
        keep_trailing_newline=True,
    )
    for out, tpl in TEMPLATED.items():
        html = env.get_template(tpl).render(**ctx)
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
