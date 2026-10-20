# Saved results diff: code vs plan

Generated: 2026-10-20 00:05 (Regina time) by save-diff
Plan document used: `Claude outputs/Telot Thesis Planning Documents v27.docx` (version v27, internal date "Project Revised: (Oct 15, 2026)", last commit 9687698 2026-10-17 "uploaded v27 doc manually from macbook"; minds-doc HEAD fc321d4 2026-10-19)
Code checked: Akane-Asahi/minds-app @ ba707ba48c21 (2026-10-19 20:38 -0600), branch main (read-only; nothing fetched or pulled)
Scope: all Saved results screens (all saved results, one direction, one session, one direction in one session, and the buttons that lead there)

> Warnings:
> - Run under caller overrides: no clone, pull or fetch, nothing committed or pushed. The clones were used as they were. minds-doc HEAD is fc321d4.
> - Plan date vs spec date: the in-repo spec `docs/spec/F6-saved-views.md` records layout decisions "by Telot 2026-10-19", four days after the plan's internal date (Oct 15) and two days after its commit (Oct 17). Where the two disagree, that is evidence the plan is stale, not proof (section 6).
> - The planning document has 0 tracked changes and 0 Word comments, so no unresolved plan comments touch saved results.
> - Nothing was run in a browser. All "Matches" rows mean the source code does it. STATUS.md says U4 was "not yet checked by keyboard or screen reader" (STATUS.md:29). Test status is quoted from STATUS.md as reported, not re-run.

## 1. Summary

- The Saved results view is built as UI only. It lives in `frontend/src/features/savedResults/` and renders from mock fixtures at the dev-only route `/ui/saved-results`. It has no production route, no endpoint, and no database reads (R26).
- Presentation matches the plan's Figs 3 and 4 closely: header with disabled search box and Return to Search, breadcrumb, grouping by session newest first, no groups for a session view, solid-blue saved chips and grey unsaved chips with stars, plain counts.
- The only saved view a participant can reach in a production build is Baseline's legacy flat list (newest first, bookmark card). The SERP copy's Saved Results toggle opens a different MINDS-flavoured flat list that has no grouping, no counts and no filters (R3, E9).
- The biggest plan-side problems are three stale Task List claims that contradict the plan's own body: goal-linked saving, "Suggested Next Step" and "Recap and Resume" screens, and embedding-based 1 to 5 star ratings (R27, R28, R29).
- Smaller differences: the plan's Figs 3 and 4 show two counts and the code shows three; the saved view shows all scored directions with no ">>"; Fig 5 shows Session 2 with 0 saved but the mock data now saves one result there.

Counts: Matches 14 · UI only 7 · Partial 4 · Differs 7 · Missing 1 · Plan defers 0 · Unverified 1 · Extra 9
(34 plan requirements, R1 to R34, plus 9 extras, E1 to E9.)
By severity, across the 20 differences (rows that are not Matches): Blocker for the study 0 · Important 7 · Minor 13. The 9 extras are all Minor.

How I used the status words: **Matches** = the code does the same thing for the same rule, and the rule does not depend on the data source. **UI only** = the behaviour exists in code but only on mock fixtures under the dev route, so it needs wiring (build row I6, plus I3, I5, I7).

## 2. Which plan document was used

Chosen by `agents/plan-diff/find_latest_plan_doc.py` ("highest version number v27"). It printed no warnings and no ties.

| Candidate | Version | Trailing | Used? |
|---|---|---|---|
| Telot Thesis Planning Documents v27.docx | 27 | 0 | **yes** |
| Telot Thesis Planning Documents v7 - SRL Stripped-3.docx | 7 | 3 | no (older) |
| Telot Thesis Planning Documents v7 - SRL Stripped-2.docx | 7 | 2 | no |
| Telot Thesis Planning Documents v7 - SRL Stripped-1.docx | 7 | 1 | no |
| Telot Thesis Planning Documents v7 - Restructured.docx | 7 | 0 | no |
| Telot Thesis Planning Documents v7 - SRL Stripped.docx | 7 | 0 | no |

v27 discusses saved results (Prototype Design Overview sections 3 and 5, Figs 3 and 4, Fig 5). No older candidate has a newer internal date. Ignored as non-plan files: two user persona docx files, `technical-specification.md`, `plan-diff.md`, `sessions-diff.md`, change summaries, `citation-verification.md`, one Word lock file.

Figure mapping is by order, as printed by the extract step: image1 = Fig 1, image2 = Fig 2.1, image3 = Fig 2.2, image4 = Fig 2.3, image5 = Fig 3, image6 = Fig 4, image7 = Fig 5. I opened image3, image5, image6 and image7. I did not open image1, image2 or image4 (not saved-results screens). Fig 2.3's description comes from the picture of image3 only; Fig 2.3 itself was not opened.

What the opened figures show:
- **Fig 3** (Screen 3, saved results for one sub-goal, "Physical health benefits"): logo; disabled-looking search box with "urban green space mental health benefits policy"; account icon; Return to Search button. Breadcrumb "Projects > How green spaces affect wellbeing > Physical health benefits". Two counts: folder icon 3, three-arrows icon 1. Group headings "SESSION 3 · SEP 23" and "SESSION 1 · SEP 18" with a rule. Three cards (1 in Session 3, 2 in Session 1). Each card has a type icon and label (Journal article, Report), title, "year · authors", "Description:" text with "Read more", then chips: a solid-blue saved chip with "4★ Physical health benefits (?)" and up to one grey chip such as "2★ Mental health benefits (?)". List fills the left ~70%; right side empty.
- **Fig 4** (Screen 4, one session, "Session 3"): same header. Breadcrumb ends "Session 3". Counts folder 6, arrows 3. Six cards, no group heading. Chips as in Fig 3.
- **Fig 5** (Screen 5, Project Overview): header with a "Saved Results" button and no search box; Continue Last Activity; three cards; Sessions panel (Session 3: Mental health +4, Physical health +1, Indigenous placemaking +1, "6 saved"; Session 2: Community access +0, "0 saved"; Session 1: Physical health +2, "2 saved"); Directions panel with circles 4, 3, 1, 0, and a dashed "–" for the New direction.
- **Fig 2.2** (image3): SERP header with a "Saved Results" button next to the account icon.

## 3. Which code is the live Saved results view

Four separate pieces of saved-view code exist. Only the legacy one is reachable in a production build.

| Piece | Files | State |
|---|---|---|
| **MINDS Saved results view (F6, U4)** | `frontend/src/features/savedResults/SavedResultsScreen.jsx`, `SavedResultCard.jsx`, `savedModel.js` (+ 2 test files) | **Dev-only, mock fixtures.** Mounted only by `frontend/src/ui-dev/UIDevRoutes.jsx:8,118-148` at `/ui/saved-results?direction=&session=`. `/ui` is lazy-loaded only when `NODE_ENV === "development"` (`frontend/src/app/router/index.js:24-27,70-79`). This is the view that implements F6 (grouping, counts, filters). |
| SERP copy's saved list | `frontend/src/features/serp/pages/WorkspaceView.jsx:84-86,157-159`, `serp/components/SavedSearchResults.jsx:11-27`, `serp/components/SavedDocumentCard.jsx:100`, `serp/minds/SavedChips.jsx` | **Dev-only** (the SERP copy is only mounted by `ui-dev/SerpDevPage.jsx:4`). A flat list, newest first, one solid chip per saved direction, unsaving the last chip removes the card (`SavedChips.jsx:8-12`, `SavedDocumentCard.jsx:44-60`). No grouping, no counts, no filters, no breadcrumb. This is what the SERP's Saved Results toggle opens (`serp/layout/Layout.jsx:65-68`). |
| **Baseline legacy saved view** | `frontend/src/features/search/pages/SavedSearchResultsView.jsx`, `search/components/SavedSearchResults.jsx`, `shared/components/SavedDocumentCard.jsx` (bookmark button), data from `features/workspace/api/savedDocsQueryService.js:10` (`POST /api/saveddocs/querylist`) | **The only live, production-routed saved view.** Reached through `/workspace` -> `features/workspace/pages/WorkspaceView.jsx:5,155` (`router/index.js:19,91-94`). Real data via `/api/saveddocs`. It is the control condition's code. |
| Duplicate | `features/search/components/SavedSearchResults.jsx` vs `features/serp/components/SavedSearchResults.jsx` | Same file apart from the card import path (diff showed only the import line). |

Entry points into the MINDS view:
- Your sessions header button, count circles, bar segments and session tiles all call `onNavigate({ to: "saved-results", ... })` (`yourSessions/YourSessionsScreen.jsx:97`, `DirectionCard.jsx:23,65`, `SessionTile.jsx:64`). The dev route turns that into a `/ui/saved-results` URL (`UIDevRoutes.jsx:52-70`). Your sessions itself has no production route.
- SERP right panel: circles and bar segments only show a mock message (`serp/minds/DirectionsPanel.jsx:69,83`); they do not open any view.
- SERP header toggle: `MainHeader.jsx:196-220` calls `onTabChange`; on the SERP copy that sets the hash to `#all` and opens the SERP copy's flat list, not the F6 view.

Data: the MINDS view reads fixtures from `getSessionsFixture` (`mocks/sessionsFixtures.js`), with no `fetch`, axios or React Query in the `savedResults` folder (grep). The "?" reason falls back to the text "Mock only: the reason would be fetched here." (`SavedResultCard.jsx:8,52`). Backend: the `SavedResult` model exists (`backend/models/savedResultModel.js:11-26`) but no route or controller uses it (grep of `backend/` finds it only in `models/`, `__tests__/models.test.js` and `subGoalModel.js`). `backend/routes/saveddocsRoutes.js:17-24` has only add, remove, byExternalId, saveQueryOnSearch, querylist, countsByWorkspace. The spec's `GET /api/workspaces/:id/saved` (`docs/spec/03-api.md:25`) does not exist. Build row I6 "F6 wiring" is not started (`docs/spec/build-plan.md:47`, `STATUS.md:46-51`).

## 4. Requirement matrix

Plan citations: "§3" = Prototype Design Overview "3 Organization: Saving into Sub-Goals"; "§4" = "4 Monitoring"; "§5" = "5 Cross-Session Support: Resuming a Project"; "Control" = "Keeping the Searcher in Control"; "Impl" = "Implementation Note"; "TL" = Task List. File paths are under `/home/claude/akane-asahi/minds-app/frontend/src/` unless marked `backend/` or `docs/`.

| ID | Plan says (section/fig) | Code does (path:line) | Status | Severity | Notes |
|---|---|---|---|---|---|
| R1 | Saved views are "Screen 3" (one sub-goal) and "Screen 4" (one session); Project Overview is "Screen 5" (Fig 3, 4, 5 captions) | No screen numbers in the UI. Spec says to use names; "numbers differed across old documents" (`docs/spec/01-core.md:36-38`). Spec calls Your sessions "Screen 3" in places | Differs | Minor | Naming only. The plan has no figure or number for the whole-project view |
| R2 | Project Overview has a Saved Results button that opens the saved results of the whole project (Fig 5; §5) | `features/yourSessions/YourSessionsScreen.jsx:97` (header button calls `onNavigate({to:"saved-results"})`); dev route turns it into `/ui/saved-results` (`ui-dev/UIDevRoutes.jsx:59-60`) | UI only | Minor | Your sessions has no production route. Navigation is wired only in `/ui` (DECISIONS.md 2026-10-19 "Dev navigation is wired ... a Phase 1 exception") |
| R3 | SERP header has a Saved Results button that opens the saved results (Fig 2.2/2.3; §5) | Button exists: `features/serp/layout/MainHeader.jsx:196-220`. On the SERP copy it sets hash `#all` (`serp/layout/Layout.jsx:65-68`) and shows the flat SERP-copy list (`serp/pages/WorkspaceView.jsx:84-86,157-159`), not the F6 view | Partial | Important | The button is there; what it opens is not the view in Figs 3 and 4. F5/F3 want it to open F6 with no filter (`docs/spec/F3-serp-cards-chips.md:103-106`); scheduled I7 |
| R4 | Saved Results opens saved results of "the whole project" (§5) | No-filter variant: `features/savedResults/savedModel.js:29-31` (no filters = all rows), crumb "All Saved Results" (`:71`), h1 "All saved results" (`:73`). Test: `savedModel.test.js:7` | UI only | Minor | Works on fixtures only. Plan gives no layout for this variant (see E1) |
| R5 | View for a sub-goal shows everything saved under it across the project (§3; Fig 3) | `savedModel.js:30` filters `r.subGoalId === directionId`; test `savedModel.test.js:35` and `:56` (equals the Your sessions circle) | UI only | Minor | Mock fixtures; I6 wires it |
| R6 | The sub-goal view groups its results by session, with a heading per session "SESSION 3 · SEP 23" and a rule (§5; Fig 3) | `savedModel.js:53-56` builds groups and headings `Session ${n} · ${day}`; `SavedResultsScreen.jsx:85-92` renders an h2 in small uppercase letter-spaced text with a rule | Matches | n/a | Only sessions with saves get a group (`savedModel.js:33-39`). Heading text is made uppercase by CSS |
| R7 | Sessions are listed newest first (Fig 3: Session 3 above Session 1) | `savedModel.js:55` sorts by `b.session.number - a.session.number` | Matches | n/a | |
| R8 | The session view shows everything saved in that session across sub-goals, as one list (§5; Fig 4 has no group headings) | `savedModel.js:30` (session filter), `:56` (heading null when `sessionId` set); `SavedResultsScreen.jsx:85` (no heading rendered) | Matches | n/a | |
| R9 | The sub-goal view "can be limited to one session" (§3) | `savedModel.js:30` supports both filters; reached from a Your sessions bar segment (`yourSessions/DirectionCard.jsx:65`); test `savedModel.test.js:50` | UI only | Minor | Dev route only |
| R10 | Order of cards inside a session group (plan text silent; Figs 3 and 4 imply earliest save first) | `savedModel.js:31` sorts by `savedAt` ascending. Card order matches Fig 4 and Fig 3 | Matches | n/a | Plan text never states the order; only the figures do |
| R11 | Header: logo, search box showing the last query (disabled look), account icon, Return to Search button (Figs 3, 4; text is silent) | `SavedResultsScreen.jsx:43` (`MainHeader ... savedMode showSearch searchPreview={lastQuery}`); disabled `TextField` `MainHeader.jsx:34-45,164-165`; label "Return to Search" `MainHeader.jsx:219`. Test `SavedResultsScreen.test.jsx:24-28` | Matches | n/a | The last-query text in the figures differs between Figs 3/4 ("...mental health benefits policy") and Fig 5 ("...mental health policy"); see P10 |
| R12 | Breadcrumb "Projects > {project name} > {sub-goal \| Session n}" (Figs 3, 4) | `SavedResultsScreen.jsx:49-59`; last segment `savedModel.js:71` ("Physical health benefits", "Session 3", "All Saved Results", "{direction} · Session n") | Matches | n/a | "Projects" is "Workspaces" in the app (terminology). Segments are links except the last (`aria-current="page"`) |
| R13 | Header counts: two plain counts, a folder icon with the number of results and a three-arrows icon with the number of directions: 3 and 1 (Fig 3), 6 and 3 (Fig 4) | Three counts: results (document icon), directions (three arrows), sessions (history icon) (`SavedResultsScreen.jsx:69-73`; `savedModel.js:58-63`). The two shared counts give 3/1 and 6/3 for the fixtures (`docs/spec/F6-saved-views.md:36-42`) | Differs | Minor | The code adds a sessions count and uses a document icon; Figs 3 and 4 have neither. Decision for Telot: yes. F6 says Telot decided on three counts, 2026-10-19 |
| R14 | Counts are plain counts, never percentages; the progress cues use little text (§4; Abstract) | `SavedResultsScreen.jsx:17-25,69-73` (icon + number, screen-reader label); `savedModel.js:59-63` counts only | Matches | n/a | |
| R15 | List fills the left part of the page, nothing on the right (Figs 3, 4) | `SavedResultsScreen.jsx:67` (`maxWidth: lg: 72%`) | Matches | n/a | |
| R16 | Card: type icon and label, title, "year · authors", "Description:" text with "Read more" (Figs 3, 4) | Shared card shell: `SavedResultCard.jsx:19-20,59` (icon via `toDoc`, title, `year · authors`), abstract with "Read more" toggle via `shared/components/AbstractToggle.jsx:5,99` | Partial | Minor | The word "Description:" in the figures is not in the code (grep for "Description" in `frontend/src` finds only icon names). I did not check whether the type label reads "Journal article" or "Article" (`shared/iconMapper.js:33-35` uses "Article") |
| R17 | Each tag shows a rating from 0 to 5 as a number and a star, then the sub-goal name, e.g. "4★ Physical health benefits" (§2.1; Fig 3) | `serp/minds/DirectionChip.jsx:60-64` (`{score}★` then label) | Matches | n/a | |
| R18 | A solid blue tag means saved; unsaved tags are lighter (§2.1; Figs 3, 4 show grey for unsaved) | Saved = solid blue (`DirectionChip.jsx:49`), unsaved on the saved view = white with grey border (`:46`, `SavedResultCard.jsx:37` passes `variant="neutral"`) | Matches | n/a | Light blue ("strongest on page") is a SERP-only rule and is not used here |
| R19 | Saved views carry "the same star-and-tag cues as the results page" (§3, §5); the results page shows the 3 highest-rated tags, ties in planning order, and ">>" reveals the rest (§2.1) | Saved chips first (by `orderIndex`), then every other scored direction highest first, with no cap and no ">>" (`savedModel.js:45-49`; `SavedResultCard.jsx:31-44`). Ties are not broken by planning order | Differs | Minor | Figs 3 and 4 show at most 2 chips per card. F6 says the same as the code (`docs/spec/F6-saved-views.md:47-50`). Decision for Telot: yes |
| R20 | Each result "still shows which sub-goals it matched when Jamie saved it" (§5) | Chips read stored scores for the result (`savedModel.js:43-44`, fixtures in `mocks/sessionsFixtures.js`) | UI only | Minor | Mock scores. STATUS.md:27 says scores are stored and never re-requested, so the real behaviour should match once I6 reads `resultscores` |
| R21 | Each tag has a "(?)" that opens an explanation of why the result may help (§2.1; Control); saved views carry the same tags | `SavedResultCard.jsx:21-26,46-55` opens the reason in place; null reason shows the placeholder (`:8,:52`). No reasoning route in `backend/routes/` (grep) | UI only | Minor | Scheduled I3 (`docs/spec/build-plan.md:44`) |
| R22 | Selecting a tag files the result under that sub-goal; selecting it again removes it (§3) | On the saved view, clicking a saved chip flips a local override (`SavedResultsScreen.jsx:34,39`; `SavedResultCard.jsx:41`); nothing is sent or stored. Test `SavedResultsScreen.test.jsx:51-60` | UI only | Minor | The plan describes this for the results page; the saved-view behaviour is in F6 (see E2, E3) |
| R23 | The system does not read the results for Jamie and does not write summaries (Control) | The card shows the Primo abstract only (`SavedResultCard.jsx:11-12`); no network or LLM call exists anywhere in `features/savedResults/` (grep) | Matches | n/a | |
| R24 | Plan's AI components are sub-goal generation, query generation, result scoring, new-direction detection (Impl); none runs on the saved view | The saved view makes no Primo or LLM call (grep, as R23) | Matches | n/a | F6 allows one on-demand reasoning call on a null reason (`docs/spec/F6-saved-views.md:14-17`); the plan's Impl Note does not list that call (section 6) |
| R25 | Purpose: saved results "can be viewed by sub-goal and by session" so a returning searcher can recover what was saved and why (Abstract; §3; §5; Jamie's Wednesday scenario) | All four scopes exist on mock data only (see R2, R4, R5, R9). A participant in a production build gets Baseline's flat list instead (section 3) | Partial | Important | Depends on R26 |
| R26 | A working Saved results view in the MVP: real data and navigation (TL "Build the MVP" Oct 5 to Nov 5; Fall goal 2) | No production route (`app/router/index.js:83-97`; the spec's `/workspace/:id/saved` is absent); no `GET /api/workspaces/:id/saved`; no controller reads or writes `savedresults` (`backend/models/savedResultModel.js:11-26`; `backend/routes/saveddocsRoutes.js:17-24`) | Missing | Important | Scheduled: I6 (`docs/spec/build-plan.md:47`), needing I2, I3, I5, I7. Not "Blocker" only because those rows are still ahead (see section 9, question 5) |
| R27 | TL: "Implement goal-linked saving so results file directly under the sub-goal through which they were found" and Fall goal 2 "goal-linked saving" | §3 says the searcher picks the sub-goal by selecting a tag, and "Jamie decides both whether to save a result and where it goes". Code: chips choose the direction (`DirectionChip.jsx:53-57`; `SavedResultCard.jsx:41`) | Differs | Important | Plan contradicts itself; the code matches §3. The plan's Task List needs to change |
| R28 | TL: "the Suggested Next Step mechanism" and "the Recap and Resume screens" (Phase 1; Fall goal 2) | §Control says the system "does not choose the next step" and writes no summaries. Code has no recap or next-step feature; both are listed as deferred (`docs/spec/deferred.md:8-10,20-25`). The Project Overview (Fig 5) replaces them | Differs | Important | Touches the saved view only indirectly (the Resume path). The plan's Task List needs to change |
| R29 | TL: "embedding-based cosine similarity ... mapped to a 1-5 star relevance rating"; Phase 3 "Validate the similarity thresholds for the star ratings (1 ★ to 5 ★)" | §2.1 and Impl say ratings are whole numbers 0 to 5 from a generative model with a rubric, and explain why embeddings were not used. Code and spec use 0 to 5 integers (`docs/spec/01-core.md:68`; `DirectionChip.jsx:60`) | Differs | Important | The stars on saved cards come from this. The plan's Task List needs to change |
| R30 | Fig 5: Session 2 saved nothing ("Community access +0", "0 saved"); Sessions panel totals 6 + 0 + 2 | Mock data now saves one result in Session 2 (`mocks/sessionsFixtures.js:128-129,155-160`), so totals are 9 results, 4 directions, 3 sessions (`SavedResultsScreen.test.jsx:32`; DECISIONS.md 2026-10-19 U4) | Differs | Minor | Decision for Telot: yes. The change was made so the all-sessions view has three groups |
| R31 | Fig 3 content: 3 results (Session 3: Walkability 4★ Physical + grey 2★ Mental; Session 1: Physical Activity Outcomes 4★ + grey 2★ Community access; Green Space Proximity 5★) | Fixture: Session 1 has the two Physical results, Session 3 has Walkability (`mocks/sessionsFixtures.js:134-148,186-190`); the code's own mockup `docs/design/05-saved-single-direction.png` is the same picture | Matches | n/a | Compared with the code's mockup and fixture text; the scores of the two Session 1 items were cut off in my read of the fixture lines, so those two chip scores are taken from the mockup, not from code |
| R32 | Fig 4 content: Session 3 has 6 cards in this order: Neighbourhood Parks 5★, Urban Green Space Exposure 4★, Mindfulness 4★, Access to Nature 3★, Walkability (4★ + grey 2★), Indigenous-Led Placemaking 3★ | Fixture session s3 produces exactly these six in this order (`mocks/sessionsFixtures.js:163-195`); same as `docs/design/06-saved-single-session.png` | Matches | n/a | |
| R33 | Accessibility on this screen: plan has no rule for it; Abstract says progress cues use little text | Spec rules exist (`docs/spec/accessibility.md:65-70`); code has a hidden h1, a polite status region, screen-reader count labels and native `aria-pressed` buttons (`SavedResultsScreen.jsx:20-22,46-47`; `DirectionChip.jsx:54-56`) | Unverified | Minor | STATUS.md:29 says not yet checked by keyboard or screen reader; I did not check either |
| R34 | Fall goal 2: by November 5 "MVP complete: planning, ... goal-linked saving, ... integrated and confirmed through informal use" | Done: U0 to U4 UI and I0, I1 (`STATUS.md:11-42`). Not done: U2 (restarted), I2 to I8 (`STATUS.md:46-51`) | Partial | Important | Plan says Nov 5; today is 2026-10-20. See section 9, question 5 |
| E1 | (plan silent) | The whole-project view's layout: h1 and breadcrumb "All saved results / All Saved Results", grouped by session, and heading text for the four scopes (`savedModel.js:71-73`) | Extra | Minor | |
| E2 | (plan silent) | Unsaving on this view keeps the card with its chip grey until the participant leaves (`savedModel.js:69-76` via overrides; `SavedResultsScreen.jsx:34-39`; test `:51`) | Extra | Minor | F6 decision; the Baseline-style legacy and SERP-copy lists remove the card instead (E9) |
| E3 | (plan silent) | Clicking a grey chip saves the result under that direction from the saved view (`SavedResultCard.jsx:41`) | Extra | Minor | |
| E4 | (plan silent) | The three counts update live when a chip is toggled (`SavedResultsScreen.jsx:35`; `savedModel.js:58-63`) | Extra | Minor | |
| E5 | (plan silent on what is clickable) | Circles, bar segments and session tiles on Your sessions open the saved view with `direction`, `direction`+`session`, `session` (`DirectionCard.jsx:23,65`; `SessionTile.jsx:64`). The SERP panel's circles and segments show a mock message only (`serp/minds/DirectionsPanel.jsx:69,83`) | Extra | Minor | The plan describes the circle, the segments and the Sessions panel but never says they open Screens 3 and 4 |
| E6 | (plan silent) | Empty state "Nothing saved here now"; loading skeletons with `aria-busy`; error with Retry (`SavedResultsScreen.jsx:61-65,76,78-80`) | Extra | Minor | |
| E7 | (plan figures show a plain solid chip) | Saved chip also shows a check icon and the text "Saved" (`DirectionChip.jsx:66-71`) | Extra | Minor | `docs/spec/F3-serp-cards-chips.md:52` and `open-questions.md` item 4 mark this provisional |
| E8 | (plan silent) | Screen-reader support: hidden h1 per scope, polite status text, labelled counts, native buttons (`SavedResultsScreen.jsx:20-22,46-47`) | Extra | Minor | See R33 |
| E9 | (plan silent) | Two other saved lists exist in code: the SERP copy's flat list with solid chips only (`serp/components/SavedSearchResults.jsx:11-27`, `serp/minds/SavedChips.jsx:13-60`) and Baseline's bookmark list (`search/components/SavedSearchResults.jsx`; `shared/components/SavedDocumentCard.jsx:8,62`) | Extra | Minor | Baseline's list is the control and must stay; the SERP copy's list is a candidate to replace at I6/I7 |

## 5. Differences in detail

### 5.1 Differs

**R1 Screen names and numbers**
- Plan says: Screen 3 and Screen 4 are the saved views; Fig 5 is Screen 5 (captions).
- Code does: names screens, not numbers, and says numbers differed across documents (`docs/spec/01-core.md:36-38`).
- Why it matters: a reader of the plan and the spec can mean different screens by "Screen 3" (the spec's feature file for Your sessions uses "Screen 3").
- Which side would change: either; no behaviour is affected. Decision for Telot: no.

**R13 Counts row**
- Plan says: two counts, a folder icon (results) and a three-arrows icon (directions) (Figs 3 and 4).
- Code does: three counts, a document icon (results), three arrows (directions) and a history icon (sessions) (`SavedResultsScreen.jsx:69-73`).
- Why it matters: the figures in the thesis would not match the screens participants see.
- Which side would change: the plan's figures, if Telot's 2026-10-19 decision stands (`docs/spec/F6-saved-views.md:36-42`); otherwise the code. Decision for Telot: yes (confirm).

**R19 Which chips a saved card shows**
- Plan says: saved views carry "the same star-and-tag cues as the results page" (§3, §5); the results page shows the three highest-rated tags, ties in planning order, with ">>" for the rest (§2.1).
- Code does: saved chips first, then every other scored direction highest first, with no cap and no ">>"; ties are not resolved by planning order (`savedModel.js:45-49`; `SavedResultCard.jsx:31-44`).
- Why it matters: with up to 8 directions a card can grow many chips; the plan's "same cues" is ambiguous about this.
- Which side would change: the plan (say saved cards show all scored directions) or the code (cap at 3 and add ">>"). Decision for Telot: yes.

**R27 Task List: goal-linked saving**
- Plan says: Task List "Implement goal-linked saving so results file directly under the sub-goal through which they were found"; Fall goal 2 repeats "goal-linked saving".
- Code does: the searcher chooses the direction by clicking a tag (`DirectionChip.jsx:53-57`). The plan body (§3) says the same.
- Why it matters: the Task List describes an automatic filing mechanism that the design no longer has.
- Which side would change: the plan's Task List. Decision for Telot: no.

**R28 Task List: Suggested Next Step, Recap and Resume**
- Plan says: Task List "Suggested Next Step mechanism" and "Recap and Resume screens" (Phase 1 and Fall goal 2).
- Code does: neither exists; both are deferred (`docs/spec/deferred.md:8-10,20-25`), and the plan body (§Control) says the system does not choose the next step or write summaries. The Project Overview with Continue Last Activity takes their place.
- Why it matters: the Task List contradicts the plan's central claim about leaving the searcher in control.
- Which side would change: the plan's Task List. Decision for Telot: no.

**R29 Task List: embedding similarity and 1 to 5 stars**
- Plan says: Task List "embedding-based cosine similarity ... 1-5 star"; Phase 3 "Validate the similarity thresholds".
- Code does: whole-number 0 to 5 ratings from a generative model (`docs/spec/01-core.md:68`); the plan's §2.1 and Impl say the same and give reasons against embeddings.
- Why it matters: the stars on saved cards come from this.
- Which side would change: the plan's Task List. Decision for Telot: no.

**R30 Fig 5 Session 2**
- Plan says: Fig 5 shows Session 2 with "Community access +0" and "0 saved".
- Code does: mock Session 2 saves one result under Community access, so the all-sessions view has 3 groups and 9 results (`mocks/sessionsFixtures.js:128-129,155-160`).
- Why it matters: the plan's figures and the fixture no longer describe the same scenario.
- Which side would change: the fixture or the plan's Fig 5 (and the text "Session 3 ... Session 1" around it). Decision for Telot: yes.

### 5.2 Missing

**R26 No wiring**
- Plan says: a working MVP by Nov 5 with the saved views (TL; Fall goal 2).
- Code does: no production route, no saved endpoint, no code that reads or writes `savedresults` (section 3).
- Why it matters: until wired, participants only get Baseline's list.
- Which side would change: the code (build I6, after I2, I3, I5, I7); or the plan's date. Decision for Telot: no for the code; the date is question 5.

### 5.3 Partial and UI only

- **R3** (Partial): the SERP's Saved Results button opens the SERP-copy flat list, not the F6 view. Code would change (I7).
- **R16** (Partial): the "Description:" label in Figs 3 and 4 is not in the code. Code would change if Telot wants the label; or the figures. Decision for Telot: yes (minor).
- **R25** (Partial) and **R34** (Partial): depend on R26.
- **R2, R4, R5, R9, R20, R21, R22** (UI only): all run on fixtures under `/ui`. Code would change at I3 (save, `?` reason endpoint), I5 (sessions), I6 (data), I7 (navigation). No plan change is needed.

### 5.4 Extra (in code, not in plan)

E1 to E9 are listed in the matrix. For each: the plan is silent; the code follows F6 or a decision in DECISIONS.md. The plan side would change only if Telot wants these behaviours in the thesis text. The ones most worth a plan sentence are E5 (what opens Screens 3 and 4) and E2 and E3 (what a card does after an unsave and what a grey chip does). Decision for Telot: yes for E2 and E3, no for the rest.

## 6. Plan vs in-repo spec drift

| Point | Plan (v27) | Spec / code (minds-app) |
|---|---|---|
| Counts row | Two counts (Figs 3, 4) | Three counts incl. sessions (`F6-saved-views.md:36-42`) |
| Header and breadcrumb wording | "Projects", "sub-goal" in figures | "Workspaces", "search direction" (`F6-saved-views.md:31-33`) |
| Chips on saved cards | "same cues as the results page" | all scored directions, no `>>`, text "Saved" on saved chips (`F6-saved-views.md:47-50`) |
| Reason ("?") | The model returns a rating and a short reason in the same scoring call (Impl) | Reason may be null and fetched on demand by a separate endpoint; this is the one LLM call the saved view may make (`F6-saved-views.md:14-17`; `03-api.md:18`) |
| Session 2 saves | 0 (Fig 5) | 1 (fixture) |
| Unsave on saved view | Silent | Card stays, chip goes grey (`F6-saved-views.md:59-61`) |
| Entry points | Only the Saved Results button is said to open the view | circle, bar segment, session tile, button (`F6-saved-views.md:19-24`) |
| Mockup counts | Figs 3, 4: 3/1 and 6/3 | `docs/design/04` shows 8 and 3; F6 says those were wrong (`F6-saved-views.md:39-40`) |
| Spec says plan is "currently v27" | n/a | `docs/spec/00-index.md:57`; consistent with the file chosen |

Other documents: `Claude outputs/technical-specification.md` describes the older "Session History" and task-based design and says nothing about saved-results screens, so it is stale for this topic. The lowercase `claude output/` folder has no saved-results text. Neither was compared.

## 7. Terminology mapping used

| Plan | Code and spec |
|---|---|
| project, Project Overview | workspace, Your sessions ("Workspace Overview" title) |
| sub-goal | search direction (UI), `subGoal` (code, API) |
| Screen 3, Screen 4 | Saved results view (one view, two optional filters) |
| Screen 5, Project Overview | Your sessions |
| tag, rating, star | chip, score |
| possible new sub-goal ("New") | new direction, `emergingDirection` |
| Saved Results button | header toggle "Saved Results" / "Return to Search" |

## 8. Not checked, and confidence

- Nothing was run: no browser, no tests, no dev server, no backend. Test names were read; STATUS.md says U4 model and render tests pass ("reported, not re-run").
- Rendering: I read the JSX, not the screen. Visual points (spacing, "Journal article" vs "Article" label, grey chip tone) are taken from source and from the code's own mockups, not from a rendered page.
- Keyboard and screen-reader behaviour of the saved view was not checked (R33).
- I did not open Figs 1, 2.1, 2.3 or the SERP copy's rendering; Fig 2.3's "Saved Results" button is described from Fig 2.2 (image3).
- R31: two of the Session 1 chip scores were cut off when I printed the fixture lines, so I took them from `docs/design/05-saved-single-direction.png`.
- Confidence: high for sections 3 and R26 (route and endpoint lists read directly); medium for visual matches (R6 to R18); low for accessibility.
- Not read in full: `F2`, `F4`, `F5`, `F7` feature files, `SerpDevPage.jsx` beyond its header, `mockApi.js`, backend controllers other than by grep.

## 9. Open questions for Telot

1. Counts row: should the thesis figures show three counts (results, directions, sessions) as F6 says, or two as Figs 3 and 4 do?
2. Chips on saved cards: show every scored direction (F6) or the top three with ">>" like the results page (plan §2.1)?
3. Fig 5 / mock data: should Session 2 save one result (fixture) or none (plan)?
4. Should the card show the word "Description:" before the abstract, as the figures and mockups do?
5. Schedule: Fall goal 2 says the MVP is complete by Nov 5, and today is Oct 20 with U2 restarted and I2 to I8 not started. Should the date or the scope in the plan change? If I6 and I7 slip, R26 becomes a blocker for the study.
6. Task List cleanup: may I take it that "goal-linked saving", "Suggested Next Step", "Recap and Resume" and "embedding-based 1 to 5 stars" are all stale and should be replaced by the §3, §5 and Impl descriptions?
7. Should the plan say what opens Screens 3 and 4 (circle, bar segment, tile, button), that a card stays after an unsave, and that a grey chip saves under another direction (E2, E3, E5)?
8. Should the on-demand "why" call (F6) be added to the plan's list of AI components in the Implementation Note?

## Appendix: files read

Plan (minds-doc @ fc321d4): `Claude outputs/Telot Thesis Planning Documents v27.docx` (extracted with `agents/save-diff/extract_plan.sh` to scratch; read whole text; opened figures image3, image5, image6, image7); `agents/save-diff/AGENT.md`, `agents/save-diff/extract_plan.sh`, `agents/plan-diff/find_latest_plan_doc.py` (output only); `Claude outputs/technical-specification.md` (grep only); `claude output/` (grep only).

Code (minds-app @ ba707ba48c21, all under `/home/claude/akane-asahi/minds-app/`):
- Docs: `STATUS.md`, `CLAUDE.md`, `DECISIONS.md` (saved and U4 entries), `docs/spec/00-index.md`, `01-core.md`, `02-data-model.md`, `03-api.md`, `F6-saved-views.md`, `build-plan.md`, `deferred.md` (lines 8-25), `open-questions.md` (grep), `accessibility.md` (lines 60-74), `F3-serp-cards-chips.md` (grep and lines 100-112), `F5-your-sessions.md` (grep), `docs/design/04, 05, 06 .png`, `docs/design/README.md`.
- Saved view: `frontend/src/features/savedResults/{SavedResultsScreen.jsx, SavedResultCard.jsx, savedModel.js, SavedResultsScreen.test.jsx (test names and lines 20-60), savedModel.test.js (test names)}`.
- Wiring and entry points: `frontend/src/app/router/index.js`, `ui-dev/UIDevRoutes.jsx`, `ui-dev/SerpDevPage.jsx` (first 60 lines), `features/serp/layout/{MainHeader.jsx, Layout.jsx}`, `features/serp/minds/{DirectionChip.jsx, SavedChips.jsx, DirectionsPanel.jsx, MindsSerpContext.jsx (partial)}`, `features/serp/components/{SavedDocumentCard.jsx, SavedSearchResults.jsx, ResultCardShell.jsx (head)}`, `features/serp/pages/WorkspaceView.jsx`, `features/search/{pages/SavedSearchResultsView.jsx, components/SavedSearchResults.jsx}` (diff only), `features/workspace/pages/WorkspaceView.jsx`, `features/workspace/api/savedDocsQueryService.js` (grep), `features/yourSessions/{YourSessionsScreen.jsx, DirectionCard.jsx, SessionTile.jsx, sessionsModel.js}`, `shared/components/{SavedDocumentCard.jsx, DocumentAbstract.jsx}` (grep/head), `mocks/sessionsFixtures.js`.
- Backend: `backend/routes/saveddocsRoutes.js`, `backend/models/savedResultModel.js`, `backend/server.js` (grep), grep across `backend/` for `savedresults`/`SavedResult`.
