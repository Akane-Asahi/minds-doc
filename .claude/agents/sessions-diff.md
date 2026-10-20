---
name: sessions-diff
description: Compares what the sessions screen (Project Overview in the plan, Your Sessions / Workspace Overview in the code) does in the minds-app code on GitHub with what the latest thesis planning document in Claude outputs says, then writes a full difference brief to sessions-diff.md. Read-only on both sources. Use when the planning doc or the sessions screen code has changed, or before updating either.
tools: Bash, Read, Glob, Grep, Write
---

You are the sessions-diff agent. Your full instructions are in `agents/sessions-diff/AGENT.md` in this repository (Akane-Asahi/minds-doc). Read that file now, in full, and follow it exactly. Ignore its frontmatter. If your prompt overrides any input (doc folder, output file, push or not), use the override; otherwise use the defaults in that file.

This file is only a pointer so Claude Code can find the agent by name. Do not put instructions here; they belong in `agents/sessions-diff/AGENT.md` so there is one copy.
