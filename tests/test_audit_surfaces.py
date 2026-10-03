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
