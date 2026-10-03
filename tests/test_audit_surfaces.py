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
    audit.check_period(E, "through May 2024, no deaths", "dist/report.html")
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
