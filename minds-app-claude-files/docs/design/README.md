# Design mockups (visual reference for the UI sessions U0 to U4)

Copied from the thesis repo (`minds-doc`, `screenshots/`). The original Illustrator file
(`UI Explanation.ai`) stays there.

| File | Screen (name) | Used in |
|---|---|---|
| `00-workspaces-list.png` | Workspaces list (Baseline, reuse unchanged; reference only) | none |
| `01-plan-workspace-generated-directions.png`, `01-plan-workspace-copy.png` | Plan Workspace (two states; open both) | U1 |
| `02-serp-a.png`, `02-serp-b.png` | SERP (two states; open both) | U2 |
| `03-your-sessions.png` | Your sessions | U3 |
| `04-saved-all-sessions.png` | Saved results view, all sessions (its counts are wrong: see F6; it also shows only 2 session groups because the mockup's Session 2 had no saves, which the fixtures now fix) | U4 |
| `05-saved-single-direction.png` | Saved results view, one direction | U4 |
| `06-saved-single-session.png` | Saved results view, one session | U4 |

## How to use them

- Open the images for the screen you are building **before planning**, and say what you see
  (layout, hierarchy, spacing) in the plan.
- **The spec wins over the picture** where they differ. Known differences: the Plan Workspace mockups (`01-*`) still show the
  "What I want to find" field (removed 2026-10-22) and lack the "Set your search goal" heading; the mockups say "Project"
  (use "workspace"); the Your sessions tiles read `S2, S2, S1` (should be `S3, S2, S1`); some pale
  text fails AA contrast (see accessibility.md). **Your sessions (`03-*`) is built exactly as drawn**
  (Telot, 2026-10-17). Its only differences: "Workspace" for "Project", "0 saved" instead of the "+0" pill,
  a taller bar (22px, so `+N` is readable), the quiet grey label kept at AA contrast, and hidden text for
  screen readers on empty cards. If a picture shows something the spec does not mention, ask Telot; do not invent.
- Use the colours, fonts and tokens from `frontend/src/theme/` (Baseline), not colours sampled from the
  pictures.
