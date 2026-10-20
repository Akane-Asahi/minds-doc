# Plan screen: planning doc vs code

Generated: 2026-10-19 23:59 CST (Regina) by the plan-diff agent

## Summary

- 13 differences: **2 Major, 4 Stale doc, 4 Minor, 3 Open**.
- Most important: (1) the doc never says the LLM is asked for about half *new* angles (X1); (2) the doc says sub-goal generation uses "its most capable model" and queries a lighter one, but the code has one model setting for every call and the dev model is a "lite" one (X2); (3) the doc's flow for starting and returning to a project no longer matches the recorded 2026-10-19 flow: workspace dialog first, then Plan Workspace, and clicking a workspace opens Plan Workspace, not the project overview (X4, X6).
- The Plan screen itself is **Wired** (real route, real API, saved) but, per STATUS.md, not yet looked at in a browser.
- Most "stale doc" items come from decisions Telot recorded on 2026-10-19 (drag reordering, update/replace a plan, Explore saves onto an existing workspace) that the planning doc has not caught up with.

## What was compared

| | Source | Version |
|---|---|---|
| Planning document | `Telot Thesis Planning Documents v27.docx`, chosen because it has the highest version number (v27); other candidates (all v7): SRL Stripped-3, -2, -1, Restructured, SRL Stripped. No warnings from the helper. Doc header says "Project Revised: (Oct 15, 2026)". | minds-doc fc321d4, 2026-10-19 22:28 -0600, "Align sessions-diff with agents/ conventions" |
| Code | Akane-Asahi/minds-app, Plan Workspace | minds-app ba707ba, 2026-10-19 20:38 -0600, "Update index title to MINDS Academic Search" |
| Intent notes | STATUS.md, DECISIONS.md, docs/spec/F1-plan-workspace.md (also open-questions.md, 01-core.md) | same commit |

Both clones were brought up to date with `git pull --ff-only` before reading.

## Differences

| ID | Area | Planning doc says | Code does | Evidence | Severity | Suggested action |
|---|---|---|---|---|---|---|
| X1 | What the LLM is asked for | D2, D17: the LLM divides the goal into candidate sub-goals "based on what the searcher already knows and wants to find out". Nothing about new angles or how many. | Asks for about 8 directions, two kinds mixed: `familiar` and `new` (not mentioned, not covered by what they know). Aim for roughly half `new`; never fill a `new` slot with a restatement of what the searcher knows. Kind is stored, never shown on this screen. | `backend/llm/prompts.js:9-17`; `backend/config/constants.js:3`; F1 spec lines 131-136; DECISIONS 2026-10-16 "one mixed list" | Major | Update the doc (1.1 and Implementation Note): say the list is about eight directions, about half deliberately outside what the searcher already knows. This is the part that answers the persona's "favours what Jamie already knows". |
| X2 | Model used for generation | D9: sub-goal generation "is the step where the design uses its most capable model" (1.1 and Implementation Note). D10: queries use "a lighter, faster generative model". | One setting for all calls: `LLM_PROVIDER` / `LLM_MODEL` / `LLM_API_KEY`; no per-call model. Dev model is `gemini-3.5-flash-lite`. 01-core says the opposite default: "cheap, fast model; escalate only where testing shows" quality is not good enough, and 5.1 targets "fast model". Query generation (5.2) is not built yet. | `backend/llm/client.js:34-40`; DECISIONS.md:85; `docs/spec/01-core.md:94,102`; `backend/.env.example:30-34` | Major | Decide first. If the two-tier design stays in the thesis, the code needs a separate model setting for 5.1 (capable) and 5.2 (light). If one cheap model is the real plan, the doc's 1.1 sentence and Implementation Note must change. |
| X3 | Order of directions: can the searcher change it? | D6, D16: "The numbered order of the list is kept and used later" for ties; 2.1: ties follow "the order the searcher set in the planning screen, so the sub-goal Jamie prioritized appears first". The doc never says how the searcher sets the order. | Any card can be dragged to a new place (mouse, or touch press-and-hold). Row numbers are fixed slot labels. `orderIndex` = position among the selected cards in list order; the first selected card is the SERP default. | `frontend/src/features/planWorkspace/PlanWorkspaceScreen.jsx:97-148`; `useWiredPlanModel.js:16-20`; DECISIONS.md:38-54; F1 spec lines 74-88 | Stale doc | Update the doc (1.1): add that the searcher can drag directions to reorder them, and that the first selected one opens first on the results page. |
| X4 | Entry flow and screen name | D7, D11: Fig 1 caption "Screen 1 — Plan Your New Project"; 2.3 "If Jamie wants to change topic entirely, she returns to the first screen and creates a new project with its own goal and sub-goals". No workspace title step is described. | Flow is `/workspaces` -> "+ New Workspace" dialog (participant's own title) -> Plan Workspace at `/workspace/:workspaceId/plan`. Plan Workspace is only reachable for a workspace that already exists. Screen title is "Plan Your New Workspace". | `frontend/src/features/workspace/pages/WorkspaceList.jsx:707-708`; `PlanWorkspaceScreen.jsx:250`; DECISIONS.md:56-81; F1 spec lines 13-23 | Stale doc | Update the doc: 2.3 should say she returns to the workspace list and creates a new workspace (title first), then plans it. Caption wording is covered under Terminology. |
| X5 | Changing the plan after Explore | Not described. 1.1 treats the plan as made once at the start; 2.3 only covers adding sub-goals later from the results page. | Opening a workspace that already has a plan shows the full saved plan (texts and directions in saved order, all ticked). The searcher can edit, add, drag, tick and press Explore, which **replaces** the plan (`replace: true`, one transaction). Unchanged Explore writes nothing. A 409 shows "Open workspace Or Update workspace". | `useWiredPlanModel.js:171-214`; `backend/controllers/planController.js:44-89`; DECISIONS.md:7-36; F1 spec lines 25-38 | Stale doc | Update the doc (1.1 or 2.3): one sentence that the plan can be reopened and changed. Check the Keeping the Searcher in Control section agrees. |
| X6 | Where "returning to a project" goes | D12: on return "the Project Overview screen (Fig 5) shows the previous search activity" and Continue Last Activity. | Clicking a workspace on `/workspaces`, or Edit Workspace in its menu, opens **Plan Workspace**, not Your sessions. Open workspace there opens the SERP. Your sessions is not reachable from the real flow yet (I7). Cost recorded: one extra click to reach the SERP. | `WorkspaceList.jsx:407-412, 626-628`; DECISIONS.md:15-20; open-questions.md item 7; STATUS.md "Next" (I7) | Open | Decide first: is Plan Workspace a permanent stop on return, or a temporary route until I7 sends returning searchers to the overview? Then change the doc (Section 5) or the code (I7). |
| X7 | How many candidates | D3: "For Jamie, the list contains six candidates". | Asks for about 8; the server accepts 4 to 12 from the model. | `backend/config/constants.js:3`; `backend/schemas/directions.js:23-24` | Minor | Update the doc example to match (about eight, in the example), or say "six" is only illustrative. Fig 1 also shows six. |
| X8 | Third field label | D1, D7: "what they want to find out"; Fig 1 label "What I want to find out". | Label is "What I want to find" (helper line still says "find out"). Chosen on purpose: "Label wording follows F1, not the mockup". | `PlanWorkspaceScreen.jsx:16,19`; DECISIONS.md:306 | Minor | Decide first (one word): doc and mockup say "find out"; code and F1 say "find". Pick one and change the other side. |
| X9 | Add-direction control label | D5: "Add search direction" (1.1 and Fig 1). | Button reads "Add Search directions" (plural, capital S), also by decision. Your sessions mockup uses "+ Add search direction". | `PlanWorkspaceScreen.jsx:374`; DECISIONS.md:306; F1 spec line 55 | Minor | Decide first: the code probably needs changing to the singular so Plan Workspace and Your sessions match the doc. |
| X10 | Where query generation happens | D15 (Task List, Oct 5 - Nov 5): "Implement the planning screen: ... LLM-based sub-goal generation and selection, and LLM-based query generation for each selected sub-goal." D18 (1.2): query is generated "the first time the searcher opens a sub-goal". | Plan Workspace only calls 5.1 (directions). No query is generated on this screen. 5.2 runs once, on a direction's first selection on the results page, then is stored (not built yet, I2). | `backend/controllers/searchDirectionsController.js:23-48`; `backend/llm/prompts.js:46` (only directions and scoring prompts exist); DECISIONS.md:212-224 | Minor | Update the doc's Task List item so the planning screen does only direction generation and selection; move query generation to the results-page item. |
| X11 | What Explore does | D1/D4 stop at "Jamie decides which of these to work with". The Explore button is in the Fig 1 image but never described. | Explore needs all three fields and at least one selected direction. It saves the three texts and **only the selected** directions (unselected AI suggestions are discarded) on the existing workspace, in list order, then opens the SERP. | `PlanWorkspaceScreen.jsx:178,386-407`; `backend/controllers/planController.js:44-89`; `backend/schemas/plan.js:20-27`; F1 spec lines 109-120 | Stale doc | Update the doc (1.1): say Explore saves the chosen directions and opens the results page on the first one; unchosen candidates are not kept. |
| X12 | Replacing a plan vs saved results | Not mentioned. | Update/replace deletes all directions and inserts new ones, so every direction gets a new `_id`. Safe today (no saved results exist yet). Once saves exist (I3) a replace would orphan them. Recorded, not built. | `planController.js:70-71`; open-questions.md item 9; STATUS.md line 38 | Open | Code needs changing before I3 (keep directions that have saved results). No doc change. |
| X13 | Reordering without a mouse | D6, D16 imply any searcher can set the order. | No keyboard reordering; touch needs press-and-hold. Recorded as a known gap awaiting Telot's decision. | DECISIONS.md:53-54; open-questions.md item 8; F1 spec line 88, 170 | Open | Decide first: build keyboard reordering (code) or accept that order is optional and say so in the doc. Matters because the doc makes the order meaningful for tie-breaking. |

## Matches

- First screen has three inputs: search goal, what I already know, what I want to find. (1.1; `PlanWorkspaceScreen.jsx:13-17`)
- The LLM generates the candidate list from the three inputs; generation is wired to a real endpoint with structured, Zod-validated output. (`searchDirectionsController.js`, `schemas/directions.js`)
- The searcher chooses: AI suggestions start unselected, nothing is saved unless ticked; the searcher can add their own directions. (1.1, Keeping the Searcher in Control; F1 spec lines 90-98)
- The LLM only proposes; nothing joins the plan on its own. (Keeping the Searcher in Control)
- Fig 1 layout (checked by image order: Fig 1 is `word/media/image1.png`, same as `docs/design/01-plan-workspace-generated-directions.png`): header logo and person icon, three fields, "Search directions" with the three-arrow icon, numbered two-column list, sparkle on AI rows, dashed add box, full-width "Explore →" button. Code follows this layout.
- Order is stored as `orderIndex`, and the spec's tie rule uses `orderIndex` (F3 spec lines 24, 34; `frontend/src/features/serp/minds/buildPills.js:5`). Ranking itself is not wired yet (I2/I3), so the doc's later tie-break is spec-level only.

## In code, not in the planning doc

- Generation trigger: runs on blur once all three fields are filled; nothing happens if any is empty; same normalized text sends nothing; a newer request aborts the older one. (`useWiredPlanModel.js:97-136`)
- Regeneration when inputs change: selected and custom cards keep their slots, only unselected AI cards are replaced. (`frontend/src/features/planWorkspace/directionList.js:38-60`)
- Each AI direction has a "Why?" button showing a one-sentence rationale, and a sparkle meaning "Suggested by AI". (`DirectionRow.jsx:82-93`)
- Custom directions can be edited and removed; AI ones can only be ticked or unticked. (`DirectionRow.jsx:95-103`)
- Every direction label is at most 7 words, with an "N of 7 words" counter. (`directionLabel.js`, `PlanWorkspaceScreen.jsx:364`)
- Explore disabled with a visible reason until three fields and one direction; double-click saves once. (`PlanWorkspaceScreen.jsx:176-182,386-412`)
- Failure state: inline error with Retry; the searcher can continue with custom directions only. (`PlanWorkspaceScreen.jsx:295-304`)
- Rate limit of 10 generate requests a minute per participant; 12 s LLM timeout; provider errors never reach the browser as 401/403. (`backend/config/constants.js:9-11`, `searchDirectionsController.js:12-17`)
- A plan is written once unless `replace: true`; double submit fails safely on a unique index. (`planController.js:60`, `backend/models/subGoalModel.js:44`)
- Scores are not repeatable at temperature 0 (smoke test); relevant to the doc's "temperature 0 ... to keep ratings as consistent as possible" but not a Plan screen difference. (DECISIONS.md:90-94)

## In the planning doc, not in code

- Nothing on the Plan screen itself is promised by the doc and missing in code, except the model tiering (X2) and, indirectly, that the sub-goals "stay on screen as the reference for the rest of the project" (1.1): Plan Workspace is not shown later; the SERP right panel and Your sessions carry the list. That panel is mock-only until I3 and is outside this brief.

## Needs a browser, a live call or Telot's decision

- Whether the page looks and behaves as Fig 1 in a real browser (STATUS.md: "not yet looked at in a browser"); column 2 layout, drag feel, the end slot, touch.
- Whether 5.1 with the dev model really gives about half `new` angles of acceptable quality; the smoke test says labels differ every run (open-questions.md).
- Decisions: X2 (one model or two), X6 (where returning searchers land), X8 and X9 (labels), X13 (keyboard reordering).
- F1 spec says "Out of scope: Editing directions after Explore" (line 174), but the Update/replace flow does exactly that. Spec inconsistency inside minds-app; Telot to say which stands.
- Where "start a new project" lives: the doc (2.3) lists it as always available; open-questions.md says the location of Start New Workspace is open (Workspaces list assumed).

## Terminology

The doc uses project / sub-goal / possible new sub-goal / Screen 1 ("Plan Your New Project"); code and UI use workspace / search direction (`subGoal` in code) / new direction (`emergingDirection`) / Plan Workspace ("Plan Your New Workspace"). This is intentional (CLAUDE.md vocabulary) and is reported once here; it is not counted in the differences, including the Fig 1 caption and the title shown in the Fig 1 image.

## Doc claims checked

| ID | Section | Claim |
|---|---|---|
| D1 | 1.1 Planning: Goal Decomposition | On the first screen the searcher enters a search goal, what they already know, and what they want to find out |
| D2 | 1.1 | From these three inputs an LLM generates a list of candidate search directions (sub-goals) |
| D3 | 1.1 | For Jamie the list contains six candidates |
| D4 | 1.1 | "Jamie decides which of these to work with" |
| D5 | 1.1 | Jamie can add sub-goals of their own "with Add search direction" |
| D6 | 1.1 (also 2.1, 3) | The numbered order of the list is kept and used later to rank sub-goals that match a result equally |
| D7 | Fig 1 caption and image | "Screen 1 — Plan Your New Project"; three labelled fields, six rows, "Add search direction", Explore button |
| D8 | 1.1 | LLM proposes, searcher decides; the sub-goals stay on screen as the reference for the rest of the project |
| D9 | 1.1, Implementation Note | Sub-goal generation uses the most capable model |
| D10 | 1.2, Implementation Note | Query generation uses a lighter, faster model |
| D11 | 2.3 Switching and Adding Sub-Goals | To change topic entirely she "returns to the first screen and creates a new project with its own goal and sub-goals" |
| D12 | 5 Cross-Session Support | On return the Project Overview screen shows previous activity; searcher can "return to the project list and start a new project" |
| D13 | Keeping the Searcher in Control | In planning the LLM offers candidates; Jamie chooses which to work with and can add others |
| D14 | Keeping the Searcher in Control | The system "does not choose the next step" |
| D15 | Task List, Oct 5 - Nov 5 | Planning screen: three inputs, LLM sub-goal generation and selection, and LLM query generation for each selected sub-goal |
| D16 | 2.1 | Tags with equal ratings follow "the order the searcher set in the planning screen" |
| D17 | Abstract | An LLM divides the goal into candidate sub-goals based on what the searcher knows and wants to find out |
| D18 | 1.2 | The first time a sub-goal is opened, the LLM generates one query; later visits reuse the stored query |
| D19 | Fall 2026 Goals, item 2 | By November 5 the MVP includes planning (met on the Plan screen: wired as of 2026-10-19) |

## Method and limits

- Read statically only: the whole planning doc (pandoc text of v27), STATUS.md, DECISIONS.md, F1 spec, parts of 01-core.md, open-questions.md, build-plan.md, the backend plan, directions, LLM and route files, and the `planWorkspace` frontend files, plus the entry-flow code in `WorkspaceList.jsx` and the router. Test names were read as supporting evidence only. No tests run, no browser, no LLM call, `.env` not read.
- Fig 1 image matched by order in the document (image1.png) and compared with the mockup in `docs/design/`; the other doc figures were not checked (outside the Plan screen).
- Not checked: `stack_changed.md` and `docs/spec/03-api.md` in detail; the Fig 2 onward SERP, sessions and saved views (other diff agents cover them).
- Out of scope but noticed: the doc's Task List (Oct 5 - Nov 5) still describes SERP ratings as "embedding-based cosine similarity ... 1-5 stars", while the body of the doc and the code use an LLM rating of 0 to 5. Worth a separate fix in the doc.
- Nothing failed. This file is written but not pushed, as requested.
