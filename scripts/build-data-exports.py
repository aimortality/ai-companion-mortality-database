#!/usr/bin/env python3
"""Generate the derived data exports from the canonical dataset.

Produces, from data/mortality-data.json:
  - data/platform-analysis.csv  — per-platform safety comparison
  - data/incidents.csv          — one row per incident, flattened
  - data/timeline.json          — chronological incident timeline

Both are DERIVED views; mortality-data.json remains the single source of truth.
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
    w.writerow(["ID", "Date", "Name", "Age", "Platform", "Chatbot Name", "Location",
                "Mechanism Type", "Mechanism Subtype", "Outcome", "Outcome Target",
                "Interaction Duration", "Verification Level", "Legal Status Category",
                "Sources"])
    for i in sorted(d["incidents"], key=lambda x: x.get("date") or ""):
        l = i.get("location", {}) or {}
        w.writerow([
            i.get("id", ""), i.get("date", ""), i.get("name", ""), i.get("age", ""),
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

# ── timeline.json ──────────────────────────────────────────────
def loc(i):
    l = i.get("location", {}) or {}
    return ", ".join(x for x in [l.get("city") if l.get("city") not in (None, "Unknown") else None,
                                 l.get("state"), l.get("country")] if x)


timeline = sorted(({
    "date": i.get("date"),
    "id": i.get("id"),
    "name": i.get("name"),
    "age": i.get("age"),
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
