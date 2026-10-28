# SERP diff: code vs plan

Generated: 2026-10-28 09:30 (Regina time) by serp-diff
Plan document used: `Claude outputs/Telot Thesis Planning Documents v30.docx` (version 30, internal date "Project Revised: (Oct 25, 2026)", last commit to the file 4fa3494, 2026-10-26 00:00 -06:00)
Code checked: Akane-Asahi/minds-app @ 533d618 (full SHA 533d618c36be06d240a2640842179a4f2ad22676, 2026-10-27 15:31 -06:00), branch main. minds-doc @ 4fa3494 (full SHA 4fa3494f066a17457b07a88acf4088b41fac58c4, 2026-10-26 00:00 -06:00), branch main
Scope: whole SERP (header, query and search box, result cards, direction tags, "(?)" sentences, "New" tags, right-hand panel, switching and adding sub-goals, progress bars, saving from the SERP). The Plan screen, Workspace Overview and Saved results view are other screens; they are touched only where the SERP links to them or shares a rule with them.

> Warnings:
> 1. **The code is newer than the plan text on the most visible SERP rules.** Several differences below trace to code comments dated 2026-10-26 and 2026-10-27 (score and star shown again, no cap of three tags, no ">>" button). The plan v30 text and the in-repo spec both date from 2026-10-25 or earlier. Where the code carries a dated decision, it may be the plan that is behind.
> 2. **The plan's own SERP figures (Fig 2.1, 2.2, 2.3) show the old design**, not the plan's text (see section 6). The figure images in the docx are dated 2026-10-20.
> 3. **The in-repo spec is not in minds-app at this SHA.** `minds-app` has no `CLAUDE.md`, `STATUS.md`, `DECISIONS.md`, `docs/spec/` or `docs/design/` (its `docs/` holds only `commands.md`, `font-size-change.md`, `font-weight-change.md`). The nearest copy is the mirror at `minds-doc/minds-app-claude-files/` (STATUS last updated 2026-10-25). Section 6 uses that mirror and says so.
> 4. Read-only run as the caller asked: no clone, pull, fetch, commit or push was done, and the repos were used as found. Nothing was run (no tests, no browser, no backend, no model calls). Every statement about the code comes from reading files. The brief cannot say whether the minds-app clone is still the newest commit on GitHub.
> 5. This file replaces an earlier `serp-diff.md` (plan v27 against code ba707ba, dated 2026-10-20).

## 1. Summary

- The live SERP is the MINDS one (`MindsSerpPage` at `/workspace/:id/serp`), wired to real endpoints (Primo, scoring, saving, new-direction detection). Almost everything in the plan about queries, switching, ordering, the "(?)" sentences, saving and the progress bars is built and matches. Nothing on the live SERP is mock-only.
- **Biggest difference 1: the rating is visible.** Plan v30 says the searcher never sees the numbers and fit is shown by order only. The code shows "N star" on every tag, and screen readers hear "score N out of 5" (`DirectionChip.jsx:61-62,77`). The code comment says the SERP shows them again since 2026-10-26; the plan says they were removed for good on 2026-10-25.
- **Biggest difference 2: no cap of three tags and no ">>".** Plan: three tags, then ">>" reveals the rest including rated 0. Code: every sub-goal rated above 0 is a tag, a 0 shows nothing, and there is no way to file a result under a sub-goal rated 0 (`buildPills.js:21-23`; test `minds.test.jsx:151`). The code comment cites Orland, 2026-10-27.
- **Biggest difference 3: the "New" tag rule** follows from the previous one: plan says the possible new sub-goal shows when it is among the three highest ratings; code shows it whenever it is rated above 0 (`buildPills.js:26-30`). Also the plus button on the Overview adds a new sub-goal as selected (`emergingService.js:233`), the plan says unselected.
- Smaller: one model for every LLM call (plan says a capable one for sub-goals and a lighter one for queries); panel heading and button say "sub-goal" where the plan says "Directions for this session" and "Add search direction"; the plan's figures are out of date.

Counts: Matches 33 · UI only 0 · Partial 1 · Differs 7 · Missing 1 · Plan defers 1 · Unverified 2 · Extra 11

## 2. Which plan document was used

Chosen by `agents/plan-diff/find_latest_plan_doc.py` ("highest version number v30"). No warnings from the helper, no tie. The docx carries no Word comments (`extract_docx_comments.py` reported none), so there is no "plan comment, not yet reflected".

| File | Version | Chosen |
|---|---|---|
| Telot Thesis Planning Documents v30.docx | 30 | yes |
| Telot Thesis Planning Documents v29.docx | 29 | no |
| Telot Thesis Planning Documents v27.docx | 27 | no |
| Telot Thesis Planning Documents v7 - SRL Stripped-3.docx | 7 (-3) | no |
| Telot Thesis Planning Documents v7 - SRL Stripped-2.docx | 7 (-2) | no |
| Telot Thesis Planning Documents v7 - SRL Stripped-1.docx | 7 (-1) | no |
| Telot Thesis Planning Documents v7 - Restructured.docx | 7 | no |
| Telot Thesis Planning Documents v7 - SRL Stripped.docx | 7 | no |

The document discusses the SERP in sections 1.2, 2.1, 2.2, 2.3, 3, 4, 5, "Keeping the Searcher in Control", the Implementation Note, the Task List, and Fig 2.1, 2.2, 2.3. The text says it was brought in line with minds-app 2f08f2c / 209f0cd (`v30-changes-summary.md`); the code checked here is later (533d618), so drift since then is expected.

Other files in the folder were not used as the plan. `technical-specification.md` and `claude output/` were not compared; see section 8.

## 3. Which code is the live SERP

Route: `frontend/src/app/router/index.js:102` sends `/workspace/:workspaceId/:view` to `MindsSerpPage`. `view` is `serp` or `saved` (`MindsSerpPage.jsx:120`); the SERP stays mounted (hidden) under the Saved results view (`MindsSerpPage.jsx:79-80`). Plan Workspace's Explore navigates to `/workspace/:id/serp` (`PlanWorkspacePage.jsx:23`); the Overview navigates to `.../serp?direction=` (`YourSessionsPage.jsx:168`).

Live (frontend), all read:
- `features/mindsSerp/MindsSerpPage.jsx`, `MindsSerpLayout.jsx`, `SerpSearchField.jsx`, `SerpResults.jsx`, `useLiveSerp.js`, `serpModel.js`, `mindsSerpApi.js`
- `features/serp/minds/ChipRow.jsx`, `DirectionChip.jsx`, `buildPills.js`, `DirectionsPanel.jsx` (shared with the MINDS layer; `MindsSerpContext.jsx` is only the mock provider)
- `features/serp/components/ResultCardShell.jsx`, `features/serp/layout/MainHeader.jsx`, `features/planWorkspace/DirectionRow.jsx` (marks)

Live (backend), all read: `controllers/sessionController.js` (search, query, scores, last state), `resultsController.js` (save, reasoning), `emergingController.js`, `services/scoringService.js`, `ranking.js`, `queryService.js`, `emergingService.js`, `savedService.js`, `primoService.js` (read at header level), `llm/client.js`, `llm/prompts.js`, `schemas/*`, `config/constants.js`.

Not the MINDS SERP:
- **Baseline SERP (the control):** `/workspace` (`router/index.js:94`) renders `features/workspace/pages/WorkspaceView.jsx`, which imports `features/search/pages/SerpView.jsx`. Contains no MINDS layer.
- **Dev-only, mock fixtures:** `/ui/serp` (`ui-dev/SerpDevPage.jsx`) mounts the copy at `features/serp/pages/WorkspaceView.jsx` with `MindsSerpProvider` and fixtures from `frontend/src/mocks/`. The route exists only when `NODE_ENV === "development"` (`router/index.js:26-28`). `features/serp/components/ResultRow.jsx`, `SearchResult.jsx`, `SavedSearchResults.jsx`, `pages/SerpView.jsx` are part of that dev copy.
- **Duplicates:** `features/search/**` and `features/serp/**` are near copies of each other (Baseline); `layout/MainHeader.jsx` and `features/serp/layout/MainHeader.jsx` are two headers, the second is the MINDS one.

## 4. Requirement matrix

Plan citations use section names of v30 ("§2.1" = "2.1 Evaluation: Relevance and Usefulness of Results"). "Impl." = Implementation Note.

| ID | Plan says (section/fig) | Code does (path:line) | Status | Severity | Notes |
|---|---|---|---|---|---|
| R1 | Results list on the left, right panel beside it (§4, Fig 2.2) | Two-column grid: `SerpResults` and a sticky `DirectionsPanel` (`MindsSerpPage.jsx:92-98`) | Matches | | Sticky panel is Extra E3 |
| R2 | Workspace button in the results-page header leads to the Overview (§5) | "Workspace" button, `aria-label` "Go to Workspace" (`MainHeader.jsx:249`), wired to `/overview` (`MindsSerpLayout.jsx:28`) | Matches | | |
| R3 | First time Jamie turns to a sub-goal, LLM writes one query of 2 to 4 plain keywords, own words plus at most one anchor word (§1.2) | Prompt asks for 2 to 4 words, at most one goal word (`llm/prompts.js:27-28`); generated only when none is stored (`queryService.js:22-25`) | Matches | | Quality of real output Unverified (R44) |
| R4 | Query is written in the search box, not run, typed letter by letter, cursor left in the box (§1.2, §2.3) | `selectDirection` puts it in the box without searching (`useLiveSerp.js:208-237`); typed out at 25 ms per letter, caret placed (`SerpSearchField.jsx:6,34`) | Matches | | Reduced motion shows it at once (`SerpSearchField.jsx`, matchMedia branch) |
| R5 | Query stored per sub-goal; returning shows the last query searched, LLM or Jamie's, no new LLM call (§1.2) | Newest `queries` row for the sub-goal is shown (`queryService.js:22`); typed ones stored as `source: 'user'` (`sessionController.js:152-155`) | Matches | | |
| R6 | Jamie can edit and search with own wording; the query she runs becomes the stored one (§1.2) | A text equal to the stored one is reused, anything else goes as `queryText` (`useLiveSerp.js:314-326`); stored at `sessionController.js:152-155` | Matches | | |
| R7 | Sub-goals use the most capable model, queries a lighter, faster one (§1.1, §1.2, Impl.) | One model for every call from `LLM_MODEL` (`llm/client.js:33-40`; each call site passes only `call:` e.g. `queryService.js:25`, `scoringService.js:59`) | Differs | Minor | Not visible to a participant. Which side changes: plan text or code. Decision for Telot |
| R8 | Search icon beside a sub-goal switches to it; results stay until Jamie presses search; what is sent is stored under the sub-goal whose icon was pressed last (§2.3) | `SearchWordsButton` calls `selectDirection` (`DirectionsPanel.jsx:119-134`); results belong to `activeId` and change only in `submitQuery` (`useLiveSerp.js:314-326`) | Matches | | |
| R9 | Results page opens on a sub-goal and searches its query at once (after Explore, Continue Last Activity); arriving from an Overview card search icon only writes the query (§2.3) | `start()` searches unless `typeOnly` (`useLiveSerp.js:241-246`); `typeOnly` comes from router state `typeQuery` (`MindsSerpPage.jsx:38`), set at `YourSessionsPage.jsx:168` | Matches | | |
| R10 | A sub-goal added later gets a generated query, is a place to file, and is rated from the next search on (§2.3) | Add appends it selected (`useLiveSerp.js:408-426`); its first icon press writes a query (`directionQuery`, `sessionController.js:218-242`); `scorePool` scores every selected direction not yet stored (`scoringService.js:100-107`) | Matches | | |
| R11 | Each result shows the three highest-rated sub-goals as tags, best first, no minimum rating (§2.1, Impl.) | Every sub-goal rated above 0 is a tag, no cap of three (`buildPills.js:21-23`; `config/constants.js:7` says "no cap since 2026-10-27"; test `buildPills.test.js:13`) | Differs | Important | A result can show five or more tags. Decision for Telot (the code comment cites Orland, 2026-10-27) |
| R12 | Tag order carries the rating, best at the left; equal ratings follow the order set on the planning screen (§2.1) | Sort by score, then `orderIndex` (`buildPills.js:8,22-23`) | Matches | | |
| R13 | A ">>" button after the last tag reveals the remaining sub-goals, including those rated 0, so Jamie can file a result under a weaker match (§2.1, §3) | No ">>" control; a 0 shows nothing (`buildPills.js:21-23`, test `minds.test.jsx:151`). A result cannot be filed under a sub-goal rated 0 from the SERP | Missing | Important | Removed on purpose 2026-10-27 (comment `buildPills.js:2-6`); not scheduled to return. Decision for Telot |
| R14 | The searcher never sees the numbers; ratings only order things; fit shown by order only (§2.1, Impl.; v30 summary "removed for good") | `showScore` defaults to true, `ChipRow` does not turn it off, so each tag prints "N" and a star (`DirectionChip.jsx:77-81`); accessible name says "score N out of 5" (`DirectionChip.jsx:61-62`). Comment: "the SERP shows them again, 2026-10-26" (`DirectionChip.jsx:50`). Saved results turns it off (`SavedResultCard.jsx:71`) | Differs | Important | A different intervention from the one the plan describes. Stale test comment at `minds.test.jsx:147` says hidden. Decision for Telot |
| R15 | No tag or result is marked as the best match (§2.1) | Top tag of the page-best score is flagged `suggested` (`buildPills.js:51-54`, `ChipRow.jsx:99`); visible look equals the others, but the accessible name adds "best match on this page" (`DirectionChip.jsx:63`) | Differs | Minor | Screen-reader only. Plan or code would change |
| R16 | Selecting a tag files the result under that sub-goal and fills it solid blue; selecting again removes it; Jamie chooses where (§2.1, §3) | `toggleDirection` saves/unsaves optimistically with rollback (`useLiveSerp.js:339-367`); saved tag solid blue (`DirectionChip.jsx:67`); `aria-pressed` (`DirectionChip.jsx:73`) | Matches | | Real endpoints: `resultsController.js:40-65,101-116` |
| R17 | A generative model rates each result per sub-goal 0 to 5 from title, abstract, subject terms; one call per page of 10; temperature 0; fixed output structure (§2.1, Impl.) | One batched call per pool of 10 (`config/constants.js:6`; `scoringService.js:58-70`); integers clamped 0 to 5 (`schemas/scoring.js` clamp); temperature 0 default (`llm/client.js:84`); Zod output schema | Matches | | The model is also sent authors, venue and resource type (`scoringService.js:19-29`), which the plan does not list (Minor, E-note in section 8) |
| R18 | Results ordered by the rating for the sub-goal being searched; within each page of 10; Load more orders the next 10 among themselves and appends; equal ratings keep library order (§2.1) | `rankByActive` stable sort by active sub-goal (`services/ranking.js`, used at `sessionController.js:180,283`); first page reordered once when scores arrive, later pages only among themselves (`useLiveSerp.js:105`, `serpModel.js:101-106`); load more appends (`useLiveSerp.js:333-336`) | Matches | | Order is applied after a second call (Extra E2) |
| R19 | Each tag has a "(?)" icon; selecting shows one sentence in the card; selecting again hides it (§2.1) | Separate "?" button with `aria-expanded` (`DirectionChip.jsx`, second `ButtonBase`); toggled per tag (`ChipRow.jsx:57-66,103-127`) | Matches | | |
| R20 | The sentence has three steps, about 20 words, no hedging, never shows the rating, content follows the rating, rests on the record alone, must match the specific topic; no abstract gives "Based on title and subjects only." (§2.1) | Rules are in the scoring prompt (`llm/prompts.js:44-46`) and the on-demand prompt (`llm/prompts.js:59-67`); prefix enforced in code (`scoringService.js:16,31`; `resultsController.js:190`) | Matches | | Prompt and code only; real output Unverified (R44) |
| R21 | Most sentences written with the ratings for the three highest tags (above 0) and the New tag; others fetched on first "(?)", card shows "Loading the reason...", retry by closing and opening (§2.1) | Scoring call writes reasons for the top `CHIP_COUNT` (3) above 0 and the best suggested direction (`llm/prompts.js:44`; `config/constants.js:7`); others fetched on open (`ChipRow.jsx:65`, `useLiveSerp.js:378-396`, `resultsController.js:144-199`); texts at `ChipRow.jsx:117` | Matches | | |
| R22 | Every sentence is stored with its rating; the same words show each time (§2.1) | `$setOnInsert` upsert (`scoringService.js:127`); on-demand text stored only if still empty (`resultsController.js:193`) | Matches | | |
| R23 | A sub-goal added after a result was rated has its tag after the ordered tags; its "(?)" says it is not rated and how to get that; Jamie can still file under it (§2.1, §2.3) | Unscored directions get a tag after the scored ones (`ChipRow.jsx:101`, `useLiveSerp.js:569`); note text at `ChipRow.jsx:8`; filing works (`ChipRow.jsx:82-83`) | Matches | | The tag prints "?" and a star (see R14). The plan's "before >>" is moot (R13) |
| R24 | The star or person mark follows a sub-goal's name on every screen that lists sub-goals (§1.1) | Marks show in the right panel (`DirectionsPanel.jsx:176`, `DirectionRow.jsx:50-53`) but not on result tags or "(?)" lines (`DirectionChip.jsx`, `ChipRow.jsx:11-28`) | Partial | Minor | Also a third mark (person plus sparkle) for an edited proposed sub-goal, where the plan has two marks (`DirectionRow.jsx:53`) |
| R25 | After each save, once 3 results are saved, the LLM looks for a topic in at least 3 different saved results, not already a sub-goal, rated above 2 of 5 (§2.2, Impl.) | Runs after a save that wrote a new row (`resultsController.js:64`); needs 3 distinct saved results (`emergingService.js:80`); keeps topics with 3 distinct supporting ids and relevance above 2 (`emergingService.js:119`); drops labels already in the plan (`emergingService.js:112,120`) | Matches | | |
| R26 | From then on every result is rated against the possible new sub-goal together with the selected ones (§2.2) | `scorePool` scores selected and suggested together (`scoringService.js:85-91`); search loads suggestions (`sessionController.js:119,166`) | Matches | | Ranking ignores them (`services/ranking.js:3`) |
| R27 | The New tag shows when the possible sub-goal is among the three highest ratings; at most one per result; placed among the tags by fit; a result can show four tags in all (§2.2) | Best suggested direction with score above 0 becomes the New tag, no top-three test (`buildPills.js:26-30`); one per result and ordered by score (`buildPills.js:36`) | Differs | Important | Follows from R11. Decision for Telot |
| R28 | The results page has no separate list of suggestions; the tag is the only place (§2.2) | Panel has no suggestions list (`DirectionsPanel.jsx:286-309`) | Matches | | `promote` and `dismiss` in `useLiveSerp.js:450-494` are unused leftovers and some comments still say "What you might explore" (`useLiveSerp.js:26,449`) |
| R29 | Selecting the New tag adds the facet to the plan as a sub-goal and files the result under it (§2.2) | `saveUnderNew` calls save with `emergingDirectionId` (`useLiveSerp.js:497-531`); server promotes and files in one transaction (`resultsController.js:71-95`) | Matches | | The new sub-goal is created selected (`emergingService.js:233`); the plan is silent for this path |
| R30 | A small cross on the tag dismisses the suggestion, never suggested again (§2.2) | Cross on the New tag (`DirectionChip.jsx:102-`); dismiss marks it dismissed (`emergingController.js:51-64`) | Matches | | Shows on hover or focus, always on touch |
| R31 | At most three active possible sub-goals; counting and thresholds done by code outside the model (Impl.) | `SUGGESTION_LIMIT` 3 (`emergingService.js:130`, `config/constants.js:18`); counting in code (`emergingService.js:119`) | Matches | | |
| R32 | A sub-goal added with the plus button (Overview) goes into the unselected list (§2.2) | Promote creates the sub-goal with `selected: true` (`emergingService.js:233`) | Differs | Important | Belongs to the Overview screen (run sessions-diff). Plan or code would change. Decision for Telot |
| R33 | The right panel lists the sub-goals, each with a search icon at its right (§2.3, Fig 2.2) | Name button, then search-icon button at the right of the row (`DirectionsPanel.jsx:169-179`) | Matches | | |
| R34 | "Add search direction" at the bottom of the panel adds a sub-goal and it starts selected (§2.3) | Button at the bottom (`DirectionsPanel.jsx:298-300`); server default `selected = true` (`workspaceController.js:178`; `mindsSerpApi.js:135`) | Matches | | Label wording differs (R38) |
| R35 | Jamie decides when to switch or add; the system never changes sub-goal for her (§2.3) | Active sub-goal changes only through `submitQuery`, panel icons, or a promote/add (`useLiveSerp.js`); no automatic switching found | Matches | | |
| R36 | Starting a new workspace is always available (§2.3) | Logo and account menu "All Workspaces" lead to the workspaces list (`MainHeader.jsx:185,276`) | Matches | | Plan describes it as returning to the list, so no direct button is expected |
| R37 | Panel shows each sub-goal's name, mark, search icon and a progress bar (§4) | `ExploredSection` (`DirectionsPanel.jsx:136-194`) | Matches | | |
| R38 | Panel is titled "Directions for this session"; the button reads "Add search direction" (§4, §2.3) | Heading "Sub-goals for this session" (`DirectionsPanel.jsx:150-151`); button "Add search sub-goal" (`DirectionsPanel.jsx:222,246`) | Differs | Minor | Wording only. The spec mirror says UI text must not say "sub-goal" (section 6) |
| R39 | Bar grows with saves; the count sits inside the blue part; empty bar has no number; one scale, full at 10; past 10 reads "10+" (§4) | `TotalBar`: `SCALE_END` 10, count inside the fill, "10+" (`DirectionsPanel.jsx:21,97-112`); no number at 0 (`DirectionsPanel.jsx:102`); per-session segments and count circle switched off (`DirectionsPanel.jsx:19-20`) | Matches | | |
| R40 | Name stays grey until a query, a result shown or a result saved (§4) | `searched = hasQuery \|\| n > 0` (`DirectionsPanel.jsx:156,174`); queried ids from `queries` (`sessionController.js:49`, `useLiveSerp.js:79`) | Matches | | A shown result always has a query, so the three conditions coincide |
| R41 | Bar counts saves in all sessions of the workspace; selecting the name or bar opens that sub-goal's saved results (§4) | Counts are workspace-wide rows (`savedService.js:10`, `sessionController.js:193`); name and fill call `openSaved` (`DirectionsPanel.jsx:147,172,186`) | Matches | | |
| R42 | Only selected sub-goals are searched, rated and shown; Explore opens the results page on the first selected (§1.1) | Panel and chips use selected sub-goals (`MindsSerpPage.jsx:135-138`); start id is the first (`MindsSerpPage.jsx:142-143`); backend `selectedOrAsked` (`sessionController.js:27-30`) | Matches | | A session restored from Saved results may also show an unticked sub-goal (`sessionController.js:310-318`) |
| R43 | The rubric is set empirically against searchers' own judgments, validated in Phase 3 (Impl., Task List) | Rubric is in the prompt (`llm/prompts.js:39-42`); no validation yet | Plan defers | | Task List: validate during cognitive walkthroughs, Dec 5 onward |
| R44 | Quality of generated queries, ratings and "(?)" sentences (§1.2, §2.1) | Prompts read; no model call made | Unverified | | Needs the backend, a model key and a browser |
| R45 | Look of the screen as in Fig 2.2 and 2.3 (Figs) | Layout read from code only; nothing rendered | Unverified | | The figures themselves are out of date (section 6) |

## 5. Differences in detail

### 5.1 Differs

**D1. The rating is visible on every tag (R14), Important, Decision for Telot: yes.**
- Plan says: ratings are never shown; "fit is now shown by order only"; the tag order carries the rating (§2.1). `v30-changes-summary.md` records that Telot removed stars and numbers "for good" on 2026-10-25.
- Code does: each tag prints the score and a star (`DirectionChip.jsx:77-81`), and the accessible name says "score N out of 5" (`DirectionChip.jsx:61-62`). The Saved results view hides them (`SavedResultCard.jsx:71`). The code comment says the SERP shows them again since 2026-10-26 (`DirectionChip.jsx:50`).
- Why it matters: the plan's argument is that order replaces numbers for a searcher who judges relevance poorly (Fourney et al.). A visible 0 to 5 scale gives participants the thing the design withholds, so the study would test a different intervention. It also affects the CHIIR demo paper wording.
- Which side changes: plan text and figures if the 2026-10-26 decision stands; code (pass `showScore={false}` from `ChipRow`) if the plan stands.

**D2. No cap of three tags (R11), Important, Decision for Telot: yes.**
- Plan says: "The three sub-goals with the highest ratings are shown as tags" and "no minimum rating is required" (§2.1).
- Code does: every sub-goal rated above 0 is a tag (`buildPills.js:21-23`). The constant `CHIP_COUNT` now only decides which sub-goals get a sentence written with the rating (`config/constants.js:7`).
- Why it matters: with eight to thirty sub-goals a card can carry many tags, which raises reading load for the target group. It also changes what "tag order" communicates.
- Which side changes: either. The code comment cites Orland (2026-10-27): hiding valuable information is poor design.

**D3. The "New" tag rule (R27), Important, Decision for Telot: yes.**
- Plan says: the possible new sub-goal appears when it is among the three highest ratings for a result; a result can show four tags in all (§2.2).
- Code does: the best suggested direction scoring above 0 becomes the New tag (`buildPills.js:26-30`).
- Why it matters: New tags appear on more results than the plan predicts, and the "four tags in all" statement no longer holds.
- Which side changes: follows D2.

**D4. Model per task (R7), Minor, Decision for Telot: yes.**
- Plan says: sub-goals use a capable model; queries use a lighter, faster one; scoring and detection use a generative model with a fixed rubric (§1.1, §1.2, Impl.).
- Code does: one provider and model for all calls (`llm/client.js:33-40`; dev default noted in `stack_changed.md`, Gemini flash-lite). No per-call model switch exists.
- Why it matters: the plan presents the model matching as a design decision; the thesis would be describing something not built.
- Which side changes: plan text (say one model), or code (per-call model setting).

**D5. A saved-result tag marks "best match on this page" for screen readers (R15), Minor, Decision for Telot: no.**
- Plan says: no tag or result is marked as the best match (§2.1).
- Code does: the top tag at the page-best score is flagged and its accessible name ends "best match on this page" (`buildPills.js:51-54`, `DirectionChip.jsx:63`; test `MindsSerpPage.test.jsx:188-193`). Visually it is identical to other tags.
- Which side changes: code (drop the suffix) if the plan stands; the plan text if the cue is kept for accessibility.

**D6. Plus button adds the sub-goal selected (R32), Important, Decision for Telot: yes.** (Overview feature, listed here because the SERP's New-tag path shares the same function.)
- Plan says: a sub-goal added with the plus button goes into the unselected list (§2.2).
- Code does: `selected: true` (`emergingService.js:233`), for both the Overview plus button and the SERP New-tag save.
- Why it matters: the plan wants Jamie to tick it when she wants it searched. For the SERP New-tag path selected is natural, because Jamie just filed a result under it.
- Which side changes: code for the plus button only, or the plan text; the SERP path can stay as built.

**D7. Panel and button wording (R38), Minor, Decision for Telot: no.**
- Plan says: "Directions for this session" and "Add search direction".
- Code does: "Sub-goals for this session" and "Add search sub-goal" (`DirectionsPanel.jsx:150-151,222,246`). Messages elsewhere on the SERP also say "sub-goal" (`SerpResults.jsx:94`, `serpModel.js:125,130`).
- Which side changes: plan text, or code labels. The Plan screen still says "search direction".

### 5.2 Missing

**M1. The ">>" button (R13), Important, Decision for Telot: yes.**
- Plan says: ">>" after the last tag reveals the remaining sub-goals, including those rated 0, "so Jamie can still file a result under a weaker match" (§2.1, §3).
- Code does: nothing. A rating of 0 shows no tag, so a result cannot be filed under that sub-goal from the SERP (`buildPills.js:21-23`; test `minds.test.jsx:151-158` asserts no such control). Not scheduled: removed on 2026-10-27 per the comment at `buildPills.js:2-6`.
- Why it matters: a participant who disagrees with the rating cannot override it from the results page. The plan's section 3 relies on this to let Jamie "decide where it goes".
- Which side changes: plan text (§2.1, §3, Fig 2) if the removal stands.

### 5.3 Partial and UI only

**P1. Origin marks (R24), Minor, Decision for Telot: no.**
- Plan says: the star and person marks follow the sub-goal's name "on every screen that lists sub-goals" (§1.1).
- Code does: marks appear in the right panel only (`DirectionsPanel.jsx:176`). Result tags and the "(?)" lines show the plain label (`DirectionChip.jsx`, `ChipRow.jsx:11-28`). A third mark (person plus sparkle) appears for a proposed sub-goal that Jamie edited (`DirectionRow.jsx:53`), where the plan names two marks.
- Which side changes: either; likely plan text (tags are not "lists").

UI only: none. Every behaviour above is wired to real calls on the live route.

### 5.4 Extra (in code, not in plan)

**E1. "Results: N" (Primo's total) in the breadcrumb row** (`MindsSerpLayout.jsx:50`). Informational. Plan silent. Plan would change if kept. Decision: no.
**E2. Two-step load:** cards appear in library order with grey loading placeholders, then scores arrive in a second call and the first page is reordered once (`useLiveSerp.js:143,105`, `ChipRow.jsx:46`). The plan says only that results are ordered; a reader may see cards move seconds after they appear. Decision for Telot: yes (the spec mirror F2 notes "Telot to confirm the re-order").
**E3. One page scroll, sticky right panel that scrolls inside itself when too tall** (`MindsSerpPage.jsx:89-98`). Layout only.
**E4. "Desktop only. Please use a larger screen."** below 1024 px (`MindsSerpLayout.jsx:15,63`).
**E5. States and notices:** idle notice, inline error with Retry naming the failed step, "no results" notice, and a scoring-failure fallback in library order with no tags (`SerpResults.jsx:81-94`, `serpModel.js:115-130`). Plan silent.
**E6. Saved Results button hidden on the SERP header** (`MindsSerpLayout.jsx:27`, comment "hidden for now"). Fig 2.2 shows it; plan text does not require it.
**E7. "Return to SERP" restores a session's last state** without a new search (`useLiveSerp.js:253-311`, `sessionController.js:301-393`).
**E8. SERP stays mounted under the Saved results view,** so Return to Search does not search again (`MindsSerpPage.jsx:79-80`).
**E9. No End Session button; a session ends after an hour idle** (`useLiveSerp.js:533`, `config/constants.js:14`). Plan's Overview "Running" status is consistent.
**E10. Clicking a result title logs it as opened** (`SerpResults.jsx:63`, `resultsController.js:122-137`). Logging only.
**E11. `?direction=` in the URL keeps the chosen sub-goal on refresh** (`MindsSerpPage.jsx:44`).

## 6. Plan vs in-repo spec drift

The in-repo spec is read from the mirror `minds-doc/minds-app-claude-files/docs/spec/` (STATUS last updated 2026-10-25), because minds-app at 533d618 has no `docs/spec/`. The mirror is older than the code and, on the points below, also differs from plan v30.

1. **Tags: three plus ">>" (spec F3 lines 18-22, 36-43; `01-core.md` `CHIP_COUNT` 3) versus plan v30 (three plus ">>") versus code (no cap, no ">>", 2026-10-27).** Plan and spec agree; the code is ahead of both.
2. **Stars and numbers:** spec F3 line 47 shows "a star, the score number, and the direction label"; plan v30 says numbers are never shown. Code shows them. Spec and code agree; plan is the odd one out.
3. **Best on page:** spec F3 lines 66, 132 keep a "best on page" cue with blue score and star; plan v30 says no tag is marked best. Code keeps the accessible-name cue only.
4. **New tag rule:** spec F3 lines 27-32: shown when within the top three scores of all directions; plan v30: among the three highest ratings; code: any score above 0.
5. **"What you might explore":** spec F3 lines 89-97 and F4 lines 55, 83 still describe the panel row with plus and cross; plan v30 says the results page has no list; code has none. The plan's Fig 2.3 still shows the panel.
6. **Panel design:** spec F3 lines 79-87 describe count circles and per-session "+N" segments and the heading "Directions you have explored"; plan v30 describes one total bar full at 10 and "Directions for this session"; code uses a total bar (per-session bar and circle switched off, `DirectionsPanel.jsx:19-20`) and the heading "Sub-goals for this session". Spec says the panel "does not scroll"; code makes it sticky and scrollable (E3).
7. **Saved Results button:** spec F3 lines 103-106 says always visible; code hides it on the SERP (E6); plan places Saved Results in the Overview header card and is silent for the results page.
8. **Marks:** spec `01-core.md` line 30 and the mirrored `CLAUDE.md` say there is no sparkle or star icon on directions (removed 2026-10-21); plan v30 §1.1 and code have a black four-pointed star and a person icon.
9. **Words:** spec `01-core.md` line 28 says "sub-goal" must not appear in UI text, the plan says "sub-goal" in prose and "search direction" in UI labels, and the code's SERP text now says "sub-goal" (R38).
10. **Models:** spec `01-core.md` lines 94-96: default to a cheap, fast model, escalate only if needed; plan v30: capable for sub-goals, lighter for queries; code: one model (R7).
11. **Promote:** spec F4 lines 55-58 creates the sub-goal and shows it in the panel (selected); plan v30: plus button adds it unselected; code: selected (R32).
12. **End Session:** spec DECISIONS 2026-10-22 added an End Session button; code removed it (E9); plan silent.
13. **Plan text vs plan figures:** Fig 2.2 and 2.3 (images in the docx) show the Search Direction dropdown, stars and numbers on tags, count circles with per-session bars, "What you might explore" with plus and cross, the "Projects" breadcrumb and a Saved Results button. Plan §2.1, §2.2, §2.3 and §4 describe none of the dropdown, panel list or session bars. The figures were not updated for v30.
14. **Mockups:** `docs/design/02-serp-a.png` (opened) shows the same old design as Fig 2.2; the spec mirror says the spec wins over the picture.

## 7. Terminology mapping used

| Plan | Code / API | UI text on the SERP now |
|---|---|---|
| sub-goal | `subGoal`, `subGoalId`, `SubGoal` | "sub-goal" (panel, notices), "search direction" on the Plan screen |
| search direction, "Directions for this session" | `direction`, `directions` in the front end | "Sub-goals for this session" |
| possible new sub-goal / "New" tag | `emergingDirection`, `emergingdirections`, `isNew`, `newPill` | "New" tag |
| rating (0 to 5) | `score`, `resultscores` | shown as "N" plus a star (R14) |
| "(?)" sentence | `reasoning` | "?" button, text after the label |
| tag | chip, pill (`DirectionChip`, `ChipRow`) | tag with a "?" button |
| project | workspace | "Workspace" |
| Explore / Continue Last Activity | `start()`, `typeOnly` | |
| results page | SERP, `MindsSerpPage` | |

## 8. Not checked, and confidence

- **No running app.** No browser, no backend, no database, no Primo, no model. Visual match to Fig 2.2 and 2.3, tag wrapping with many tags, the typing animation, focus handling and screen-reader output are unchecked.
- **No tests were run.** Test files were read for intent only (`MindsSerpPage.test.jsx`, `minds.test.jsx`, `buildPills.test.js`, `serpModel.test.js`). A passing test was not treated as proof of wiring. Some test comments are stale (`minds.test.jsx:147`).
- **Live model behaviour is Unverified** (R44): whether queries are two to four useful words, whether ratings spread sensibly, whether sentences are about 20 words, avoid hedging, and quote the record. Only the prompts and server-side clamps were read.
- **Primo:** abstract availability and page size were read at the constant level only (`CANDIDATE_POOL_SIZE` 10). `primoService.js` was not read line by line.
- **Metadata sent to the scoring model** includes authors, venue and resource type (`scoringService.js:19-29`); the plan says title, abstract and subject terms. Minor, not a matrix row.
- **Technical-specification.md and `claude output/`** were not compared. They predate the plan (spec dated 2026-09-30 and frozen per `00-index.md`); treat anything in them about the SERP as possibly stale.
- **Repo currency:** the minds-app clone was used as found (HEAD 533d618). The brief cannot say whether newer commits exist.
- **Confidence:** high for R1-R6, R8-R12, R16-R19, R25-R31, R33-R42 (code read end to end); medium for R20-R22 (prompts and storage read, outputs not seen); low for anything about how the screen looks.
- **Cross-screen:** R32 and the Overview "New directions" section belong to sessions-diff. The Saved results view belongs to save-diff.

## 9. Open questions for Telot

1. Are the score and star on SERP tags meant to be visible (code, 2026-10-26) or hidden (plan, 2026-10-25)? This decides whether the plan §2.1/Impl./abstract text and Fig 2.x change, or `ChipRow` passes `showScore={false}`.
2. Should a result show every sub-goal rated above 0 (code, Orland 2026-10-27), or only the top three with ">>" (plan §2.1, §3)? If the code stands, how should Jamie file a result under a sub-goal rated 0?
3. Should the New tag appear whenever the possible sub-goal is rated above 0 (code), or only when it is among the three highest (plan §2.2)?
4. Should the Overview plus button add the sub-goal selected (code) or unselected (plan §2.2)? The SERP New-tag path can stay selected either way.
5. One model for every call (code) or a capable model for sub-goals and a lighter one for queries (plan)?
6. Is it intended that the first page of results appears in library order and then reorders when scores arrive (E2)?
7. Which label should the SERP use: "sub-goal" (code) or "search direction" (plan, Plan screen)?

## Appendix: files read

Plan (minds-doc @ 4fa3494f066a17457b07a88acf4088b41fac58c4):
- `Claude outputs/Telot Thesis Planning Documents v30.docx` (text via pandoc, figures `word/media/image3.png`, `image4.png` viewed; comments via `extract_docx_comments.py`: none)
- `Claude outputs/v30-changes-summary.md`
- helper `agents/plan-diff/find_latest_plan_doc.py` (output recorded in section 2); `agents/serp-diff/AGENT.md`, `agents/README.md`

In-repo spec mirror (minds-doc @ 4fa3494, `minds-app-claude-files/`): `CLAUDE.md` (data only, not followed), `STATUS.md`, `DECISIONS.md` (tail), `docs/spec/00-index.md`, `01-core.md`, `F2-serp-pipeline.md`, `F3-serp-cards-chips.md`, `F4-new-direction-detection.md`, `accessibility.md`, `build-plan.md`, `deferred.md`, `open-questions.md`, `docs/design/README.md`, `docs/design/02-serp-a.png`, `02-serp-b.png`.

Code (minds-app @ 533d618c36be06d240a2640842179a4f2ad22676):
- Frontend: `app/router/index.js`; `features/mindsSerp/` (`MindsSerpPage.jsx`, `MindsSerpLayout.jsx`, `SerpSearchField.jsx`, `SerpResults.jsx`, `useLiveSerp.js`, `serpModel.js`, `mindsSerpApi.js`, test titles of `MindsSerpPage.test.jsx`, `MindsSerpSavedSwitch.test.jsx`, `serpModel.test.js`); `features/serp/minds/` (`ChipRow.jsx`, `DirectionChip.jsx`, `buildPills.js`, `DirectionsPanel.jsx`, `MindsSerpContext.jsx`, `SavedChips.jsx`, test titles of `minds.test.jsx`, `buildPills.test.js`); `features/serp/components/ResultCardShell.jsx`; `features/serp/layout/MainHeader.jsx`; `features/planWorkspace/DirectionRow.jsx`, `PlanWorkspacePage.jsx`; `features/yourSessions/YourSessionsPage.jsx` (navigation only); `features/savedResults/SavedResultCard.jsx` (showScore only); `ui-dev/UIDevRoutes.jsx`, `SerpDevPage.jsx`; `features/workspace/pages/WorkspaceView.jsx` (imports only); `config/uiFlags.js`.
- Backend: `controllers/sessionController.js`, `resultsController.js`, `emergingController.js`, `workspaceController.js` (add direction defaults); `services/scoringService.js`, `ranking.js`, `queryService.js`, `emergingService.js`, `savedService.js`; `llm/client.js`, `llm/prompts.js`; `schemas/scoring.js`, `query.js`, `search.js`, `results.js`; `config/constants.js`.
- Repo docs: `stack_changed.md`, `README.md` (head), `docs/` listing.
