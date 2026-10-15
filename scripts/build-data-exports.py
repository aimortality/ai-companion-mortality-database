#!/usr/bin/env python3
"""Generate the derived data exports from the canonical dataset.

Produces, from data/mortality-data.json:
  - data/platform-analysis.csv  — per-platform safety comparison
  - data/incidents.csv          — one row per incident, flattened
  - data/people.csv             — one row per person (user, third-party victim, perpetrator)
  - data/timeline.json          — chronological incident timeline

All are DERIVED views; mortality-data.json remains the single source of truth.
Re-run after any data change so the exports stay in lockstep.

Run:  python3 scripts/build-data-exports.py
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "data/mortality-data.json"), encoding="utf-8"))


def as_text(v):
    if isinstance(v, dict):
        return "; ".join(f"{k.replace('_', ' ')} ({val})" for k, val in v.items())
    if isinstance(v, list):
        return "; ".join(str(x) for x in v)
    return "" if v is None else str(v)


# ── platform-analysis.csv ──────────────────────────────────────
plat_path = os.path.join(ROOT, "data/platform-analysis.csv")
with open(plat_path, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Platform", "Company", "User Deaths", "Third-Party Victims",
                "Attempts", "Safety Measures Added", "Legal Status"])
    for p in d["platforms"]:
        w.writerow([
            p.get("name", ""), p.get("company", ""),
            p.get("deaths", 0), p.get("third_party_fatalities", 0),
            p.get("attempts", 0),
            as_text(p.get("safety_measures_added")),
            as_text(p.get("legal_status")),
        ])

# ── incidents.csv ──────────────────────────────────────────────
inc_path = os.path.join(ROOT, "data/incidents.csv")
with open(inc_path, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["ID", "Date", "Date Precision", "Name", "Age", "Fatalities", "Survived-Attempt Victims",
                "Tier", "Sub-labels",
                "Platform", "Chatbot Name", "Location",
                "Mechanism Type", "Mechanism Subtype", "Outcome", "Outcome Target",
                "Interaction Duration", "Verification Level", "Legal Status Category",
                "Sources"])
    for i in sorted(d["incidents"], key=lambda x: x.get("date") or ""):
        l = i.get("location", {}) or {}
        w.writerow([
            i.get("id", ""), i.get("date", ""), i.get("date_precision", ""), i.get("name", ""), i.get("age", ""),
            i.get("fatalities", 0), i.get("survived_attempt_victims", 0),
            i.get("tier", ""), "; ".join(i.get("sub_labels") or []),
            i.get("platform", ""), i.get("chatbot_name", ""),
            ", ".join(x for x in [l.get("city") if l.get("city") not in (None, "Unknown") else None,
                                  l.get("state"), l.get("country")] if x),
            i.get("mechanism_type", ""), i.get("mechanism_subtype", ""),
            i.get("outcome", ""), i.get("outcome_target", ""),
            i.get("interaction_duration", ""), i.get("verification_level", ""),
            i.get("legal_status_category", ""),
            as_text(i.get("sources")),
        ])

print(f"wrote {inc_path} ({len(d['incidents'])} incidents)")

# ── people.csv ─────────────────────────────────────────────────
# One row per person named or counted in an incident's `people` array: the AI user, each third-party
# victim, and any perpetrator. `Outcome` is died / survived / wounded / uninjured. This is the file to chart from;
# incident-level `age` mixes users and perpetrators and is null for multi-victim events.
ppl_path = os.path.join(ROOT, "data/people.csv")
n_people = 0
with open(ppl_path, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Incident ID", "Incident Date", "Date Precision", "Platform", "Mechanism Type",
                "Role", "Outcome", "Name", "Name Type", "Age", "Age Precision", "Note"])
    for i in sorted(d["incidents"], key=lambda x: x.get("date") or ""):
        for p in i.get("people") or []:
            n_people += 1
            w.writerow([
                i.get("id", ""), i.get("date", ""), i.get("date_precision", ""),
                i.get("platform", ""), i.get("mechanism_type", ""),
                p.get("role", ""), p.get("outcome", ""),
                "" if p.get("name") is None else p["name"], p.get("name_type", ""),
                "" if p.get("age") is None else p["age"], p.get("age_precision", ""),
                p.get("note", "") or "",
            ])

print(f"wrote {ppl_path} ({n_people} people)")

# ── timeline.json ──────────────────────────────────────────────
def loc(i):
    l = i.get("location", {}) or {}
    return ", ".join(x for x in [l.get("city") if l.get("city") not in (None, "Unknown") else None,
                                 l.get("state"), l.get("country")] if x)


timeline = sorted(({
    "date": i.get("date"),
    "date_precision": i.get("date_precision"),
    "id": i.get("id"),
    "name": i.get("name"),
    "age": i.get("age"),
    "tier": i.get("tier"),
    "fatalities": i.get("fatalities", 0),
    "survived_attempt_victims": i.get("survived_attempt_victims", 0),
    "platform": i.get("platform"),
    "location": loc(i),
    "mechanism_type": i.get("mechanism_type"),
    "outcome": i.get("outcome"),
    "legal_status": i.get("legal_status_category"),
    "verification_level": i.get("verification_level"),
} for i in d["incidents"]), key=lambda r: r["date"] or "")

tl_path = os.path.join(ROOT, "data/timeline.json")
with open(tl_path, "w", encoding="utf-8") as fh:
    json.dump({
        "_note": "Derived chronological view of data/mortality-data.json (the canonical source). "
                 "Regenerate with scripts/build-data-exports.py.",
        "generated_from_version": d["metadata"].get("version"),
        "count": len(timeline),
        "incidents": timeline,
    }, fh, ensure_ascii=False, indent=2)

print(f"wrote {plat_path} ({len(d['platforms'])} platforms)")
print(f"wrote {tl_path} ({len(timeline)} incidents)")
