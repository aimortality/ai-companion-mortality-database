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
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = "data/mortality-data.json"
SITE = "dist"  # what ships: build.py output. The audit checks the built site, not its sources.
SURFACES = [
    f"{SITE}/index.html",
    f"{SITE}/index-academic.html",
    f"{SITE}/report.html",
    "README.md",
    "docs/methodology.md",
]
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
    r"(Between March 2023 and|Mar 2023\s?[–\-]\s?|Period: March 2023 —|March 2023 to)\s?([A-Z][a-z]+ \d{4})")
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
    if f == "docs/methodology.md":  # the zero-deaths claim is also a coverage statement
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


def rendered_desc(text, did):
    m = re.search(r'<desc id="' + did + r'">(.*?)</desc>', text, re.S)
    return html.unescape(m.group(1)) if m else None


def check_index_charts(E, d, text):
    """Checks the RENDERED page: what a reader and a screen reader actually get. A chart whose
    <desc> is missing FAILS -- removing a chart must come with an edit here, so it is explicit."""
    f = f"{SITE}/index.html"
    # age distribution: the <desc> bucket counts must sum to total fatalities, and its minors
    # count must equal canonical's victims_by_age_group.minors
    desc = rendered_desc(text, "age-dist-desc")
    if desc is None:
        fail(f"{f}: age-dist <desc> not found")
    else:
        counts = [int(c) for c in re.findall(r"\((\d+) people\)", desc)]
        (ok if counts and sum(counts) == E["F"] else fail)(
            f"{f}: age-dist <desc> buckets {counts} sum={sum(counts)} vs fatalities {E['F']}")
        minors = re.search(r"minors[^()]*\((\d+) people\)", desc)
        want_minors = d["statistics"]["victims_by_age_group"]["minors"]
        (ok if minors and int(minors.group(1)) == want_minors else fail)(
            f"{f}: age-dist <desc> minors={minors.group(1) if minors else 'absent'} vs canonical {want_minors}")
    # duration denominator: desc, caption, note must all agree with canonical
    want = f"Duration known for {E['duration_known']} of {E['I']} cases"
    hits = set(re.findall(r"Duration known for \d+ of \d+ cases", text))
    (ok if hits == {want} else fail)(f"{f}: duration strings {sorted(hits)} vs canonical '{want}'")
    # platform chart: the <desc> must state canonical's ChatGPT user deaths
    desc = rendered_desc(text, "platform-desc")
    want = E["platform_deaths"].get("ChatGPT")
    if desc is None:
        fail(f"{f}: platform <desc> not found")
    else:
        m = re.search(r"ChatGPT: (\d+) user deaths", desc)
        (ok if m and int(m.group(1)) == want else fail)(
            f"{f}: platform <desc> ChatGPT={m.group(1) if m else 'absent'} vs canonical {want}")


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
            if p in line and not re.search(r"v3\.\d\.0\)|corrected|raised from|prior count|added in v|promoted |first captured ", line):
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
    for f in (f"{SITE}/index.html", f"{SITE}/report.html", f"{SITE}/index-academic.html", f"{SITE}/methodology.html"):
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
    for f in (f"{SITE}/index.html", f"{SITE}/report.html", f"{SITE}/index-academic.html", "README.md"):
        for u in re.findall(r"https?://[^\"'<>)\s`]+", read(f)):
            if not re.search(r"img\.shields\.io|esm\.sh|aimortality\.org|creativecommons\.org|schema\.org|googletagmanager|github\.com/aimortality|w3\.org|sitemaps\.org", u):
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

    for f in SURFACES:
        text = read(f)
        check_headline(E, text, f)
        check_period(E, text, f)
        check_version(E, text, f)
        check_updated(E, text, f)
        check_pathways(E, text, f)
        check_stale(E, B, text, f)
    check_index_charts(E, d, read(f"{SITE}/index.html"))
    check_sources(d)
    check_exports()
    check_relative_links()
    check_publish_copies()
    if args.links:
        check_links()

    for p in passes: print(f"  PASS  {p}")
    for w in warns: print(f"  WARN  {w}")
    for x in fails: print(f"  FAIL  {x}")
    print(f"\n{len(passes)} passed · {len(warns)} warnings · {len(fails)} failures")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
