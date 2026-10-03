#!/usr/bin/env python3
"""audit-surfaces.py — cross-surface consistency audit for aimortality.org.

Derives every expected value from data/mortality-data.json (never hardcoded),
derives every STALE value from the canonical file at a git base ref, then checks
the surfaces for both. Builds dist/ first (build.py) and checks the BUILT pages --
what ships -- not their sources. Companion to validate_data.py (which checks the
JSON's internal invariants); this checks that the surfaces agree with the JSON.

    python3 scripts/audit-surfaces.py             # base = main
    python3 scripts/audit-surfaces.py --base HEAD~1
    python3 scripts/audit-surfaces.py --links     # also test every external URL
    python3 scripts/audit-surfaces.py --no-build  # audit the existing dist/ (the Netlify gate)

Exit 0 if no FAIL. WARN never fails the run.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = "data/mortality-data.json"
SITE = "dist"  # what ships: build.py output. The audit checks the built site, not its sources.
# Every built page is audited -- derived from dist/, so a new page cannot escape the gate by
# someone forgetting a list. Agreement checks (period, version, updated, pathways, stale values)
# only fail on a WRONG value, so they run on every surface. Presence checks (the headline totals,
# the academic masthead) are page-specific.
EXEMPT_PAGES = {"google59ac8b7ece0bfc3a.html": "Search Console verification stub"}
MARKDOWN_SURFACES = ["README.md", "data/README.md", "docs/methodology.md", "docs/verification-standards.md"]
HEADLINE_SURFACES = {f"{SITE}/index.html", f"{SITE}/index-academic.html", f"{SITE}/report.html",
                     f"{SITE}/methodology.html", "README.md", "docs/methodology.md"}
# The methodology document's zero-deaths sentence ("through <Month YYYY>, no deaths ...") is also a
# coverage statement; both the Markdown source and the page rendered from it are held to it.
THROUGH_SURFACES = {"docs/methodology.md", f"{SITE}/methodology.html"}


def site_pages(root=None):
    """Repo-relative paths of every HTML page the build produced, excluding the data/ and docs/
    publish copies (checked by check_publish_copies) and EXEMPT_PAGES."""
    root = root or ROOT
    site = os.path.join(root, SITE)
    pages = []
    for dirpath, dirnames, files in os.walk(site):
        rel = os.path.relpath(dirpath, site)
        if rel.split(os.sep)[0] in ("data", "docs"):
            dirnames[:] = []
            continue
        for fn in files:
            if fn.endswith(".html") and not (rel == "." and fn in EXEMPT_PAGES):
                pages.append(os.path.normpath(os.path.join(SITE, rel, fn)).replace(os.sep, "/"))
    return sorted(pages)


def surfaces():
    return site_pages() + MARKDOWN_SURFACES
ALIAS = {"wsj": "wall street journal", "nyt": "new york times", "ap": "associated press", "wapo": "washington post"}
# canonical incident name -> the token its report.html header uses, where they differ
CASE_ALIAS = {"University of South Florida double homicide": "USF"}
MARQUEE = ("associated press", " ap ", "reuters", "bbc", "guardian", "new york times", "washington post")

fails, warns, passes = [], [], []


def fail(msg): fails.append(msg)
def warn(msg): warns.append(msg)
def ok(msg): passes.append(msg)


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


def month_long(ymd):
    y, m = int(ymd[:4]), int(ymd[5:7])
    return date(y, m, 1).strftime("%B %Y")          # "August 2026"


def month_short(ymd):
    y, m = int(ymd[:4]), int(ymd[5:7])
    return date(y, m, 1).strftime("%b %Y")          # "Aug 2026"


def day_long(ymd):
    y, m, d = (int(x) for x in ymd.split("-"))
    return f"{date(y, m, d).strftime('%B')} {d}, {y}"  # "August 21, 2026"


def expected(d):
    m, s = d["metadata"], d["statistics"]
    paths = Counter(i["mechanism_type"] for i in d["incidents"])
    known = sum(1 for i in d["incidents"]
                if i.get("interaction_duration") and not re.search(r"unknown|n/a|not applicable", i["interaction_duration"], re.I))
    return {
        "F": m["total_fatalities"], "I": m["total_incidents"], "U": m["ai_users_deceased"],
        "T": m["third_party_victims"], "version": m["version"],
        "updated": m["last_updated"], "period_end": m["time_range"]["end"],
        "period_start": m["time_range"]["start"],
        "relational": paths["relational_pathway"], "cognitive": paths["cognitive_pathway"],
        "instrumental": paths["instrumental_pathway"],
        "duration_known": known,
        "platform_deaths": {p["name"]: p["deaths"] for p in d["platforms"]},
        "minors_pct": s.get("minors_percentage_deaths"), "avg_age": s.get("average_age"),
        "deaths_by_year": s.get("deaths_by_year", {}),
    }


# ── expected / stale derivation ───────────────────────────────────────────
def load_base(ref):
    try:
        out = subprocess.check_output(["git", "show", f"{ref}:{CANON}"], cwd=ROOT, stderr=subprocess.DEVNULL)
        return json.loads(out)
    except subprocess.CalledProcessError:
        return None


# ── checks ────────────────────────────────────────────────────────────────
PERIOD_RE = re.compile(
    r"([Bb]etween March 2023 and|Mar 2023\s?[–\-]\s?|March 2023\s?[–—\-]\s?|Period: March 2023 —|March 2023 to)\s?([A-Z][a-z]+ \d{4})")
PERIOD_THROUGH_RE = re.compile(r"(through)\s?([A-Z][a-z]+ \d{4}), no deaths")
VERSION_RE = re.compile(r"\b[Vv]ersion:?\s?v?(\d+\.\d+(?:\.\d+)?)\b|·\s?v(\d+\.\d+\.\d+)\b|(?<!taxonomy_)version:\s?\"(\d+\.\d+\.\d+)\"")
UPDATED_RE = re.compile(r"(?:last updated|data current as of|database last updated):?\*{0,2}:?\s*([A-Z][a-z]+ \d{1,2}, \d{4})", re.I)
PATHWAY_RE = re.compile(r"\b(relational|cognitive|instrumental)(?: pathway)?(?:</strong>)?:?\s?\(?(\d+)\)?", re.I)


def check_headline(E, text, f):
    for key, label in (("F", "total_fatalities"), ("I", "total_incidents"), ("U", "ai_users_deceased")):
        n = len(re.findall(rf"\b{E[key]}\b", text))
        (ok if n else fail)(f"{f}: {label}={E[key]} present ({n} hits)")


def check_period(E, text, f):
    want = {month_long(E["period_end"]), month_short(E["period_end"])}
    bad = {m.group(2) for m in PERIOD_RE.finditer(text) if m.group(2) not in want}
    if f in THROUGH_SURFACES:  # the zero-deaths claim is also a coverage statement
        bad |= {m.group(2) for m in PERIOD_THROUGH_RE.finditer(text) if m.group(2) not in want}
    if bad:
        fail(f"{f}: coverage-period string(s) {sorted(bad)} ≠ time_range.end {month_long(E['period_end'])}")
    else:
        ok(f"{f}: coverage-period strings agree with time_range.end")
    if f == f"{SITE}/index.html":
        tc = re.search(r'"temporalCoverage":\s*"([0-9/\-]+)"', text)
        want_tc = f"{E['period_start'][:7]}/{E['period_end'][:7]}"
        if tc and tc.group(1) != want_tc:
            fail(f"{f}: JSON-LD temporalCoverage {tc.group(1)} ≠ {want_tc}")


def check_version(E, text, f):
    found = {a or b or c for a, b, c in VERSION_RE.findall(text)}
    found = {v for v in found if v.count(".") >= 1 and not v.startswith(("18.", "19."))}  # React 18 CDN pins
    stale = {v for v in found if v != E["version"]}
    if stale:
        fail(f"{f}: version string(s) {sorted(stale)} ≠ canonical {E['version']}")
    elif found:
        ok(f"{f}: version {E['version']}")


def check_masthead(E, text, f):
    """The academic page's journal-header issue month tracks the coverage period end. The skill
    listed this as caught by the version/updated checks; it was not (neither regex matches it)."""
    m = re.search(r'<header class="journal-header">.*?<span>([A-Z][a-z]+ \d{4})</span>\s*</header>', text, re.S)
    if m is None:
        fail(f"{f}: journal-header masthead month not found")
    elif m.group(1) != month_long(E["period_end"]):
        fail(f"{f}: masthead '{m.group(1)}' ≠ coverage end {month_long(E['period_end'])}")
    else:
        ok(f"{f}: masthead {m.group(1)}")


def check_updated(E, text, f):
    want = day_long(E["updated"])
    found = set(UPDATED_RE.findall(text))
    stale = {v for v in found if v != want}
    if stale:
        fail(f"{f}: last-updated string(s) {sorted(stale)} ≠ canonical {want}")
    elif found:
        ok(f"{f}: last-updated {want}")


def check_pathways(E, text, f):
    seen = {}
    for name, n in PATHWAY_RE.findall(text):
        seen.setdefault(name.lower(), set()).add(int(n))
    for p in ("relational", "cognitive", "instrumental"):
        vals = seen.get(p, set())
        bad = {v for v in vals if v != E[p] and v > 1}   # ignore "cognitive (1 of …)" style
        if bad:
            fail(f"{f}: {p} pathway count(s) {sorted(bad)} ≠ canonical {E[p]}")
    if seen:
        ok(f"{f}: pathway counts checked against canonical {E['relational']}/{E['cognitive']}/{E['instrumental']}")


SITE_URL = "https://aimortality.org"
SITEMAP_EXCLUDED = {f"{SITE}/404.html"}     # an error page is not a destination


def page_url(rel):
    """Canonical URL of a built page (the URL contract in AUDIT.md): dist/index.html -> /,
    dist/x.html -> /x. Extensionless, no trailing slash."""
    path = rel[len(SITE) + 1:] if rel.startswith(SITE + "/") else rel
    path = path[:-len(".html")] if path.endswith(".html") else path
    return SITE_URL + "/" + ("" if path == "index" else path)


def check_sitemap(E, root=None):
    """dist/sitemap.xml exists, lists every built page (minus 404) exactly once and nothing else,
    and every <lastmod> is the canonical last_updated. Fails closed: a missing file is a FAIL."""
    root = root or ROOT
    path = os.path.join(root, SITE, "sitemap.xml")
    if not os.path.exists(path):
        fail(f"{SITE}/sitemap.xml: missing")
        return
    xml = open(path, encoding="utf-8").read()
    locs = re.findall(r"<loc>\s*([^<]*?)\s*</loc>", xml)
    want = {page_url(p) for p in site_pages(root) if p not in SITEMAP_EXCLUDED}
    if not want:
        fail(f"{SITE}/sitemap.xml: no built pages found to check it against (site_pages() is empty)")
        return
    missing, extra = sorted(want - set(locs)), sorted(set(locs) - want)
    dupes = sorted({u for u in locs if locs.count(u) > 1})
    lastmods = re.findall(r"<lastmod>\s*([^<]*?)\s*</lastmod>", xml)
    stale = sorted({m for m in lastmods if m != E["updated"]})
    for label, bad in (("page(s) not listed", missing), ("URL(s) listed that are not built pages", extra),
                       ("URL(s) listed more than once", dupes), (f"<lastmod> value(s) != last_updated {E['updated']}", stale)):
        if bad:
            fail(f"{SITE}/sitemap.xml: {label}: {bad}")
    if len(lastmods) != len(locs):
        fail(f"{SITE}/sitemap.xml: {len(locs)} <loc> but {len(lastmods)} <lastmod>")
    if not (missing or extra or dupes or stale) and locs and len(lastmods) == len(locs):
        ok(f"{SITE}/sitemap.xml: {len(locs)} pages, all lastmod {E['updated']}")
    elif not locs:
        fail(f"{SITE}/sitemap.xml: lists no URLs")


class _Head(HTMLParser):
    """Collects the tags check_meta cares about: <title> count/text, <meta>, <link>."""
    def __init__(self):
        super().__init__()
        self.titles, self.metas, self.links, self._in_title = [], [], [], False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
            self.titles.append("")
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.titles[-1] += data


def check_meta(E, root=None):
    """Every built page carries the shared head metadata: one <title>, one canonical equal to its
    expected URL, og:title / og:description / og:url (= canonical), twitter:card by name=, and a
    non-empty description. No twitter:* by property=. Fails closed on any absence."""
    root = root or ROOT
    pages = site_pages(root)
    if not pages:
        fail(f"{SITE}/: no built pages found to check for head metadata (site_pages() is empty)")
        return
    for f in pages:
        h = _Head()
        h.feed(open(os.path.join(root, f), encoding="utf-8").read())
        want, problems = page_url(f), []

        def meta(key, attr):
            return [m.get("content", "") for m in h.metas if m.get(attr) == key]

        if len(h.titles) != 1 or not h.titles[0].strip():
            problems.append(f"{len(h.titles)} <title> (need exactly one, non-empty)")
        canon = [l.get("href") for l in h.links if l.get("rel") == "canonical"]
        if canon != [want]:
            problems.append(f"canonical {canon} != [{want!r}]")
        for prop in ("og:title", "og:description"):
            if len([c for c in meta(prop, "property") if c.strip()]) != 1:
                problems.append(f"{prop} missing or empty")
        if meta("og:url", "property") != [want]:
            problems.append(f"og:url {meta('og:url', 'property')} != [{want!r}]")
        if len(meta("twitter:card", "name")) != 1:
            problems.append('name="twitter:card" missing')
        if len([c for c in meta("description", "name") if c.strip()]) != 1:
            problems.append("description missing or empty")
        if any(str(m.get("property", "")).startswith("twitter:") for m in h.metas):
            problems.append('twitter:* tag uses property= (must be name=)')
        if problems:
            for p in problems:
                fail(f"{f}: {p}")
        else:
            ok(f"{f}: title, canonical, og, twitter, description present")


class _Scripts(HTMLParser):
    """Collects what check_inline_scripts cares about: <script> elements with no src (and their
    type), and any attribute named on*= (an inline event handler) on any element."""
    def __init__(self):
        super().__init__()
        self.inline_scripts, self.handlers = [], []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): v for k, v in attrs}
        if tag == "script" and not a.get("src"):
            self.inline_scripts.append((a.get("type") or "").strip().lower())
        for name in a:
            if name.startswith("on"):
                self.handlers.append(f"<{tag} {name}=...>")


def check_inline_scripts(E, root=None):
    """The Content-Security-Policy in netlify.toml has no 'unsafe-inline' in script-src, so a page
    that carries an inline executable script or an inline event handler would break in the browser.
    Every <script> without a src must be a type="application/ld+json" data block (never executed),
    and no element may have an on*= attribute. Fails closed on an empty page list."""
    root = root or ROOT
    pages = site_pages(root)
    if not pages:
        fail(f"{SITE}/: no built pages found to check for inline scripts (site_pages() is empty)")
        return
    for f in pages:
        p = _Scripts()
        p.feed(open(os.path.join(root, f), encoding="utf-8").read())
        bad = [t for t in p.inline_scripts if t != "application/ld+json"]
        for t in bad:
            fail(f"{f}: inline <script> (type={t or 'none'!r}) -- move it to a file under src/assets/; the CSP forbids it")
        for h in p.handlers:
            fail(f"{f}: inline event handler {h} -- attach it from a script file; the CSP forbids it")
        if not bad and not p.handlers:
            ok(f"{f}: no inline scripts or event handlers (JSON-LD data blocks only)")


def check_duration_statements(E):
    """Any "Duration known for N of M cases" statement, on any surface, must match canonical.

    The index page's charts -- age distribution, engagement duration, platform bars, timeline,
    cumulative -- and its duration and statistics tables were removed 2026-09-29 (maintainer's
    decision: take every visualization off the front page and reintroduce them only as generated
    output). Their chart checks went with them. When a generated chart returns, its check returns
    with it, reading the rendered page.
    """
    want = f"Duration known for {E['duration_known']} of {E['I']} cases"
    found = {}
    for f in surfaces():
        for h in re.findall(r"Duration known for \d+ of \d+ cases", read(f)):
            found.setdefault(h, []).append(f)
    bad = {h: fs for h, fs in found.items() if h != want}
    if bad:
        fail(f"duration statement(s) disagree with canonical '{want}': {bad}")
    else:
        ok(f"duration statements: {sum(len(v) for v in found.values())} found, all match canonical")


def check_stale(E, B, text, f):
    """Old values that changed between base and canonical must not survive in surfaces."""
    if not B:
        return
    probes = []
    if B["updated"] != E["updated"]:
        probes.append(day_long(B["updated"]))
    if B["version"] != E["version"]:
        probes.append(f"v{B['version']}")
        probes.append(f"Version: {B['version']}")
    if B["period_end"][:7] != E["period_end"][:7]:
        for form in (f"and {month_long(B['period_end'])}", f"to {month_long(B['period_end'])}",
                     f"— {month_long(B['period_end'])}", f"–{month_short(B['period_end'])}", f"- {month_short(B['period_end'])}"):
            probes.append(form)
    if B["F"] != E["F"]:
        probes += [f"{B['F']} fatalities", f"{B['F']} total fatalities", f"{B['F']} deaths", f"All {B['F']} Fatalities"]
    if B["I"] != E["I"]:
        probes += [f"{B['I']} incidents", f"of {B['I']} cases"]
    if B["U"] != E["U"]:
        probes += [f"{B['U']} AI users", f"{B['U']} users"]
    for p in ("relational", "cognitive", "instrumental"):
        if B[p] != E[p]:
            probes += [f"{p} ({B[p]}", f"{p.capitalize()} pathway</strong>: {B[p]}"]
    for name, n in B["platform_deaths"].items():
        if E["platform_deaths"].get(name) != n:
            probes += [f"{name}: {n} user deaths", f"deaths: {n}, type"]
    hits = []
    for p in probes:
        for ln, line in enumerate(text.splitlines(), 1):
            if p not in line or re.search(r"v3\.\d\.0\)|corrected|raised from|prior count|added in v|promoted |first captured ", line):
                continue
            # A dated status snapshot ("no ruling located as of September 5, 2026") is history, not a stale
            # value. It shares the release date by construction, because a release checks dockets that day.
            # "Data current as of" is a last-updated form and is still checked.
            if all(re.search(r"(?<!data current )\bas of\s*$", line[:i], re.I)
                   for i in [m.start() for m in re.finditer(re.escape(p), line)]):
                continue
            hits.append(f"  L{ln}: '{p}' → {line.strip()[:110]}")
    if hits:
        fail(f"{f}: stale pre-change value(s) survive:\n" + "\n".join(hits))
    else:
        ok(f"{f}: no stale pre-change values ({len(probes)} probes)")


def check_sources(d):
    """report.html 'Verification Sources' lines vs canonical sources arrays."""
    f = f"{SITE}/report.html"
    text = read(f)
    sections = re.split(r"<h3[^>]*>CASE #\d+: ", text)[1:]
    by_name = {}
    for sec in sections:
        title = re.sub(r"<.*?>", "", sec.split("\n", 1)[0]).strip()
        m = re.search(r"<strong>Verification Sources</strong>:\s*(.+?)</p>", sec, re.S)
        if m:
            by_name[title] = re.sub(r"<.*?>", "", m.group(1))
    def norm(s):
        s = re.sub(r"\(.*?\)", "", s).lower()
        return re.sub(r"[^a-z0-9]+", " ", s).strip()
    checked, unmatched = 0, []
    for inc in d["incidents"]:
        name = inc.get("name", "")
        needle = CASE_ALIAS.get(name, name.split(" (")[0]).lower()
        toks = needle.split()
        key = next((t for t in by_name if all(tok in t.lower() for tok in toks)), None)
        if not key:
            unmatched.append(name)
            continue
        checked += 1
        canon = [norm(s) for s in inc["sources"]]
        rendered = [norm(s) for s in by_name[key].split(";") if s.strip()]
        rendered = [r for r in rendered if not re.search(r"confirmed by|sweep|verified|retrieved|order|\b(19|20)\d\d\b|independent outlets|perp", r)]
        rendered = [ALIAS.get(r, r) for r in rendered]
        extra = [r for r in rendered if r and not any(r in c or c in r for c in canon)]
        marquee = [r for r in extra if any(m.strip() in f" {r} " for m in MARQUEE)]
        if marquee:
            fail(f"{f}: '{name}' cites marquee outlet(s) NOT in canonical sources: {marquee}")
        elif extra:
            warn(f"{f}: '{name}' rendered outlets not matched to canonical (check wording): {extra[:4]}")
    expected = d["metadata"]["total_incidents"]
    if len(sections) < expected or checked < expected:
        fail(f"{f}: source attribution compared {checked} of {expected} incidents "
             f"({len(sections)} case sections found); unmatched: {unmatched or 'none'} — "
             f"fix the header or add a CASE_ALIAS entry")
    else:
        ok(f"{f}: source attribution compared for {checked} of {len(sections)} case sections")


def check_exports():
    """Derived exports must equal what build-data-exports.py would generate from canonical now."""
    targets = ["data/platform-analysis.csv", "data/incidents.csv", "data/timeline.json"]
    before = {t: open(os.path.join(ROOT, t), "rb").read() for t in targets}
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts/build-data-exports.py")], capture_output=True)
    after = {t: open(os.path.join(ROOT, t), "rb").read() for t in targets}
    stale = [t for t in targets if before[t] != after[t]]
    for t in targets:  # never leave the working tree modified by an audit
        if before[t] != after[t]:
            open(os.path.join(ROOT, t), "wb").write(before[t])
    if stale:
        fail("derived exports stale vs canonical — run scripts/build-data-exports.py: " + ", ".join(stale))
    else:
        ok("derived exports (platform-analysis.csv, incidents.csv, timeline.json) match canonical")


def check_relative_links():
    """Every relative href/src in the built pages must resolve inside the built site (dist/),
    which contains data/ and docs/ -- so a link to a file the build did not produce fails."""
    import glob
    missing = []
    for f in site_pages():
        text = read(f)
        for u in re.findall(r"""(?:href|src)[=:]\s?["']([^"']+)["']""", text):
            u = u.split("#")[0].split("?")[0]
            if not u or u.startswith(("http", "mailto:", "tel:", "data:")) or u == "/":
                continue
            base = os.path.dirname(f) if not u.startswith("/") else SITE
            path = os.path.normpath(os.path.join(ROOT, base, u.lstrip("/")))
            if not os.path.exists(path):
                missing.append(f"{f} -> {u}")
    if missing:
        fail("relative links to nonexistent files: " + "; ".join(sorted(set(missing))))
    else:
        ok("relative links in served pages all resolve")


def check_publish_copies():
    """dist/data and dist/docs are the build's copies of data/ and docs/, and they are what
    ships. They must exist and be exact and un-nested (`cp -r data X` onto an existing X copies
    INTO it, leaving the stale file at the top level -- the failure this check was written for)."""
    problems = []
    for src_dir, pub_dir in (("data", f"{SITE}/data"), ("docs", f"{SITE}/docs")):
        pub = os.path.join(ROOT, pub_dir)
        if not os.path.isdir(pub):
            problems.append(f"{pub_dir}/ missing from the build")
            continue
        if os.path.isdir(os.path.join(pub, src_dir)):
            problems.append(f"{pub_dir}/{src_dir}/ exists (nested copy)")
        for base, other, label in ((os.path.join(ROOT, src_dir), pub, "missing from"),
                                   (pub, os.path.join(ROOT, src_dir), "not in source, still in")):
            for dirpath, _, files in os.walk(base):
                if os.path.relpath(dirpath, base).split(os.sep)[0] == src_dir and base == pub:
                    continue  # the nested copy is reported once above
                for fn in files:
                    if fn == ".DS_Store":
                        continue
                    rel = os.path.relpath(os.path.join(dirpath, fn), base)
                    twin = os.path.join(other, rel)
                    if not os.path.exists(twin):
                        problems.append(f"{rel} {label} {pub_dir}")
                    elif base != pub and open(os.path.join(dirpath, fn), "rb").read() != open(twin, "rb").read():
                        problems.append(f"{pub_dir}/{rel} is stale vs {src_dir}/{rel}")
    if problems:
        fail("publish copies would ship stale data -- rebuild with the netlify.toml command: "
             + "; ".join(sorted(set(problems))[:8]))
    else:
        ok(f"publish copies ({SITE}/data, {SITE}/docs) exact")


def check_links():
    import concurrent.futures
    urls = set()
    for f in site_pages() + MARKDOWN_SURFACES:
        for u in re.findall(r"https?://[^\"'<>)\s`]+", read(f)):
            if not re.search(r"img\.shields\.io|aimortality\.org|creativecommons\.org|schema\.org|googletagmanager|github\.com/aimortality|w3\.org|sitemaps\.org", u):
                urls.add(u.rstrip(".,;"))
    def probe(u):
        ua = ["-A", "Mozilla/5.0 (link-checker)"]
        code = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L", "--max-time", "25", *ua, "--head", u],
                              capture_output=True, text=True).stdout
        if code in ("403", "405", "000"):
            code = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L", "--max-time", "25", *ua, "-r", "0-1024", u],
                                  capture_output=True, text=True).stdout
        return code, u
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        results = list(ex.map(probe, sorted(urls)))
    broken = [(c, u) for c, u in results if not c.startswith("2")]
    if broken:
        fail("broken URLs:\n" + "\n".join(f"  {c}  {u}" for c, u in broken))
    ok(f"links: {len(results) - len(broken)}/{len(results)} external URLs 2xx")


def audit_surface(E, B, f, text):
    if f in HEADLINE_SURFACES:
        check_headline(E, text, f)
    check_period(E, text, f)
    check_version(E, text, f)
    check_updated(E, text, f)
    check_pathways(E, text, f)
    check_stale(E, B, text, f)
    if f.endswith("index-academic.html"):
        check_masthead(E, text, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="main", help="git ref whose canonical JSON supplies the STALE values (default: main)")
    ap.add_argument("--links", action="store_true", help="also test every external URL")
    ap.add_argument("--no-build", action="store_true", help="audit the existing dist/ instead of rebuilding it first")
    args = ap.parse_args()

    if not args.no_build:
        r = subprocess.run([sys.executable, os.path.join(ROOT, "build.py")], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout + r.stderr + "\n  FAIL  build.py failed -- nothing to audit")
            sys.exit(1)
    if not os.path.isdir(os.path.join(ROOT, SITE)):
        print(f"  FAIL  {SITE}/ does not exist -- run build.py or drop --no-build")
        sys.exit(1)

    d = json.loads(read(CANON))
    E = expected(d)
    base = load_base(args.base)
    B = expected(base) if base else None
    print(f"canonical: {E['F']} fatalities / {E['I']} incidents / {E['U']} users / {E['T']} third-party · "
          f"v{E['version']} · updated {E['updated']} · period → {month_long(E['period_end'])} · "
          f"pathways {E['relational']}/{E['cognitive']}/{E['instrumental']}")
    if B:
        print(f"base {args.base}: {B['F']}/{B['I']}/{B['U']} v{B['version']} updated {B['updated']} period → {month_long(B['period_end'])}")
    else:
        print(f"base {args.base}: not readable — stale-value probes skipped")

    for f in surfaces():
        audit_surface(E, B, f, read(f))
    check_duration_statements(E)
    check_sources(d)
    check_exports()
    check_relative_links()
    check_publish_copies()
    check_sitemap(E)
    check_meta(E)
    check_inline_scripts(E)
    if args.links:
        check_links()

    for p in passes: print(f"  PASS  {p}")
    for w in warns: print(f"  WARN  {w}")
    for x in fails: print(f"  FAIL  {x}")
    print(f"\n{len(passes)} passed · {len(warns)} warnings · {len(fails)} failures")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
