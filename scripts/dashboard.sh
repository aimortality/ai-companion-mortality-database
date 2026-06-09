#!/usr/bin/env bash
#
# dashboard.sh — Generate a self-contained internal status dashboard (dashboard.html).
#
# The repo is PRIVATE, so a plain .html file can't fetch live data without
# embedding a secret. Instead this script uses your already-authenticated
# `gh` + `git` to bake a fresh snapshot into dashboard.html, which you then
# just open in a browser. No token lives in the file.
#
# Usage:
#   ./scripts/dashboard.sh           # regenerate dashboard.html
#   ./scripts/dashboard.sh --open    # regenerate and open in default browser
#
# Refresh whenever you want current data (after a triage run, before review, etc.).

set -euo pipefail

# Resolve repo root regardless of where the script is called from.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

OUT="$ROOT/dashboard.html"

command -v gh >/dev/null 2>&1   || { echo "error: gh CLI not found"; exit 1; }
command -v git >/dev/null 2>&1  || { echo "error: git not found"; exit 1; }

echo "Gathering data via gh + git ..."

# Pull data refs so commit/PR state is current.
git fetch origin main --quiet 2>/dev/null || true

# Hand everything to Python, which assembles the JSON payload and writes the HTML.
python3 "$ROOT/scripts/_dashboard_build.py" "$OUT"

echo "Wrote $OUT"

if [[ "${1:-}" == "--open" ]]; then
  open "$OUT"
fi
