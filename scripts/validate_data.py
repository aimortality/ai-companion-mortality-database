#!/usr/bin/env python3
"""validate_data.py -- integrity + statistical-consistency checks for the canonical dataset
(data/mortality-data.json). Run before shipping data updates; build.py also runs it and refuses
to build from data that fails.

  python3 scripts/validate_data.py

Exits 0 if every ERROR-level check passes (WARN-level notes don't fail the run), 1 on errors,
2 if the file is not valid JSON. Ported from validate-data.js with identical checks and labels.
"""
import json
import math
import os
import re
import sys

FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "mortality-data.json")


def _num(v):
    try:
        n = float(v)
    except (TypeError, ValueError):
        return 0
    return 0 if math.isnan(n) else n


def _isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validate(d):
    """Return (passes, warns, errors) as lists of labels."""
    passes, warns, errors = [], [], []

    def check(cond, label, bucket=errors):
        (passes if cond else bucket).append(label)

    m = d["metadata"]
    incidents = d.get("incidents") or []
    platforms = d.get("platforms") or []

    def total(rows, k):
        s = sum(_num(r.get(k)) for r in rows)
        return int(s) if s == int(s) else s

    # structural integrity
    check(len(incidents) == m["total_incidents"],
          f"incidents array ({len(incidents)}) === metadata.total_incidents ({m['total_incidents']})")
    ids = [i.get("id") for i in incidents]
    check(len(set(ids)) == len(ids), "no duplicate incident ids")
    required = ["id", "date", "platform", "verification_level", "sources"]
    missing = [i for i in incidents if any(
        i.get(k) is None or (k == "sources" and (not isinstance(i.get("sources"), list) or not i["sources"]))
        for k in required)]
    check(not missing, f"every incident has {'/'.join(required)}"
          + (f" (offenders: {', '.join(str(i.get('id')) for i in missing)})" if missing else ""))
    bad_date = [i for i in incidents if not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", i.get("date") or "")]
    check(not bad_date, "all incident dates are YYYY[-MM[-DD]]"
          + (f" (bad: {', '.join(i['id'] for i in bad_date)})" if bad_date else ""))

    # statistical consistency
    check(m["ai_users_deceased"] + m["third_party_victims"] == m["total_fatalities"],
          f"ai_users_deceased ({m['ai_users_deceased']}) + third_party_victims ({m['third_party_victims']}) "
          f"=== total_fatalities ({m['total_fatalities']})")
    check(total(platforms, "deaths") == m["ai_users_deceased"],
          f"Σ platform.deaths ({total(platforms, 'deaths')}) === ai_users_deceased ({m['ai_users_deceased']})")
    tp = total(platforms, "third_party_fatalities")
    check(tp == m["third_party_victims"],
          f"Σ platform.third_party_fatalities ({tp}) === third_party_victims ({m['third_party_victims']})")
    dby = (d.get("statistics") or {}).get("deaths_by_year") or {}
    dby_sum = int(sum(_num(v) for v in dby.values()))
    check(dby_sum == m["total_incidents"],
          f"Σ deaths_by_year ({dby_sum}) === total_incidents ({m['total_incidents']})", warns)
    bad_fat = [i for i in incidents
               if not _isnum(i.get("fatalities")) or i["fatalities"] < 0
               or not _isnum(i.get("survived_attempt_victims")) or i["survived_attempt_victims"] < 0]
    check(not bad_fat, "every incident has a non-negative fatalities and survived_attempt_victims"
          + (f" (offenders: {', '.join(i['id'] for i in bad_fat)})" if bad_fat else ""))
    fs = total(incidents, "fatalities")
    check(fs == m["total_fatalities"], f"Σ incident.fatalities ({fs}) === total_fatalities ({m['total_fatalities']})")
    ss = total(incidents, "survived_attempt_victims")
    check(ss == m["total_attempts"], f"Σ incident.survived_attempt_victims ({ss}) === total_attempts ({m['total_attempts']})")

    # currency
    max_date = max((i.get("date") or "" for i in incidents), default="")
    check((m.get("last_updated") or "") >= max_date,
          f"last_updated ({m.get('last_updated')}) >= latest incident date ({max_date})", warns)
    return passes, warns, errors


def main():
    try:
        with open(FILE, encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError) as e:
        print(f"FATAL: {FILE} is not valid JSON — {e}", file=sys.stderr)
        return 2
    passes, warns, errors = validate(d)
    for label in passes:
        print(f"  PASS  {label}")
    for label in warns:
        print(f"  WARN  {label}")
    for label in errors:
        print(f"  FAIL  {label}")
    print(f"\n{len(passes)} passed · {len(warns)} warnings · {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
