---
name: serp-diff
description: Compares what the SERP screen does in the minds-app code on GitHub with what the latest thesis planning document in Claude outputs says about it, then writes a full difference brief to serp-diff.md. Read-only on both sources. Use when the planning doc or the SERP code has changed, or before updating either.
tools: Bash, Read, Glob, Grep, Write
---

You are the serp-diff agent. Your full instructions are in `agents/serp-diff/AGENT.md` in this repository (Akane-Asahi/minds-doc). Read that file now, in full, and follow it exactly. Ignore its frontmatter. If your prompt overrides any input (doc folder, output file, push or not, focus), use the override; otherwise use the defaults in that file.

This file is only a pointer so Claude Code can find the agent by name. Do not put instructions here; they belong in `agents/serp-diff/AGENT.md` so there is one copy.
