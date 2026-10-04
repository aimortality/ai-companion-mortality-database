import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)  # later tests in this file `import build` directly

import build  # noqa: E402


def test_every_page_is_templated_and_extends_base():
    assert set(build.TEMPLATED) == {"index.html", "report.html", "index-academic.html", "methodology.html",
                                    "verification-standards.html", "404.html"}
    for tpl in build.TEMPLATED.values():
        with open(os.path.join(ROOT, "templates", tpl), encoding="utf-8") as f:
            assert f.read().lstrip().startswith('{% extends "base.html.j2" %}')
    assert not any(os.path.exists(os.path.join(ROOT, "src", p)) for p in build.TEMPLATED)


def test_sitemap_lists_every_page_with_canonical_lastmod():
    import json
    import re
    build.main()
    xml = open(os.path.join(ROOT, "dist", "sitemap.xml"), encoding="utf-8").read()
    canon = json.load(open(os.path.join(ROOT, "data", "mortality-data.json"), encoding="utf-8"))["metadata"]["last_updated"]
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    assert "https://aimortality.org/" in locs and "https://aimortality.org/report" in locs
    # every page that has a path: an error page (path None) is not a destination
    assert sorted(locs) == sorted(f"https://aimortality.org{m['path']}" for m in build.PAGES_META.values() if m["path"])
    assert not any("404" in loc for loc in locs)
    assert set(re.findall(r"<lastmod>([^<]+)</lastmod>", xml)) == {canon}
    assert not os.path.exists(os.path.join(ROOT, "src", "sitemap.xml"))   # generated, never hand-typed


def test_every_page_has_canonical_og_twitter():
    import re
    build.main()
    for out in build.TEMPLATED:
        if build.PAGES_META[out].get("noindex"):
            continue            # an unindexed page claims no canonical URL (see test_404_page_*)
        html = open(os.path.join(ROOT, "dist", out), encoding="utf-8").read()
        for needle in ('rel="canonical"', 'property="og:title"', 'property="og:description"', 'name="twitter:card"'):
            assert needle in html, (out, needle)
        assert 'property="twitter:' not in html, out
        url = "https://aimortality.org" + build.PAGES_META[out]["path"]
        assert f'rel="canonical" href="{url}"' in html, out
        assert f'property="og:url" content="{url}"' in html, out
        assert len(re.findall(r"<title>", html)) == 1, out


def test_pages_meta_covers_every_templated_page():
    assert set(build.PAGES_META) == set(build.TEMPLATED)
    for out, m in build.PAGES_META.items():
        if m.get("noindex"):
            assert m["path"] is None and m["ld_type"] is None, out      # claims no URL, carries no JSON-LD
            continue
        assert m["path"] == ("/" if out == "index.html" else "/" + out[:-5])
        assert m["ld_type"] in ("Dataset", "Article", "WebPage")


def test_404_page_is_unindexed_claims_no_url_and_keeps_the_shared_chrome():
    import re
    build.main()
    html = open(os.path.join(ROOT, "dist", "404.html"), encoding="utf-8").read()
    head = html[:html.index("</head>")]
    assert '<meta name="robots" content="noindex">' in head
    for absent in ('rel="canonical"', 'property="og:url"', "application/ld+json"):
        assert absent not in head, absent
    assert re.findall(r"<title>([^<]*)</title>", head) == ["Page not found \u2014 AI Companion Mortality Database"]
    assert 'content="The page you requested does not exist on the AI Companion Mortality Database."' in head
    assert '<h1>Page not found</h1>' in html
    assert 'class="crisis-bar"' in html and 'href="tel:988"' in html and 'class="site-footer"' in html
    assert 'aria-current' not in html          # no nav item is current
    # root-absolute assets and links: it is served at any path depth
    assert 'href="/assets/base.css"' in html and 'src="/assets/theme.js"' in html
    assert 'href="/report.html"' in html
    sitemap = open(os.path.join(ROOT, "dist", "sitemap.xml"), encoding="utf-8").read()
    assert "/404" not in sitemap


def test_descriptions_and_doi_come_from_canonical():
    import json
    import re
    d = json.load(open(os.path.join(ROOT, "data", "mortality-data.json"), encoding="utf-8"))
    m = d["metadata"]
    build.main()
    for out in ("index.html", "report.html", "index-academic.html"):
        html = open(os.path.join(ROOT, "dist", out), encoding="utf-8").read()
        desc = re.search(r'<meta name="description" content="([^"]*)"', html).group(1)
        assert f"{m['total_fatalities']} " in desc and f"{m['total_incidents']} incidents" in desc, out
    html = open(os.path.join(ROOT, "dist", "index-academic.html"), encoding="utf-8").read()
    assert html.count(build.VERSION_DOI) == 6       # description x3 (meta, og, twitter), DOI href + text, citation
    assert f"Version {m['version']}, DOI {build.VERSION_DOI}" in html
    assert f"Version {m['version']}. Zenodo. https://doi.org/{build.VERSION_DOI}" in html
    assert "10.5281/zenodo." not in open(os.path.join(ROOT, "templates", "index-academic.html.j2"), encoding="utf-8").read()


def test_non_index_pages_get_derived_json_ld():
    import json
    import re
    build.main()
    for out, ld in (("report.html", "Article"), ("index-academic.html", "Article"), ("methodology.html", "WebPage"),
                    ("verification-standards.html", "WebPage")):
        html = open(os.path.join(ROOT, "dist", out), encoding="utf-8").read()
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        assert len(blocks) == 1, out
        data = json.loads(blocks[0])
        assert data["@type"] == ld and data["url"] == "https://aimortality.org" + build.PAGES_META[out]["path"]
        assert data["isPartOf"]["url"] == "https://aimortality.org/"


# ── Task 6: the two documents render at build time ───────────────────────────────────────────
DOC_PAGES = (("methodology.html", "On What Counts as an Incident"),
             ("verification-standards.html", "Tier 1: Juridical Evidence"))


def test_docs_render_statically():
    import re
    build.main()
    for out, needle in DOC_PAGES:
        html = open(os.path.join(ROOT, "dist", out), encoding="utf-8").read()
        assert needle in html and "Loading" not in html, out
        assert 'type="module"' not in html, out
        assert len(re.findall(r"<h1[ >]", html)) == 1, out
        assert len(re.findall(r"<main[ >]", html)) == 1 and 'id="main-content"' in html, out
        assert len(re.findall(r"<footer[ >]", html)) == 1 and 'class="site-footer"' in html, out
        assert re.search(r'<nav [^>]*aria-label="On this page"', html), out
        assert 'class="doc-source"' in html and 'href="/docs/' in html, out
    for name in os.listdir(os.path.join(ROOT, "dist")):
        if name.endswith(".html"):
            assert "esm.sh" not in open(os.path.join(ROOT, "dist", name), encoding="utf-8").read(), name


def test_doc_switch_is_two_real_links_with_aria_current():
    import re
    build.main()
    for out, current in (("methodology.html", "/methodology.html"), ("verification-standards.html", "/verification-standards.html")):
        html = open(os.path.join(ROOT, "dist", out), encoding="utf-8").read()
        sw = re.search(r'<nav class="doc-switch" aria-label="Document">(.*?)</nav>', html, re.S).group(1)
        hrefs = re.findall(r'<a [^>]*href="([^"]+)"', sw)
        assert hrefs == ["/methodology.html", "/verification-standards.html"], hrefs
        assert re.findall(r'<a [^>]*href="([^"]+)"[^>]*aria-current="page"', sw) == [current]
        site_nav = re.search(r'<nav aria-label="Site">(.*?)</nav>', html, re.S).group(1)
        assert re.findall(r'href="([^"]+)"[^>]*aria-current="page"', site_nav) == [current]
        assert "doc=verification-standards" not in html


def test_headings_get_stable_ids_toc_and_labelled_permalinks():
    import re
    build.main()
    html = open(os.path.join(ROOT, "dist", "verification-standards.html"), encoding="utf-8").read()
    assert '<h2 id="tier-1-juridical-evidence">' in html
    assert '<h3 id="minors">' in html
    toc = re.search(r'<nav [^>]*aria-label="On this page">(.*?)</nav>', html, re.S).group(1)
    assert 'href="#tier-1-juridical-evidence"' in toc and 'href="#minors"' not in toc   # h2s only
    # every permalink is a link with an accessible name, never a bare symbol
    anchors = re.findall(r'<a class="header-anchor"[^>]*>', html)
    assert anchors and all('aria-label="' in a for a in anchors), anchors
    # every contents link lands on a real id
    for frag in re.findall(r'href="#([^"]+)"', toc):
        assert f'id="{frag}"' in html, frag


def test_doc_links_between_docs_published_files_and_unpublished_files():
    g = "https://gitlab.com/aimortality/ai-companion-mortality-database/-/blob/main/"
    # links between the two documents -> their rendered pages (fragment kept)
    assert build.rewrite_doc_link("methodology.md") == "/methodology.html"
    assert build.rewrite_doc_link("./verification-standards.md#minors") == "/verification-standards.html#minors"
    # files that ARE published under dist/ (docs/, data/) -> root-absolute site path
    assert build.rewrite_doc_link("../data/mortality-data.json") == "/data/mortality-data.json"
    assert build.rewrite_doc_link("sources/README.md") == "/docs/sources/README.md"
    # repository files that are NOT published -> the repository URL
    assert build.rewrite_doc_link("../CONTRIBUTING.md") == g + "CONTRIBUTING.md"
    # external, mailto and #fragment links are untouched
    for untouched in ("https://orcid.org/0009-0004-5699-6035", "mailto:contact@aimortality.org", "#minors"):
        assert build.rewrite_doc_link(untouched) == untouched
    # a link to a file that does not exist fails the build; it never ships a dead link
    import pytest
    with pytest.raises(ValueError):
        build.rewrite_doc_link("../no-such-file.md")


def test_rendered_docs_contain_no_relative_markdown_links():
    import re
    build.main()
    for out, _ in DOC_PAGES:
        html = open(os.path.join(ROOT, "dist", out), encoding="utf-8").read()
        doc = html[html.index('id="doc"'):html.index("</main>")]
        assert not re.findall(r'href="(?!https?://|mailto:|#|/)[^"]*"', doc), out


def test_doc_sources_are_published_unmodified():
    # the document is rewritten at render time only; dist/docs must stay exact copies of docs/
    build.main()
    for name in ("methodology.md", "verification-standards.md"):
        assert (open(os.path.join(ROOT, "docs", name), "rb").read()
                == open(os.path.join(ROOT, "dist", "docs", name), "rb").read())


def test_root_absolute_doc_links_pass_through_when_published_and_fail_when_not():
    import pytest
    # a root-absolute link is already a site path: untouched if the site will serve it
    assert build.rewrite_doc_link("/data/mortality-data.json") == "/data/mortality-data.json"
    assert build.rewrite_doc_link("/docs/methodology.md#a") == "/docs/methodology.md#a"
    assert build.rewrite_doc_link("/methodology.html") == "/methodology.html"      # a built page
    assert build.rewrite_doc_link("/favicon.jpg") == "/favicon.jpg"                 # copied from src/
    # ... and a build failure if the site would 404 on it (never re-pointed at the repository)
    for dead in ("/CONTRIBUTING.md", "/data/no-such-file.json", "/no-such-page.html", "/data/"):
        with pytest.raises(ValueError):
            build.rewrite_doc_link(dead)
    # //host/... is protocol-relative, i.e. external: untouched
    assert build.rewrite_doc_link("//example.org/x") == "//example.org/x"


def test_doc_link_query_is_kept_and_directory_links_fail():
    import pytest
    # the query and fragment travel with the rewritten target; only the path decides what it is
    assert build.rewrite_doc_link("../data/README.md?x=1#a") == "/data/README.md?x=1#a"
    assert (build.rewrite_doc_link("../CONTRIBUTING.md?plain=1#top")
            == "https://gitlab.com/aimortality/ai-companion-mortality-database/-/blob/main/CONTRIBUTING.md?plain=1#top")
    with pytest.raises(ValueError):
        build.rewrite_doc_link("../data/")          # a directory is not a published page


def test_markdown_tables_render_inside_labelled_scroll_regions():
    import re
    html, _ = build.render_markdown("docs/verification-standards.md")
    tables = re.findall(r"<table>", html)
    wrapped = re.findall(r'<div class="table-scroll" role="region" tabindex="0" aria-label="([^"]+)">\s*<table>', html)
    assert tables and len(wrapped) == len(tables)
    assert len(set(wrapped)) == len(wrapped)              # labels on one page are unique
    assert "Quick Reference table" in wrapped             # named from the nearest preceding heading
    assert html.count("</table>\n</div>") == len(tables)  # and every region is closed right after its table


def test_missing_dependency_exits_with_one_setup_line_not_a_traceback(tmp_path):
    import subprocess
    # a shim directory whose markdown_it cannot be imported, ahead of the real packages on the path
    (tmp_path / "markdown_it.py").write_text("raise ModuleNotFoundError(\"No module named 'markdown_it'\", name='markdown_it')\n")
    env = dict(os.environ, PYTHONPATH=str(tmp_path))
    r = subprocess.run([sys.executable, os.path.join(ROOT, "build.py")], capture_output=True, text=True, env=env)
    assert r.returncode != 0
    assert "Traceback" not in r.stderr
    assert "requirements.txt" in r.stderr and "python3.12 -m venv .venv" in r.stderr and "markdown_it" in r.stderr
    assert len(r.stderr.strip().splitlines()) == 1, r.stderr


def test_root_absolute_doc_links_are_normalised_before_the_published_check():
    import pytest
    # /data/../CONTRIBUTING.md resolves to /CONTRIBUTING.md, which the site does not serve; it must not
    # pass just because its first segment is "data" and the file exists in the repository
    for escaping in ("/data/../CONTRIBUTING.md", "/docs/../README.md", "/data/../../etc/passwd", "/data/./../CONTRIBUTING.md"):
        with pytest.raises(ValueError):
            build.rewrite_doc_link(escaping)
    assert build._is_published("/data/../favicon.jpg")          # normalises to a file src/ does publish
    assert not build._is_published("/data/../CONTRIBUTING.md")
    # a harmless dot segment inside a published path still passes, and the href is kept as written
    assert build.rewrite_doc_link("/data/./mortality-data.json") == "/data/./mortality-data.json"
