#!/usr/bin/env bash
#
# dashboard.sh — Generate the internal status board (dashboard.html).
#
# Thin launcher over the personal `status-board` skill. The generic half (PRs,
# issues, commits) lives in the skill's generate.py; the aimortality-specific
# half (fatality counts, Tier-3 watch, weekly-triage PR detection) lives in
# .status-board/adapter, which the generator auto-discovers.
#
# The repo is PRIVATE, so this bakes a snapshot using your already-authenticated
# `gh` + `git` rather than embedding a token in a static file. Re-run to refresh.
#
# Usage:
#   ./scripts/dashboard.sh           # regenerate dashboard.html
#   ./scripts/dashboard.sh --open    # regenerate and open in default browser

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEN="$HOME/.claude/skills/status-board/generate.py"

if [[ ! -f "$GEN" ]]; then
  echo "error: status-board skill not found at $GEN" >&2
  echo "       (install the personal 'status-board' skill, or restore scripts/_dashboard_build.py)" >&2
  exit 1
fi

OPEN_FLAG=()
[[ "${1:-}" == "--open" ]] && OPEN_FLAG=(--open)

python3 "$GEN" \
  --project "$ROOT" \
  --out "$ROOT/dashboard.html" \
  --title "AIMD · internal dashboard" \
  --refresh-cmd "./scripts/dashboard.sh --open" \
  "${OPEN_FLAG[@]}"
