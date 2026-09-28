#!/usr/bin/env python3
"""Generate the site's SVG charts from the canonical dataset.

Reads data/mortality-data.json and emits self-contained SVG fragments to
build/charts/. Every axis is linear, every mark is computed from canonical,
and every editorial convention is stated in the chart itself or its <desc>.

Charts:
  timeline.svg    — incidents on a linear time axis (Jan 2023 → coverage end)
  cumulative.svg  — cumulative fatalities, monthly steps, linear time axis
  platforms.svg   — stacked user deaths + third-party victims per platform
  durations.svg   — strip plot of quantifiable engagement durations

Conventions (stated here, in code, and in each <desc>):
  - Partial dates plot at a midpoint: YYYY → July 1; YYYY-MM → the 15th.
    Such marks are drawn hollow-ringed and the caption says "approximate date".
  - Durations are plotted only where the record states a quantifiable span;
    qualitative durations ("Months", "Unknown") are counted in the caption,
    never invented as positions.
  - Colors are emitted as CSS classes (chart-p-<slug>) plus a fallback fill,
    so the site's theme tokens can restyle them; previews carry both palettes.

Run:  python3 scripts/build-charts.py
"""
import json
import math
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "charts")
os.makedirs(OUT, exist_ok=True)

d = json.load(open(os.path.join(ROOT, "data/mortality-data.json"), encoding="utf-8"))
incidents = sorted(d["incidents"], key=lambda i: i["date"])
COVERAGE_START = date(2023, 1, 1)
COVERAGE_END = date.fromisoformat(d["metadata"]["time_range"]["end"])

PLATFORM_SLUGS = {
    "ChatGPT": "chatgpt", "Character.AI": "characterai", "Chai AI": "chai",
    "Meta AI": "meta", "Gemini": "gemini", "DeepSeek": "deepseek",
    "Claude": "claude", "Replika": "replika",
}
# Fallback fills, chosen to survive BOTH light and dark grounds (no pure black).
PLATFORM_FILLS = {
    "ChatGPT": "#5b6470", "Character.AI": "#c0392b", "Chai AI": "#8e6a1f",
    "Meta AI": "#2471a3", "Gemini": "#7d3c98", "DeepSeek": "#148f77",
    "Claude": "#a04000", "Replika": "#5d6d7e",
}


def parse_date(s):
    """YYYY[-MM[-DD]] → (date, approximate?). Midpoint convention documented above."""
    parts = s.split("-")
    if len(parts) == 3:
        return date(int(parts[0]), int(parts[1]), int(parts[2])), False
    if len(parts) == 2:
        return date(int(parts[0]), int(parts[1]), 15), True
    return date(int(parts[0]), 7, 1), True


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def svg_open(w, h, title_id, title, desc_id, desc):
    return (
        f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="{title_id} {desc_id}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="ui-monospace, SF Mono, Menlo, monospace">\n'
        f'  <title id="{title_id}">{esc(title)}</title>\n'
        f'  <desc id="{desc_id}">{esc(desc)}</desc>\n'
    )


# ── shared time scale ──────────────────────────────────────────────
def make_xscale(x0, x1):
    span = (COVERAGE_END - COVERAGE_START).days
    def x(dt):
        return x0 + (dt - COVERAGE_START).days / span * (x1 - x0)
    return x


def year_ticks(x, y_axis, y_label):
    out = []
    yr = COVERAGE_START.year
    while date(yr, 1, 1) <= COVERAGE_END:
        tx = x(date(yr, 1, 1))
        out.append(f'  <line x1="{tx:.1f}" y1="{y_axis-4}" x2="{tx:.1f}" y2="{y_axis+4}" class="chart-axis" stroke="#888" stroke-width="1"/>')
        out.append(f'  <text x="{tx:.1f}" y="{y_label}" text-anchor="middle" font-size="11" class="chart-label" fill="#666">{yr}</text>')
        yr += 1
    # explicit coverage-end tick so the axis states its own boundary
    tx = x(COVERAGE_END)
    out.append(f'  <line x1="{tx:.1f}" y1="{y_axis-4}" x2="{tx:.1f}" y2="{y_axis+4}" class="chart-axis" stroke="#888" stroke-width="1"/>')
    out.append(f'  <text x="{tx:.1f}" y="{y_label}" text-anchor="middle" font-size="10" class="chart-label" fill="#666">{COVERAGE_END.strftime("%b %Y")}</text>')
    return "\n".join(out)


# ── 1. timeline ────────────────────────────────────────────────────
def build_timeline():
    W, H = 960, 300
    x0, x1, y_axis = 50, 930, H - 46
    x = make_xscale(x0, x1)

    marks = []
    for i in incidents:
        dt, approx = parse_date(i["date"])
        f = i.get("fatalities", 0)
        marks.append({
            "x": x(dt), "date": dt, "approx": approx, "platform": i["platform"],
            "fatalities": f, "id": i["id"], "name": i.get("name", ""), "age": i.get("age"),
            "r": 4 if f == 0 else 4 + 2 * math.sqrt(f),
        })

    # greedy lane stagger: same lane only if horizontally clear
    lanes = []  # last x per lane
    LANE_DY, CLEAR = 26, 26
    for m in sorted(marks, key=lambda m: m["x"]):
        for li, last in enumerate(lanes):
            if m["x"] - last >= CLEAR:
                m["lane"] = li
                lanes[li] = m["x"]
                break
        else:
            m["lane"] = len(lanes)
            lanes.append(m["x"])
    n_lanes = len(lanes)
    y_base = y_axis - 18

    total_f = sum(m["fatalities"] for m in marks)
    desc = (
        f"Chronological timeline of {len(marks)} documented incidents from "
        f"{COVERAGE_START.strftime('%B %Y')} through {COVERAGE_END.strftime('%B %Y')} on a linear time axis. "
        f"Marker area scales with fatalities per incident (total {total_f}); hollow markers are survived attempts; "
        f"ring-outlined markers have approximate dates (year or month known, day unknown). "
        f"Colors denote platform. Each marker's tooltip names the incident date, platform, and fatalities."
    )
    s = svg_open(W, H, "tl-title", "Incident timeline", "tl-desc", desc)
    s += f'  <line x1="{x0}" y1="{y_axis}" x2="{x1}" y2="{y_axis}" class="chart-axis" stroke="#888" stroke-width="1"/>\n'
    s += year_ticks(x, y_axis, y_axis + 18) + "\n"
    for m in sorted(marks, key=lambda m: -m["r"]):
        cy = y_base - m["lane"] * LANE_DY
        slug = PLATFORM_SLUGS.get(m["platform"], "other")
        fill = PLATFORM_FILLS.get(m["platform"], "#777")
        hollow = m["fatalities"] == 0
        ring = ' stroke-dasharray="2,2"' if m["approx"] else ""
        label = f'{m["date"].isoformat() if not m["approx"] else m["date"].strftime("%Y (approx.)")} — {m["platform"]} — ' + (
            f'{m["fatalities"]} fatalit{"y" if m["fatalities"]==1 else "ies"}' if not hollow else "survived attempt")
        s += (
            f'  <g tabindex="0"><circle cx="{m["x"]:.1f}" cy="{cy:.1f}" r="{m["r"]:.1f}" '
            f'class="chart-p-{slug}" fill="{"none" if hollow else fill}" stroke="{fill}" stroke-width="1.5"{ring}/>'
            f'<title>{esc(label)}</title></g>\n'
        )
        s += f'  <line x1="{m["x"]:.1f}" y1="{cy + m["r"]:.1f}" x2="{m["x"]:.1f}" y2="{y_axis}" stroke="{fill}" stroke-width="0.5" opacity="0.35"/>\n'
    s += "</svg>\n"
    return s, n_lanes


# ── 2. cumulative fatalities ───────────────────────────────────────
def build_cumulative():
    W, H = 960, 320
    x0, x1, y_axis, y_top = 50, 930, H - 46, 24
    x = make_xscale(x0, x1)

    series_defs = ["ChatGPT", "Character.AI"]
    events = []
    for i in incidents:
        dt, _ = parse_date(i["date"])
        events.append((dt, i["platform"], i.get("fatalities", 0)))
    events.sort()
    total_max = sum(e[2] for e in events)

    def y(v):
        return y_axis - v / total_max * (y_axis - y_top)

    def step_path(platform=None):
        run, pts = 0, [f"{x0:.1f},{y_axis:.1f}"]
        for dt, p, f in events:
            if f == 0 or (platform and p != platform):
                continue
            px = x(dt)
            pts.append(f"{px:.1f},{y(run):.1f}")
            run += f
            pts.append(f"{px:.1f},{y(run):.1f}")
        pts.append(f"{x1:.1f},{y(run):.1f}")
        return " ".join(pts), run

    desc = (
        f"Cumulative documented fatalities from {COVERAGE_START.strftime('%B %Y')} through "
        f"{COVERAGE_END.strftime('%B %Y')} on a linear time axis, counting all victims "
        f"(AI users and third parties). Total reaches {total_max}. "
        f"Separate step lines show ChatGPT and Character.AI cumulative totals; "
        f"steps rise at incident dates by the number killed in that incident."
    )
    s = svg_open(W, H, "cm-title", "Cumulative fatalities", "cm-desc", desc)
    s += f'  <line x1="{x0}" y1="{y_axis}" x2="{x1}" y2="{y_axis}" class="chart-axis" stroke="#888" stroke-width="1"/>\n'
    s += year_ticks(x, y_axis, y_axis + 18) + "\n"
    for gv in range(0, total_max + 1, 10):
        gy = y(gv)
        s += f'  <line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="#888" stroke-width="0.5" opacity="0.25"/>\n'
        s += f'  <text x="{x0-6}" y="{gy+4:.1f}" text-anchor="end" font-size="10" class="chart-label" fill="#666">{gv}</text>\n'
    path, total = step_path(None)
    s += f'  <polyline points="{path}" fill="none" stroke="#5b6470" stroke-width="2.5" class="chart-total"><title>All platforms: {total} cumulative fatalities</title></polyline>\n'
    s += f'  <text x="{x1}" y="{y(total)-8:.1f}" text-anchor="end" font-size="11" font-weight="bold" fill="#5b6470" class="chart-label">All platforms: {total}</text>\n'
    for pl in series_defs:
        pp, pt = step_path(pl)
        fill = PLATFORM_FILLS[pl]
        s += f'  <polyline points="{pp}" fill="none" stroke="{fill}" stroke-width="1.5" stroke-dasharray="5,3" class="chart-p-{PLATFORM_SLUGS[pl]}"><title>{pl}: {pt} cumulative fatalities</title></polyline>\n'
        s += f'  <text x="{x1}" y="{y(pt)+12:.1f}" text-anchor="end" font-size="10" fill="{fill}" class="chart-label">{pl}: {pt}</text>\n'
    s += "</svg>\n"
    return s


# ── 3. platform stacked bars ───────────────────────────────────────
def build_platforms():
    platforms = sorted(
        d["platforms"], key=lambda p: -(p.get("deaths", 0) + p.get("third_party_fatalities", 0)))
    ROW, PAD_T, PAD_B = 30, 26, 40
    W = 960
    H = PAD_T + ROW * len(platforms) + PAD_B
    x0, x1 = 150, 850
    vmax = max(p.get("deaths", 0) + p.get("third_party_fatalities", 0) for p in platforms) or 1

    def bw(v):
        return v / vmax * (x1 - x0)

    totals = {p["name"]: p.get("deaths", 0) + p.get("third_party_fatalities", 0) for p in platforms}
    desc = (
        "Documented fatalities by platform, stacked: solid segment = AI users deceased, "
        "hatched-lighter segment = third-party victims. Totals: "
        + "; ".join(f"{n} {t}" for n, t in totals.items()) + ". "
        "Zero-fatality platforms are listed to show tracking scope, not equivalence."
    )
    s = svg_open(W, H, "pf-title", "Fatalities by platform", "pf-desc", desc)
    y = PAD_T
    for p in platforms:
        name, u, t = p["name"], p.get("deaths", 0), p.get("third_party_fatalities", 0)
        fill = PLATFORM_FILLS.get(name, "#777")
        slug = PLATFORM_SLUGS.get(name, "other")
        s += f'  <text x="{x0-8}" y="{y+15}" text-anchor="end" font-size="12" class="chart-label" fill="#444">{esc(name)}</text>\n'
        if u:
            s += f'  <rect x="{x0}" y="{y}" width="{bw(u):.1f}" height="20" fill="{fill}" class="chart-p-{slug}"><title>{esc(name)}: {u} user deaths</title></rect>\n'
        if t:
            s += f'  <rect x="{x0+bw(u):.1f}" y="{y}" width="{bw(t):.1f}" height="20" fill="{fill}" opacity="0.45" class="chart-p-{slug}-tp"><title>{esc(name)}: {t} third-party victims</title></rect>\n'
        label = f"{u+t}" + (f" ({u}+{t})" if u and t else "")
        if u + t:
            s += f'  <text x="{x0+bw(u+t)+8:.1f}" y="{y+15}" font-size="12" font-weight="bold" class="chart-label" fill="#444">{label}</text>\n'
        else:
            s += f'  <text x="{x0+8}" y="{y+15}" font-size="11" class="chart-label" fill="#888">0 documented</text>\n'
        y += ROW
    s += (
        f'  <text x="{x0}" y="{H-14}" font-size="10" class="chart-label" fill="#666">'
        f'solid = AI users deceased · lighter = third-party victims · totals sum to '
        f'{sum(totals.values())} fatalities</text>\n'
    )
    s += "</svg>\n"
    return s


# ── 4. duration strip plot ─────────────────────────────────────────
DUR_PATTERNS = [
    (re.compile(r"(\d+)\s*weeks?", re.I), lambda m: int(m.group(1)) / 4.345),
    (re.compile(r"(\d+)\s*months?", re.I), lambda m: float(m.group(1))),
    (re.compile(r"over one year", re.I), lambda m: 12.0),
]


def parse_duration(s):
    """Return (months, floor?) or None. 'Over one year' is a floor (≥)."""
    if not s:
        return None
    for pat, fn in DUR_PATTERNS:
        m = pat.search(s)
        if m:
            return fn(m), bool(pat.pattern == "over one year")
    return None


def build_durations():
    W, H = 960, 190
    x0, x1, y_axis = 60, 920, H - 46
    quant, qual = [], 0
    for i in incidents:
        raw = i.get("interaction_duration") or ""
        parsed = parse_duration(raw)
        if parsed:
            quant.append({"months": parsed[0], "floor": parsed[1], "platform": i["platform"],
                          "id": i["id"], "raw": raw})
        elif raw and raw.lower() != "unknown":
            qual += 1
    unknown = len(incidents) - len(quant) - qual
    vmax = max(q["months"] for q in quant)

    def x(v):
        return x0 + v / vmax * (x1 - x0)

    desc = (
        f"Strip plot of engagement duration before the incident, in months, for the "
        f"{len(quant)} of {len(incidents)} incidents whose records state a quantifiable span. "
        f"A further {qual} record durations only qualitatively (e.g. 'months'), and {unknown} are unknown; "
        f"those are counted here, not plotted. Range: {min(q['months'] for q in quant):.1f} to {vmax:.0f} months. "
        f"Marks labeled with '≥' are stated floors ('over one year')."
    )
    s = svg_open(W, H, "du-title", "Engagement duration before incident", "du-desc", desc)
    s += f'  <line x1="{x0}" y1="{y_axis}" x2="{x1}" y2="{y_axis}" class="chart-axis" stroke="#888" stroke-width="1"/>\n'
    for mth in range(0, int(vmax) + 1, 3):
        tx = x(mth)
        s += f'  <line x1="{tx:.1f}" y1="{y_axis-4}" x2="{tx:.1f}" y2="{y_axis+4}" stroke="#888" stroke-width="1" class="chart-axis"/>\n'
        s += f'  <text x="{tx:.1f}" y="{y_axis+18}" text-anchor="middle" font-size="10" class="chart-label" fill="#666">{mth}mo</text>\n'
    # jitter marks vertically when close together
    lanes = []
    for q in sorted(quant, key=lambda q: q["months"]):
        qx = x(q["months"])
        for li, last in enumerate(lanes):
            if qx - last >= 18:
                q["lane"] = li
                lanes[li] = qx
                break
        else:
            q["lane"] = len(lanes)
            lanes.append(qx)
        cy = y_axis - 22 - q["lane"] * 22
        fill = PLATFORM_FILLS.get(q["platform"], "#777")
        slug = PLATFORM_SLUGS.get(q["platform"], "other")
        mark = f'≥{q["months"]:.0f}' if q["floor"] else (f'{q["months"]:.0f}' if q["months"] >= 1 else f'{q["months"]:.1f}')
        s += (
            f'  <g tabindex="0"><circle cx="{qx:.1f}" cy="{cy:.1f}" r="6" fill="{fill}" class="chart-p-{slug}"/>'
            f'<title>{esc(q["raw"])} — {esc(q["platform"])}</title></g>\n'
            f'  <text x="{qx:.1f}" y="{cy-10:.1f}" text-anchor="middle" font-size="9" class="chart-label" fill="#666">{mark}</text>\n'
        )
    s += (
        f'  <text x="{x0}" y="{H-6}" font-size="10" class="chart-label" fill="#666">'
        f'{len(quant)} of {len(incidents)} incidents have a quantifiable duration; '
        f'{qual} qualitative (&#8220;months&#8221;, &#8220;weeks to months&#8221;), {unknown} unknown — counted, not plotted</text>\n'
    )
    s += "</svg>\n"
    return s


# ── emit ───────────────────────────────────────────────────────────
timeline_svg, n_lanes = build_timeline()
outputs = {
    "timeline.svg": timeline_svg,
    "cumulative.svg": build_cumulative(),
    "platforms.svg": build_platforms(),
    "durations.svg": build_durations(),
}
for name, svg in outputs.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"wrote build/charts/{name} ({len(svg)} bytes)")
print(f"timeline lanes: {n_lanes} · coverage: {COVERAGE_START} → {COVERAGE_END} · "
      f"generated from mortality-data.json v{d['metadata'].get('version')}")
