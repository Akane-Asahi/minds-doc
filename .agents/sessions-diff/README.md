# sessions-diff

A subagent that audits the MINDS sessions screen. It reads the code in `minds-app`, reads the latest planning document in `Claude outputs/`, and writes `sessions-diff.md`: a full brief on where the two differ.

| File | What it is |
|---|---|
| `AGENT.md` | The agent definition and full instructions. This is the file an agent runs. |
| `README.md` | This page. |
| `sessions-diff.md` | The latest brief the agent wrote. Overwritten on every run; git keeps the older ones. |

## What it does

1. Updates both repos to their latest commit.
2. Finds the newest plan in `Claude outputs/` by version number (`Telot Thesis Planning Documents v<N>`, highest `N`) and reads `technical-specification.md` beside it as a secondary source.
3. Extracts the plan text and figures, and lists what the plan says the screen must do.
4. Traces each of those through the code: component, real or mock data, API, model, route, test.
5. Writes the brief: status per requirement, findings with evidence, code-only items, naming drift, decisions for Telot, and a hand-off list for a coding agent.

It never edits `minds-app`, never commits, and never pushes.

## How another agent runs it

You need `minds-doc` and `minds-app` available on disk (or the agent clones them), `git`, and `pandoc` (it falls back to `python-docx` without it).

**Any agent that can spawn a subagent.** Spawn a general-purpose subagent with a prompt like:

```
Read and follow <path-to-minds-doc>/.agents/sessions-diff/AGENT.md exactly.
DOC_REPO=<path-to-minds-doc>
APP_REPO=<path-to-minds-app>
```

Both lines are optional; the defaults are in `AGENT.md`.

**Claude Code, by name.** Copy `AGENT.md` to `.claude/agents/sessions-diff.md` in the project you work in. Its front matter is already in Claude Code's subagent format, so it can then be invoked as `sessions-diff`.

**An agent that cannot spawn subagents.** Have it read `AGENT.md` and do the steps itself.

## Parameters

| Name | Default |
|---|---|
| `DOC_REPO` | local clone of `https://github.com/Akane-Asahi/minds-doc` |
| `APP_REPO` | local clone of `https://github.com/Akane-Asahi/minds-app` |
| `OUTPUT` | `<DOC_REPO>/.agents/sessions-diff/sessions-diff.md` |

## After a run

The agent only writes the file. Whoever started it reviews `sessions-diff.md` and commits it to `minds-doc`. The brief's header records the plan version and the code commit it compared, so an old brief can always be traced to what it was based on.

## Keeping it accurate

The "known code locations" and "sanity anchors" in `AGENT.md` are hints dated 2026-10-19 (minds-app `ba707ba`, plan v27). The agent is told to verify them, but update them when screens are renamed or moved, or when the plan's wording for this screen changes.

If a cloud session is used, attach `minds-doc` with push access and `minds-app` with read access before starting the agent.
