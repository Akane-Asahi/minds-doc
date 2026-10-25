---
name: done
description: Use when the user says "/done", "wrap the docs", "document this change" or after a functional change in minds-app is committed. Updates the spec, DECISIONS, STATUS, the change ledger and the minds-doc backup so the planning doc can later be brought up to date.
---

# /done: document what just changed

Runs in the **minds-app** repo after functional work is committed. It records what changed and why, so that whoever updates the planning document later (you, or a cloud session) can see exactly what happened since the last sync. It does not edit the planning document and does not run the diff agents unless asked.

## Before you start

1. Confirm the repo: `git remote -v` must show `Akane-Asahi/minds-app`. Never push minds-app from this skill.
2. Read `.claude/doc-sync.local.json` for `docRepo` (path of the minds-doc clone). In that clone run `git remote -v` (must show `Akane-Asahi/minds-doc`) and `git pull --ff-only`. If either fails, stop and say so.
3. If functional files are uncommitted (`git status --short frontend/src backend`), stop and ask the user to commit first. One functional change per commit; the commit message needs a `doc-impact:` line.

## Steps

1. **Find what changed since the last /done.**
   ```
   BASE=$(cat .claude/last-done)
   python3 <docRepo>/agents/doc-sync/which-diff.py --from $BASE --app . --doc <docRepo> --files
   git log --format='%h %ad %s%n%b---' --date=short $BASE..HEAD
   ```
   (`python` instead of `python3` on Windows.) The first command lists the areas, spec files and planning-doc sections touched. The second gives the commit messages and their `doc-impact:` lines. If nothing functional changed, say so and stop.

2. **Update the spec.** For each affected area open the listed `docs/spec/F*.md` (and `02-data-model.md` / `03-api.md` if the data model or an endpoint changed). Change only what is no longer true. If the user's request conflicts with the spec, say so and update the spec; Telot's latest statement is the decision.

3. **DECISIONS.md.** Add a dated line (`YYYY-MM-DD`) for each decision, with the reason in the user's words. If nobody gave a reason, write that a reason was not stated. Do not invent one.

4. **STATUS.md.** Update done / next / blocked.

5. **CLAUDE.md** only if a rule, the structure, a command or the stack changed. Keep it short; details belong in `docs/spec/`.

6. **Change ledger.** In `<docRepo>/Claude outputs/change-ledger.md` add one entry per functional change at the top (above the first existing entry, below the `---` line), in the format described at the top of that file. `Doc status` is `pending` unless the commit says `doc-impact: none` (then `n/a`). Fill "Affects" from the which-diff output. Fill "Why" from this session and DECISIONS only.

7. **Mirror and push the doc repo.** Copy `CLAUDE.md`, `STATUS.md`, `DECISIONS.md`, `docs/spec/`, `docs/templates/` and, if changed, `docs/design/` from minds-app into `<docRepo>/minds-app-claude-files/` (`cp -R`, no deletes). In `<docRepo>`: `git add "Claude outputs/change-ledger.md" minds-app-claude-files`, commit `doc-sync: ledger and backup (minds-app <short HEAD>)`, `git fetch origin main`, rebase if behind, `git push`. If the push is refused, keep the commit and say so.

8. **Record the point.** `git rev-parse HEAD > .claude/last-done` (in minds-app).

9. **Report in four lines or fewer:** entries added, files updated, how many ledger entries are now `pending` for the planning doc, and whether to run the diff agents the map named. Offer the next step ("update the planning doc to v31") but do not start it.

## Rules

- Never edit the planning document, minds-app code or the frozen `technical-specification-1.md` from this skill.
- Never write secrets, `.env` values or participant data into any of these files (minds-doc and minds-app are public).
- If the ledger already has an entry for the same commit, update it instead of adding a second.
