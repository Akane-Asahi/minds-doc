# agents/

Subagents for the MINDS thesis work. Each agent has one folder with its instructions in `AGENT.md`, so any other agent can read the file and run it.

| Agent | What it does | Writes |
|---|---|---|
| [plan-diff](plan-diff/AGENT.md) | Compares the Plan screen in the `minds-app` code with the latest planning document in `Claude outputs/` and lists every difference | `Claude outputs/plan-diff.md` |

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
