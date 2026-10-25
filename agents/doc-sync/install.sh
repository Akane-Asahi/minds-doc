#!/usr/bin/env bash
# Install the doc-sync kit into a local minds-app clone.
#   bash agents/doc-sync/install.sh <path to minds-app> <path to minds-doc>
# Safe to run again. It never touches tracked minds-app files, never pushes, and never overwrites a
# commit-msg hook that is not ours.
set -e

APP="$1"; DOC="$2"
if [ -z "$APP" ] || [ -z "$DOC" ]; then
  echo "Usage: bash install.sh <path to minds-app> <path to minds-doc>" >&2; exit 2
fi
SRC="$(cd "$(dirname "$0")" && pwd)"
APP="$(cd "$APP" && pwd)"; DOC="$(cd "$DOC" && pwd)"

git -C "$APP" remote -v | grep -qi 'minds-app' || { echo "$APP is not a minds-app clone." >&2; exit 1; }
git -C "$DOC" remote -v | grep -qi 'minds-doc' || { echo "$DOC is not a minds-doc clone." >&2; exit 1; }
PY="$(command -v python3 || command -v python)" || { echo "python3 is needed." >&2; exit 1; }

mkdir -p "$APP/.claude/hooks" "$APP/.claude/skills/done"
cp "$SRC/hooks/doc-sync-check.sh" "$APP/.claude/hooks/doc-sync-check.sh"; chmod +x "$APP/.claude/hooks/doc-sync-check.sh"
cp "$SRC/skills/done/SKILL.md" "$APP/.claude/skills/done/SKILL.md"

# Stop hook: merge into .claude/settings.json without removing anything already there
"$PY" - "$APP/.claude/settings.json" "$SRC/settings.json" <<'PYEOF'
import json, os, sys
target, new = sys.argv[1], json.load(open(sys.argv[2]))
cur = json.load(open(target)) if os.path.exists(target) else {}
stops = cur.setdefault("hooks", {}).setdefault("Stop", [])
entry = new["hooks"]["Stop"][0]
cmd = entry["hooks"][0]["command"]
if not any(h.get("command") == cmd for g in stops for h in g.get("hooks", [])):
    stops.append(entry)
json.dump(cur, open(target, "w"), indent=2)
PYEOF

# git commit-msg hook
HOOKS="$(git -C "$APP" rev-parse --git-path hooks)"; case "$HOOKS" in /*) ;; *) HOOKS="$APP/$HOOKS" ;; esac
mkdir -p "$HOOKS"
if [ -f "$HOOKS/commit-msg" ] && ! grep -q 'doc-impact' "$HOOKS/commit-msg"; then
  echo "A different commit-msg hook already exists at $HOOKS/commit-msg. Not overwritten; merge by hand with $SRC/hooks/commit-msg." >&2
else
  cp "$SRC/hooks/commit-msg" "$HOOKS/commit-msg"; chmod +x "$HOOKS/commit-msg"
fi

# local config and starting point
printf '{\n  "docRepo": "%s"\n}\n' "$DOC" > "$APP/.claude/doc-sync.local.json"
MARK="$("$PY" -c "import json,sys;print(json.load(open(sys.argv[1])).get('minds_app_commit',''))" "$DOC/Claude outputs/doc-sync.json" 2>/dev/null || true)"
if [ -n "$MARK" ] && git -C "$APP" cat-file -e "${MARK}^{commit}" 2>/dev/null; then
  [ -f "$APP/.claude/last-done" ] || echo "$MARK" > "$APP/.claude/last-done"
else
  [ -f "$APP/.claude/last-done" ] || git -C "$APP" rev-parse HEAD > "$APP/.claude/last-done"
  echo "Note: the doc-sync commit is not in this clone (run git pull); last-done was set to HEAD instead." >&2
fi

# keep the kit out of the public repo
touch "$APP/.gitignore"
grep -qxF '.claude/' "$APP/.gitignore" || printf '\n# Claude working files: doc-sync kit (local)\n.claude/\n' >> "$APP/.gitignore"

# CLAUDE.md section
if [ -f "$APP/CLAUDE.md" ]; then
  grep -q '^## Docs sync' "$APP/CLAUDE.md" || { printf '\n' >> "$APP/CLAUDE.md"; cat "$SRC/claude-md-snippet.md" >> "$APP/CLAUDE.md"; }
else
  echo "No CLAUDE.md in $APP; add $SRC/claude-md-snippet.md to it by hand." >&2
fi

echo "Installed in $APP"
echo "  /done skill, Stop hook, commit-msg hook, doc repo = $DOC, last-done = $(cat "$APP/.claude/last-done" | cut -c1-7)"
echo "Restart Claude Code in minds-app so it picks up the skill and the hook."
