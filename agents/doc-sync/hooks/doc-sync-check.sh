#!/usr/bin/env bash
# Claude Code Stop hook for minds-app.
# When functional files (frontend/src, backend; not tests, mocks or ui-dev) changed since the last /done,
# block the stop ONCE per distinct set of changed files and tell Claude to run /done.
# Never loops: it exits quietly when Claude Code says a stop hook is already active, and it remembers
# which file set it already nudged about (.claude/.last-nudge).
# Needs: bash, git. Exits 0 (allow) on any doubt, so it can never trap a session.

input="$(cat 2>/dev/null)"
case "$input" in *'"stop_hook_active":true'*|*'"stop_hook_active": true'*) exit 0 ;; esac

root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}"
cd "$root" 2>/dev/null || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0
[ -f .claude/last-done ] || exit 0
base="$(tr -d '[:space:]' < .claude/last-done)"
git cat-file -e "${base}^{commit}" 2>/dev/null || exit 0

IGNORE='(\.test\.[jt]sx?$|/__tests__/|^frontend/src/(mocks|ui-dev)/|\.md$|package(-lock)?\.json$)'
files="$( { git diff --name-only "$base" -- frontend/src backend 2>/dev/null; git ls-files --others --exclude-standard -- frontend/src backend 2>/dev/null; } | grep -Ev "$IGNORE" | sort -u )"
[ -z "$files" ] && exit 0

hasher="sha1sum"; command -v sha1sum >/dev/null 2>&1 || hasher="shasum"
sig="$(printf '%s\n' "$files" | $hasher | cut -d' ' -f1)"
[ "$(cat .claude/.last-nudge 2>/dev/null)" = "$sig" ] && exit 0
printf '%s\n' "$sig" > .claude/.last-nudge

n="$(printf '%s\n' "$files" | wc -l | tr -d ' ')"
sample="$(printf '%s\n' "$files" | head -4 | sed 's#.*/##' | paste -sd, - | sed 's/,/, /g')"
reason="Functional files changed since the last /done (${n} file(s), for example ${sample}). Run /done to update the spec, DECISIONS, STATUS and the change ledger, or tell the user in one line that no doc change is needed."
printf '{"decision":"block","reason":"%s"}\n' "$reason"
exit 0
