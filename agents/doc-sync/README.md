# doc-sync: keep the specs, the ledger and the planning document in step with the code

The diff agents show **what differs now**. This kit records **what changed, why and when**, so a planning-document update does not depend on anyone remembering.

## The pieces

| Piece | Where | What it does |
|---|---|---|
| Change ledger | `Claude outputs/change-ledger.md` (minds-doc) | One entry per functional change: what, why, which plan sections and spec files, `Doc status` (pending / vNN / n/a) |
| Sync marker | `Claude outputs/doc-sync.json` (minds-doc) | The minds-app commit the current planning doc was synced to |
| Path map | `agents/doc-sync/doc-map.json` | Which files belong to which screen, diff agent, spec file and plan sections |
| `which-diff.py` | `agents/doc-sync/` | Lists the agents, specs, sections and pending ledger entries since the marker |
| `/done` skill | installed to `minds-app/.claude/skills/done/` | Updates spec, DECISIONS, STATUS, ledger and the minds-doc backup after a functional change |
| Stop hook | `minds-app/.claude/hooks/doc-sync-check.sh` | Nudges Claude to run `/done` once per set of changed files |
| commit-msg hook | `minds-app/.git/hooks/commit-msg` | Refuses a functional commit without a `doc-impact:` line |

## Install (on each machine that has the minds-app clone: Mac and Windows)

```
cd <minds-doc>
git pull
bash agents/doc-sync/install.sh <path to minds-app> <path to minds-doc>
```

On Windows run it from Git Bash. Then restart Claude Code in minds-app. Nothing is committed or pushed to minds-app: `.claude/` is added to `.gitignore`, like `CLAUDE.md`.

## Day to day

1. Work and commit. End each functional commit message with a `doc-impact:` line (`none`, or the plan sections and spec files affected).
2. Run `/done` after the commit (the Stop hook reminds Claude once if you forget). It writes the ledger entries and refreshes the backup in `minds-app-claude-files/`.
3. That is all. The planning document stays untouched until you ask for it.

## When you say "update the planning doc"

Whoever does it (any session, local or cloud) follows these steps:

1. `git pull` both repos. In minds-doc read `Claude outputs/doc-sync.json` and `change-ledger.md`.
2. `python3 agents/doc-sync/which-diff.py --app <minds-app> --files`. It prints the agents to run, the spec files, the plan sections and the pending ledger entries since the marker. (A shallow minds-app clone may need `git fetch --depth=200 origin` first.)
3. Run only the listed diff agents against the newest planning document, with "do not push", and read the briefs.
4. Cross-check: every pending ledger entry should appear in a brief, and every brief difference should be in the ledger. Anything unlogged is a gap; add a ledger entry for it.
5. Edit the planning document as a new version (copy the docx, change the text, validate, render). Figures that changed go in the version's changes summary as "needs new screenshot".
6. Set `Doc status` of the covered entries to the new version, update `doc-sync.json` (new `planningDoc`, `file`, `minds_app_commit`, date), commit and push minds-doc.

The "why" and the direction of the project come from DECISIONS.md and the ledger's Why lines, not from the diffs.

## Limits

- The ledger entries dated 2026-10-25 and earlier were rebuilt from commit history, so most have "Why: not stated".
- The hooks are plain bash and need `git`. `which-diff.py` and the installer need Python 3. They were tested on Linux only; on Windows use Git Bash and check that `python3` or `python` is on the PATH.
- The Stop hook prints the `{"decision":"block","reason":...}` JSON that Claude Code expects. It was tested as a script, not inside Claude Code, so watch the first real run. If it misbehaves, delete the `Stop` block from `minds-app/.claude/settings.json`.
- `doc-map.json` is hand-written. If `which-diff.py` prints "Changed but not in doc-map.json", add those paths.
- Only the diff agents named in the map are suggested; `/done` does not run them for you.

## Uninstall

Delete `minds-app/.claude/`, `minds-app/.git/hooks/commit-msg` and the "Docs sync" section of `CLAUDE.md`.
