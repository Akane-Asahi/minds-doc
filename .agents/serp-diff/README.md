# serp-diff agent

Compares what is built for the SERP screen in `Akane-Asahi/minds-app` with the latest SERP plan in this repo's `Claude outputs/` folder, and writes the full gap brief to `Claude outputs/serp-diff.md`.

| File | Purpose |
|---|---|
| `AGENT.md` | The agent's complete instructions (inputs, rules, steps, output format). This is the file the agent follows. |
| `README.md` | This file: how to run it. |

## How another agent runs it

The agent reads both repos, so they need to be available in the session first (attach `Akane-Asahi/minds-doc` and `Akane-Asahi/minds-app` with `add_repo`; the agent clones them if the checkout is missing).

**Option 1, works anywhere** (a general-purpose subagent that reads the instructions from this repo):

```
Agent(
  subagent_type: "general-purpose",
  description: "SERP code vs plan diff",
  prompt: "Read /home/claude/minds-doc/.agents/serp-diff/AGENT.md and follow it exactly.
           minds_doc_path: /home/claude/minds-doc
           minds_app_path: /home/claude/akane-asahi/minds-app
           publish: false"
)
```

**Option 2, as a named Claude Code subagent:** copy `AGENT.md` to `.claude/agents/serp-diff.md` (the frontmatter already has the format Claude Code expects), then start it with `subagent_type: "serp-diff"` and the same inputs in the prompt.

**Inputs** (all optional): `minds_doc_path`, `minds_app_path`, `plan_doc` (override which planning document to use), `focus` (narrow the scope, for example "result cards only"), `publish` (`true` commits and pushes `serp-diff.md` to this repo; default `false`).

## What it does about "latest"

It lists every candidate planning document in `Claude outputs/`, picks the highest version number (for example `v27`), cross-checks it against the document's own revision date and the commit date, and records the whole table in the brief. If the version number and the dates disagree, the brief says so at the top.

## What comes back

The agent writes `Claude outputs/serp-diff.md` and returns only a short note: the file path, which plan and which code commit were compared, the status counts, and the top three differences. It never edits `minds-app`.
