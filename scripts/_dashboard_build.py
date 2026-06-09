#!/usr/bin/env python3
"""Assemble the internal dashboard snapshot and write a self-contained HTML file.

Invoked by scripts/dashboard.sh. Not meant to be run standalone (it expects to be
run from the repo root with `gh` authenticated), but it will work if you do.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone


def sh(args):
    """Run a command, return stdout (stripped). Empty string on failure."""
    try:
        return subprocess.run(
            args, capture_output=True, text=True, check=True, timeout=60
        ).stdout.strip()
    except Exception:
        return ""


def gh_json(args, default):
    out = sh(args)
    if not out:
        return default
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return default


def load_data_metadata():
    """Headline stats from data/mortality-data.json (defensive about key names)."""
    meta = {"incidents": None, "deaths": None, "platforms": None, "version": None,
            "last_updated": None, "records": None}
    try:
        with open("data/mortality-data.json", encoding="utf-8") as fh:
            d = json.load(fh)
    except Exception:
        return meta
    m = d.get("metadata", {})
    meta["incidents"] = m.get("total_incidents")
    meta["platforms"] = m.get("total_platforms")
    meta["version"] = m.get("version")
    meta["last_updated"] = m.get("last_updated")
    # Prefer explicit headline keys; fall back to a gentle heuristic.
    meta["deaths"] = m.get("total_fatalities") or m.get("total_deaths")
    if meta["deaths"] is None:
        for k, v in m.items():
            kl = k.lower()
            if isinstance(v, int) and ("death" in kl or "fatal" in kl) \
                    and not any(x in kl for x in ("note", "percent", "year", "group")):
                meta["deaths"] = v
                break
    inc = d.get("incidents")
    if isinstance(inc, list):
        meta["records"] = len(inc)
    return meta


def parse_tier3():
    """Count Tier-3 monitor rows, find latest date, tally statuses."""
    info = {"rows": 0, "last_date": None, "statuses": {}}
    path = "drafts/tier3-monitor.md"
    if not os.path.exists(path):
        return info
    dates = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            # Data rows look like: | 2026-05-18 | slug | ... | status |
            if re.match(r"\s*\|\s*20\d\d-\d\d-\d\d\s*\|", line):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if not cells:
                    continue
                info["rows"] += 1
                dates.append(cells[0])
                status = cells[-1].lower() if cells else ""
                if status:
                    info["statuses"][status] = info["statuses"].get(status, 0) + 1
    if dates:
        info["last_date"] = max(dates)
    return info


def _classify(fn, head=""):
    kind = "candidate" if fn.startswith("candidate") else "docket"
    breach = ("48h" in head and "breach" in head.lower()) or "⚠️" in head
    return {"name": fn, "kind": kind, "breach": breach}


def latest_triage(open_prs):
    """Most recent weekly-triage run — whether merged to main locally or still on
    an open routine/triage-* PR branch (in which case files come from gh)."""
    base = "drafts/weekly-triage"
    out = {"date": None, "files": [], "pending_pr": None}

    # Dates present locally (i.e. already merged to main).
    local_dirs = []
    if os.path.isdir(base):
        local_dirs = sorted(d for d in os.listdir(base)
                            if re.match(r"20\d\d-\d\d-\d\d$", d)
                            and os.path.isdir(os.path.join(base, d)))

    # Dates sitting in open routine PRs (not yet merged).
    pr_runs = {}  # date -> pr dict
    for pr in open_prs:
        mobj = re.search(r"triage-(20\d\d-\d\d-\d\d)", pr.get("headRefName", "")) \
            or re.search(r"(20\d\d-\d\d-\d\d)", pr.get("title", ""))
        if mobj and ("triage" in pr.get("headRefName", "").lower()
                     or "triage" in pr.get("title", "").lower()):
            pr_runs[mobj.group(1)] = pr

    candidates = set(local_dirs) | set(pr_runs)
    if not candidates:
        return out
    latest = max(candidates)
    out["date"] = latest

    if latest in pr_runs and latest not in local_dirs:
        # Pending PR — pull the file list from GitHub.
        pr = pr_runs[latest]
        out["pending_pr"] = {"number": pr["number"], "url": pr.get("url", "")}
        paths = gh_json(["gh", "pr", "view", str(pr["number"]), "--json", "files",
                         "--jq", "[.files[].path]"], [])
        for p in paths:
            if p.endswith(".md") and "/%s/" % latest in p:
                out["files"].append(_classify(os.path.basename(p)))
    else:
        for fn in sorted(os.listdir(os.path.join(base, latest))):
            if not fn.endswith(".md"):
                continue
            try:
                with open(os.path.join(base, latest, fn), encoding="utf-8") as fh:
                    head = fh.read(4000)
            except Exception:
                head = ""
            out["files"].append(_classify(fn, head))
    return out


REPO = sh(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"]) \
    or "closestfriend/ai-companion-mortality-database"


def gh_url(kind, number):
    return f"https://github.com/{REPO}/{kind}/{number}"


def build_payload():
    open_prs = gh_json(
        ["gh", "pr", "list", "--state", "open", "--limit", "30",
         "--json", "number,title,headRefName,createdAt,url"], [])
    open_issues = gh_json(
        ["gh", "issue", "list", "--state", "open", "--limit", "30",
         "--json", "number,title,createdAt,url"], [])
    merged = gh_json(
        ["gh", "pr", "list", "--state", "merged", "--limit", "8",
         "--json", "number,title,mergedAt,url"], [])

    commits_raw = sh(["git", "log", "origin/main", "-8",
                      "--format=%h%x1f%cI%x1f%s"])
    commits = []
    for line in commits_raw.splitlines():
        parts = line.split("\x1f")
        if len(parts) == 3:
            commits.append({"hash": parts[0], "date": parts[1], "subject": parts[2]})

    return {
        "repo": REPO,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data": load_data_metadata(),
        "tier3": parse_tier3(),
        "triage": latest_triage(open_prs),
        "open_prs": open_prs,
        "open_issues": open_issues,
        "merged_prs": merged,
        "commits": commits,
    }


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>AIMD · internal dashboard</title>
<style>
  :root{
    --bg:#0d0d0d; --panel:#141414; --line:#2a2a2a; --fg:#e8e8e8;
    --dim:#8a8a8a; --accent:#e0c000; --warn:#ff5c5c; --ok:#5cd97e; --link:#7ab8ff;
  }
  *{box-sizing:border-box}
  body{
    margin:0; background:var(--bg); color:var(--fg);
    font-family:"SF Mono",Menlo,Monaco,"Courier New",monospace;
    font-size:13px; line-height:1.5; padding:24px 20px 60px;
  }
  a{color:var(--link); text-decoration:none}
  a:hover{text-decoration:underline}
  header{border-bottom:2px solid var(--line); padding-bottom:14px; margin-bottom:22px}
  h1{font-size:15px; margin:0 0 4px; letter-spacing:.04em; text-transform:uppercase}
  .meta{color:var(--dim); font-size:11px}
  .stale{color:var(--warn); font-weight:bold}
  .fresh{color:var(--ok)}
  .grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:10px; margin-bottom:24px}
  .stat{background:var(--panel); border:1px solid var(--line); padding:12px}
  .stat .n{font-size:22px; font-weight:bold; color:var(--accent)}
  .stat .l{font-size:10px; color:var(--dim); text-transform:uppercase; letter-spacing:.05em; margin-top:2px}
  section{margin-bottom:26px}
  h2{font-size:11px; text-transform:uppercase; letter-spacing:.08em; color:var(--dim);
     border-bottom:1px solid var(--line); padding-bottom:6px; margin:0 0 10px}
  .row{display:flex; gap:10px; padding:7px 0; border-bottom:1px dotted var(--line); align-items:baseline}
  .row:last-child{border-bottom:none}
  .num{color:var(--accent); min-width:42px; font-weight:bold}
  .when{color:var(--dim); font-size:11px; margin-left:auto; white-space:nowrap}
  .tag{font-size:10px; padding:1px 6px; border:1px solid var(--line); border-radius:2px; color:var(--dim); text-transform:uppercase}
  .tag.routine{border-color:var(--accent); color:var(--accent)}
  .tag.breach{border-color:var(--warn); color:var(--warn)}
  .empty{color:var(--dim); font-style:italic; padding:6px 0}
  .files .row{padding:5px 0}
  .pill{display:inline-block; font-size:10px; padding:1px 7px; border-radius:10px; margin-right:6px}
  .pill.watching{background:#222; color:var(--dim)}
  .pill.promoting{background:#3a2e00; color:var(--accent)}
  .twocol{display:grid; grid-template-columns:1fr 1fr; gap:26px}
  @media(max-width:680px){.twocol{grid-template-columns:1fr}}
  code{color:var(--dim)}
  .hint{color:var(--dim); font-size:11px; margin-top:30px; border-top:1px solid var(--line); padding-top:12px}
</style>
</head>
<body>
<header>
  <h1>AI Companion Mortality Database — internal dashboard</h1>
  <div class="meta">
    <span id="repo"></span> ·
    snapshot <span id="genrel"></span> <span id="genabs"></span>
  </div>
</header>
<main id="root"></main>
<div class="hint">
  Static snapshot of a private repo. To refresh: <code>./scripts/dashboard.sh --open</code>
  &nbsp;·&nbsp; Generated by <code>scripts/dashboard.sh</code>.
</div>

<script id="payload" type="application/json">%%PAYLOAD%%</script>
<script>
const D = JSON.parse(document.getElementById('payload').textContent);

function relTime(iso){
  if(!iso) return '';
  const then = new Date(iso), now = new Date();
  const s = Math.floor((now-then)/1000);
  if(s<60) return 'just now';
  const m=Math.floor(s/60); if(m<60) return m+'m ago';
  const h=Math.floor(m/60); if(h<24) return h+'h ago';
  const d=Math.floor(h/24); if(d<30) return d+'d ago';
  return then.toISOString().slice(0,10);
}
function dayOnly(iso){ return iso ? new Date(iso).toISOString().slice(0,10) : '—'; }

// header
document.getElementById('repo').textContent = D.repo;
document.getElementById('genabs').textContent = '('+new Date(D.generated_at).toLocaleString()+')';
(function(){
  const ageH = (new Date() - new Date(D.generated_at))/3.6e6;
  const el = document.getElementById('genrel');
  el.textContent = relTime(D.generated_at);
  el.className = ageH > 24 ? 'stale' : 'fresh';
  if(ageH > 24) el.textContent += ' ⚠ stale — re-run dashboard.sh';
})();

const esc = s => (s||'').replace(/[&<>]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const root = document.getElementById('root');

// ---- stat cards ----
const m = D.data, t3 = D.tier3;
const stats = [
  ['fatalities', m.deaths],
  ['incidents', m.incidents],
  ['platforms', m.platforms],
  ['data version', m.version],
  ['data updated', m.last_updated],
  ['tier-3 watch', t3.rows],
  ['open PRs', D.open_prs.length],
];
root.insertAdjacentHTML('beforeend',
  '<div class="grid">' + stats.map(([l,v]) =>
    `<div class="stat"><div class="n">${v==null||v===''?'—':esc(String(v))}</div><div class="l">${l}</div></div>`
  ).join('') + '</div>');

// ---- helper to render a list section ----
function section(title, rows){
  return `<section><h2>${title}</h2>${rows || '<div class="empty">none</div>'}</section>`;
}

// ---- latest triage run ----
const tr = D.triage;
let triageHtml = '<div class="empty">no triage output found</div>';
if(tr.date){
  const pr = tr.pending_pr
          || D.open_prs.find(p => (p.headRefName||'').includes('triage-'+tr.date))
          || D.merged_prs.find(p => (p.title||'').includes(tr.date));
  const files = tr.files.map(f =>
    `<div class="row"><span>${esc(f.name)}</span>`
    + (f.breach?'<span class="tag breach">48h breach</span>':'')
    + `<span class="tag">${f.kind}</span></div>`).join('');
  const link = pr ? ` · <a href="${esc(pr.url||'#')}" target="_blank">PR #${pr.number} →</a>` : '';
  const status = tr.pending_pr
    ? '<span class="tag routine">pending review</span>'
    : '<span class="tag" style="border-color:var(--ok);color:var(--ok)">merged</span>';
  triageHtml = `<div class="meta" style="margin-bottom:8px">run <b>${tr.date}</b> ${status} · ${tr.files.length} file(s)${link}</div>`
             + `<div class="files">${files || '<div class="empty">no files</div>'}</div>`;
}
root.insertAdjacentHTML('beforeend', section('Latest weekly triage', triageHtml));

// ---- needs review: open PRs + issues ----
function ghRow(item, kind){
  const isRoutine = (item.headRefName||'').startsWith('routine/') || (item.title||'').toLowerCase().includes('triage');
  const when = relTime(item.createdAt);
  return `<div class="row"><span class="num">#${item.number}</span>`
    + `<a href="${esc(item.url)}" target="_blank">${esc(item.title)}</a>`
    + (isRoutine?'<span class="tag routine">routine</span>':'')
    + `<span class="when">${when}</span></div>`;
}
const prRows = D.open_prs.map(p=>ghRow(p,'pr')).join('');
const issueRows = D.open_issues.map(i=>ghRow(i,'issue')).join('');
root.insertAdjacentHTML('beforeend',
  '<div class="twocol">'
  + section(`Open PRs · ${D.open_prs.length}`, prRows)
  + section(`Open issues · ${D.open_issues.length}`, issueRows)
  + '</div>');

// ---- tier-3 monitor summary ----
let t3html = `<div class="meta">${t3.rows} row(s) · latest lead ${t3.last_date||'—'}</div>`;
const sk = Object.keys(t3.statuses||{});
if(sk.length){
  t3html += '<div style="margin-top:8px">' + sk.map(k=>
    `<span class="pill ${esc(k)}">${esc(k)} · ${t3.statuses[k]}</span>`).join('') + '</div>';
}
root.insertAdjacentHTML('beforeend', section('Tier-3 watch list', t3html));

// ---- recent activity: merged PRs + commits ----
const mergedRows = D.merged_prs.map(p =>
  `<div class="row"><span class="num">#${p.number}</span>`
  + `<a href="${esc(p.url)}" target="_blank">${esc(p.title)}</a>`
  + `<span class="when">${dayOnly(p.mergedAt)}</span></div>`).join('');
const commitRows = D.commits.map(c =>
  `<div class="row"><span class="num">${esc(c.hash)}</span>`
  + `<span>${esc(c.subject)}</span>`
  + `<span class="when">${dayOnly(c.date)}</span></div>`).join('');
root.insertAdjacentHTML('beforeend',
  '<div class="twocol">'
  + section('Recently merged', mergedRows)
  + section('Recent commits · main', commitRows)
  + '</div>');
</script>
</body>
</html>
"""


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "dashboard.html"
    payload = build_payload()
    html = HTML.replace("%%PAYLOAD%%", json.dumps(payload))
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)


if __name__ == "__main__":
    main()
