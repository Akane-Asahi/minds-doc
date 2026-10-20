# Plan screen: planning doc vs code

Generated: 2026-10-20 08:20 CST (Regina) by the plan-diff agent

## Summary

- 9 differences: **2 Major, 0 Stale doc, 2 Minor, 5 Open**. Counts are by the rules in the agent file; the Why? row is Major because a feature is in the code and missing from the doc.
- **Why? button (X1): the planning doc says nothing about it.** The code has it on every AI direction, and the spec calls it a rule (01-core rule 4, F1 spec). The doc's only "why" features are the "(?)" icon on result tags (2.1, Keeping the Searcher in Control). Details in the next section.
- Model tiers (X2): the doc says sub-goals use "its most capable model" and queries a lighter one. The code has one model setting for every call, and the dev model is `gemini-3.5-flash-lite`.
- The doc caught up with most of the 2026-10-19 decisions (about eight candidates with about half new, drag to reorder, reopen and replace a plan, Explore saves only the selected, workspace-list flow in 2.3). Those were Major or Stale doc in the previous brief and now match.
- The Plan screen is **Wired**, but STATUS.md says it has not been looked at in a browser. The look-and-feel Matches below are from the code and the mockup image, not from a browser.

## The "Why?" button on AI-generated search directions

### What the planning doc says: nothing

The doc (v27, minds-doc 139f7c6) does not mention a Why? button, a reason for a candidate direction, or any explanation attached to the generated list. It does not mention the sparkle icon either. Fig 1 (image1.png, mapped by order) shows a sparkle at the end of each AI row and no Why? button or reason text. So the answer to "does the doc say clicking Why? shows why a direction was generated" is **no**.

Where I searched (whole text of v27 converted with pandoc, plus the raw `word/document.xml`, which has no comments or footnotes part; `word/media` has 7 images, only image1 is Fig 1). Terms and number of matches in the text:

| Term | Matches | Any about why a direction was generated? |
|---|---|---|
| why | 17 (13 lines) | No. Lines: Goals/Tasks and Scenario ("why those two resources were saved"), Related Work (SearchPath tags that explain why a result was saved; cross-session reconstruction), 2.1 and Keeping the Searcher in Control ("why the result may help", "why the system did what it did", "why a particular output was generated"), Section 5 ("why a particular resource was saved"). All are about results, saved resources or tags |
| reason | 21 (15 lines) | No. "reasons for saving", stopping reasons (Li and Capra), "reason based on the metadata" and "an embedding can neither give a reason for its score" (Implementation Note, about result ratings), reasoning in the literature review |
| rationale | 2 | No. "a rationale grounded in evidence" (Related Work) and "design rationale of Seihoon et al.'s SearchPath" (Research Approach) |
| explain | 3 (explain, explains, explaining) | No. 2.1 "(?) ... explains why the result may help with that sub-goal"; SearchPath tags "explaining why a result was saved" (twice) |
| explanation | 1 | No. 2.1: "The ratings and explanations help Jamie judge a result" |
| justif | 1 | No. Research Approach: "each design feature justified against a specific problem or literature finding" (a method statement) |
| "one-sentence" / "one sentence" | 0 | none |
| sparkle, tooltip, "Why?" | 0 | none |

Sections read in full for this: 1.1 Planning: Goal Decomposition (and Fig 1 caption), 1.2, 2.1, 2.2, 2.3, Keeping the Searcher in Control, Implementation Note, Task List and Fall 2026 Goals, Abstract, Research Approach.

The nearest sentences, so you can judge them yourself:

- **1.1 Planning: Goal Decomposition:** "Jamie decides which of these to work with, can add sub-goals of their own with Add search direction, and can drag any sub-goal to a new place in the list to set the order." No reason or explanation for a candidate.
- **Keeping the Searcher in Control:** "In planning, the LLM offers candidate sub-goals, and Jamie chooses which to work with and can add others." Then: "The “(?)” icon on each tag lets Jamie check how the system rated a result before relying on it. This follows the guideline to make clear why the system did what it did (Amershi et al. 2019) and the strategy of showing the user why a particular output was generated (Weisz et al. 2024)." This is about result tags on the results page, not about directions on the Plan screen.
- **2.1 Evaluation: Relevance and Usefulness of Results:** "Each tag has a “(?)” icon. Selecting it opens a window that explains why the result may help with that sub-goal (Fig 2, inset)". Again a result tag.
- **Implementation Note:** the rating call returns "a short reason based on the metadata". Sub-goal generation is described only as a call that proposes about eight candidates (1.1); no reason is mentioned.

The doc's own principle (show why a particular output was generated, Weisz et al. 2024; Amershi et al. 2019) would cover directions too, but the doc applies it only to result tags.

### What the code does

Status: **Wired** on the real route `/workspace/:workspaceId/plan` (`frontend/src/app/router/index.js:96`) and in the dev preview `/ui/plan-workspace`. Not looked at in a browser (STATUS.md).

| Question | Answer | Evidence |
|---|---|---|
| Where does the reason text come from? | The LLM. The call-5.1 system prompt asks for a `rationale` for every direction: "one plain sentence saying why searching this direction helps the goal". | `backend/llm/prompts.js:16` |
| Schema | Each item in `sub_goals` has `label`, `kind` (`familiar` or `new`) and `rationale` (a required non-empty string, described as "one sentence: why searching this direction helps the goal"). The server checks it is non-empty but does not check it is one sentence or any length limit. | `backend/schemas/directions.js:14-23` (rationale at line 20) |
| Same call as the directions? | Yes. One call (5.1) returns label, kind and rationale together. There is no separate call when Why? is clicked. | `backend/controllers/searchDirectionsController.js:23-38`; `backend/schemas/directions.js:46-50` (`toDirectionsResult` returns `rationale` with each label) |
| How it reaches the screen | The API returns `{subGoals: [{label, kind, rationale}]}`; the wired model copies `rationale` onto each AI card. | `frontend/src/features/planWorkspace/useWiredPlanModel.js:123` |
| When is the button shown? | Only on AI directions (not custom) and only when the rationale is a non-empty string. A card with no rationale shows the sparkle but no Why?. | `DirectionRow.jsx:81-94` (`!isCustom && rationale`) |
| Look | A text button "Why?" (no capitals change, semi-bold) placed after the sparkle ("Suggested by AI") at the right end of the card. | `DirectionRow.jsx:81-93` |
| Show and hide | Clicking toggles that card's reason. The reason is a paragraph under the card (indented, grey, may wrap even though labels never wrap). Click again to hide. Several can be open at once. There is no Escape key, no click-away close, no auto-close. State is view-only: a `Set` of card ids. It is not cleared when you tick the card or drag it. A card that regeneration replaces gets a new id, so its reason is closed; kept (ticked) cards keep theirs. | `PlanWorkspaceScreen.jsx:88,150-156,197-198`; `DirectionRow.jsx:173-177`; `useWiredPlanModel.js:123` (new `ai-N` ids); DECISIONS.md:298 ("The Why? rationale panel may still wrap") |
| Keyboard | It is a real MUI `<Button>`: Tab to reach it, Enter or Space to toggle. Drag uses only mouse and touch sensors, so no keyboard handler competes with it. A mouse drag starts only after 6 px, so a click on Why? does not start a drag (a test checks this). | `DirectionRow.jsx:83-93`; `PlanWorkspaceScreen.jsx:30-33,97-100`; test `PlanWorkspaceDrag.test.jsx:185` |
| Screen reader | The button's accessible name is `Why? <direction label>` (starts with the visible word, so the visible text is inside the name). It has `aria-expanded` and `aria-controls` pointing at the panel id. The panel is a plain paragraph, not a live region, so opening it is announced only through `aria-expanded` and by reading on. While the panel is closed the `aria-controls` target does not exist in the page (minor). No focus change happens. The drag preview copy is `aria-hidden` and `inert`. | `DirectionRow.jsx:54-59,86-89,116,173-177` |
| Custom directions | No Why?, no sparkle. The server rejects a custom direction that carries a rationale (and a `kind`). Custom cards get Edit and Remove instead. | `DirectionRow.jsx:95-103`; `backend/schemas/plan.js:16-17`; `backend/models/subGoalModel.js:31-36` |
| Saved? | Yes, but only for selected AI directions. Explore sends `rationale` with each ticked AI direction; it is stored in `subgoals.rationale` (null for custom); unticked suggestions are discarded with their reasons. | `useWiredPlanModel.js:16-20`; `backend/schemas/plan.js:13,42`; `backend/models/subGoalModel.js:31-36`; `docs/spec/02-data-model.md:19` |
| Shown again later? | On the Plan screen only. Reopening a workspace that has a plan loads the saved directions (all ticked) with their stored rationale, so Why? shows again for AI ones (`GET /plan` returns `rationale`). I found no use of a direction's `rationale` on the results page, saved results or Your sessions code (those screens use `label`, `orderIndex` and similar; the one hit in `YourSessionsScreen.jsx:90` sets `rationale: null` on a custom direction). | `useWiredPlanModel.js:28-37`; `backend/controllers/planController.js:10`; grep of `rationale` across `frontend/src` and `backend` |
| Spec and DECISIONS entries | `01-core.md:48-49` rule 4: every LLM output "has a one-line 'why' reachable by tap (the `?`, the rationale on suggested directions)". `F1-plan-workspace.md:92`: "Each can show its `rationale` via tap-to-expand."; `:143` schema line; `:78` Why? still clicks during a drag. `02-data-model.md:19` and `03-api.md:13` store and send it. DECISIONS.md:298 only says the panel may wrap. No DECISIONS entry records the decision to add the button, who asked for it or when; it follows rule 4. The F1 spec calls it "Why?" nowhere except line 78, and the layout table (line 55) does not list the button. | files and lines as shown |
| Tests (supporting only) | "Why? expands the rationale" (`PlanWorkspaceScreen.test.jsx:75`); "clicking the checkbox or Why? works and never starts a drag" (`PlanWorkspaceDrag.test.jsx:185`); plan and schema tests carry `rationale` through. No test of keyboard, screen reader, or the custom-direction case in the UI. | as shown |

Intent versus drift: the button follows spec rule 4 (01-core), so it is intended in the code project; the planning doc has not caught up. Suggested action: update the doc (1.1 and the "Keeping the Searcher in Control" paragraph that lists the "(?)" icon) with one sentence that each AI candidate carries a one-sentence reason behind a "Why?" button, or decide to leave it out of the thesis text. Also add the button to the Fig 1 mockup and to the F1 layout table.

## What was compared

| | Source | Version |
|---|---|---|
| Planning document | `Telot Thesis Planning Documents v27.docx` in `Claude outputs/`, chosen because it has the highest version number (v27); other candidates (all v7): SRL Stripped-3, -2, -1, Restructured, SRL Stripped. No helper warnings. Header: "Project Revised: (Oct 15, 2026)". This is the version edited and pushed 2026-10-20. | minds-doc 139f7c6, 2026-10-20 00:22 -0600, "Fix planning doc v27: Task List, Plan/SERP/Saved/Sessions text, workspace wording" |
| Code | Akane-Asahi/minds-app, Plan Workspace | minds-app ba707ba, 2026-10-19 20:38 -0600, "Update index title to MINDS Academic Search" |
| Intent notes | STATUS.md, DECISIONS.md, F1-plan-workspace.md (also 01-core.md, 02-data-model.md, 03-api.md, accessibility.md) | same commit |

Both clones (`/home/claude/minds-doc`, `/home/claude/akane-asahi/minds-app`) had the expected `origin` URLs and `git pull --ff-only` reported "Already up to date" before reading.

## Differences

| ID | Area | Planning doc says | Code does | Evidence | Severity | Suggested action |
|---|---|---|---|---|---|---|
| X1 | Why? button on AI directions | Nothing (see section above). Only result tags have a "(?)" why. | Each AI direction has a Why? button that shows a one-sentence LLM reason from the same call; saved for ticked directions. | `DirectionRow.jsx:81-94,173-177`; `prompts.js:16`; `schemas/directions.js:20`; 01-core.md:48-49; F1 spec line 92. Doc: whole-text search above | Major | Update the doc (1.1, Keeping the Searcher in Control, Fig 1) or decide to drop the button |
| X2 | Model used for generation | 1.1 and Implementation Note: sub-goal generation "uses its most capable model"; 1.2: queries use "a lighter, faster" one. | One setting for all calls: `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY`; no per-call model. Dev model `gemini-3.5-flash-lite`. 01-core says default to "a cheap, fast model; escalate only where testing shows" it is needed. Query generation (5.2) not built yet. | `backend/llm/client.js:33-37,121`; DECISIONS.md:85; `docs/spec/01-core.md:94,102` | Major | Decide first: keep two tiers (code needs a separate model setting for 5.1 and 5.2) or change the doc to one model |
| X3 | Third field label | 1.1 and Fig 1 image: "what they want to find out" / "What I want to find out". | Label is "What I want to find" (the helper line says "find out"); recorded as following F1, not the mockup. | `PlanWorkspaceScreen.jsx:15,19`; DECISIONS.md:306 | Minor | Decide first: one word, then change the other side |
| X4 | Add-direction button label | 1.1 and Section 5: "Add search direction". | Button reads "Add Search directions"; Your sessions mockup uses "+ Add search direction". | `PlanWorkspaceScreen.jsx:374`; F1 spec line 55 | Minor | Decide first; the code probably changes to the singular |
| X5 | Where Explore leads | 1.1: Explore "opens the results page on the first of them". | Explore saves the plan (selected directions only, in list order) and opens Baseline's SERP tab. The MINDS results page that starts on the first direction is not built yet (I2/I3); first selected = default is spec-level. | `PlanWorkspacePage.jsx:14`; `workspaceNavigation.js:17-21`; F1 spec lines 117-118; STATUS.md "Next" | Open | No change now; re-check after I2/I3 |
| X6 | Where a returning searcher lands | Section 5: on return "the Workspace Overview screen (Fig 5) shows the previous search activity". | Clicking a workspace, or Edit Workspace, opens Plan Workspace; Open workspace there opens the SERP. Your sessions is not reachable from the real flow yet (I7). | `WorkspaceList.jsx:409-412,626-628`; F1 spec lines 31-40; open-questions.md item 7; STATUS.md "Blocked" | Open | Decide first: is Plan Workspace a permanent stop on return, or a temporary route until I7? |
| X7 | Reordering without a mouse | 1.1: Jamie "can drag any sub-goal to a new place in the list to set the order". Order is used for tie-breaks (2.1). | Drag works with mouse and touch press-and-hold only. No keyboard way to reorder (recorded gap). | `PlanWorkspaceScreen.jsx:97-100`; F1 spec lines 88,170; accessibility.md:43; open-questions.md item 8 | Open | Decide first: build it, or say order is optional |
| X8 | Replacing a plan vs saved results | 1.1: "A saved plan can be reopened and changed, and pressing Explore again replaces it." Nothing about results already filed. | Replace deletes all directions and inserts new ones with new ids. Safe today (nothing saved yet); would orphan saved results after I3. | `planController.js:70-71`; open-questions.md item 9; STATUS.md "I1 follow-up" | Open | Code change before I3: keep directions that have saved results |
| X9 | Sub-goals stay on screen on the results page | 1.1: the sub-goals "stay on screen as the reference for the rest of the workspace, in the directions panel of the results page". | The directions panel exists only in fixtures (`MindsSerpContext` reads a fixture); not wired to saved directions until I3. | `frontend/src/features/serp/minds/MindsSerpContext.jsx:15`; STATUS.md "Next" | Open | No change now; re-check after I3 |

## Matches

- Three inputs: search goal, what they already know, what they want to find (wording in X3). 1.1; `PlanWorkspaceScreen.jsx:13-17`.
- The LLM generates the candidates from the three inputs, about eight, roughly half angles the searcher did not mention, mixed in one list. 1.1, Abstract; `prompts.js` rules (two kinds, "roughly half new", mixed); `constants.js:3` (`DIRECTION_COUNT: 8`). The doc's six-candidate list is labelled "shortened here for illustration".
- The searcher decides: suggestions start unselected, nothing joins the plan unless ticked, own directions can be added. 1.1, Keeping the Searcher in Control; F1 spec lines 92-98.
- Drag to reorder; the number order is stored as `orderIndex` and used for ties. 1.1; F1 spec lines 74-88; `useWiredPlanModel.js:16-20`.
- Explore saves the three texts and only the selected directions, in order; unselected candidates are not kept. 1.1; `planController.js:44-89`; `schemas/plan.js`.
- A saved plan can be reopened and changed; Explore again replaces it. 1.1; `useWiredPlanModel.js:139-214`; F1 spec lines 25-38.
- Entry flow in 2.3: back to the workspaces list, new workspace with its own title, then plan it on the first screen. `WorkspaceList.jsx:707-708`; F1 spec lines 13-23.
- Task List item "Implement the planning screen: ... LLM-based sub-goal generation and selection" (query generation no longer listed there); the code's Plan screen calls only 5.1. `searchDirectionsController.js:23-48`.
- Fig 1 layout (image1.png by order; same as `docs/design/01-plan-workspace-generated-directions.png`): logo and person icon, three fields, "Search directions" with three-arrow icon, numbered two-column list, sparkle on AI rows, dashed add box, full-width Explore. The code follows it, except the Why? button the image lacks (X1).

## In code, not in the planning doc

- Why? button and reason (X1). `DirectionRow.jsx:81-94`.
- Sparkle on AI rows with accessible name "Suggested by AI". `DirectionRow.jsx:9-15`.
- Generation runs on blur once all three fields are filled; nothing happens if any is empty; unchanged normalized text sends nothing; a newer request aborts the older one. `useWiredPlanModel.js:97-136`.
- Regeneration keeps ticked and custom cards in their slots and replaces only unticked AI ones; a batch that arrives mid-drag waits. `directionList.js:38-62`; `useWiredPlanModel.js:124-127`.
- Custom directions can be edited and removed; AI ones can only be ticked or unticked. `DirectionRow.jsx:95-103`.
- 7-word limit with an "N of 7 words" counter. `PlanWorkspaceScreen.jsx:364`; `schemas/plan.js:10`.
- Explore disabled with a visible reason until all three fields are filled and one direction is ticked; double click saves once. `PlanWorkspaceScreen.jsx:178,386-408`.
- Failure state: inline error with Retry; the searcher can continue with custom directions. `PlanWorkspaceScreen.jsx:295-304`; `searchDirectionsController.js:12-17`.
- Rate limit of 10 generate requests a minute per participant; 12 s LLM timeout. `constants.js:9-11`.
- A plan is written once unless `replace: true`; a double submit fails safely on a unique index. `planController.js:60`; `subGoalModel.js:44`.

## In the planning doc, not in code

- Two-tier models (X2) and the results-page directions panel (X9, not wired yet). Nothing else on the Plan screen is promised and missing.

## Needs a browser, a live call or Telot's decision

- Whether the page, the Why? panel and the drag behave as intended in a real browser and with a screen reader (STATUS.md: "not yet looked at in a browser"; F1 acceptance list has `[~]` items; the closed-panel `aria-controls` target and the lack of a live region for the Why? panel have not been tried with a screen reader).
- Whether the model's one-sentence reasons are good: the server only checks the rationale is a non-empty string. Needs a live 5.1 call to judge quality and length.
- Decisions: X1 (put Why? in the doc?), X2 (one model or two), X3 and X4 (labels), X6 (where returning searchers land), X7 (keyboard reordering).
- F1 spec says "Out of scope: Editing directions after Explore" (line 174), but the reopen-and-replace flow does exactly that. Spec inconsistency inside minds-app; Telot to say which stands.
- Fig 1 in the doc still shows "Plan your new project", "What I want to find out" and no Why? button, while its caption now says "Plan Your New Workspace". The image needs replacing from the current mockup (image text only; the title part is Terminology).

## Terminology

The doc uses project / sub-goal / possible new sub-goal / Screen 1; the code and UI use workspace / search direction (`subGoal` in code) / new direction (`emergingDirection`) / Plan Workspace ("Plan Your New Workspace"). This is intentional and is reported once here. The v27 text already says workspace almost everywhere and the Fig 1 caption says "Plan Your New Workspace"; only the Fig 1 image still says "project". Not counted as a difference.

## Doc claims checked

| ID | Section | Claim |
|---|---|---|
| D1 | 1.1 Planning: Goal Decomposition | On the first screen the searcher enters a search goal, what they already know, and what they want to find out |
| D2 | 1.1 | From the three inputs an LLM generates candidate search directions (sub-goals); about eight, roughly half angles the searcher has not mentioned |
| D3 | 1.1 | Jamie's list "shortened here for illustration" has six candidates |
| D4 | 1.1 | "Jamie decides which of these to work with, can add sub-goals of their own with Add search direction" |
| D5 | 1.1 | Jamie can drag any sub-goal to set the order; the numbered order of selected sub-goals is kept and used to rank ties |
| D6 | 1.1 | Explore saves the three texts and the selected sub-goals in order, opens the results page on the first; unselected candidates are not kept |
| D7 | 1.1 | A saved plan can be reopened and changed; pressing Explore again replaces it |
| D8 | Fig 1 caption and image | "Screen 1 — Plan Your New Workspace"; image shows sparkle only, no Why? button |
| D9 | 1.1 | LLM proposes, searcher decides; the sub-goals stay on screen in the directions panel of the results page |
| D10 | 1.1, Implementation Note | Sub-goal generation uses the most capable model |
| D11 | 1.2, Implementation Note | Query generation uses a lighter, faster model |
| D12 | 2.3 | To change topic entirely she returns to the workspaces list, creates a new workspace with its own title, and plans it on the first screen |
| D13 | 5 Cross-Session Support | On return the Workspace Overview screen shows previous activity; "Add search direction" or start a new workspace from the list |
| D14 | Keeping the Searcher in Control | In planning the LLM offers candidates; Jamie chooses and can add others |
| D15 | Keeping the Searcher in Control | The "(?)" icon on each tag shows why a result was rated; no why for directions |
| D16 | 2.1 | "(?)" on each result tag explains why the result may help with that sub-goal; ties follow "the order the searcher set in the planning screen" |
| D17 | Task List, Oct 5 - Nov 5 | Implement the planning screen: three inputs, LLM sub-goal generation and selection |
| D18 | Fall 2026 Goals, item 2 | By November 5 the MVP includes planning |
| D19 | Search for why/reason/rationale/explain/explanation/justif/one-sentence/sparkle/tooltip/"Why?" | No statement about a reason or Why? control on candidate directions (X1) |

## Method and limits

- Read statically only: the whole text of planning doc v27 (pandoc), the raw `document.xml` for the Why? search (no comments or footnotes part exists in the file), Fig 1 image, STATUS.md, DECISIONS.md, the F1 spec, 01-core.md, 02-data-model.md, 03-api.md, accessibility.md, the `planWorkspace` frontend files, the plan and directions controllers, schemas, models, prompts, LLM client, constants, and the entry-flow code. Test names read as supporting evidence only. No tests run, no browser, no LLM call, `.env` not read.
- Line numbers are from minds-app ba707ba, checked with grep.
- Not checked in detail: Fig 2 onward (SERP, saved, sessions; other diff agents cover them). X9 is judged from the SERP context file reading a fixture, not from running it.
- The previous version of this file compared against the older doc (minds-doc fc321d4). Its X1, X3, X4, X5, X7, X10, X11 are now resolved in the doc and are listed under Matches. Nothing failed. This file is written but not pushed, as requested.
