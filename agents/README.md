# agents/

Subagents for the MINDS thesis work. Each agent has one folder with its instructions in `AGENT.md`, so any other agent can read the file and run it.

| Agent | What it does | Writes |
|---|---|---|
| [plan-diff](plan-diff/AGENT.md) | Compares the Plan screen in the `minds-app` code with the latest planning document in `Claude outputs/` and lists every difference | `Claude outputs/plan-diff.md` |
| [serp-diff](serp-diff/AGENT.md) | Same comparison for the SERP screen (results page, result cards, directions panel, saving), plus drift between the planning document and the in-repo spec | `Claude outputs/serp-diff.md` |
| [save-diff](save-diff/AGENT.md) | Same comparison for the Saved results screens (all results, one direction, one session, and the buttons that lead there), including the planning document's Fig 3 and Fig 4 and whether the view is wired or mock-only | `Claude outputs/save-diff.md` |
| [sessions-diff](sessions-diff/AGENT.md) | Same comparison for the sessions screen (called Project Overview in the plan, Your Sessions / Workspace Overview in the code), including the Sessions panel, the per-session progress bars, the in-repo spec, and whether the screen is wired or mock-only | `Claude outputs/sessions-diff.md` |

serp-diff, save-diff and sessions-diff reuse `plan-diff/find_latest_plan_doc.py` to pick the newest planning document. To run any of them, use the same prompts as plan-diff below with `serp-diff`, `save-diff` or `sessions-diff` in place of `plan-diff` (for example `Agent(subagent_type: "serp-diff", prompt: "Run the serp-diff agent with its defaults.")`). Both accept `focus: <part of the screen>` to narrow the scope. save-diff also has `save-diff/extract_plan.sh`, which turns the planning document into text and extracts its figures so the agent can look at Fig 3 and Fig 4.

## Keeping the docs in step with the code: doc-sync

The four diff agents compare the code with the planning document as it is now. [doc-sync/](doc-sync/README.md) records what changed and why as it happens: a change ledger and a sync marker in `Claude outputs/`, a `/done` skill, a Stop hook and a commit-msg hook for minds-app, and `which-diff.py`, which says which of these agents to run for the work done since the planning document was last synced.

## Layout

```
agents/
  README.md                      this file
  <agent-name>/
    AGENT.md                     the full instructions (the only copy)
    <helper scripts>             deterministic steps the agent calls
.claude/agents/<agent-name>.md   one-paragraph pointer so Claude Code can find the agent by name
```

Keep one copy of the instructions. Edit `AGENT.md`; leave the pointer alone.

## Running plan-diff from another agent

The agent does not see your conversation, so the prompt can be short. It fetches both repos itself and picks the newest planning document by version number (v27 beats v7).

**A. In a Claude Code session whose repo is `minds-doc`** (the pointer is found automatically):

```
Agent(subagent_type: "plan-diff",
      description: "Plan screen doc vs code",
      prompt: "Run the plan-diff agent with its defaults.")
```

**B. From any other session** (works wherever a general-purpose agent can run):

```
Agent(subagent_type: "general-purpose",
      description: "Plan screen doc vs code",
      prompt: "Clone Akane-Asahi/minds-doc (shallow), read agents/plan-diff/AGENT.md
               and follow it exactly. Use its defaults.")
```

**C. By hand:** open `agents/plan-diff/AGENT.md` and follow it step by step.

### Optional overrides (put them in the prompt)

| Override | Example prompt text | Default |
|---|---|---|
| Do not push | "Do not push; just write the file." | commits and pushes only `plan-diff.md` to minds-doc |
| Other output path | "Write the brief to `Claude outputs/plan-diff-2.md`." | `Claude outputs/plan-diff.md` |
| Other folder | "The planning documents are in `<folder>/`." | `Claude outputs/` |

### What it needs

- Network access to GitHub (`Akane-Asahi/minds-doc` and `Akane-Asahi/minds-app`); both are cloned shallow.
- `python3` and `pandoc` (pandoc is optional; the agent falls back to reading the `.docx` XML).
- Push access to `minds-doc` only if it should push the brief. It never pushes to `minds-app` and never edits the planning document or the code.

### What you get back

A short message (planning document used, counts by severity, top three differences, file location) and the full brief in `Claude outputs/plan-diff.md`. Each run replaces that file; older versions stay in git history.
