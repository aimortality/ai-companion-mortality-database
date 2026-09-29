#!/usr/bin/env python3
"""Render-equivalence oracle: do two HTML documents show a reader the same thing?

Used to prove a no-op migration: the browser-rendered DOM of the old page (captured once)
against the build's static output. Compares element structure, significant attributes, and
whitespace-collapsed text. Ignores what a reader never sees: <script> bodies (analytics inject
tags at runtime), attributes set at runtime by the theme script, and whitespace-only text nodes.
<style> is compared as a separate, exact block.

  python3 scripts/compare_rendered.py OLD.html NEW.html [--section app]

Exit 0 when equivalent; exit 1 with a unified diff of the first differences otherwise.
"""
import argparse
import difflib
import re
import sys
from html.parser import HTMLParser

SKIP = {"script", "noscript"}
# HTML void elements have no end tag; "<meta ... />" and "<meta>" are the same element
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
RUNTIME_ATTRS = {("html", "data-theme"), ("button", "aria-pressed")}


PRETTY = False  # --pretty-urls: Netlify rewrites internal "page.html" links to "/page" at deploy time


def norm_attr(k, v):
    if v is None:
        return ""
    if PRETTY and k == "href" and not re.match(r"[a-z]+:|//|#", v):
        v = re.sub(r"^/", "", v)
        v = re.sub(r"^([^?#]*?)\.html(?=$|[?#])", r"\1", v)
    if k == "style":
        return ";".join(p.strip() for p in v.split(";") if p.strip())
    return " ".join(v.split())


class Norm(HTMLParser):
    def __init__(self, section=None):
        super().__init__(convert_charrefs=True)
        self.nodes, self.styles = [], []
        self.skip = self.in_style = 0
        self.section, self.depth, self.inside = section, 0, section is None

    def _emit(self, s):
        if self.inside and not self.skip:
            self.nodes.append(s)

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
            return
        if tag == "style":
            self.in_style += 1
            return
        if self.section and not self.inside and dict(attrs).get("id") == self.section:
            self.inside, self.depth = True, 0
        if self.inside:
            self.depth += 1
        a = sorted((k, norm_attr(k, v)) for k, v in attrs if (tag, k) not in RUNTIME_ATTRS)
        self._emit(f"<{tag}" + "".join(f' {k}="{v}"' for k, v in a) + ">")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in SKIP:
            self.skip -= 1
            return
        if tag == "style":
            self.in_style -= 1
            return
        self._emit(f"</{tag}>")
        if self.section and self.inside:
            self.depth -= 1
            if self.depth == 0:
                self.inside = False

    def handle_data(self, d):
        if self.in_style:
            self.styles.append(d.strip())
            return
        t = " ".join(d.split())
        if t:
            self._emit("T:" + t)


def normalize(path, section=None):
    p = Norm(section)
    p.feed(open(path, encoding="utf-8").read())
    return p.nodes, "\n".join(p.styles)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--section", help="compare only the element with this id (and its subtree)")
    ap.add_argument("--pretty-urls", action="store_true",
                    help="compare internal links as Netlify serves them (page.html == /page); use when one side is pre-deploy")
    ap.add_argument("--context", type=int, default=3)
    ap.add_argument("--max", type=int, default=60, help="max diff lines to print")
    a = ap.parse_args()
    global PRETTY
    PRETTY = a.pretty_urls
    old_nodes, old_css = normalize(a.old, a.section)
    new_nodes, new_css = normalize(a.new, a.section)
    ok = True
    if old_css != new_css and not a.section:
        ok = False
        print("STYLE differs:")
        d = list(difflib.unified_diff(old_css.splitlines(), new_css.splitlines(), "old", "new", lineterm="", n=1))
        print("\n".join(d[: a.max]))
    if old_nodes != new_nodes:
        ok = False
        sm = difflib.SequenceMatcher(None, old_nodes, new_nodes, autojunk=False)
        changes = [op for op in sm.get_opcodes() if op[0] != "equal"]
        print(f"DOM differs: {len(changes)} change region(s); {len(old_nodes)} vs {len(new_nodes)} nodes")
        d = list(difflib.unified_diff(old_nodes, new_nodes, "old", "new", lineterm="", n=a.context))
        print("\n".join(d[: a.max]))
        if len(d) > a.max:
            print(f"... {len(d) - a.max} more diff lines")
    if ok:
        print(f"EQUIVALENT: {len(old_nodes)} nodes, styles identical" + (f" (section #{a.section})" if a.section else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
