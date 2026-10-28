# Saved results diff: code vs plan

Generated: 2026-10-28 09:20 (Regina time) by save-diff
Plan document used: `Claude outputs/Telot Thesis Planning Documents v30.docx` (version v30, internal date "Project Revised: (Oct 25, 2026)", last commit 4fa3494 2026-10-26)
Code checked: Akane-Asahi/minds-app @ 533d618c36be06d240a2640842179a4f2ad22676 (2026-10-27 15:31 -0600), branch main (reused the existing clone; nothing fetched or pulled, as the caller instructed)
Scope: all Saved results screens (all saved results, one direction, one session, one direction in one session, and the buttons that lead there)

> Warnings:
> 1. **The plan is older than the code.** v30 was written to match minds-app `2f08f2c` / `209f0cd` (2026-10-25), per `Claude outputs/v30-changes-summary.md`. The code I read is at `533d618` (2026-10-27) and includes changes made after that, with dates in code comments: per-sub-goal colours on Saved results (2026-10-26), "Saved Results for Session N" (2026-10-26), "Continue searching" on a session's saved results, and "Continue Last Activity" removed from the Overview (2026-10-27). Several differences below come from that gap alone. The `change-ledger.md` has no entry after 2026-10-25.
> 2. **The in-repo spec files are not in the minds-app checkout.** There is no `STATUS.md`, `DECISIONS.md`, `CLAUDE.md`, `docs/spec/` or `docs/design/` in minds-app at this SHA (the repo has only `docs/commands.md`, `docs/font-size-change.md`, `docs/font-weight-change.md`). A copy of them lives in minds-doc under `minds-app-claude-files/` (last commit 4fa3494, 2026-10-26; its `DECISIONS.md` ends at 2026-10-25 and `STATUS.md` says "Last updated: 2026-10-25"). I used that copy for section 6 only. It is older than the code, so it cannot confirm any 2026-10-26/27 decision.
> 3. **The figures in v30 are known to be out of date.** `v30-changes-summary.md` says so for Figs 3, 4 and 5 ("Only text changed: no figure ... was touched"). Rows for the figures are listed separately so they do not hide the text-versus-code result.
> 4. Static reading only. Nothing was run in a browser, with a keyboard or with a screen reader, and no tests were re-run.

## 1. Summary

- The Saved results view is **live on real data**: one route (`/workspace/:id/saved?direction=&session=`), one real endpoint (`GET /api/workspaces/:id/saved`) reading stored rows only, no Primo call and no model call except the on-demand "?" sentence. The v30 **text** of section 3 and section 5 matches the code on almost every behaviour (scopes, grouping, counts, right panel, undo, "?" sentence, entry points).
- **Most important difference (Important, Decision for Telot):** a session's saved results opened from the Overview show a button "Continue searching" that jumps to the results page restoring that session's last state. The plan says the one button is "Return to Workspace" and goes back to the Overview (R15).
- **Second:** the tag and panel colours. The plan says saved tags and selected panel names are solid blue. The code gives every sub-goal its own pastel colour with dark text (Telot, 2026-10-26, per code comment), and the "grey" unsaved tag is white with a grey outline (R23, R25, R30). All Minor.
- **Third:** Figs 3, 4 and 5 still show the 2026-10-20 design (rating stars on tags, two counts, no right panel, no title card, "Projects" breadcrumb). The v30 text says the opposite on each of these points (R36 to R38).
- No requirement is Missing. Open risk needing a browser: whether "Return to Workspace" survives after the participant uses the right panel (R16).
Counts: Matches 26 · UI only 0 · Partial 1 · Differs 8 · Missing 0 · Plan defers 0 · Unverified 3 · Extra 12

## 2. Which plan document was used

Helper: `agents/plan-diff/find_latest_plan_doc.py` on `Claude outputs/`. Reason printed: "highest version number v30". No warnings, no tie.

| Candidate | Version | Used? |
|---|---|---|
| Telot Thesis Planning Documents v30.docx | 30 | **yes** |
| Telot Thesis Planning Documents v29.docx | 29 | no |
| Telot Thesis Planning Documents v27.docx | 27 | no |
| Telot Thesis Planning Documents v7 - SRL Stripped-3 / -2 / -1 / Restructured / SRL Stripped (five files) | 7 | no |

Checks made on v30: it discusses saved results (section 3 "Organization: Saving into Sub-Goals", sections 4 and 5, Figs 3 to 5, Task List, Fall 2026 Goals). Internal date "Oct 25, 2026" is the newest; no older-numbered candidate has a newer internal date. The extract step reports 0 insertions, 0 deletions and 0 comments, so there are no Word review comments to list ("plan comment, not yet reflected": none). Figure-to-caption mapping is by order (the extract script's rule): image5 = Fig 3, image6 = Fig 4, image7 = Fig 5; I opened all three and the images match their captions. `technical-specification.md` and the lowercase `claude output/` folder say nothing about saved results, so there is no stale context from them.

## 3. Which code is the live Saved results view

| Piece | State | Evidence |
|---|---|---|
| `frontend/src/features/savedResults/SavedResultsPage.jsx` + `SavedResultsScreen.jsx` + `SavedResultCard.jsx` + `savedModel.js` + `savedApi.js` | **Live MINDS view**, real data | route `app/router/index.js:102` (`/workspace/:workspaceId/:view` -> `MindsSerpPage`); `MindsSerpPage.jsx:79` renders `SavedResultsPage` when `view === "saved"`; data from `savedApi.js:9-14` |
| `frontend/src/features/mindsSerp/MindsSerpPage.jsx` | Hosts the view. `serp` and `saved` are one route, so the SERP stays mounted (hidden) under the saved view and Return does not search again | `MindsSerpPage.jsx:30-34, 79-80, 114, 120` |
| `backend/controllers/savedViewController.js` (`getSaved`), route `backend/routes/workspaceRoutes.js:72` | Live data path: stored rows only (`savedresults`, `resultscache`, `resultscores`, sessions, sub-goals) | `savedViewController.js:15-17, 36-40, 62-69`; test `backend/__tests__/savedView.test.js:134` ("makes no Primo call and no LLM call") |
| `backend/controllers/resultsController.js` (`saveResult`, `unsaveResult`, `getReasoning`) | Live: chip save, removal, and the on-demand "?" sentence | `resultsController.js:36-65, 144-172` |
| `frontend/src/ui-dev/UIDevRoutes.jsx` route `/ui/saved-results` | **Dev only**, mock fixtures (`frontend/src/mocks/sessionsFixtures.js`); not in a production build | `router/index.js:26-29, 72-81` (route only when `NODE_ENV === "development"`); `UIDevRoutes.jsx:15, 118-145` |
| `features/search/pages/SavedSearchResultsView.jsx` (+ `features/search/components/SavedSearchResults.jsx`, `shared/components/SavedDocumentCard.jsx`, `workspace/context/SavedBookmarksContext.jsx`) | **Baseline legacy**, still routed at `/workspace` as the control condition; not the MINDS view | `router/index.js:19, 40, 93-97`; `features/workspace/pages/WorkspaceView.jsx:4-5` |
| `features/serp/pages/SavedSearchResultsView.jsx`, `features/serp/components/SavedSearchResults.jsx`, `features/serp/components/SavedDocumentCard.jsx`, `features/serp/minds/SavedChips.jsx` | **Duplicate / dev only**: reached only from `ui-dev/SerpDevPage.jsx` (imports `serp/pages/WorkspaceView`); not routed in the app | `grep` of imports: only `ui-dev/SerpDevPage.jsx:4` imports `serp/pages/WorkspaceView` |
| `backend/routes/saveddocsRoutes.js`, `controllers/saveddocsController.js`, `models/savedDocModel.js` | Baseline saved-documents API; MINDS chips write `savedresults` only | `backend/services/savedService.js:1-5` |

Entry points and how they reach the view (all real navigation, no mock):
- **Overview header "Saved Results" button** -> `YourSessionsScreen.jsx:240` -> `YourSessionsPage.jsx:162-167` -> `/workspace/:id/saved` with router state `{ from: "overview" }`.
- **Overview sub-goal name or bar** -> `DirectionCard.jsx:92, 129-132, 146` (`?direction=`).
- **Overview session tile** -> `SessionTile.jsx:68-76` (`?session=`).
- **Results-page right panel, sub-goal name or bar** -> `DirectionsPanel.jsx:147, 162-172, 186` (`?direction=`).
- **Results-page header "Saved Results" button**: built but hidden (`MindsSerpLayout.jsx:27`, `hideSavedButton`).
- **Count circle and per-session bar segments** (Overview and results page): built but switched off (`DirectionsPanel.jsx:19-20`, `DirectionCard.jsx:18, 145`); the total bar replaces them.
- Route order: `/workspace/:id/overview` is a static segment, so it wins over `/:view` (`router/index.js:102-104`; React Router v6 ranking, not run).

Mock versus real: everything the participant reaches in the app runs on real data. Only `/ui/saved-results` runs on fixtures.

## 4. Requirement matrix

Plan citations are to v30 section names: "§2.1" = Evaluation: Relevance and Usefulness of Results; "§3" = Organization: Saving into Sub-Goals; "§4" = Monitoring; "§5" = Cross-Session Support; "KSC" = Keeping the Searcher in Control; "TL" = Task List; "FG" = Fall 2026 Goals.

| ID | Plan says (section/fig) | Code does (path:line) | Status | Severity | Notes |
|---|---|---|---|---|---|
| R1 | Saved results is one view with two filters (a sub-goal and a session); Figs 3 and 4 show two of its states (§3) | One component, two optional filters: `SavedResultsPage.jsx:26-28`, `savedModel.js:31-33` | Matches | Minor | Whole-workspace state has no figure. "Screen 3 / Screen 4" numbering exists only in the figure captions; code has no screen numbers. |
| R2 | The Saved Results button in the Overview header card opens the saved results of the whole workspace (§5) | `YourSessionsScreen.jsx:240`; `YourSessionsPage.jsx:162-167`; `router/index.js:102` | Matches | | |
| R3 | The name of a sub-goal, or its bar, opens the saved results for that sub-goal (Overview) (§4, §5) | `DirectionCard.jsx:92, 129-132, 146` | Matches | | |
| R4 | On the results page, selecting the name or the bar opens the results saved under that sub-goal (§4) | `DirectionsPanel.jsx:147, 162-172, 186` | Matches | | |
| R5 | A session tile on the Overview opens that session's results (§5) | `SessionTile.jsx:68-76` | Matches | | |
| R6 | Whole-workspace view is grouped by session, newest session first (§5) | `savedModel.js:35-41, 51-54` (sorted by session number descending, line 53) | Matches | | |
| R7 | The view for one sub-goal groups its results by session (§5, Fig 3) | `savedModel.js:31-33, 51-54` (heading present unless a session is set) | Matches | | |
| R8 | The view for one session shows everything saved in that session across sub-goals (§5, Fig 4) | `savedModel.js:31-33, 54` (`heading: null` with a session filter) | Matches | | |
| R9 | The same view can be limited to one session on top of a sub-goal (§3, "two filters") | `savedModel.js:31-33`; reachable via the right panel inside a session view (`SavedResultsPage.jsx:95`) | Matches | | The per-segment entry point is switched off (E2). |
| R10 | Group heading per session, e.g. "SESSION 3 · SEP 23" (Figs 3, 4) | `savedModel.js:54`; `SavedResultsScreen.jsx:190-194` | Matches | | Plan text does not describe headings; figure does. |
| R11 | Each saved card shows a tag for each sub-goal the result is saved under, in the order set in planning, not in order of fit (§3) | `savedModel.js:43-49` (sorted by `orderIndex`, line 47); `SavedResultCard.jsx:63-77` | Matches | Minor | Chips are limited to saves made in that same session (`savedViewController.js:47-49`, `savedModel.js:44`), so a result saved under A in Session 1 and under B in Session 3 appears as two cards, one tag each. `orderIndex` can also change when the sub-goals are re-ordered on the Overview, so "order set in planning" is not strictly true (v30-changes-summary.md notes this). |
| R12 | Title card like the Workspace Overview, with the path Workspaces > workspace name > Saved Results (§3) | `SavedResultsScreen.jsx:145-157`; `WorkspaceTitleCard.jsx:21-35` | Matches | | |
| R13 | Last path segment is "Saved Results" (§3) | `savedModel.js:70, 72`: for a session scope it is "Saved Results for Session N" (breadcrumb and h1) | Differs | Minor | Code comment cites Telot 2026-10-26. Fig 4 shows "Session 3". Plan side would change. |
| R14 | One button: "Return to Workspace" when opened from the Overview, "Return to Search" otherwise (§3) | `SavedResultsPage.jsx:24, 88`; `WorkspaceTitleCard.jsx:71` | Matches | | For views with no session filter. See R15 for the session view. |
| R15 | Return takes Jamie back to where the view was opened from: the Overview when opened from there; the results page otherwise (§3) | With a session filter the button is "Continue searching" (`SavedResultsScreen.jsx:147`) and, from the Overview, goes to the results page with `?restore=<session>` (`SavedResultsPage.jsx:79`), not to the Overview. Other cases follow the plan (`SavedResultsPage.jsx:80-81`) | Differs | Important | Session tile -> session's saved results -> button: plan says back to the Overview with no search box; code opens the SERP restored to that session's last state. Test `SavedResultsPage.test.jsx:220-225` protects the code behaviour. Decision for Telot. |
| R16 | Same "Return to Workspace" behaviour holds while Jamie uses the saved view (§3, "Return takes Jamie back to where the view was opened from") | Choosing a name in the right panel calls `setSearchParams(..., { replace: true })` with no `state` (`SavedResultsPage.jsx:95`), while the all-saved path passes `state: location.state` explicitly (`SavedResultsPage.jsx:73`). Router state `from: "overview"` is read at `SavedResultsPage.jsx:24` | Unverified | Important if confirmed | Probably the state is dropped after the first panel click, so the search box returns and the button reads "Return to Search". Not run; no test covers it (`SavedResultsPage.test.jsx:176-199` clicks the panel but never checks the button). `v30-changes-summary.md:74, 110` suspects the same thing. Needs a browser click-through. |
| R17 | No search box when opened from the Overview; from the results page the header keeps a (disabled) search box with the last query (§3; Figs 3, 4) | `SavedResultsPage.jsx:88-92` (`showSearch={!cameFromOverview}`, `lastQuery`); `MainHeader.jsx:38-45`; `SavedResultsScreen.jsx:140` | Matches | | |
| R18 | A row of three counts at the top: saved results, sub-goals and sessions in the view (§3) | `SavedResultsScreen.jsx:168-172` | Matches | | |
| R19 | Counts are plain counts, never percentages (§4) | `savedModel.js:56-61` counts distinct results, sub-goals, sessions | Matches | | |
| R20 | The counts are of what is "in the view" (§3) | `savedModel.js:56-61` counts every saved chip on the shown cards, including other sub-goals saved on the same card (`savedViewController.js:47-49` sends them) | Partial | Minor | With a direction filter the sub-goals count can be above 1 when a card is also saved under another sub-goal. Fig 3 shows "1". Plan wording is ambiguous. The unit tests use fixtures where each card has one saved chip (`savedModel.test.js:34-39`). Decision for Telot. |
| R21 | A card shows title, year and authors, description and tags (Figs 3, 4; §3) | `SavedResultCard.jsx:25-28, 92`; card chrome `features/serp/components/ResultCardShell.jsx` (type icon and label at 30-54, 76; abstract at 267-272) | Matches | | Fig label differences are in R36 and R37. |
| R22 | The searcher never sees the 0 to 5 ratings; they only order things (§2.1) | `SavedResultCard.jsx:71` (`showScore={false}`); `DirectionChip.jsx:77` | Matches | | Text matches code; Figs 3 and 4 still show "4★" (R36, R37). |
| R23 | A solid blue tag means saved; "fills the tag solid blue" (§2.1, §3) | Saved chip is filled with the sub-goal's own pastel colour and dark text (`DirectionChip.jsx:67`; palette `theme/directionColors.js:9-19`; passed in at `SavedResultCard.jsx:73`) | Differs | Minor | Code comment: "One colour per search direction on Saved results (Telot, 2026-10-26)". On the results page saved chips are still blue. Plan side would change. |
| R24 | Selecting a saved tag removes the result from that sub-goal, but the card stays with a grey tag until Jamie leaves the view; selecting the grey tag again undoes it (§3) | `SavedResultsScreen.jsx:123-136` (overrides keep the card and flip the chip); `SavedResultsPage.jsx:41-50`; `savedModel.js:43-49`; test `SavedResultsScreen.test.jsx:51-60`, `SavedResultsPage.test.jsx:120-133` | Matches | | The removal is saved at once on the server, and undo saves back into the original session (`resultsController.js:52-61`). |
| R25 | The removed tag looks grey (§3, Fig 3) | Unsaved chip is white with a grey outline (`DirectionChip.jsx:12-13, 65`) | Differs | Minor | |
| R26 | Jamie decides where a result goes; selecting a tag files or removes it (§3) | `SavedResultsPage.jsx:41-43` -> `saveResult` / `unsaveResult` (`mindsSerpApi.js:68-77`) -> `resultsController.js:36-65` | Matches | | Edge cases in E9. |
| R27 | "?" on a saved tag shows the stored sentence and writes it on first selection if none is stored; selecting again hides it (§3, §2.1) | `SavedResultCard.jsx:30-58` (`loadReason`, `toggleReason`, `reasonText`); `SavedResultsPage.jsx:51`; `resultsController.js:144-172` (returns stored reasoning first) | Matches | | Error text: "The reason is not available right now. Tap ? to try again." (`SavedResultCard.jsx:10`). |
| R28 | Right panel "Directions with saved results" lists each sub-goal that has saved results, with its mark and the number saved (§3) | `SavedResultsScreen.jsx:62-90, 104-116` (mark via `LabelWithMark`, line 40) | Matches | Minor | Panel title in code is "Sub-goals with saved results" (line 70); see section 7. |
| R29 | Selecting a name shows only that sub-goal's results, without a new search; several names can be chosen; selecting again, or Reset, shows everything (§3) | `SavedResultsScreen.jsx:62-79`; `SavedResultsPage.jsx:29-37, 95`; test `SavedResultsPage.test.jsx:176-199` ("no new request") | Matches | | |
| R30 | Selected names in the panel are solid blue (§3) | Panel buttons are filled with the sub-goal's colour; a selected one gets a dark inset ring (`SavedResultsScreen.jsx:38`) | Differs | Minor | Same decision as R23. |
| R31 | No Primo call; the only model call is the sentence written on first "?" (§3, KSC) | `savedViewController.js:15-17`; test `savedView.test.js:134-139`; `SavedResultsPage.jsx:14-16` | Matches | | Re-saving from the view can start new-direction detection (E10). |
| R32 | The system does not read results for Jamie, write summaries or choose the next step (KSC) | No such code in `features/savedResults/` or `savedViewController.js` | Matches | | |
| R33 | Saved results screens built and integrated, viewable by sub-goal and by session (TL "Implement goal-linked saving ... viewed by sub-goal and by session"; FG 2; abstract) | Live route, real endpoint (section 3) | Matches | | |
| R34 | MVP "confirmed through informal use" by Nov 5 (TL, FG 2) | Not visible in code. The mirrored `STATUS.md` says "not yet checked in a browser, by keyboard or with a screen reader" (as of 2026-10-25) | Unverified | Minor | Reported, not re-run. |
| R35 | Progress cues "use little text" (abstract) and the interface is meant to be usable with low working memory (abstract, Related Work) | Plain counts, one-line reasons, aria roles and a live region exist (`SavedResultsScreen.jsx:143, 168-172`; `DirectionChip.jsx:58-63, 71-74`); no keyboard or screen-reader check possible here | Unverified | Minor | The plan has no accessibility rule specific to this screen. |
| R36 | Fig 3 (single sub-goal) | Figure shows: breadcrumb "Projects > How green spaces affect wellbeing > Physical health benefits", two counts only, "4★"/"2★" scores on tags, "Description:" and "Journal article" labels, empty right side, no title card, "Return to Search" in the header. Code: "Workspaces" breadcrumb ending in "Saved Results", three counts, no scores, no "Description:" prefix (none in `frontend/src`), right panel, title card (`SavedResultsScreen.jsx:145-157, 165-208`) | Differs | Minor | Figure is out of date; v30 text is right on each point. Plan figure would change. |
| R37 | Fig 4 (single session) | Same as R36, plus breadcrumb "Session 3" and a different "Return to Search" place; code ends the path in "Saved Results for Session 3" and uses "Continue searching" | Differs | Minor | Figure is out of date. |
| R38 | Fig 5 (Overview) as the entry point: "Saved Results" in the top bar, title "Project Overview", "Continue Last Activity", session pills with "S1" badges, count circles and segments | Header card titled "Workspace" holding the Saved Results button (`YourSessionsScreen.jsx:235-241`); no Continue Last Activity; total bars, no circles or segments (`DirectionCard.jsx:145-146`) | Differs | Minor | Only the saved-results entry points matter here; the rest is for sessions-diff. |

## 5. Differences in detail

### 5.1 Differs

**R15 Return button on a session's saved results (Important, Decision for Telot: yes)**
- Plan says: one button, "Return to Workspace" when opened from the Overview, and Return goes to the Overview with no search box (§3).
- Code does: for any session-filtered view the button reads "Continue searching" (`SavedResultsScreen.jsx:147`); from the Overview it opens the results page with `?restore=<sessionId>`, which loads that session's last direction, query and results from stored rows (`SavedResultsPage.jsx:79`; `useLiveSerp.js:248-285`). Test `SavedResultsPage.test.jsx:220-225`.
- Why it matters: a participant who taps a session tile to remind themselves what was saved is sent into a search instead of back to the Overview. That is arguably a different cross-session path than the plan describes ("Jamie chooses where to resume", §5). It does not stop the study, but the plan and the interface describe two different flows.
- Which side would change: plan (if the new flow is wanted) or code (if "Return to Workspace" is wanted).

**R13 Last path segment for a session (Minor, Decision: no)**
- Plan says "Saved Results" (§3). Code: "Saved Results for Session N" (`savedModel.js:70, 72`), a dated Telot decision in a code comment. Plan side would change (one phrase).

**R23, R25, R30 Colours (Minor, Decision: yes)**
- Plan says saved tags and selected panel names are solid blue, the unsaved tag is grey, and "solid blue means saved" (§2.1, §3).
- Code does: per-sub-goal pastel fills for saved tags and panel buttons (`directionColors.js:9-19`), white-with-grey-outline for an unsaved tag (`DirectionChip.jsx:12-13, 65`). Colour is never the only cue (names are written out; `aria-pressed` is set).
- Why it matters: §2.1 uses "solid blue" as a rule ("Every other tag is plain"). On the results page that rule still holds; on Saved results it does not. A participant sees two colour systems for "saved".
- Which side would change: plan text (and the figures), since the code comment records a Telot decision dated after the v30 baseline. Telot should confirm that the results page is meant to stay blue.

**R36, R37, R38 Figures (Minor, Decision: no)**
- Plan figures 3, 4 and 5 predate the v30 text. Differences are listed in the matrix rows. `v30-changes-summary.md:85-92, 119` already lists them as needing new screenshots. The plan side would change (new screenshots).

### 5.2 Missing
None. Every behaviour the v30 text describes for Saved results has a trace in code.

### 5.3 Partial and UI only

**R20 "Sub-goals" count with a direction filter (Partial, Minor, Decision: yes)**
- Plan says the row of counts gives the number of saved results, sub-goals and sessions "in the view" (§3); Fig 3 shows "1" sub-goal for a one-sub-goal view.
- Code does: counts the saved chips on the shown cards, and a card carries all the sub-goals saved on that result in that session (`savedViewController.js:47-49`; `savedModel.js:43-49, 56-61`). A result saved under both A and B, viewed with the filter on A, counts two sub-goals.
- Why it matters: the number can disagree with the one sub-goal the participant chose. Real data with two-sub-goal saves is common; the unit tests do not cover it.
- Which side would change: either (plan clarified to "sub-goals shown on the cards", or code counts only the filtered sub-goal).

**UI only:** none. The dev route `/ui/saved-results` is a mock-data copy of the same components, not a separate requirement.

### 5.4 Extra (in code, not in plan)

Each item: Plan says nothing / Code does / Why it matters / which side / Decision.

- **E1 Header "Saved Results" button on the results page.** Built and hidden (`MindsSerpLayout.jsx:27`; `MainHeader.jsx:235-245`). The plan names only the Overview button. The mirrored `F6-saved-views.md:21` still lists the SERP toggle as an entry point. Either remove the dead code or restore it. Decision: yes.
- **E2 Count circle and per-session bar segments** are switched off (`DirectionsPanel.jsx:19-20`; `DirectionCard.jsx:18, 145`). The plan already says there is no circle or segment. The "one direction in one session" scope (a bar segment) is only reachable through a session tile plus the panel. Decision: no.
- **E3 Panel lists the session's other sub-goals greyed with a 0** when a session is open (`SavedResultsScreen.jsx:50-60, 113-115`; test `SavedResultsPage.test.jsx:203-211`). Plan says the panel lists sub-goals "that has saved results". Plan side would change. Decision: no.
- **E4 Empty, loading, error and not-found states**: "Nothing saved here now" (`SavedResultsScreen.jsx:183-185`), skeleton cards (181), "Saved results could not be loaded." with Retry (159-163), "Saved results not found" page for an unknown sub-goal, session or workspace (`SavedResultsPage.jsx:59-68`). The plan does not describe them. Decision: no.
- **E5 A failed save or removal** puts the chip back and shows a visible message (`SavedResultsScreen.jsx:130-135, 175-179`). Not in plan. Decision: no.
- **E6 The results page stays mounted under the view**, so returning does not search again, and a change made in the view updates the results page (`MindsSerpPage.jsx:30-34, 79`). Not in plan. Decision: no.
- **E7 Workspace-name link in the path goes to the Overview** (`SavedResultsScreen.jsx:154`); on the Overview the plan says the name links to the plan (§4). Plan silent for this screen. Decision: yes (consistency).
- **E8 Saved results cannot be opened when the workspace has no selected sub-goals.** `MindsSerpPage.jsx:139-141` shows "No search sub-goals yet" before the saved view is rendered, and the Overview lets a participant untick sub-goals. §5 says the button opens the saved results with no condition. Edge case. Which side: code. Decision: yes.
- **E9 Undo for a sub-goal that was unticked afterwards is refused.** `ownedDirection` accepts only selected sub-goals (`resultsController.js:27`), so clicking the grey tag shows the failure message and the tag stays grey (`SavedResultsScreen.jsx:130-135`). Edge case, also noted in the mirrored `F6-saved-views.md:96`. Decision: yes.
- **E10 Re-saving from the view starts new-direction detection** in the background (`resultsController.js:64`). §2.2 says detection follows a save, so this is consistent, but the view's "no model call" statement (R31) is true only for the view's own data request. Decision: no.
- **E11 Baseline's saved view is still routed at `/workspace`** (control condition) and several duplicate files exist (section 3). Not in plan. Decision: no.
- **E12 Dev-only `/ui/saved-results`** on mock fixtures (`UIDevRoutes.jsx:15, 118-145`). Not in plan. Decision: no.

## 6. Plan vs in-repo spec drift

Source: `minds-doc/minds-app-claude-files/docs/spec/F6-saved-views.md` and `DECISIONS.md` (copy, not the minds-app checkout; see warning 2). It describes the state of 2026-10-22 to 2026-10-25.

| Topic | In-repo spec copy (F6) | Plan v30 | Code at 533d618 |
|---|---|---|---|
| SERP header Saved Results toggle as an entry point | Yes (`F6:21, 92`) | Not mentioned | Built, hidden (E1) |
| Count circle and bar segment entry points | Yes (`F6:22-23, 92`) | Name or bar only (§4, §5) | Switched off (E2) |
| Right panel | "All directions" row first (`F6:43-47`) | No "All directions" row; Reset; several names (§3) | Reset, several names; matches plan |
| Saved chip | Solid blue, score and a check icon (`F6:56-57`) | Solid blue, no check mark, no score (§2.1) | Pastel per sub-goal, no score, no check icon (R22, R23) |
| Breadcrumb last segment | "All Saved Results", direction label, "Session {n}" (`F6:31-33`) | "Saved Results" | "Saved Results" or "Saved Results for Session N" |
| h1 | Visually hidden (`F6:34-35`) | Not described | Visible title in the title card (`SavedResultsScreen.jsx:145-157`) |
| Title card, Return button | Header button "Return to Search"; no title card (`F6:28-30`) | Title card with one button, Return to Workspace / Search (§3) | Title card; "Continue searching" for a session (R15) |
| Return from the Overview | `DECISIONS.md:482` (2026-10-23): "Return to Search" goes back to the Overview, search box hidden | Return to Workspace | Matches the plan except the session case |
| Counts | Three counts (`F6:36-42`) | Three counts | Three counts; Figs 3, 4 show two |

The plan v30 is closer to the code than the spec copy is. The spec copy is stale on the 2026-10-25 and later changes. In both, the spec says a card shows only directions saved in that session (`F6:57`), which matches the code. Technical-specification.md and the lowercase `claude output/` folder have nothing on saved results.

## 7. Terminology mapping used

- Plan "sub-goal" = code `subGoal` / API `subGoalId` = UI "sub-goal" or "search sub-goal" (the UI now uses "sub-goal" on these screens, for example "Sub-goals with saved results", "Sub-goals for this session", "Last Sub-goal"). Plan v30 headings still say "Directions" in places ("Directions with saved results", "Directions for this session", "Selected Directions", "Directions you have explored" in Fig 5). Wording only; not counted as differences.
- Plan "workspace" = code "workspace"; Figs 3, 4, 5 still say "Projects" / "Project Overview".
- Plan "saved results" / "Saved Results" = route `/saved`; "New direction" = `emergingDirection`.
- "Return to Workspace" in plan = button reading `Return to ${returnTo}` with `returnTo = "Workspace"` (`SavedResultsPage.jsx:88`; `WorkspaceTitleCard.jsx:71`).

## 8. Not checked, and confidence

- Not run in a browser, with a keyboard or with a screen reader: whether the router state survives the right-panel click (R16), real contrast of the pastel colours (a unit test exists, `directionColors.test.js`, not run), focus order, and whether the "Description:" prefix or any type label differ visually in a real card (I only confirmed there is no "Description:" string in `frontend/src` and that the card shows a type icon and label from `ResultCardShell.jsx:30-54`).
- Real backend and database not exercised. The backend test `savedView.test.js` mocks the models; I read the test names only and quote nothing about pass or fail ("reported, not re-run").
- React Router ranking of `/overview` over `/:view` is from my knowledge of v6 (package.json pins `^6.3.0`; installed version not checked).
- The git history is shallow (one commit), so I could not see what changed between `2f08f2c` (the v30 baseline) and `533d618`. Differences caused only by the later commits are inferred from dated code comments.
- Confidence: high on routes, entry points, counts, grouping, filters, the "?" path and the backend; medium on R16 and R20 (reasoned from code, not run); low on any claim about visual styling.

## 9. Open questions for Telot

1. A session's saved results opened from the Overview: should the button be "Return to Workspace" (back to the Overview, as the plan says) or "Continue searching" (restore that session's results page, as the code does)? (R15)
2. Are the per-sub-goal pastel colours on Saved results final, and should saved tags on the results page stay blue? If yes, the plan's "solid blue" wording changes. (R23, R25, R30)
3. In a one-sub-goal view, should the sub-goals count show only the chosen sub-goal, or every sub-goal on the shown cards? (R20)
4. Should a participant who unticked every sub-goal still be able to open Saved results from the Overview? (E8)
5. Should the hidden header "Saved Results" button and the hidden count circle and session segments stay as dead code, or be removed? (E1, E2)

## Appendix: files read

Plan (minds-doc @ 4fa3494, 2026-10-26): `Claude outputs/Telot Thesis Planning Documents v30.docx` (extracted to a scratch folder outside both repos; images image5.png, image6.png, image7.png opened); `Claude outputs/v30-changes-summary.md`; `Claude outputs/change-ledger.md`; `Claude outputs/technical-specification.md` (searched only); `agents/save-diff/AGENT.md`, `agents/save-diff/extract_plan.sh`, `agents/plan-diff/find_latest_plan_doc.py` (run).

Spec copy (minds-doc @ 4fa3494): `minds-app-claude-files/docs/spec/F6-saved-views.md`, `build-plan.md`, `minds-app-claude-files/STATUS.md`, `minds-app-claude-files/DECISIONS.md` (saved-related entries only). Design mockups `docs/design/04-06*.png` were not opened.

Code (minds-app @ 533d618c36be06d240a2640842179a4f2ad22676, 2026-10-27):
- `frontend/src/features/savedResults/`: `SavedResultsPage.jsx`, `SavedResultsScreen.jsx`, `SavedResultCard.jsx`, `savedModel.js`, `savedApi.js`, test names in `SavedResultsPage.test.jsx`, `SavedResultsScreen.test.jsx`, `savedModel.test.js`; `savedModel.test.js` read in part.
- `frontend/src/features/mindsSerp/`: `MindsSerpPage.jsx`, `MindsSerpLayout.jsx`, `mindsSerpApi.js` (lines 60-115), `useLiveSerp.js` (lines 245-285), `MindsSerpSavedSwitch.test.jsx` (names).
- `frontend/src/features/serp/`: `layout/MainHeader.jsx`, `minds/DirectionChip.jsx`, `minds/DirectionsPanel.jsx`, `components/ResultCardShell.jsx` (parts), `shared/components/WorkspaceTitleCard.jsx`, `shared/components/DocumentAbstract.jsx`.
- `frontend/src/features/yourSessions/`: `YourSessionsPage.jsx`, `YourSessionsScreen.jsx`, `DirectionCard.jsx`, `SessionTile.jsx`.
- `frontend/src/app/router/index.js`, `frontend/src/theme/directionColors.js`, `frontend/src/ui-dev/UIDevRoutes.jsx`, `mockApi.js` (searched), `frontend/src/features/workspace/pages/WorkspaceView.jsx` (head), import search for the legacy and duplicate saved views.
- `backend/controllers/savedViewController.js`, `resultsController.js` (lines 18-70, 144-172), `backend/services/savedService.js`, `backend/models/savedResultModel.js`, `backend/routes/workspaceRoutes.js`, `backend/routes/resultsRoutes.js`, `backend/schemas/results.js` (saved query schema), `backend/__tests__/savedView.test.js` (test names and lines 134-139).
