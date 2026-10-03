import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)  # later tests in this file `import build` directly

import build  # noqa: E402


def test_every_page_is_templated_and_extends_base():
    assert set(build.TEMPLATED) == {"index.html", "report.html", "index-academic.html", "methodology.html"}
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
    assert sorted(locs) == sorted(f"https://aimortality.org{m['path']}" for m in build.PAGES_META.values())
    assert set(re.findall(r"<lastmod>([^<]+)</lastmod>", xml)) == {canon}
    assert not os.path.exists(os.path.join(ROOT, "src", "sitemap.xml"))   # generated, never hand-typed


def test_every_page_has_canonical_og_twitter():
    import re
    build.main()
    for out in build.TEMPLATED:
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
        assert m["path"] == ("/" if out == "index.html" else "/" + out[:-5])
        assert m["ld_type"] in ("Dataset", "Article", "WebPage")


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
    for out, ld in (("report.html", "Article"), ("index-academic.html", "Article"), ("methodology.html", "WebPage")):
        html = open(os.path.join(ROOT, "dist", out), encoding="utf-8").read()
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        assert len(blocks) == 1, out
        data = json.loads(blocks[0])
        assert data["@type"] == ld and data["url"] == "https://aimortality.org" + build.PAGES_META[out]["path"]
        assert data["isPartOf"]["url"] == "https://aimortality.org/"
