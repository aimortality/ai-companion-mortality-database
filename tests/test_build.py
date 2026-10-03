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
