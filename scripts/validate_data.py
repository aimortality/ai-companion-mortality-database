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
    stats = d.get("statistics") or {}
    iby = stats.get("incidents_by_year") or {}
    iby_sum = int(sum(_num(v) for v in iby.values()))
    check(iby_sum == m["total_incidents"],
          f"Σ incidents_by_year ({iby_sum}) === total_incidents ({m['total_incidents']})")
    dby = stats.get("deaths_by_year") or {}
    dby_sum = int(sum(_num(v) for v in dby.values()))
    check(dby_sum == m["total_fatalities"],
          f"Σ deaths_by_year ({dby_sum}) === total_fatalities ({m['total_fatalities']})")
    by_year_fat = {}
    for i in incidents:
        y = (i.get("date") or "")[:4]
        by_year_fat[y] = by_year_fat.get(y, 0) + int(_num(i.get("fatalities")))
    check({k: int(_num(v)) for k, v in dby.items()} == by_year_fat,
          "deaths_by_year equals Σ incident.fatalities per incident year")

    # successor schema: tier, sub_labels, date_precision, people[]
    bad_tier = [i["id"] for i in incidents if i.get("tier") not in (1, 2, 3)]
    check(not bad_tier, "every incident has tier ∈ {1, 2, 3}" + (f" (offenders: {', '.join(bad_tier)})" if bad_tier else ""))
    bad_sub = [i["id"] for i in incidents if not isinstance(i.get("sub_labels"), list)
               or any(not isinstance(s, str) or "_" in s for s in i["sub_labels"])]
    check(not bad_sub, "every incident has sub_labels (list, hyphenated)" + (f" (offenders: {', '.join(bad_sub)})" if bad_sub else ""))
    prec_for_len = {4: "year", 7: "month", 10: "day"}
    bad_prec = [i["id"] for i in incidents
                if i.get("date_precision") not in ("day", "month", "year")
                or prec_for_len.get(len(i.get("date") or ""), "?") not in (i.get("date_precision"), "day", "month")
                # a placeholder day (-01) may be declared month precision; a shorter date may not claim more precision
                or (len(i.get("date") or "") == 7 and i.get("date_precision") == "day")
                or (len(i.get("date") or "") == 4 and i.get("date_precision") != "year")]
    check(not bad_prec, "every incident has a date_precision consistent with its date"
          + (f" (offenders: {', '.join(bad_prec)})" if bad_prec else ""))
    roles, outcomes = {"user", "third_party", "perpetrator"}, {"died", "survived", "wounded", "uninjured"}
    bad_people = [i["id"] for i in incidents if not isinstance(i.get("people"), list) or not i["people"]
                  or any(p.get("role") not in roles or p.get("outcome") not in outcomes
                         or p.get("name_type") not in ("real", "pseudonym", "unnamed")
                         or (p.get("age") is not None and not _isnum(p["age"])) for p in i["people"])]
    check(not bad_people, "every incident has a well-formed people[] (role/outcome/name_type/age)"
          + (f" (offenders: {', '.join(bad_people)})" if bad_people else ""))
    if not bad_people:
        died = [p for i in incidents for p in i["people"] if p["outcome"] == "died"]
        survived = [p for i in incidents for p in i["people"] if p["outcome"] == "survived"]
        check(len(died) == m["total_fatalities"], f"Σ people died ({len(died)}) === total_fatalities ({m['total_fatalities']})")
        n_user = sum(1 for p in died if p["role"] == "user")
        n_third = sum(1 for p in died if p["role"] == "third_party")
        check(n_user == m["ai_users_deceased"], f"people died as user ({n_user}) === ai_users_deceased ({m['ai_users_deceased']})")
        check(n_third == m["third_party_victims"], f"people died as third_party ({n_third}) === third_party_victims ({m['third_party_victims']})")
        check(len(survived) == m["total_attempts"], f"Σ people survived ({len(survived)}) === total_attempts ({m['total_attempts']})")
        per_inc = [i["id"] for i in incidents
                   if sum(1 for p in i["people"] if p["outcome"] == "died") != int(_num(i.get("fatalities")))
                   or sum(1 for p in i["people"] if p["outcome"] == "survived") != int(_num(i.get("survived_attempt_victims")))]
        check(not per_inc, "per incident, people died/survived counts equal fatalities/survived_attempt_victims"
              + (f" (offenders: {', '.join(per_inc)})" if per_inc else ""))
        minors = sum(1 for p in died if p.get("age") is not None and p["age"] < 18)
        exp_minors = (stats.get("victims_by_age_group") or {}).get("minors")
        check(minors == exp_minors, f"people died aged <18 ({minors}) === victims_by_age_group.minors ({exp_minors})")
        unknown_age = sum(1 for p in died if p.get("age") is None)
        check(unknown_age == 0, f"every deceased person has an age ({unknown_age} unknown)", warns)
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
