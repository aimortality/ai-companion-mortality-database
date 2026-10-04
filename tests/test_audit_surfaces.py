import importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("audit", os.path.join(HERE, "..", "scripts", "audit-surfaces.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def touch(p, text="<html></html>"):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(text)


def test_site_pages_is_derived_from_dist(tmp_path):
    for rel in ("dist/index.html", "dist/new-page.html", "dist/cases/2023-03-BE-001.html",
                "dist/data/stray.html", "dist/docs/stray.html", "dist/google59ac8b7ece0bfc3a.html",
                "dist/sitemap.xml"):
        touch(tmp_path / rel)
    assert audit.site_pages(str(tmp_path)) == [
        "dist/cases/2023-03-BE-001.html", "dist/index.html", "dist/new-page.html"]


def test_wrong_version_on_a_page_nobody_listed_fails():
    audit.fails.clear()
    E = {"version": "3.5.9", "period_end": "2026-09-28", "period_start": "2023-03-01", "updated": "2026-09-29",
         "relational": 12, "cognitive": 7, "instrumental": 5}
    audit.audit_surface(E, None, "dist/brand-new.html", "<p>Version 3.5.7</p>")
    assert any("3.5.7" in f for f in audit.fails)


def test_headline_presence_only_required_on_headline_surfaces():
    audit.fails.clear()
    E = {"F": 35, "I": 24, "U": 18, "version": "3.5.9", "period_end": "2026-09-28", "period_start": "2023-03-01",
         "updated": "2026-09-29", "relational": 12, "cognitive": 7, "instrumental": 5}
    audit.audit_surface(E, None, "dist/cases/x.html", "<p>no totals here</p>")
    assert audit.fails == []


def test_check_updated_flags_last_updated_but_not_a_documents_own_revision_label():
    E = {"updated": "2026-09-29"}
    audit.fails.clear()
    audit.check_updated(E, "*Last updated: May 30, 2026*", "docs/x.md")
    assert any("May 30, 2026" in f for f in audit.fails)
    audit.fails.clear()
    audit.check_updated(E, "*Standards last revised: May 30, 2026*", "docs/x.md")
    assert audit.fails == []


SITEMAP_PAGE = '<html><head><title>T</title></head></html>'


def _sitemap(urls, lastmod="2026-09-29"):
    body = "".join(f"<url><loc>{u}</loc><lastmod>{lastmod}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>'


def _site(tmp_path, urls, lastmod="2026-09-29", write_sitemap=True):
    touch(tmp_path / "dist/index.html")
    touch(tmp_path / "dist/report.html")
    touch(tmp_path / "dist/404.html")
    if write_sitemap:
        touch(tmp_path / "dist/sitemap.xml", _sitemap(urls, lastmod))
    return str(tmp_path)


GOOD = ["https://aimortality.org/", "https://aimortality.org/report"]
E_SM = {"updated": "2026-09-29"}


def test_check_sitemap_passes_on_a_complete_sitemap(tmp_path):
    audit.fails.clear()
    audit.check_sitemap(E_SM, root=_site(tmp_path, GOOD))
    assert audit.fails == []


def test_check_sitemap_fails_when_missing_incomplete_extra_or_stale(tmp_path):
    for kwargs, needle in (
        ({"urls": GOOD, "write_sitemap": False}, "sitemap.xml"),
        ({"urls": GOOD[:1]}, "/report"),
        ({"urls": GOOD + ["https://aimortality.org/ghost"]}, "ghost"),
        ({"urls": GOOD, "lastmod": "2026-01-01"}, "2026-01-01"),
    ):
        audit.fails.clear()
        sub = tmp_path / needle.strip("/").replace(".", "_")
        audit.check_sitemap(E_SM, root=_site(sub, **kwargs))
        assert any(needle in f for f in audit.fails), (needle, audit.fails)


def _meta_page(url="https://aimortality.org/report", title="<title>T</title>", desc='<meta name="description" content="d">',
               extra=""):
    return (f'<html><head>{title}{desc}<link rel="canonical" href="{url}">'
            f'<meta property="og:title" content="T"><meta property="og:description" content="d">'
            f'<meta property="og:url" content="{url}"><meta name="twitter:card" content="summary">{extra}</head></html>')


def _meta_site(tmp_path, report_html):
    touch(tmp_path / "dist/index.html", _meta_page("https://aimortality.org/"))
    touch(tmp_path / "dist/report.html", report_html)
    return str(tmp_path)


def test_check_meta_passes_on_complete_head(tmp_path):
    audit.fails.clear()
    audit.check_meta({}, root=_meta_site(tmp_path, _meta_page()))
    assert audit.fails == []


def test_check_meta_fails_closed_on_each_missing_or_wrong_tag(tmp_path):
    good = _meta_page()
    broken = {
        "no canonical": good.replace('<link rel="canonical" href="https://aimortality.org/report">', ""),
        "wrong canonical": _meta_page("https://aimortality.org/report.html"),
        "no og:title": good.replace('<meta property="og:title" content="T">', ""),
        "no og:description": good.replace('<meta property="og:description" content="d">', ""),
        "og:url mismatch": good.replace('property="og:url" content="https://aimortality.org/report"',
                                        'property="og:url" content="https://aimortality.org/x"'),
        "no twitter:card": good.replace('<meta name="twitter:card" content="summary">', ""),
        "twitter by property": _meta_page(extra='<meta property="twitter:title" content="T">'),
        "two titles": _meta_page(extra="<title>again</title>"),
        "no title": _meta_page(title=""),
        "empty description": _meta_page(desc='<meta name="description" content="">'),
        "no description": _meta_page(desc=""),
    }
    for label, html in broken.items():
        audit.fails.clear()
        audit.check_meta({}, root=_meta_site(tmp_path / label.replace(" ", "_").replace(":", "_"), html))
        assert audit.fails, f"check_meta passed silently: {label}"


NOINDEX = '<meta name="robots" content="noindex">'


def _noindex_page(extra="", canonical=False):
    """A head like the 404 page's: noindex, no canonical, no og:url; every other tag present."""
    link = '<link rel="canonical" href="https://aimortality.org/report">' if canonical else ""
    return (f'<html><head><title>T</title><meta name="description" content="d">{NOINDEX}{link}'
            f'<meta property="og:title" content="T"><meta property="og:description" content="d">'
            f'<meta name="twitter:card" content="summary">{extra}</head></html>')


def test_check_meta_noindex_page_needs_no_canonical_or_og_url(tmp_path):
    audit.fails.clear()
    audit.check_meta({}, root=_meta_site(tmp_path, _noindex_page()))
    assert audit.fails == []


def test_check_meta_noindex_page_must_not_claim_a_canonical_or_og_url(tmp_path):
    for label, html in {
        "noindex with canonical": _noindex_page(canonical=True),
        "noindex with og:url": _noindex_page(extra='<meta property="og:url" content="https://aimortality.org/report">'),
    }.items():
        audit.fails.clear()
        audit.check_meta({}, root=_meta_site(tmp_path / label.replace(" ", "_").replace(":", "_"), html))
        assert audit.fails, f"check_meta passed silently: {label}"


def test_check_meta_noindex_page_still_needs_title_description_and_twitter_card(tmp_path):
    good = _noindex_page()
    for label, html in {
        "no title": good.replace("<title>T</title>", ""),
        "no description": good.replace('<meta name="description" content="d">', ""),
        "no twitter:card": good.replace('<meta name="twitter:card" content="summary">', ""),
    }.items():
        audit.fails.clear()
        audit.check_meta({}, root=_meta_site(tmp_path / label.replace(" ", "_").replace(":", "_"), html))
        assert audit.fails, f"check_meta passed silently: {label}"


def test_check_meta_indexable_page_without_canonical_still_fails(tmp_path):
    # the carve-out is the robots noindex tag, nothing else: a page that merely lacks a canonical fails
    audit.fails.clear()
    html = _meta_page().replace('<link rel="canonical" href="https://aimortality.org/report">', "")
    audit.check_meta({}, root=_meta_site(tmp_path, html))
    assert any("canonical" in f for f in audit.fails), audit.fails
    audit.fails.clear()
    html = _meta_page(extra='<meta name="robots" content="index, follow">').replace(
        '<link rel="canonical" href="https://aimortality.org/report">', "")
    audit.check_meta({}, root=_meta_site(tmp_path / "index_follow", html))
    assert any("canonical" in f for f in audit.fails), audit.fails


def test_checks_fail_when_there_are_no_pages_to_check(tmp_path):
    # an empty dist/ (build produced nothing, or the path is wrong) must not pass silently
    audit.fails.clear()
    audit.check_meta({}, root=str(tmp_path))
    assert audit.fails, "check_meta passed with no pages"
    audit.fails.clear()
    touch(tmp_path / "dist/sitemap.xml", _sitemap([]))      # a sitemap exists, but no pages do
    audit.check_sitemap(E_SM, root=str(tmp_path))
    assert any("no built pages" in f for f in audit.fails), audit.fails


def test_check_period_matches_the_lowercase_between_form():
    # report.html Conclusions say "...linked to chatbot interactions between March 2023 and <Month YYYY>"
    E = {"period_end": "2026-09-28", "period_start": "2023-03-01"}
    audit.fails.clear()
    audit.check_period(E, "linked to chatbot interactions between March 2023 and May 2024.", "dist/report.html")
    assert any("May 2024" in f for f in audit.fails), audit.fails
    audit.fails.clear()
    audit.check_period(E, "linked to chatbot interactions between March 2023 and September 2026.", "dist/report.html")
    assert audit.fails == []


def test_built_methodology_page_is_a_headline_surface_and_gets_the_through_clause():
    assert "dist/methodology.html" in audit.HEADLINE_SURFACES
    E = {"period_end": "2026-09-28", "period_start": "2023-03-01"}
    audit.fails.clear()
    audit.check_period(E, "We claim only that, through May 2024, no deaths meeting our standards", "dist/methodology.html")
    assert any("May 2024" in f for f in audit.fails), audit.fails
    audit.fails.clear()
    audit.check_period(E, "We claim only that, through September 2026, no deaths meeting our standards", "dist/methodology.html")
    assert audit.fails == []
    audit.fails.clear()    # the clause stays scoped: other pages may say "through <month>, no deaths" of something else
    audit.check_period(E, "between March 2023 and September 2026. Separately: through May 2024, no deaths", "dist/report.html")
    assert audit.fails == []


def _script_site(tmp_path, body):
    touch(tmp_path / "dist/index.html", f"<html><head><title>T</title></head><body>{body}</body></html>")
    return str(tmp_path)


def test_check_inline_scripts_passes_json_ld_and_external_scripts_only(tmp_path):
    audit.fails.clear()
    body = ('<script type="application/ld+json">{"@type": "Dataset"}</script>'
            '<script src="/assets/theme.js" defer></script>'
            '<script async src="https://www.googletagmanager.com/gtag/js?id=X"></script>')
    audit.check_inline_scripts({}, root=_script_site(tmp_path, body))
    assert audit.fails == []


def test_check_inline_scripts_fails_on_an_inline_executable_script(tmp_path):
    for label, body in {
        "bare": "<script>alert(1)</script>",
        "typed javascript": '<script type="text/javascript">alert(1)</script>',
        "module": '<script type="module">import("/x.js")</script>',
        "empty src": "<script src>alert(1)</script>",
    }.items():
        audit.fails.clear()
        audit.check_inline_scripts({}, root=_script_site(tmp_path / label.replace(" ", "_"), body))
        assert audit.fails and "index.html" in audit.fails[0], f"inline script passed silently: {label}"


def test_check_inline_scripts_fails_on_an_inline_event_handler(tmp_path):
    for label, body in {
        "onclick": '<button onclick="x()">go</button>',
        "uppercase": '<a href="/" ONMOUSEOVER="x()">go</a>',
        "onload on body-level tag": '<img src="/a.png" onerror="x()">',
    }.items():
        audit.fails.clear()
        audit.check_inline_scripts({}, root=_script_site(tmp_path / label.replace(" ", "_"), body))
        assert audit.fails and "index.html" in audit.fails[0], f"inline handler passed silently: {label}"


def test_check_inline_scripts_ignores_text_that_only_looks_like_a_handler(tmp_path):
    # prose and attribute VALUES mentioning onclick= are not handler attributes; only a parser can tell
    audit.fails.clear()
    body = '<p>Do not write onclick="x()" in a page.</p><a href="/" title="onload=1" data-note="onerror=2">ok</a>'
    audit.check_inline_scripts({}, root=_script_site(tmp_path, body))
    assert audit.fails == []


def test_check_inline_scripts_fails_when_there_are_no_pages(tmp_path):
    audit.fails.clear()
    audit.check_inline_scripts({}, root=str(tmp_path))
    assert audit.fails, "check_inline_scripts passed with no pages"


# ── close-out: gate holes found by the Track 1 final review ───────────────────────────────────
import subprocess  # noqa: E402
import sys  # noqa: E402

sys.path.insert(0, os.path.join(HERE, ".."))  # for `import build` (REQUIRED_PAGES must track TEMPLATED)


def _reset():
    audit.fails.clear()
    audit.passes.clear()


def test_check_exports_fails_when_the_generator_crashes(monkeypatch):
    # the generator exiting non-zero leaves the files unchanged; that must not read as "exports match"
    _reset()
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(
        a[0], 1, stdout=b"", stderr=b"Traceback ...\nKeyError: 'boom-marker'\n"))
    audit.check_exports()
    assert any("boom-marker" in f for f in audit.fails), audit.fails
    assert not any("match canonical" in p for p in audit.passes), audit.passes


def test_check_exports_passes_when_the_generator_succeeds_and_nothing_drifts(monkeypatch):
    _reset()
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a[0], 0, stdout=b"", stderr=b""))
    audit.check_exports()
    assert audit.fails == [] and any("match canonical" in p for p in audit.passes)


def test_required_pages_equal_the_templated_pages():
    import build
    assert audit.REQUIRED_PAGES == set(build.TEMPLATED), (
        "a page was added to (or removed from) build.TEMPLATED: update REQUIRED_PAGES in audit-surfaces.py too")


def test_check_required_pages_fails_for_each_page_missing_from_dist(tmp_path):
    for name in sorted(audit.REQUIRED_PAGES):
        touch(tmp_path / "dist" / name)
    _reset()
    audit.check_required_pages(root=str(tmp_path))
    assert audit.fails == [] and audit.passes
    (tmp_path / "dist" / "404.html").unlink()
    (tmp_path / "dist" / "report.html").unlink()
    _reset()
    audit.check_required_pages(root=str(tmp_path))
    assert any("404.html" in f for f in audit.fails) and any("report.html" in f for f in audit.fails), audit.fails


E_PER = {"period_end": "2026-09-28", "period_start": "2023-03-01"}


def test_check_period_passes_only_when_a_period_string_was_compared():
    _reset()
    audit.check_period(E_PER, "<p>Period: March 2023 — September 2026</p>", "dist/report.html")
    assert audit.fails == [] and any("agree" in p for p in audit.passes), (audit.fails, audit.passes)
    # a surface that is allowed to have no period string records nothing (no PASS to inflate the count)
    _reset()
    audit.check_period(E_PER, "<p>nothing</p>", "dist/cases/x.html")
    assert audit.fails == [] and audit.passes == []


def test_check_period_fails_a_headline_surface_with_no_period_string():
    for f in sorted(audit.HEADLINE_SURFACES):
        _reset()
        audit.check_period(E_PER, "<p>the register line was reworded</p>", f)
        assert any(f in x and "no coverage-period" in x for x in audit.fails), (f, audit.fails)
        assert audit.passes == []


def _links_site(tmp_path, href, target=None):
    touch(tmp_path / "dist/index.html", f'<html><body><a href="{href}">x</a></body></html>')
    if target:
        touch(tmp_path / target, "x")
    return str(tmp_path)


def test_check_relative_links_passes_inside_dist(tmp_path):
    _reset()
    audit.check_relative_links(root=_links_site(tmp_path, "/data/x.json", "dist/data/x.json"))
    assert audit.fails == [] and audit.passes


def test_check_relative_links_fails_when_a_dotdot_escapes_dist_even_if_the_file_exists(tmp_path):
    # ../data/x.json from dist/index.html resolves to <root>/data/x.json: it exists, but outside dist/
    for href in ("../data/x.json", "/../data/x.json"):
        _reset()
        sub = tmp_path / href.replace("/", "_").replace(".", "-")
        audit.check_relative_links(root=_links_site(sub, href, "data/x.json"))
        assert audit.fails and "x.json" in audit.fails[0], (href, audit.fails)


VERSION_DOI_SRC = 'VERSION_DOI = "10.5281/zenodo.23115481"\n'
CONCEPT = "10.5281/zenodo.22062862"


def _doi_root(tmp_path, build_src=VERSION_DOI_SRC, **page_texts):
    touch(tmp_path / "build.py", build_src)
    touch(tmp_path / "dist/index.html", f"<p>concept {CONCEPT}</p>")
    for rel in audit.MARKDOWN_SURFACES:
        touch(tmp_path / rel, page_texts.get(rel, f"Zenodo. https://doi.org/10.5281/zenodo.23115481 and {CONCEPT}"))
    return str(tmp_path)


def test_check_version_doi_passes_when_every_surface_agrees(tmp_path):
    _reset()
    audit.check_version_doi(root=_doi_root(tmp_path))
    assert audit.fails == [] and any("23115481" in p for p in audit.passes), (audit.fails, audit.passes)


def test_check_version_doi_fails_on_a_stale_doi_naming_surface_and_doi(tmp_path):
    _reset()
    audit.check_version_doi(root=_doi_root(tmp_path, **{"docs/methodology.md": "Zenodo. https://doi.org/10.5281/zenodo.22428187"}))
    assert any("docs/methodology.md" in f and "10.5281/zenodo.22428187" in f for f in audit.fails), audit.fails
    assert not any("README.md" in f for f in audit.fails)


def test_check_version_doi_fails_closed_when_the_constant_cannot_be_parsed(tmp_path):
    for label, src in {"missing": "x = 1\n", "not a doi": 'VERSION_DOI = "TBD"\n',
                       "computed": 'VERSION_DOI = "10.5281/zenodo." + str(n)\n'}.items():
        _reset()
        audit.check_version_doi(root=_doi_root(tmp_path / label.replace(" ", "_"), build_src=src))
        assert any("VERSION_DOI" in f for f in audit.fails), (label, audit.fails)
        assert not any("agree" in p for p in audit.passes)
