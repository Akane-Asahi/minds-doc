# SERP diff: code vs plan

Generated: 2026-10-20 00:15 (Regina time) by serp-diff
Plan document used: `Claude outputs/Telot Thesis Planning Documents v27.docx` (version 27, internal date "Project Revised: (Oct 15, 2026)", last commit to the file 9687698, 2026-10-17)
Code checked: Akane-Asahi/minds-app @ ba707ba48c21172c85a607d13f3cca9259e4ff12 (2026-10-19 20:38 -06:00), branch main. minds-doc @ fc321d45366acb135f2f6ac193422c09ca3ad3a8 (2026-10-19 22:28 -06:00)
Scope: whole SERP (header, query, result cards, chips, right-hand panel, new directions, switching, monitoring cues, saving from the SERP). The Saved results view, Your sessions and Plan Workspace are other screens; they are touched only where the SERP links to them.

> Warnings:
> 1. **The SERP a participant reaches today is plain Baseline.** The route `/workspace` renders `features/workspace/pages/WorkspaceView` and `features/search/*` (`frontend/src/app/router/index.js:19,32-38,92-93`), which contain none of the MINDS layer. Everything MINDS on the SERP (chips, `>>`, `?`, Search Direction dropdown, right panel) exists only on the development route `/ui/serp`, runs on mock fixtures, and is excluded from production builds (`router/index.js:24-27`, `ui-dev/SerpDevPage.jsx`). "UI only" in this brief means exactly that.
> 2. Read-only run: no clone, pull, fetch, checkout, commit or push was done. Nothing was run (no tests, no browser). All claims come from reading files.

## 1. Summary

- The planning document (v27) and the in-repo spec (`docs/spec/F2`, `F3`, `F4`) agree on almost every SERP rule (top-three tags, 0 to 5 scores, `>>`, light/solid blue, New tag, panel rows, counts, query stored once per direction). The pieces that are built match them; the gap is that **almost none of it runs on real data yet**.
- Biggest code gaps (all scheduled in `docs/spec/build-plan.md`): no query generation (5.2), scoring (5.3) exists only as a prompt, schema and smoke script and is not called by any route, no stored scores, no save-under-direction write, no new-direction detection (5.6). Without these the study cannot be run as the plan describes it.
- Biggest plan-vs-code differences that are not just "not wired yet": the plan says the right-panel rows switch direction (code: only the dropdown does), the plan says `(?)` opens a "window" (code: toggles one sentence in place), and the plan's Task List still describes an embedding-based 1 to 5 star rating and a "Suggested Next Step" that the plan body, spec and code have dropped.
- The plan is silent on whether results are re-ordered by the active direction's score. The spec says yes (and that new directions never affect ranking). This decides what the study measures.
- Plan wording needs about ten edits (listed in the hand-off message and in sections 5 and 6).

Counts: Matches 4 · UI only 19 · Partial 6 · Differs 5 · Missing 5 · Plan defers 1 · Unverified 0 · Extra 7
By severity (35 differences, not counting Matches and Plan defers): Blocker for the study 5 · Important 15 · Minor 15. Extra items are all Minor and are not in these totals.

## 2. Which plan document was used

Helper: `agents/plan-diff/find_latest_plan_doc.py` run on `Claude outputs/`. Reason given: "highest version number v27". No ties, no warnings.

| File | Version | Chosen |
|---|---|---|
| Telot Thesis Planning Documents v27.docx | 27 | **yes** |
| Telot Thesis Planning Documents v7 - SRL Stripped-3.docx | 7 (-3) | no |
| Telot Thesis Planning Documents v7 - SRL Stripped-2.docx | 7 (-2) | no |
| Telot Thesis Planning Documents v7 - SRL Stripped-1.docx | 7 (-1) | no |
| Telot Thesis Planning Documents v7 - Restructured.docx | 7 | no |
| Telot Thesis Planning Documents v7 - SRL Stripped.docx | 7 | no |

Checks: v27 discusses the SERP at length (sections 1.2, 2.1 to 2.3, 3, 4, Implementation Note, Figs 2.1 to 2.3). Internal date Oct 15, 2026 is the newest of any file; no older-numbered file has a newer date, so no version/date conflict. The docx has no Word comments (`extract_docx_comments.py` reported none), so there are no "plan comment, not yet reflected" items. Read via pandoc; figure images 2, 2.2, 2.3 were opened (labels: Fig 2.1 query bar, Fig 2.2 SERP, Fig 2.3 "What you might explore" with New).

Other documents (not compared): `Claude outputs/technical-specification.md` still describes Plan Strip, Coverage Map, evaluation badges and a `/task/:id/serp` route (lines 90, 268-274 of that file). That is the old design and is stale context only. The sibling folder `claude output/` (wireframe html, slides, persona notes) was listed but not read.

## 3. Which code is the live SERP

Live (what a logged-in participant gets at `/workspace`):
- Router: `frontend/src/app/router/index.js:19` imports `features/workspace/pages/WorkspaceView`; `:32-38` `WorkspaceRoute`; `:92-93` the `/workspace` route. Layout is `frontend/src/layout/Layout.jsx` and `layout/MainHeader.jsx`; results come from `features/search/pages/SerpView.jsx` and `features/search/components/*`. This is the Baseline control. No MINDS component is imported anywhere in this path.
- Plan Workspace "Explore" ends with `openWorkspace(..., "serp")` (`features/planWorkspace/PlanWorkspacePage.jsx:14`, `features/workspace/api/workspaceNavigation.js:17-21`), i.e. it lands on that Baseline SERP, with no direction and no generated query.

MINDS SERP (dev only, mock data): `/ui/serp`, mounted by `ui-dev/UIDevRoutes.jsx` -> `ui-dev/SerpDevPage.jsx` (in-memory localStorage, `ui-dev/mockApi.js` answering `/api/library/search` and `/api/saveddocs/*`). It renders a copy of Baseline's SERP in `features/serp/`:
- Page: `features/serp/pages/WorkspaceView.jsx` (right rail holds `DirectionsPanel`, lines 149-153) and `pages/SerpView.jsx`.
- Layout and header: `features/serp/layout/Layout.jsx` (breadcrumb, total results, `DirectionDropdown` at line 150) and `layout/MainHeader.jsx` (search box, account menu, Saved Results / Return to Search button, lines 157-220).
- Cards: `components/SearchResult.jsx` -> `components/ResultRow.jsx` -> `components/ResultCardShell.jsx` (footer slot) -> `minds/ChipRow.jsx`, `minds/DirectionChip.jsx`.
- MINDS layer: `minds/MindsSerpContext.jsx` (state, from `mocks/serpDirections.js`), `minds/buildPills.js` (chip rules), `minds/DirectionDropdown.jsx`, `minds/DirectionsPanel.jsx`, `minds/SavedChips.jsx`.
- Data: `mocks/serpDirections.js` (directions, scores, reasons, queries, sessions, saved rows) and `mocks/serpDocs.js` (10 mock Primo documents).

Duplicates and legacy: `features/serp/components/SearchResult.jsx` and `VirtualizedSearchResults.jsx` are byte-identical to the `features/search/` copies; `ResultRow.jsx`, `SearchSection.jsx` and `SavedSearchResults.jsx` differ only by the MINDS changes. `features/search/*` is the Baseline control and is deliberately untouched (`DECISIONS.md` 2026-10-17). `shared/components/ResultCardShell.jsx` and `SavedDocumentCard.jsx` are the Baseline originals.

Backend that serves the SERP today: Baseline Primo proxy only (`backend/controllers/libraryController.js:38-113`, `GET /api/library/search`), Baseline `saveddocs` routes, and `PUT/GET /api/workspaces/:id/plan` for the plan. Present but not called by any route: `backend/llm/prompts.js` `buildScoringPrompt` (line 22), `backend/schemas/scoring.js` (Zod schema, clamp), `backend/models/savedResultModel.js` (model, never written by any controller). Absent: query generation (5.2), a scoring route, `resultscores`, `emergingdirections`, `sessions`, `resultscache` models, new-direction detection (5.6), promote/dismiss, reasoning-on-demand, save-under-direction routes (`backend/server.js:26-30` lists only users, workspaces, saveddocs, library, search-directions).

Tests touching the SERP: `features/serp/minds/minds.test.jsx`, `minds/buildPills.test.js`, `ui-dev/*.test.jsx`, backend `__tests__/schemas.test.js`, `models.test.js`. They show intended behaviour; they were not run.

## 4. Requirement matrix

Statuses: UI only = visible on `/ui/serp` on mock data. "Plan" cites section or figure of v27. Dates and ids in code: `path:line`.

| ID | Plan says (section/fig) | Code does (path:line) | Status | Severity | Notes |
|---|---|---|---|---|---|
| R1 | Screen layout: header with query bar, account icon, Saved Results button; breadcrumb with total results; Search Direction control; result list; right panel (Fig 2.2). | All present on `/ui/serp`: `MainHeader.jsx:157-220`, `Layout.jsx:114-150`, `WorkspaceView.jsx:149-153`. Live `/workspace` has the Baseline header and no right panel. | UI only | Minor | Breadcrumb reads "workspaces" (`Layout.jsx:124`), Fig 2.2 says "Projects" (terminology). Search submit icon is on the right (`SearchSection.jsx:279-298`), Fig 2.2 draws it on the left. |
| R2 | The Saved Results button opens the saved results of the whole project (section 5, Fig 2.2). | Button toggles Saved Results / Return to Search (`MainHeader.jsx:196-220`) to the Baseline saved list (`WorkspaceView.jsx:84-98`). MINDS saved view with chips is a separate dev screen. | UI only | Minor | Live button is Baseline's; works, but without direction chips. |
| R3 | First time a sub-goal is opened the LLM writes one query from goal, sub-goal and what the searcher knows, and the search starts with it (section 1.2, Fig 2.1). | No call 5.2 anywhere in `backend/` (only prompts for 5.1 `prompts.js:8` and 5.3 `:22`). Dev dropdown reads a fixed string (`serpDirections.js:66-72`). | Missing | Blocker | Scheduled I2 (`build-plan.md`). |
| R4 | The query is stored per sub-goal; returning to a sub-goal runs the last stored query with no LLM call (sections 1.2, 2.3). | `selectDirection` sends the fixture's query as a search term (`MindsSerpContext.jsx:103-109`); nothing is stored. Baseline `Queries` model has no `subGoalId` or source (`backend/models/queriesModel.js`). | UI only | Important | Scheduled I2. |
| R5 | Searcher can edit the query and run their own wording at any time; the query they run becomes the stored one for that sub-goal (section 1.2). | Field is editable and submit searches (`SearchSection.jsx:125-145,208-300`). A typed query is saved as a workspace-level Baseline query (`:106-107`), not tied to the active direction; `selectDirection` ignores it (`MindsSerpContext.jsx:106`). | Partial | Important | Editing works; "becomes the stored query for that direction" does not. |
| R6 | A sub-goal added later gets a generated query, is a place to file results, and results are rated against it (section 2.3). | "Add search direction" button exists but only shows "Mock only" (`DirectionsPanel.jsx:138-145`). No route to add a direction after planning (`PATCH /subgoals` not built). | Missing | Important | Scheduled I3. |
| R7 | Query generation uses a lighter, faster model than sub-goal generation, which uses the most capable model (sections 1.2, Implementation Note). | One model for every call, from `LLM_MODEL` (`backend/llm/client.js:33-41,121`); there is no per-call model option. `01-core.md` says default cheap model, escalate only if testing shows it is needed. | Differs | Minor | Decision for Telot. Plan vs spec vs code all differ. |
| R8 | Each card shows type icon and label, title, year and authors, "Description:" with Primo abstract and "Read more" (Fig 2.2; the text of section 2.1 says only "result"). | Icon plus type label (`ResultCardShell.jsx:157-182`), title, one line year, authors, source (`ResultRow.jsx:216-221`), two-line abstract with Read more (`AbstractToggle.jsx`). No "Description:" prefix; no "No description available" text, the abstract row is simply omitted (`DocumentAbstract.jsx:37-39`). | Partial | Minor | `F3` also asks for the label and the empty text. |
| R9 | Each result shows the three sub-goals it matches most strongly, ordered by rating; rating 0 to 5 shown as a number with one star, e.g. "5 ★ Mental health benefits" (section 2.1). | `buildPills.js:20` (top three, sorted), `DirectionChip.jsx` shows `{score}★ label`. Scores come from the fixture (`serpDirections.js:23-34`). | UI only | Important | Real scores need I2/I3. |
| R10 | A sub-goal rated 0 is not shown by default; no minimum rating is required (section 2.1). | `buildPills.js:20` keeps only scores above 0. | UI only | Minor | Matches the rule; mock data. |
| R11 | Tags with equal ratings follow the planning-screen order (section 2.1). | `buildPills.js:5` (tie by `orderIndex`). | UI only | Minor | Plan Workspace drag order feeds `orderIndex`. |
| R12 | A ">>" button after the last tag reveals the remaining sub-goals, including those rated 0, so a result can be filed under a weaker match (sections 2.1, 3). | Icon-only button "Show other directions", `aria-expanded`, per card (`ChipRow.jsx:60-75`); lists `card.others` including 0-scored. | UI only | Minor | Fig 2.2 does not draw the `>>`. |
| R13 | Solid blue tag = result saved under that sub-goal (section 2.1). | Saved chip is solid blue with check and "Saved", `aria-pressed` (`DirectionChip.jsx:36-70`). Saved state is in memory (`MindsSerpContext.jsx:46-58`). | UI only | Important | Not persisted per direction; see R19. |
| R14 | Light blue tag marks the strongest match on the page: top tag of its result, rating equal to the highest tag rating among the 10 results shown (section 2.1). | `buildPills.js:56-59`: top selected chip whose score equals the page best; New pill never light blue. | UI only | Minor | Plan does not say New tags are excluded from "highest tag rating"; spec does. |
| R15 | "(?)" on each tag opens a window explaining why the result may help with that sub-goal (section 2.1, Keeping the Searcher in Control; Fig 2 inset). Fig 2.2 also draws an always-visible "Why this may help" line under each description. | `?` is a separate button that toggles one italic sentence in place under the chips (`ChipRow.jsx:77-90`, `DirectionChip.jsx:78-86`). No window; no always-visible line (label removed 2026-10-17, `DECISIONS.md`). Reason text comes from the fixture; the fetch is "Mock only" (`ChipRow.jsx:78`). | Differs | Minor | Decision for Telot (window vs in place vs always visible). |
| R16 | One batched LLM call per page of 10 results scores each result against each sub-goal on a fixed rubric, temperature 0, fixed output structure, metadata only; no embeddings (Implementation Note). | Prompt (`prompts.js:22-44`), Zod schema with floor and clamp (`schemas/scoring.js:7-23`), client default temperature 0 (`client.js:84`). Used only by `scripts/smoke-llm.js`; no route, controller or frontend call. Prompt does not take `known_scores` (spec F2 says it should). | Partial | Blocker | Scheduled I2. Scores measured as not repeatable at temperature 0 (`open-questions.md`). |
| R17 | Each rating comes with a short reason based on the metadata (Implementation Note). | Prompt writes a reason only for each result's top three directions above 0 and the best new direction, others null (`prompts.js:31`). On-demand reasoning route missing. | Partial | Important | Plan implies a reason for every tag; spec fetches the rest when `?` is tapped (I3). |
| R18 | The ratings are stored; the three highest per result are displayed (Implementation Note). | No `resultscores` model (`backend/models/` has queries, savedDoc, savedResult, subGoal, user, workspace). | Missing | Blocker | Scheduled I2. |
| R19 | The tags are the save control: selecting a tag files the result under that sub-goal and fills it solid; selecting again removes it (section 3). | Chip click toggles in memory and optimistic UI with rollback (`MindsSerpContext.jsx:86-100`). The only persistence is Baseline's document save (`ResultRow.jsx:192-214`, first chip saves, last unsave removes). No write of a result-to-direction row: `SavedResult` model exists but no route or controller uses it. | Partial | Blocker | Scheduled I3. The direction a result is filed under is lost on reload. |
| R20 | Task List: "goal-linked saving so results file directly under the sub-goal through which they were found" (Task List, Oct 5 to Nov 5). | Code and section 3 of the plan: the searcher picks the direction by clicking a tag (R19). | Differs | Minor | Plan contradicts itself; the plan body and spec agree with the code. Plan Task List needs changing. |
| R21 | Detection runs in the background after each save once at least 3 results are saved; LLM reads saved-result metadata; topic must appear in at least 3 different saved results, not already a sub-goal, rated above 2; counting and threshold in code (section 2.2, Implementation Note). | No call 5.6 prompt, schema, route or model. No call after save. | Missing | Blocker | Scheduled I4. |
| R22 | A qualifying topic is stored as a possible new sub-goal; at most three active (section 2.2, Implementation Note). | No storage. Display limit of 3 on the mock list (`MindsSerpContext.jsx:7,124`). | UI only | Important | Needs `emergingdirections` (I4). |
| R23 | Once stored, every result is rated against the possible new sub-goal together with the selected ones (section 2.2). | Fixture scores include two new directions (`serpDirections.js:17-20,24-29`); real scoring not wired (R16). | UI only | Important | |
| R24 | When the possible new sub-goal is among the three highest ratings it appears on the result as a "fourth tag" marked "New" (section 2.2; Fig 2.2, 2.3). | New pill logic: at most one, shown when fewer than three selected directions score at or above it (`buildPills.js:23-34`); dashed faded pill with "New" tag (`DirectionChip.jsx`). | UI only | Important | Fig 2.2 draws New as the 2nd or 3rd tag, not always the 4th; see section 6. |
| R25 | The possible new sub-goal also appears in the "What you might explore" panel on the right (section 2.2; Fig 2.3). | `DirectionsPanel.jsx:94-124` (hidden when empty). | UI only | Important | |
| R26 | Jamie decides whether to add it or dismiss it; nothing joins the plan unless added (sections 2.2, Keeping the Searcher in Control). | Dismiss works in memory and removes the row and its pills (`MindsSerpContext.jsx:128-134`). Add (`+`) and clicking a New pill are "Mock only" (`DirectionsPanel.jsx:106`, `ChipRow.jsx:50`). No promote route. | Partial | Important | Scheduled I3/I4. |
| R27 | The right panel lists the sub-goals; selecting any of them switches the search to that sub-goal and loads its stored query (section 2.3; also section 5 "Directions panel"). | Panel row label is plain text (`DirectionsPanel.jsx:77-81`); the circle and bar segments are buttons that open the Saved results view (mock, `:69,83`). Switching is only through the Search Direction dropdown (`DirectionDropdown.jsx:20`). | Differs | Important | Decision for Telot. |
| R28 | Search Direction dropdown beside the breadcrumb (Fig 2.1, 2.2; not described in the text). | Native select in `orderIndex` order, first selected, hidden in saved view (`DirectionDropdown.jsx`, `Layout.jsx:150`). Dev search returns the same mock docs for every direction. | UI only | Minor | Plan text never describes it; figure only. |
| R29 | "Add search direction" button at the foot of the right panel; sub-goals can be added at any time (section 2.3; Fig 2.2). | Dashed button, Mock only (`DirectionsPanel.jsx:138-145`). | UI only | Important | I3. |
| R30 | Right panel "Directions You Have Explored" lists every sub-goal with a circle and a progress bar (section 4). | `DirectionsPanel.jsx:53-92`, heading "Directions you have explored" (`:60`). | UI only | Important | Data from fixture. |
| R31 | The circle shows how many results are saved under that sub-goal, 0 when none; the bar grows as results are saved, no manual marking (section 4). | Counts derived from saved rows, 0 outlined, 1+ filled, updates on save (`MindsSerpContext.jsx:44`, `DirectionsPanel.jsx:19-30`; test `minds.test.jsx:79`). Rows come from the fixture, not `savedresults`. | UI only | Important | Real counts need R19. |
| R32 | Bars are stacked on one scale so lengths can be compared (section 4). | `computeBarUnit` shared scale (`DirectionsPanel.jsx:57`). | UI only | Minor | |
| R33 | The bar counts what was saved; it does not claim a sub-goal is complete (section 4). | Grey unlabelled ruler, plain counts, no percentage (`DirectionsPanel.jsx:35-36`). | Matches | n/a | |
| R34 | On the SERP the bar grows with saves (section 4 text); one segment per session appears on the Project Overview (section 4). Fig 2.2 draws segments (+2, +1) on the SERP too. | Per-session `+N` segments on the SERP bar (`DirectionsPanel.jsx:38-47`). | UI only | Minor | Plan text and Fig 2.2 disagree; code follows the figure and spec. |
| R35 | No resume or recap entry belongs on the SERP; Continue Last Activity and the cards sit on the Project Overview (section 5). | No such control on the SERP in code. | Matches | n/a | |
| R36 | The system does not read the results for the searcher or write summaries; descriptions are not generated (Keeping the Searcher in Control). | Card text is Primo metadata only (`AbstractToggle.jsx`, `DocumentAbstract.jsx`); the only generated text is the per-chip reason. | Matches | n/a | |
| R37 | Results are rated "for each page of 10"; light blue is judged among the 10 shown (sections 2.1, Implementation Note). | Page size 10 (`SearchResult.jsx:41`), Baseline numbered Previous/Next paging (`:620+`). | Matches | n/a | Spec F2 calls for Load more and prefetch instead; see section 6. |
| R38 | Task List: SERP relevance via "embedding-based cosine similarity ... mapped to a 1-5 star rating" (Task List, Oct 5 to Nov 5). | Plan Implementation Note, spec and prompt: LLM judgement, 0 to 5, embeddings explicitly rejected (`prompts.js:22-44`, `F2` out of scope). | Differs | Minor | Plan contradicts itself; Task List is stale. |
| R39 | Task List: "per-direction coverage tracking and the Suggested Next Step mechanism". | Neither exists. Coverage Map and next-step features are deferred in the spec (`deferred.md:19-20`); plan body (section 4) describes only saved-count bars. | Missing | Minor | Unscheduled by design; Task List is stale. |
| R40 | The rubric is set empirically by comparing displayed ratings with searchers' own judgments (Implementation Note). | A validation plan is listed as "not scheduled" (`open-questions.md`, To measure or schedule). | Plan defers | n/a | Future study work, not a code gap. |

## 5. Differences in detail

### 5.1 Differs

**R7 Model per task.** Plan says: sub-goal generation uses "its most capable model", queries a lighter one (sections 1.2, Implementation Note). Code does: one `LLM_MODEL` for all calls (`backend/llm/client.js:33-41`). Why it matters: the plan's rationale for the Urgo and Arguello citation relies on a stronger model at planning time. Which side would change: plan (say one default model, escalate if testing shows it is needed, as `01-core.md` does) or code (add a per-call model setting). Decision for Telot: yes.

**R15 What `(?)` shows.** Plan says: opens a window (section 2.1, Fig 2 inset); Fig 2.2 also shows the reason always visible under the description. Code does: toggles one sentence in place under the chips; no window; no always-visible sentence (`ChipRow.jsx:77-90`). Why it matters: the plan cites Amershi and Weisz for "show why"; the figure in the thesis would not match the built screen. Which side would change: the plan text and Fig 2.2 if Telot keeps the in-place toggle (decided 2026-10-17 in `DECISIONS.md`); otherwise the code. Decision for Telot: yes (the 2026-10-17 decision removed the label but the plan was not updated).

**R20 and R38 Stale Task List lines.** Plan says (Task List): file "under the sub-goal through which they were found"; rate by "embedding-based cosine similarity ... 1-5 star". Plan body (section 3, Implementation Note) says the searcher picks the direction by tag; ratings are LLM 0 to 5 and embeddings were rejected. Code and spec follow the body. Which side would change: the plan's Task List. Decision for Telot: no.

**R27 Selecting a direction in the right panel.** Plan says: selecting any sub-goal in the right panel switches the search to it, loading the stored query (section 2.3). Code does: only the dropdown switches; the panel's circle and segments open the Saved results view; the label does nothing (`DirectionsPanel.jsx:69,77-83`). Why it matters: it is the plan's stated way to "turn to a sub-goal she has not touched" and the monitoring cue that informs the choice. Which side would change: either (code: make the row a switch button; or plan: describe the dropdown as the switch and the panel as monitoring plus saved-results links). Decision for Telot: yes.

### 5.2 Missing

**R3 Query generation (5.2).** Plan: LLM writes the first query for each sub-goal (section 1.2). Code: nothing. Matters: the study measures the effect of system-written queries. Side: code (scheduled I2). Decision: no.

**R6 Later-added direction gets a query and becomes a filing place.** Code: button is mock. Side: code (I3). Decision: no.

**R18 Ratings are stored.** Code: no `resultscores` model. Side: code (I2). Decision: no.

**R21 New-direction detection (5.6).** Code: nothing. Side: code (I4). Decision: no.

**R39 Suggested Next Step and per-direction coverage tracking.** Plan Task List mentions them; spec defers them. Side: plan (remove from Task List). Decision: no.

### 5.3 Partial and UI only

**R5 Typed query becomes the stored one.** Editing and submit work; the typed text is saved as a Baseline workspace query without a direction (`SearchSection.jsx:106-107`) and the next switch back would load the fixture/AI query, not it (`MindsSerpContext.jsx:106`). Side: code (I2 with `queries` extended). Decision: no.

**R8 Card text.** No "Description:" label and no "No description available" (`DocumentAbstract.jsx:37-39`). Both Fig 2.2 and `F3` show/require them. Side: code. Decision: no.

**R16 and R17 Scoring and reasons.** Building blocks exist but are not called; reasons exist only for shown chips (`prompts.js:31`) so tapping `?` on a revealed `>>` chip needs the on-demand route, which is missing. Side: code (I2, I3); plan could add one sentence on on-demand reasons. Decision: no.

**R19 Saving under a direction.** The document is saved through Baseline's call, but the link row (result, direction, session) is never written, so per-direction counts cannot survive a reload and Your sessions and Saved results cannot show real data. Side: code (I3). Decision: no.

**R26 Promote and add.** Dismiss is local only; promote is mock. Side: code (I3, I4).

**UI-only rows (R1, R2, R4, R9 to R14, R22 to R25, R28 to R32, R34).** Behaviour matches the plan on mock data; nothing is wired to real scores, saves or sessions, and `/ui/serp` is not reachable in production (Warning 1). Side: code (I2 to I7). Decision: no. Wording notes: R24 plan says "fourth tag" while Fig 2.2 shows New as a second or third tag and the rule is "at most one"; R34 plan text and Fig 2.2 disagree on segments (section 6).

### 5.4 Extra (in code, not in plan)

- E1: non-colour cues "Saved" with a check icon and "Best on page" text on chips (`DirectionChip.jsx:36-74`). Provisional (`open-questions.md` 4). Plan says only that colour carries two meanings. Side: plan (add one sentence) or leave. Decision: no.
- E2: polite live-region announcements "Saved under X. N results saved." (`MindsSerpContext.jsx:55`, `DirectionsPanel.jsx:147`). Accessibility; plan silent. Decision: no.
- E3: optimistic save with rollback and visible failure message (`MindsSerpContext.jsx:86-100`). Plan silent. Decision: no.
- E4: low-confidence reasons beginning "Based on title and subjects only" (`ChipRow.jsx:78`, `prompts.js:33`). Plan silent. Decision: no.
- E5: sparkle icon on AI-generated directions in the panel (`DirectionsPanel.jsx:80`); drawn in Fig 2.2 but not described in the text. Decision: no.
- E6: dev-only harness `/ui/serp` with in-memory localStorage and mock API (`ui-dev/SerpDevPage.jsx`, `mockApi.js`). Not a product feature. Decision: no.
- E7: "Desktop only. Please use a larger screen." gate (`features/serp/pages/WorkspaceView.jsx` desktop check, `Layout.jsx:177-186`), inherited from Baseline. Plan silent. Decision: no.

## 6. Plan vs in-repo spec drift

Points where `minds-doc` v27 and `minds-app/docs/spec/` disagree on the SERP (this is a finding on its own: it is why code and plan diverge). Spec statements are in `F2-serp-pipeline.md`, `F3-serp-cards-chips.md`, `F4-new-direction-detection.md`, `01-core.md`.

1. **Reason display.** Plan: window (section 2.1). Spec F3: toggles in place, no always-visible label. Plan Fig 2.2 still draws the always-visible line.
2. **Switching direction.** Plan section 2.3: right-panel rows switch. Spec F2/F3: the Search Direction dropdown switches; panel circle and segments open the Saved results view. Plan text never mentions the dropdown that Fig 2.2 shows.
3. **Ranking.** Plan: silent on result order. Spec F2: sort the pool by the active direction's score, ties keep Primo order; `01-core.md` rule 6: new directions never affect ranking. Needs a plan statement either way.
4. **Paging.** Plan: "page of 10" (Implementation Note). Spec F2: first 10, then "Load more" with background prefetch. Code (Baseline): numbered Previous/Next pages (`SearchResult.jsx:620+`). Spec is the odd one out.
5. **Reasons for every rating.** Plan: a short reason with each rating (Implementation Note). Spec F2: reasons written only for chips shown, rest generated when `?` is tapped.
6. **New tag position.** Plan section 2.2: "fourth tag". Spec F3: at most one New pill, shown when within the top three scores of all directions (so it can be second or third). Fig 2.2 matches the spec.
7. **Clicking a New pill.** Spec F3: adds the direction to the plan and saves the result under it. Plan: only the panel `+` is described.
8. **SERP bar segments.** Plan section 4 text: segments only on the Project Overview. Spec F3 and Fig 2.2: per-session segments on the SERP bar.
9. **Header wording.** Plan Fig 2.2: "Projects ›" and "total results: N". Spec F2: "Results: N" on a meta bar; `DECISIONS.md` 2026-10-16 says the header shows "Workspace: <title>" as plain text. Code shows "workspaces ›" breadcrumb and "total results: N" (`Layout.jsx:124,145`). Spec text is stale against both.
10. **Card meta line.** Spec F3: `Article · 2022 | Authors: ...`. Plan Fig 2.2 and code: type beside the icon, one line "year · authors" (`ResultRow.jsx:216-221`). Spec is the odd one out here.
11. **Task List.** Plan Task List: embeddings, 1 to 5 stars, Suggested Next Step, coverage tracking, Recap and Resume screens. Spec and plan body: LLM 0 to 5, no next-step feature, Your sessions snapshot instead of recaps (`deferred.md`).
12. **Model choice.** Plan: stronger model for sub-goals, lighter for queries. Spec `01-core.md`: cheap default, escalate only if testing shows it.
13. **Spec status lag.** `F3` says the header Saved Results toggle is not built; the button exists (`MainHeader.jsx:196-220`) though its MINDS saved view is a separate dev screen.
14. **Code vs spec (inside the repo).** `F2` says call 5.3 receives `known_scores`; `buildScoringPrompt` does not (`prompts.js:22`).

## 7. Terminology mapping used

| Plan | Code and API | UI text |
|---|---|---|
| sub-goal | `subGoal`, `subgoals`, `sub_goal_id` | search direction |
| possible new sub-goal, "New" tag | `emergingDirection`, `emergingdirections` | new direction, New pill |
| project | workspace | workspace (Fig 2.2 still says "Projects") |
| tag, rating | chip / pill, score | chip with star and number |
| (?) | `?` button, `reasoning` | "Why ..." button |
| Directions You Have Explored | `ExploredSection` | "Directions you have explored" |
| What you might explore | `MightExploreSection`, `suggestions` | same |
| Add search direction | button in `DirectionsPanel` | same |

Not counted as differences: "sub-goal" vs "search direction", "project" vs "workspace", capitalization of panel headings.

## 8. Not checked, and confidence

- Nothing was run: no tests, no dev server, no browser. Whether `/ui/serp` renders as `docs/design/02-serp-a.png` and the plan's Fig 2.2 was not verified visually; `STATUS.md` itself says several screens are not yet checked in a browser or with a screen reader.
- Real Primo behaviour (abstract availability, `totalHits`, paging cap) and real LLM latency or score stability were not checked; `open-questions.md` records 3.5 to 6 s per scoring call and unstable scores on mock metadata.
- Baseline's Saved Results view, Your sessions and Plan Workspace were not compared (other screens). Plan Figs 3 to 5 (saved views and Project Overview) were not part of this scope.
- The plan's accessibility requirements for the SERP are minimal (tag colour only), so accessibility behaviour was read from the spec and code but not compared to the plan beyond E1 to E4.
- Mock-driven behaviours (top three rule, New pill, light blue) were confirmed by reading `buildPills.js` and its tests, not by running them.
- Confidence: high on the live-versus-dev finding, on what is missing in the backend (file list and route list were checked), and on plan-versus-spec drift. Medium on exact visual match with the figures.

## 9. Open questions for Telot

1. `(?)`: a window (plan text), an in-place sentence (spec, code), or an always-visible "Why this may help" line (Fig 2.2)? The plan text and Fig 2.2 need to agree with the choice.
2. Should selecting a direction row in the right panel switch the search (plan 2.3), or is the Search Direction dropdown the only switch, with the panel as a monitoring and saved-results shortcut?
3. Are results re-ordered by the active direction's score (spec F2), or shown in Primo order with chips only? The plan should say which, because it changes what the study measures.
4. One default model for all LLM calls, or a stronger model for sub-goal generation as the plan states?
5. Paging: keep Baseline's numbered pages (matches plan wording and code) or build "Load more" with prefetch (spec F2)?
6. Does clicking a New tag on a card promote the direction and save the result in one step (spec F3), and should the plan say so?

## Appendix: files read

Plan (minds-doc @ fc321d4): `Claude outputs/Telot Thesis Planning Documents v27.docx` (commit 9687698; full text via pandoc, figures `word/media/image2.png`, `image3.png`, `image4.png` opened; comments extracted: none); `agents/serp-diff/AGENT.md`; `agents/plan-diff/find_latest_plan_doc.py` (run); `Claude outputs/extract_docx_comments.py` (run); `Claude outputs/technical-specification.md` (grep only, stale context).

Spec and design (minds-app @ ba707ba): `CLAUDE.md`, `STATUS.md`, `DECISIONS.md` (SERP entries), `docs/spec/00-index.md`, `01-core.md`, `02-data-model.md` (head), `03-api.md`, `build-plan.md`, `F2-serp-pipeline.md`, `F3-serp-cards-chips.md`, `F4-new-direction-detection.md`, `open-questions.md`, `deferred.md` (grep), `accessibility.md` (grep), `docs/design/02-serp-a.png`, `02-serp-b.png`.

Frontend: `app/router/index.js`, `app/App.jsx`, `config/uiFlags.js`, `ui-dev/UIDevRoutes.jsx`, `ui-dev/SerpDevPage.jsx`, `ui-dev/mockApi.js`, `features/serp/{pages/WorkspaceView,pages/SerpView,layout/Layout,layout/MainHeader,components/ResultRow,components/ResultCardShell,components/SearchSection,components/SearchResult,components/VirtualizedSearchResults,minds/*}.jsx/js`, `features/workspace/pages/WorkspaceView.jsx`, `features/workspace/api/workspaceNavigation.js`, `features/planWorkspace/PlanWorkspacePage.jsx` (navigation lines), `shared/components/DocumentAbstract.jsx`, `AbstractToggle.jsx`, `mocks/serpDirections.js`, `mocks/serpDocs.js`, `mocks/types.js`; diffs between `features/search/*` and `features/serp/*`; test names in `minds.test.jsx`, `buildPills.test.js`.

Backend: `server.js`, `config/constants.js`, `controllers/libraryController.js`, `controllers/searchDirectionsController.js`, `llm/client.js`, `llm/prompts.js`, `schemas/scoring.js`, `models/{queriesModel,savedResultModel,subGoalModel}.js`, route lists, `scripts/smoke-llm.js` (grep).
