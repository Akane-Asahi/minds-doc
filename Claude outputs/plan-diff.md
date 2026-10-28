# Plan screen: planning doc vs code

Generated: 2026-10-28 09:20 CST (Regina) by the plan-diff agent

## Summary

- 11 differences: **2 Major, 4 Stale doc, 4 Minor, 1 Open**. Counts follow the severity rules in the agent file.
- **Workspace name (X1, Major):** the doc says the new-workspace screen opens with the title field ready and "the title can be left empty". In the code the Workspace name field is required: Explore stays off until it is filled in.
- **Model tiers (X2, Major):** the doc says sub-goals use "its most capable model" and queries a lighter one. The code has one model setting for every call, and the development model is `gemini-3.5-flash-lite`.
- **Three behaviours the code changed after the doc was synced (X3, X4, X5, Stale doc):** the screen autosaves a draft before Explore; removing a sub-goal that has saved results now asks and can delete those results; the Overview now shows one list in plan order (ticking never moves a card). The code comments name Telot (2026-10-26) or Orland (2026-10-27) as the source. DECISIONS.md and STATUS.md stop at 2026-10-25, so these are recorded only in code comments.
- Most of what v30 says about this screen matches the code: the two fields, blur trigger and regeneration rule, 16 asked and 8 shown with a reserve, Generate more up to 30, Add Custom, drag to reorder, the Why? card, the marks, Explore saving every sub-goal, reopening a saved plan. See Matches.
- The Plan screen is **Wired**, but STATUS.md says it has not been looked at in a browser. Look-and-feel matches below come from the code, not from a browser.

## What was compared

| | Source | Version |
|---|---|---|
| Planning document | Telot Thesis Planning Documents v30.docx, chosen because highest version number v30; other candidates: v29, v27, and five v7 files (the helper reported no warnings) | minds-doc 4fa3494 2026-10-26 00:00 -0600 "v30: bring text in line with minds-app 2f08f2c ..." |
| Code | Akane-Asahi/minds-app, Plan Workspace (frontend and backend) | minds-app 533d618 2026-10-27 15:31 -0600 "SERP: one page scroll; ..." |
| Intent notes | STATUS.md, DECISIONS.md, docs/spec/F1-plan-workspace.md, open-questions.md, CLAUDE.md. They are not inside the minds-app clone; they are in minds-doc/minds-app-claude-files/ | minds-doc 4fa3494; STATUS.md says "Last updated 2026-10-25" |

Sync marker: `doc-sync.json` says v30 was written against minds-app 2f08f2c (2026-10-26). The minds-app clone is shallow, so I could not list what changed between 2f08f2c and 533d618. Several differences below are changes after that point.

## Differences

| ID | Area | Planning doc says | Code does | Evidence | Severity | Suggested action |
|---|---|---|---|---|---|---|
| X1 | Workspace name on the Plan screen (D29) | 2.3: a new workspace's first screen "opens with the title field ready to type in (the title can be left empty and changed later)". 1.1 names only two inputs | A third field, "Workspace name", sits above Search goal, with a red star and `aria-required`. It opens empty and focused for a new workspace. Leaving it empty shows "Workspace name is required", and Explore stays disabled with "Still needed: Workspace name". A duplicate name is refused (409). The workspace itself is created as "Untitled workspace" first, and on a later visit the field shows that name, so it passes | PlanWorkspaceScreen.jsx:215-218, 234-241, 341-358; PlanWorkspacePage.jsx:16-21, 35-36; WorkspaceList.jsx:646-668; PlanWorkspaceScreen.test.jsx:209; change-ledger 7e3042e says "can be left empty" with no reason | Major | Decide first: required (update doc and ledger) or optional (update code) |
| X2 | Model used for sub-goal generation (D19, D28) | 1.1 and Implementation Note: sub-goal generation "uses its most capable model"; 1.2: queries use "a lighter, faster model" | One `LLM_MODEL` setting is read for every call. No call picks its own model; only timeouts differ per call. The recorded development model is `gemini-3.5-flash-lite`. The study model is not chosen | backend/llm/client.js:3, 35; searchDirectionsController.js:33-38; config/constants.js:12-18; DECISIONS.md:128; open-questions.md item 1; stack_changed.md:30 | Major | Decide first: add a per-call model setting, or reword the doc to say the design intends two tiers |
| X3 | What is saved before Explore (D13, D18) | 1.1: "Pressing Explore saves the two texts and all the sub-goals". Nothing is saved before it | A draft is autosaved 400 ms after any change (and when leaving the page) once both texts are filled and at least one sub-goal exists, even with none ticked. So a plan exists before Explore, and reopening the page shows "Saved plan loaded. Edit it, then press Explore." Errors are silent. Explore waits for a save in progress, and writes nothing if the loaded plan is unchanged | useWiredPlanModel.js:15, 127-167, 229, 322-352; schemas/plan.js:30-36; PlanWorkspacePage.test.jsx:741 | Stale doc | Update doc; add the decision to DECISIONS.md (only the code comment "Telot, 2026-10-26" records it) |
| X4 | Removing a sub-goal that has saved results (D17) | 1.1: such a sub-goal "is never lost by removing or renaming it: it comes back unticked at the end of the list" | Renaming still works as the doc says (the old wording is kept unticked at the end). Removing now opens "Remove X? ... also removes those results from your saved list. This cannot be undone." with "Keep it" and "Remove it and its saved results". Confirming deletes the sub-goal and its saved results, scores, stored query and shown-result rows | PlanWorkspaceScreen.jsx:272, 410-423; useWiredPlanModel.js:101, 378-382; planController.js:17-23, 50-71; schemas/plan.js:32-34; PlanWorkspacePage.test.jsx:832; open-questions.md item 9 still says "kept, unselected" | Stale doc | Update doc (code comment cites Telot, 2026-10-26); update open-questions 9 |
| X5 | Overview list order and ticking (D15) | 1.1 and 5: the Overview "lists the selected sub-goals first and the unselected ones below them"; under All they sit under "Selected Directions" and "Unselected directions" | One list in plan order, ticked or not. Ticking only flips the flag; the card does not move. The list can be dragged to reorder (PUT /subgoals/order). The All and Explored tabs are switched off (`SHOW_DIRECTION_TABS = false`) and an Explore button takes their place. The last ticked sub-goal cannot be unticked (matches the doc) | sessionsModel.js:181-188; YourSessionsScreen.jsx:75, 122-125, 139-152, 175; planController.js:201-206, 237-271; v30-changes-summary.md:111 (item 7) is also out of date | Stale doc | Update doc. Orland, 2026-10-27 is named in code comments only. The tabs and header changes belong to sessions-diff |
| X6 | Mark for a reworded proposal (D24) | 1.1: a black four-pointed star for an LLM proposal, "a black person icon for one that Jamie added or edited" | Three marks. Star = LLM proposal. Person = typed by Jamie. Person beside the sparkle = an LLM proposal Jamie reworded (`aiEdited`), with the hover and screen-reader text "AI generated the sub-goal, and then it was edited". It follows the name on every screen | DirectionRow.jsx:30-56; planModels.js:27-35; schemas/plan.js:17, 74; subGoalModel.js:40; ledger a52ed50 says edited gets the person icon | Minor | Update doc (one clause), or decide to drop the third mark |
| X7 | Screen title (D2) | Fig 1 caption: "Screen 1 - Plan Your New Workspace" | The visible heading is "Plan your search" (h2, beside the breadcrumb). "Plan Your New Workspace" is a visually hidden h1. The list heading reads "Sub-Goals". F1 spec still says there is no visible title and a heading "Set your search goal", which is out of date | PlanWorkspaceScreen.jsx:325-332, 388-390; F1-plan-workspace.md:45 | Minor | No action, or change the caption to the visible heading when Fig 1 is redone |
| X8 | Exact counts and the reserve (D6, D9) | 1.1: "sixteen candidates in one call ... shows eight of them, keeping the other eight in reserve" | The prompt asks for "about 16" and the server accepts 8 to 20, so the split is 8 shown plus whatever is left. The reserve lives in page state only: after a reload or reopening a saved plan the first Generate more calls the model | prompts.js:12; schemas/directions.js:22-23; config/constants.js:3-4; useWiredPlanModel.js:9-10, 102, 196-198, 219, 278-286 | Minor | Update doc to "about sixteen"; optionally add one clause on the reserve |
| X9 | Fig 1 picture (D33) | Fig 1 (image1.png, matched by order) shows "Plan your new project", three fields including "What I want to find out", a "Search directions" heading, a star on every row, a dashed "Add search direction" and no Edit, Remove or "?" | Two text fields plus Workspace name, "Plan your search" with a breadcrumb, Generate more and Add Custom buttons, Edit and Remove on every row, a "?" badge on proposals, black marks | PlanWorkspaceScreen.jsx:15-18, 325-390, 245; DirectionRow.jsx:191-236; image1.png; v30-changes-summary.md:89, 119 already lists Fig 1 as old | Stale doc | New screenshot from the code (already on the v30 to-do list) |
| X10 | Keyboard reordering (D8) | 1.1: Jamie "can drag any sub-goal to a new place in the list" | Mouse (after 6 px) and touch (after a 250 ms hold) only. No keyboard way to reorder; the doc does not say so | PlanWorkspaceScreen.jsx:30-35, 131-134; STATUS.md:79 and open-questions.md item 8 list it as needing Telot's decision | Open | Decide first (before the study); then add a sentence to the doc or build it |
| X11 | Wording on screen (terminology) | The doc uses "sub-goal" throughout, plus "search direction" for the results-page button | The screen mixes both. "Sub-Goals", "Type a sub-goal" and "Cancel adding a sub-goal" sit beside "Search directions ready", "Choose at least one search direction", "Edit search direction: ..." and the idle hint "search directions will appear here" | PlanWorkspaceScreen.jsx:21-26, 240, 388-397; DirectionRow.jsx:272; GenerateOrAddBar.jsx:100, 115 | Minor | Decide first which word participants see, then make the screen consistent |

## Matches

- Two inputs, Search goal and What I already know, feed the LLM (D1, D3). The LLM sees only those two texts (prompts.js:18).
- Generation starts when a field is left with both filled and the (trimmed, whitespace-collapsed) texts changed (D4). The sub-goal list stays hidden until the first generation starts.
- A new run keeps ticked and own sub-goals in their slots and replaces only unticked proposals (D5). Kept labels are sent so the model does not repeat them.
- Every proposal is an angle the searcher has not mentioned (D7): prompt rule plus the server stamping every direction as new.
- Generate more takes the next item from the reserve with no model call, asks for a new batch only when the reserve is empty or outdated, stops at 30 (D9). Added items start unticked (D10). Generate more is hidden while the Add Custom box is open (D11).
- Drag to reorder, across both columns (D8). Order is stored for all sub-goals and used for ties on result tags (D12; tie-break reads `orderIndex`, not run).
- Explore saves both texts and every sub-goal, ticked or not, in list order, and opens the results page on the first ticked one (D13). Only ticked ones are searched (D14).
- Unticked sub-goals come back unticked on reopening (D16). A saved plan is shown on reopening; changed, Explore replaces it; unchanged, it writes nothing (D18).
- Why? button: round "?" on the right edge, shown on hover or keyboard focus and always on touch screens; opens a card above the sub-goal with an arrow, one sentence, closed by its cross, Esc or a click outside (D20, D21). The sentence comes with the proposal, no extra call (D22). Own sub-goals have none (D23). The reason is stored with each proposal and returns on reopening (D26).
- Edit and Remove on every sub-goal; an edited proposal becomes Jamie's own and loses its "?" (D25).
- The LLM proposes and Jamie chooses; no proposal is ticked by default and Explore needs at least one ticked by Jamie (D27).
- New workspace: the screen opens with the name field focused and its hint typed out (D29, first half only; the "can be left empty" half is X1).
- Overview: Generate more and Add Custom as on this screen, both unticked (D31).

## In code, not in the planning doc

- 7-word limit on every sub-goal label, with a screen-reader count; a pasted longer text is cut to 7 (directionLabel.js:2-21; GenerateOrAddBar.jsx:109-114; schemas/plan.js:10).
- Explore stays disabled with a visible reason until Workspace name, both fields and at least one ticked sub-goal are present (PlanWorkspaceScreen.jsx:234-241, 495-499).
- Loading states: eight shimmer cards, "Updating search directions...", "Finding one more search direction. This can take up to 30 seconds." (PlanWorkspaceScreen.jsx:232, 425-430, 447-459).
- Error box with Retry; a 429 says "Too many requests"; the generate endpoint allows 10 requests per minute per participant (PlanWorkspaceScreen.jsx:399-408; useWiredPlanModel.js:58-61; config/constants.js:11).
- A batch that arrives while a card is being dragged waits until the drop (useWiredPlanModel.js:199-202, 355-363).
- Opening a workspace that already has a plan loads it at once; the "Open workspace Or Update workspace" row appears if Explore answers 409 or Jamie typed first (useWiredPlanModel.js:63-66, 248-260).
- Duplicate labels (case-insensitive) are dropped when saving; 30 sub-goals is the hard limit on the server (schemas/plan.js:6, 60-70).
- Add Custom, Generate more and Overview ticking all enforce limits with messages ("No new search directions this time", "Keep at least one search direction selected.") (useWiredPlanModel.js:306-309; planController.js:224-226).
- Autosave (X3), delete-with-results question (X4), Overview reordering (X5), third mark (X6): see the table.
- The dev-only `/ui/plan-workspace` preview uses fixtures and is not on the real route (UIDevRoutes.jsx:101-113; router/index.js:24-28). This is **UI only**; the real route `/workspace/:workspaceId/plan` is **Wired** (router/index.js:98).

## In the planning doc, not in code

- Two model tiers, a most-capable model for sub-goals and a lighter one for queries (X2).
- "The title can be left empty" (X1).
- "A sub-goal with saved results is never lost by removing it" (X4).
- Overview lists selected sub-goals first and unselected below (X5).
- Fig 1 as drawn (X9).

Everything else the doc says about this screen was found in the code.

## Needs a browser, a live call or Telot's decision

- Telot: X1 (name required or optional), X2 (one model or two tiers; the study provider is also open, open-questions 1), X10 (keyboard reordering), X11 (which word the screen uses), and whether X6's third mark stays.
- Browser: where the Why? card sits and whether its arrow points at the "?"; the hover, focus and touch behaviour of the "?"; the drag line and end slot; layout of the two columns. STATUS.md says none of this has been checked in a browser.
- Live model call: whether a real run gives about 16 proposals, all new angles, with one-sentence reasons; the quality of proposals 9 to 16 (unmeasured per STATUS.md).
- Ties on result tags still follow plan order now that the Overview can reorder: the code passes `orderIndex` to the tag builder (mindsSerp/serpModel.js:89), but I did not trace the sort or run it.

## Terminology

Planning document / AGENT table: project = workspace; sub-goal = search direction (UI) = `subGoal` (code); possible new sub-goal = new direction = `emergingDirection`; Screen 1 / first screen / "Plan Your New Project" = Plan Workspace ("Plan Your New Workspace"). The doc already says workspace and "Plan Your New Workspace". One thing differs from the AGENT table: the screen no longer follows "search direction in the UI" consistently. Headings and placeholders say "Sub-Goals" and "sub-goal", and the Overview now says "Sub-goals" and "New sub-goals", while status and error text still say "search direction" (X11). The doc's "New directions" section name on the Overview no longer matches the Overview's "New sub-goals" heading (YourSessionsScreen.jsx:372); that belongs to sessions-diff.

## Doc claims checked

| ID | Section | Claim |
|---|---|---|
| D1 | 1.1, Abstract | The first screen asks for a search goal and what the searcher already knows |
| D2 | Fig 1 caption | "Screen 1 - Plan Your New Workspace" |
| D3 | 1.1 | From the two inputs an LLM generates candidate sub-goals |
| D4 | 1.1 | Generation starts when either field is left with both filled and one changed |
| D5 | 1.1 | A new run replaces only proposals Jamie has not ticked; ticked and own stay |
| D6 | 1.1 | Sixteen candidates in one call, eight shown, eight in reserve |
| D7 | 1.1, Abstract | Every candidate is an angle the searcher has not mentioned |
| D8 | 1.1 | Jamie chooses, adds own with Add Custom, asks for another with Generate more, drags to set order |
| D9 | 1.1 | Generate more takes from the reserve, asks the LLM only when it is empty, up to 30 in all |
| D10 | 1.1 | A sub-goal added by either button starts unselected |
| D11 | 1.1 | While Jamie types a custom sub-goal, Generate more is hidden |
| D12 | 1.1, 2.1, 3 | The numbered order is kept and used to rank sub-goals when a result matches several equally |
| D13 | 1.1 | Explore saves both texts and all sub-goals, selected or not, in that order, and opens the results page on the first selected one |
| D14 | 1.1 | Only the selected sub-goals are searched, rated and shown on the results page |
| D15 | 1.1, 5 | The Overview lists selected sub-goals first and unselected below; each card has a tick; at least one stays selected |
| D16 | 1.1 | An unselected candidate comes back unticked when the plan is reopened |
| D17 | 1.1 | A sub-goal with saved results is never lost by removing or renaming it; it returns unticked at the end |
| D18 | 1.1 | A saved plan can be reopened and changed; Explore replaces it, or writes nothing if unchanged |
| D19 | 1.1 | Sub-goal generation is the step that uses the design's most capable model |
| D20 | 1.1 | Each LLM candidate has a "Why?" round "?" on the right edge, on hover or focus, always visible on touch |
| D21 | 1.1 | It opens a small card above the candidate, with an arrow and one sentence; closes by cross, Esc or outside click |
| D22 | 1.1 | The LLM writes the reason in the same step as the candidate, so no further call |
| D23 | 1.1 | A sub-goal Jamie adds has no "Why?" and no reason |
| D24 | 1.1 | A black four-pointed star marks an LLM proposal, a black person icon one Jamie added or edited, on every screen |
| D25 | 1.1 | Jamie can edit or remove any sub-goal; an edited proposal becomes Jamie's own and loses its "Why?" |
| D26 | 1.1 | The reason is kept with each proposal, selected or not, and returns on reopening |
| D27 | Keeping the Searcher in Control | The LLM offers candidates each with "Why?"; Jamie chooses and can add others |
| D28 | Implementation Note | Sub-goal generation warrants a capable generative model; query generation a lighter one |
| D29 | 2.3 | A new workspace's first screen opens with the title field ready; the title can be left empty |
| D31 | 5 | On the Overview, Generate more and Add Custom work as on the first screen and add unselected |
| D32 | Task List, Fall goals | Planning screen with goal and prior-knowledge input, LLM generation and selection, is part of the MVP due Nov 5 |
| D33 | Fig 1 image | The figure shows the screen as designed on 2026-10-20 |

(D30 is not used.) D32 is not a behaviour claim: the screen is built and wired, so the task is met in code; whether it was confirmed in informal use is not something code can show.

## Method and limits

- Read in full: AGENT.md; the v30 text (pandoc to plain text, whole document, then every passage on the first screen, the Overview parts that depend on the plan, Keeping the Searcher in Control, the Implementation Note, Task List and Fall goals); `image1.png` (Fig 1, matched to the figure by order in `document.xml`).
- Code read statically: all files in `frontend/src/features/planWorkspace/` (screen, rows, bar, model hooks, list rules, API, page), `PlanWorkspacePage.jsx`, the New Workspace flow in `WorkspaceList.jsx`, router, `backend/controllers/planController.js`, `searchDirectionsController.js`, routes, `schemas/plan.js`, `schemas/directions.js`, `subGoalModel.js`, `workspaceModel.js`, `config/constants.js`, `llm/prompts.js`, `llm/client.js`, `llm/providers/gemini.js`, the Overview's list and tick code, and test names in the three Plan test files. `.env` was not read; the model name comes from DECISIONS.md and stack_changed.md.
- Not done: no tests run, no server, no browser, no LLM call. Test names were used as supporting evidence only. One test title, "no icon marks them as AI" (PlanWorkspaceScreen.test.jsx:14), contradicts the code's star marks, so that test is either out of date or failing; I did not run it.
- The minds-app clone is shallow (one commit), so I could not see what changed since 2f08f2c.
- minds-app does not contain STATUS.md, DECISIONS.md or the F1 spec; I used the copies in minds-doc/minds-app-claude-files/. They are older than the code: F1 still says there is no name field, no visible title and "no sparkle or star icon", which the code no longer follows. For X3, X4 and X5 the only record found is a dated code comment.
- Noticed outside this screen and left to the other diff agents: the results-page tag cap (`CHIP_COUNT` comment in config/constants.js:7 says every sub-goal scored above 0 is a tag, "no cap since 2026-10-27", while the doc says the three highest plus ">>"), and the removal of "Continue Last Activity" from the Overview (YourSessionsPage.jsx:22) while the doc still describes it.
- Nothing failed. The previous `plan-diff.md` (2026-10-20, against v27) was replaced.
