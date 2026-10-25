# DECISIONS.md

Dated log of decisions. Newest first. The feature files in `docs/spec/` hold the current behaviour;
this file holds when and why it changed. Add a line here in the same session as any spec change.
Telot's latest statement is the decision.


## 2026-10-22 (terminal commands: clear the saved Primo answer, perf suite)
- **Telot:** a command to clear the saved Primo answer any time. `cd backend && npm run cache:clear -- "search words"` removes every cached page of that search (match built from the Primo service's own `normalizeQuery` and key layout via `cacheKeyPattern`); `--all` clears `primocache`; `--dry-run` only counts. Only `primocache` is touched; it refuses when `NODE_ENV` is production or the database name lacks "minds" or contains "baseline"; it prints counts only. (The saved answer also expires by itself after about 24 h.)
- `npm run perf` runs the SERP performance suite (`scripts/perf-serp.js`, now committed; the `perf-report/` output stays untracked). `--cold` clears each query's saved answer before every timed Primo run. **The timed Primo call is the library call itself, which never reads the saved answer, so `--cold` does not change today's numbers**; it matters for any timing that goes through the service.

## 2026-10-22 (npm run compare)
- **Telot:** `cd backend && npm run compare -- "exact search words" [--runs N]` (1 to 10, default 3) times one search through Baseline (the shared Primo fetch behind `/api/library/search`) and MINDS (session, Primo, scoring 5.3, ranking, for a typed query so no 5.2), alternating which goes first. The saved Primo answer is bypassed (`searchPrimo({ bypassCache: true })` neither reads nor writes `primocache`); the MINDS side runs on a throwaway workspace with 8 invented directions and removes it; same database guard as `cache:clear`. Prints ms and the hit count only. Results go into the same HTML report as `npm run perf`, with earlier comparisons kept in `perf-report/compare-history.json` (untracked, holds the search text you typed).
- **Counts (added):** each run also prints the hit count (Primo's `info.total`, the "Results: N"), the records returned, and for MINDS the usable records before and after duplicate merging (`searchPrimo` now also returns `counts`). A run in which Baseline and MINDS report different hit counts prints a WARNING (both use the same Primo call); the counts and the warning are in the console table, the HTML report and the history.
- **Reading the numbers:** Primo answers a repeated identical query faster on its own side, so the first call of a comparison pays the cold cost and the side that goes second can benefit. The table's "first cards" row is what a participant waits for now (the list shows before scoring); "total" is when the chips and ranking are done.

## 2026-10-21 (SERP: the list first, the scores second)
- **Telot:** "show the serp even if the scores aren't done, and while the scoring is still coming make all the chips a loading state, like when directions get generated in planning." Cause (perf suite, `perf-report/`): scoring was about 72% of the first-visit wait (6.9 s of 9.6 s, 8 directions; Primo about 0.9 s).
- **Built:** `POST /api/sessions/:id/search` accepts `scoring: 'later'` and answers with the library's list (`scorePending: true`) unless every pair is already stored; new `POST /api/sessions/:id/scores` scores them (still one batched call, stored pairs skipped, rule 5) and returns the ranking order. The SERP shows cards with skeleton chips, then the chips, and orders the list once. Without `scoring` the search behaves as before.
- **My call, Telot to confirm:** once the scores arrive the first page is **re-ordered once** by the active direction (F2 ranking is unchanged), announced in the live region. The alternative is to keep the library's order and only add chips; a card could otherwise move while someone is reading it. A "Load more" batch only reorders itself.
- **Side effect:** `sessionresults.rank` records the order first shown (the library's), not the order after scoring.
- Not changed: scoring time itself (still about 3 to 7 s depending on the number of selected directions); this only stops it blocking the cards.

## 2026-10-21 (no sparkle or star icons)
- **Spec change (Telot):** the sparkle icon is removed everywhere (Plan Workspace rows, Your sessions cards, SERP Directions panel, reason lines on chips and saved results). It was meant to show which directions are AI-generated, but the "?" (Why?) button already explains that. From now on **no sparkle or star icon marks AI directions**. AI rows have "?"; custom rows have Edit / Remove (Your sessions keeps its Custom tag). The save star on SERP chips is a different control and stays. Updated: CLAUDE.md, 01-core.md, accessibility.md, F1, F3, F5, code, tests. Older entries below that mention the sparkle are history.

## 2026-10-21 (Plan Workspace: simpler rows and header)

- **Spec change (Telot):** on Plan Workspace the "Why?" button shows only a **?** (its accessible name stays "Why? <label>"); the **Custom** tag is removed; the
  visible title "Plan Your New Workspace" and the helper line are removed. Kept: a visually hidden `h1` with the old title (a page needs one) and the sparkle
  for AI rows. Cost: custom rows now differ from AI rows by the missing sparkle and by Edit / Remove only, so the "never the only cue" rule rests on those
  buttons. Your sessions' direction cards still show their own Custom tag (not asked). Frontend 229 tests pass.

## 2026-10-21 (Plan Workspace: breadcrumb)

- **Spec change (Telot):** Plan Workspace has a breadcrumb `Workspaces › {workspace title}` above the form, same markup as Your sessions. `Workspaces` goes back to
  `/workspaces`. A workspace with no title shows "Untitled workspace". Frontend 231 tests pass.

## 2026-10-20 (I2: search pipeline, backend)

- **Built** (Telot said go straight to I2 with U2 still open): models `Session`, `ResultsCache` (no expiry), `PrimoCache` (24 h TTL), `ResultScore`,
  `SessionResult`; `Queries` extended; Primo service; 5.2 and 5.3 services; sessions; `POST /api/sessions/:id/search`. 136 backend tests, no network.
  Details in F2 "As built". Not checked against real Primo or the real model yet.
- **The scoring prompt changed:** each result now carries `known_scores` and `score_directions`, and the model scores only those directions. Cost: a
  result that is half-scored is still sent whole (title and abstract again); benefit: a stored score is never asked for again (rule 5).
- **Two small additions to the spec:** the low-confidence flag and the "Based on title and subjects only" prefix are also enforced in code, and a unique
  partial index allows one `ai` query row per direction (stored query rule).
- **`libraryController.js`** now exports `fetchPrimoPage`, which the Baseline proxy and MINDS both call (Baseline behaviour unchanged).

## 2026-10-19 (I1: a workspace with a plan shows the full plan by default)

- **Spec change (Telot):** opening the plan page for a workspace that already has a plan shows the saved plan straight away (what "Update workspace" did): texts
  and directions in saved order, all ticked. The top "Open workspace Or Update workspace" row is no longer the default; it stays as a fallback when the participant
  typed before the lookup returned, and the bottom row stays for an Explore 409.
- **Explore on a loaded plan:** unchanged -> opens the SERP and writes nothing (otherwise every open would give every direction a new `_id`, which matters from
  I3, open-questions.md 9); changed -> `replace: true`. Cost: no separate "Open workspace" button when the plan loaded by default; Explore is the way to the SERP.

## 2026-10-19 (I1: clicking a workspace opens Plan Workspace)

- **Spec change (Telot):** on `/workspaces`, clicking a workspace no longer opens the SERP; it opens that workspace's Plan Workspace page. A planned
  workspace shows "Open workspace  Or  Update workspace" at the top there, and Open workspace opens the SERP. Cost: one extra click to reach the SERP.
  Baseline change: `handleSelectWorkspace` in `WorkspaceList.jsx` (stack_changed.md). The menu item **Edit Workspace** (next entry) is kept and now
  goes to the same page as a click.

## 2026-10-19 (I1: "Edit Workspace" in the Workspaces list menu)

- **Spec change (Telot):** the three-dots menu on a workspace gets one more option, **Edit Workspace** (placed first), that goes to that workspace's
  Plan Workspace page. For a workspace that already has a plan the page shows "Open workspace  Or  Update workspace" at the top as soon as it opens
  (a `GET /plan` lookup on load; empty or failed lookup: no row). Baseline change: one menu item and one case in `WorkspaceList.jsx` (stack_changed.md).

## 2026-10-19 (I1: "Update workspace" replaces an existing plan)

- **Spec change (Telot):** when Explore finds a plan already saved, the message offers two choices in one row: "This workspace already has a plan.
  [Open workspace] Or [Update workspace]". Update loads the saved texts and directions (saved order, all ticked) into the normal screen; Explore then replaces the plan.
- **API (smallest change):** `PUT /plan` accepts an explicit `replace: true` (strict boolean); without it the 409 `PLAN_EXISTS` rule is unchanged, so a plan is never
  replaced by accident. A new `GET /plan` returns the saved texts and directions (owner only) and is fetched only when Update is chosen. No new write route.
- **Safety:** the replace (delete old directions, insert new, update texts) is one `runInTransaction` (Atlas). On a standalone MongoDB the old directions and
  texts are snapshotted first and put back if a write fails. Errors are logged by name only.
- **Not built (open-questions.md 9):** once saved results exist (I3), a replace must keep directions that have saved results (their `_id`s).

## 2026-10-19 (I1: reorder search directions by drag and drop)

- **Spec change (Telot):** the participant can drag and drop any search direction to change the list order (F1 "Reordering"). One ordered list
  (`order` in the shared model, used by `/ui/plan-workspace` and the real page); row numbers are fixed slot labels, not part of the card.
  Insertion point is a 3px black line above/below the card under the pointer, or a grey end slot in column 2 (outside the list, space reserved,
  so no card changes column). Explore sends the selected cards in list order (first selected = SERP default); **no payload or endpoint change**.
- **Regeneration rule:** selected and custom cards keep their slots; unselected AI cards are holes filled top to bottom by the new suggestions;
  leftovers at the end; unfilled holes removed. A batch that arrives mid-drag is held until the drop. (This replaces the earlier
  "kept first, then fresh" ordering.)
- **End slot position (Telot's correction):** the grey end slot is drawn in the next available position, right after the last card, not in a
  fixed row below the list (that left a one-cell gap when the last column was not full). Odd count on two columns: the free cell at the bottom
  of column 2 (it is the (n+1)th grid cell, so nothing moves). Even count: directly under the last card of column 2 in the Add row. Narrow
  screen: right after the last card. The placeholder `li` is `aria-hidden` and has no number.
- **Library:** `@dnd-kit/core` only; MouseSensor (6px) + TouchSensor (250 ms press-and-hold, approved by Telot because a swipe over the cards is scrolling).
- **Known gap, recorded not hidden:** no keyboard reordering. dnd-kit's keyboard sensor needs extra code to choose an insertion point, so it is
  left off (accessibility.md, STATUS.md, open-questions.md 8). Telot to decide.
- dnd-kit's own announcements are silent (they would read "draggable item 1" for a mouse drag).

## 2026-10-19 (I1: Plan Workspace flow, Explore saves the plan)

- **Flow (Telot):** `/start` -> `/workspaces` -> **+ New Workspace** (Baseline's Create New Workspace dialog, participant's own title)
  -> **Plan Workspace for that workspace** -> **Explore** -> Baseline SERP. Explore does **not** create a workspace: it saves the three
  texts and the selected directions onto the existing one with `PUT /api/workspaces/:id/plan`. Baseline's `POST /api/workspaces {title, color}`
  is unchanged. F1, 03-api.md and 02-data-model.md updated.
- **Baseline dialog navigation changed** (stack_changed.md): after Create it goes to `/workspace/<id>/plan` instead of opening the SERP
  with the title as the query. `Layout` renders only the page on that route.
- **Dropped:** the MINDS body on `POST /api/workspaces`, the AI-generated workspace name (`project_name` removed from call 5.1) and
  the unique-title work. The participant's title is the workspace name.
- **Route:** `/workspace/:workspaceId/plan` with the id in the URL, not `WorkspaceContext`: the context is filled by a window event after
  navigation, is wiped on `/workspaces`, and does not survive being the source of truth on refresh. The page fetches the workspace
  (ownership checked server-side); Explore then calls `openWorkspace`, which fills the context for the SERP.
- **`PUT /plan` writes once:** 409 `PLAN_EXISTS` if the workspace already has directions (rewriting later would orphan saved results and
  scores); `{workspaceId, orderIndex}` is a unique index so a double submit also fails safely. `orderIndex` is 0 to n-1 over the selected
  directions in list order (no gaps). One transaction on Atlas; a local standalone MongoDB falls back to a compensated plain write.
  No session is created by the plan (sessions are lazy, 02-data-model.md; this corrects the old 03-api.md line).
- **Provider errors never reach the browser as 401/402/403:** the frontend signs the participant out on any 401/403, so every LLM failure is a
  502/503 `LLM_UNAVAILABLE`.
- **Rate limit:** 10 requests a minute per participant on `/generate` (`GENERATE_RATE_LIMIT`, my default; tune in testing).
- **Regeneration UX:** existing rows stay in place while an update runs ("Updating search directions…"); skeleton rows show only when
  there are no suggestions yet; on failure the old rows stay with the error box and Retry.
- **Safety:** the server now warns at startup when the MongoDB database name looks like Baseline's, or has no "minds" in it
  (`backend/config/dbName.js`; `node backend/scripts/show-db-name.js` prints the name and collection counts only). At the time of I1 the
  development `MONGO_URI` pointed at a database named `baseline`: no manual try was made until that is changed to a MINDS-only database.
- **Open for I7:** a workspace with no directions yet should reopen Plan Workspace (open-questions.md 7).

## 2026-10-19 (I0: LLM provider, SavedDoc, scoring repeatability)

- **Development LLM provider: Gemini, model `gemini-3.5-flash-lite`** (Telot). Env vars `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY`
  in `backend/.env` (names only in `.env.example`). For development with made-up data only: a free tier may use prompts to
  improve the provider's products, so no participant text. The study provider is still open (open-questions.md 1).
- **`SavedDoc` stays the document record; `savedresults` holds the per-direction link rows** (Telot, taking the open-questions.md
  recommendation). `savedresults.resultId` points at `resultscache` (scores exist before saving). See 02-data-model.md.
- **Scores are not repeatable at temperature 0, so scores are stored and never re-requested.** Smoke test on the mock pool:
  5 to 20 of 70 scores changed between two identical runs (temperature 0 and default alike); call 5.1 gave different labels every run.
  Rule 5 already says to skip stored pairs; this is the measured reason. The 5.3 prompt now says a score is 0 unless the metadata
  names the direction's topic (F2); after the change the irrelevant mock-005 scored all 0 in the two default-temperature runs
  but "Community access" still got 1 in the two temperature-0 runs.
- **Structured output works with the full JSON schema** (`responseJsonSchema`); the fallbacks (reduced `responseSchema`, then JSON in
  the prompt) exist in the client and are covered by tests but were never needed.
- **LLM client rules:** key only in the `x-goog-api-key` header; errors reduced to a fixed `LlmError` and logs to an allow-list
  (no key, URL, header, prompt or output can appear); one retry (timeout, network, 5xx, a one-off 403, invalid output; 429 waits for the
  provider's hint, 10 s if none, and is not retried if the hint is over 60 s). Latency on the mock pool: 5.1 about 1.6 to 2 s,
  5.3 about 3.5 to 6 s.
- **Scope of I0:** the rate-limit factory and the React Query provider move to I1, where they are first used (Telot).
  `server.js` now exports `configureApp` for Supertest (stack_changed.md).

## 2026-10-17 (U2: chips on the Saved results view)

- **No bookmark on Saved results cards either** (Telot). The MINDS copy of `SavedDocumentCard` shows a solid-blue chip for each
  direction the result is saved under, in its footer. A chip does what the bookmark did: it unsaves under that direction, and
  unsaving the **last** chip runs Baseline's unsave and removes the result from the list. (If a result is saved under two
  directions, one chip click removes only that direction; the result leaves the list when none is left.)
- Chip click logic is shared (`toggleDirection` in `MindsSerpContext`): optimistic, rollback with a visible message on failure.
- Fixtures: earlier-session saved results (ids x1 to x6) now have scores so their chips show a star and number; they are not
  part of the page's scored batch.

## 2026-10-17 (U2: chips replace the bookmark)

- **The bookmark button is removed from MINDS cards** (Telot). Direction chips take over its exact actions: the first chip
  saved under a result runs Baseline's save (`ensureSavedThenGetId`), unsaving the last chip runs Baseline's unsave
  (`unsaveSavedDocument`). The nav-bar Saved Results button therefore shows every result with a saved chip. A chip updates at
  once and rolls back with a visible message if the call fails; unsaving on the Saved results view clears the chips.
- The card has no actions column any more, so the abstract uses the full card width.
- The Search Direction dropdown is hidden on the Saved results view (it only applies to searching).
- Mock API: the saved list starts with the documents behind the chips that are already saved, so both screens agree.

## 2026-10-17 (U2: right panel as in the design)

- **The right panel follows the design image** (Telot): one card with three rows. Row 1 "Directions you have explored"
  now also has the per-session bar (`+N` segments, plain counts, unlabelled grey ruler), reversing the earlier "no bars on
  the SERP" call. Row 2 "What you might explore" lists the suggestions behind every New pill (dashed rows, New tag,
  `+`, `×`; no circle or sparkle). Row 3 is a dashed "Add search direction" button, which was not in the spec.
- Dismissing a suggestion also removes its New pills from the cards. Promote and Add are Mock only until I3.
- F3 rewritten to match (panel section, acceptance criteria).

## 2026-10-17 (U2: direction layer on Baseline's SERP)

- **Built on the copy** (Telot's order: dropdown, panel, chips): Search Direction dropdown beside the workspace
  breadcrumb (native select, right-aligned); fixed right panel in Baseline's right rail; direction chips in a footer
  row of each card, with `>>` and `?`. All MINDS pieces are in `features/serp/minds/` and render nothing without
  `MindsSerpProvider`, so the copy still behaves as Baseline without it.
- **Panel heading is "Directions you have explored"** (Telot's wording, same as the mockup), replacing F3's "What you have
  explored" on the SERP; Your sessions (F5) keeps its own wording until Telot says otherwise.
- **`ResultCardShell` copied** into `features/serp/components/` with one addition (a footer slot); the shared Baseline
  one is untouched.
- **Provisional chip cue again:** light blue = border + "Best on page"; solid blue = check + "Saved". Still open in
  open-questions.md 4.
- **Not done yet:** "What you might explore", header Saved Results toggle behaviour, New-pill promote, removing
  Baseline's bookmark button from the card, re-ranking by the active direction (I2).

## 2026-10-17 (U2 restarted on Baseline's SERP)

- **Reuse Baseline's SERP, do not rebuild it** (Telot). The from-scratch `features/serp` (card, chips, panels,
  fixtures, tests) was deleted; `features/serp/` is now a copy of `features/search/`, which stays untouched as
  the control. Both conditions then share the same card look, so differences come from the intervention.
- **How `/ui/serp` shows it with no network:** the copied page runs unmodified Baseline code. `ui-dev/mockApi.js`
  replaces the axios adapter of the shared `apiClient` (search, details, saved docs) while the screen is open;
  `ui-dev/SerpDevPage.jsx` replaces `window.localStorage` with an in-memory copy (fake participant and workspace),
  so a real login in the same browser is never read or overwritten. Only deliberate change in the copy:
  `SearchSection` skips `navigate()` on `/ui/...` paths (Phase 1: no navigation).
- This supersedes the 2026-10-16 U2 entries below (mockup-vs-spec calls, provisional chip cue, local-only
  behaviour); the chip cue is open again (open-questions.md 4). The label removal below still stands.

## 2026-10-17 (U2 follow-up)

- **The label "Why this may help your search" is removed** from the result card, F3 and every other place. A card
  now goes title, meta line, description, then the chips and `>>`; the reason is reached only through each
  chip's `?`.
- **`docs/design/02-serp-c.png` deleted:** it was the wrong screen. SERP mockups are `02-serp-a.png` and
  `02-serp-b.png`.

## 2026-10-16 (U2: SERP UI)

- **Mockups vs spec (spec wins, Telot confirmed):** "What you have explored" keeps the F3 title; no segmented
  bars in that panel (they belong to Your sessions); the reason is shown only through the `?` toggle, not as an
  always-visible sentence; no "Read more" link; the header shows `Workspace: <title>` as plain
  text (no "Projects" link, no crest, no account icon); `Results: N` sits on the meta bar.
- **Light blue and solid blue cue (provisional):** light blue = 2px blue border plus the text "Best on page" and
  the name suffix "best match on this page"; solid blue = check icon plus "Saved". Still to be tested
  with participants (open-questions.md 4).
- **Local-only behaviour in U2:** a chip click toggles saved in memory (live region "Saved under X. N results
  saved."; panel counts derived from the saved rows); the New pill, the panel `+`, the circles, Saved Results
  and search submit only show a "Mock only" status; dismissing a suggestion hides it for the visit.
- **Mockup 02-serp-c** was the wrong screen and is removed (see 2026-10-17).
- `ResultMeta` fixtures gain an optional `year`; U2 states live in `mocks/serpFixtures.js` (`SERP_STATES`).

## 2026-10-19 (Your sessions: one colour per session)

- **Fixed colour per session** (Telot): newest near-black, second newest slate `#475569`, older `#EEF0F4`. Used for
  that session's bar segments in every bar and, only while one of its segments is hovered or focused, the tile's
  border (no coloured border by default, Telot 2026-10-19; replaces the black 3px outline). Replaces the alternating two shades,
  which were by position and could show one session in two colours. Light-grey segments get a thin outline and
  dark text. The `S3` / `S2` / `S1` badges are removed from the tiles. The SERP right panel (U2) still alternates
  two shades; not changed.

## 2026-10-19 (U4: Saved results view)

- **One saved view, built from the Your sessions fixtures** so the numbers agree: all sessions = sum of tile totals,
  a direction = its circle, a session = its tile. It follows `04`, `05`, `06` with the corrections below.
- **Grouped by session** (newest first, heading `SESSION 3 · SEP 23`, earliest save first inside a group; no
  heading when a session filter is set).
- **Counts row has three counts** (Telot): saved results (document icon), unique search directions (three
  arrows) and sessions (history icon). The mockup's numbers were wrong.
- **Session 2 now has a saved result** (Community Gardens... under Community access) so the all-sessions view has
  three groups. This changes Your sessions: Session 2 shows `Community access +1` and `1 saved`, and the Community
  access card has circle 1 and a `+1` bar segment; the reviewed-only card state is now only visible in the `many` state.
  Totals: 9 saved results, 4 directions, 3 sessions.
- **Header = SERP `MainHeader` in saved mode** (disabled search box with the last query, Return to Search); no
  Back button; h1 visually hidden. `MainHeader` gained `savedMode` and `searchPreview`.
- **Dev navigation is wired for this flow** (a Phase 1 exception): Your sessions' Saved Results button, tiles,
  count circles and bar segments, and Return to Search / breadcrumb on the saved view, move between the `/ui`
  screens with the state kept. Last Saved on Your sessions is now the newest saved result (Indigenous-Led
  Placemaking...), not the mockup's sample.

## 2026-10-18 (stored query rule)

- **The query for a direction is generated once, stored, and reused (Telot).** 5.2 runs only the first time a
  direction is selected; the result is a `queries` row (`source: 'ai'`). It is never regenerated on switching,
  on returning in a later session, or from Your sessions. Reasons: token cost, latency, and the LLM wording the
  same direction differently each time, which confuses the participant. Typed queries are extra rows
  (`source: 'user'`); the newest row is shown.
- **Removed:** `regenerateQuery` on `POST /api/sessions/:id/search`, and the 5.2 inputs `previousQueries` and
  `savedTitles` ("better, different query" on entering from Your sessions). Clicking a card on Your sessions
  now just opens the SERP with the stored query. Written into 01-core rule 5, CLAUDE.md rule 5, F2, F5,
  02-data-model, 03-api, build-plan.
- **Last Query** (Your sessions) = the search phrase in the SERP search box when the session last had activity
  (typed or AI), i.e. the active direction's newest stored query.

## 2026-10-18 (Last Direction)

- **Last Direction** on Your sessions = the direction **selected on the SERP** when the newest session last had
  activity (Telot), not the direction of the newest query. Stored as `sessions.activeSubGoalId`, updated when the
  dropdown selection changes or a search runs. **Last Query** = the newest query under that direction (the one
  the SERP search box shows for it; assumption, Telot to confirm). Last Saved is unchanged.

## 2026-10-18 (check-out removed)

- **The check-out feature does not exist** (Telot). Removed from F5 (section, tag, mentions), `02-data-model.md`
  (`sessions.checkoutReason`), `03-api.md` (`POST /api/sessions/:id/checkout`, `checkoutReason` in the overview),
  `build-plan.md`, `00-index.md`, `F7-logging.md` (event), `deferred.md` (recap input), `open-questions.md`, the
  fixtures and `types.js`. A session still ends by idle gap only (`SESSION_GAP`). The thesis planning document in
  `minds-doc` must drop it too (separate session there).

## 2026-10-17 (U3 redo: Your sessions exactly as the mockup)

- **Mockup wins for Your sessions** (`03-your-sessions.png`), with "Project" replaced by "Workspace". Added:
  header Saved Results button, breadcrumb `Workspaces › name`, title "Workspace Overview", Continue Last
  Activity, Last Direction / Last Saved / Last Query cards, headings SESSIONS and DIRECTIONS YOU HAVE EXPLORED,
  arrow circle on each card, dashed "+ Add search direction". Details in F5.
- **Tile snapshot = the mockup's pills** (first two words + `+N`), replacing the numbered journey blocks and the
  "N reviewed" count of 2026-10-16. A zero pill reads "0 saved", never "+0".
- **Removed from the screen:** the "Workspace Name:" line, Start New Workspace, the Check out menu and tag
  (superseded 2026-10-18: check-out removed entirely).
- **0-saved cards: empty grey track, no visible text** (overrides the visible-text-cue rule in accessibility.md
  for this case; hidden screen-reader text kept). Count circle always outlined, never filled.
- **New tag (UI only):** a direction added from the SERP in the newest session shows an amber New tag and, with
  0 saved, a dashed "–" circle, until that session ends (idle more than `SESSION_GAP`, or a later session
  starts). Needs `addedInSessionId` on `subgoals` in I0. Reverses the 2026-10-16 deferral of "New" badges for
  this screen only.
- **Header = the SERP's `MainHeader` without the search box** (Telot, 2026-10-17), not a new one. `MainHeader`
  gained `showSearch` and an optional `onNavigate` (dev screens use it so the logo, menu and logout do not leave `/ui`).
- **+ Add search direction** allowed on this screen (UI only; saving decided in I5); renaming and removing stay
  deferred.

## 2026-10-16 (U3: Your sessions UI)

- **Snapshot design confirmed:** numbered block grid (ordered list), saved mark `+N` pill or "0 saved", plain
  "+N more" after 6, totals line `N reviewed · N saved`, check-out tag (superseded 2026-10-17 and 2026-10-18). Details in F5.
- ~~**Check-out control:** a "Check out" button with a four-reason menu on the newest session tile only.~~ Removed 2026-10-18.
- **Block saves** are attributed by time window (query `createdAt` to the next visit); `Query` fixtures gain
  an optional `createdAt`. Phase 2 needs the same field in `queries`.
- **Bar overflow:** one shared unit shrinks until every bar fits with 32px minimum segments; if that is
  impossible the segment row wraps.
- Dev route slug renamed `/ui/your-sessions` to `/ui/sessions`. Mockup extras (summary cards, "Continue Last
  Activity", header "Saved Results" button, card arrow, "+ Add search direction", "New" tag) not built: not in F5.
  Custom directions carry a "Custom" tag as on Plan Workspace (sparkle is never the only cue).

## 2026-10-16 (U1 follow-up 2: one mixed list, 7-word limit)

- **One mixed list across both columns.** Familiar and `new` suggestions are interleaved in the order the
  model returns them; custom directions go at the end. The list fills column 1 then column 2 (one `<ul>`,
  layout only). This replaces the "column 1 familiar, column 2 new" rule in F1. `suggestionKind` is still
  stored for the study but is not visible on this screen. `orderIndex` = the row number minus 1.
- **Word limit, not just an ellipsis.** Every direction label is at most `DIRECTION_LABEL_MAX_WORDS` = 7
  words (new constant in 01-core.md), so labels fit on one line. Typing an 8th word is ignored, a longer
  paste is cut to 7, and "N of 7 words" is shown. AI labels stay 2 to 5 words in the prompt, with a hard
  cap of 7 in Zod (I1). The ellipsis from the previous entry stays only as a safety net.
- **Bug fixed:** `minmax(0, 1fr)` columns. With `1fr`, a nowrap label stretched column 1 and pushed
  column 2 out of the window.

## 2026-10-16 (U1 follow-up: Telot's review of the Plan Workspace)

- **Corners:** every box on Plan Workspace (fields, direction rows, Add box, inline inputs, error box,
  Explore) uses the SERP result card radius, `CARD_BORDER_RADIUS` = 12px (not 8), rectangular, not pills.
- **Column 2 is not different from column 1.** No "New" tag and no faded or dashed styling for `new`
  directions; same row design. (The column split by kind was removed in the entry above;
  `suggestionKind` in the data is unchanged.) This supersedes the "New" tag and fading rules in F1,
  accessibility.md and open-questions.md (all edited). The faded **New pill on the SERP** (F3, 01-core)
  is a different thing and is unchanged.
- **One line per direction**, however long the text: no wrapping, ellipsis when it does not fit, full text
  in `title` and the accessible name. The "Why?" rationale panel may still wrap.

## 2026-10-16 (U1: Plan Workspace UI)

- **Mockups checked first** (`docs/design/01-plan-workspace-*.png`). Telot decided on the three things
  the mockup shows and F1 did not: keep the **row numbers** (list position, same as `orderIndex` + 1),
  keep the **participant icon** in the header (becomes the account control when login is integrated),
  keep the decorative **three-arrow icon** beside "Search directions". F1 updated.
- **Label wording follows F1**, not the mockup: "What I want to find", "Add Search directions".
- Unselected `new` directions: dashed border and no fill; checkbox outline and sparkle stay at 3:1 or
  better (accessibility.md), label text stays at full contrast, visible "New" tag (the dashed border and
  "New" tag were removed later the same day, see the entry above). Disabled Explore
  uses dark text on grey (4.5:1) plus a visible reason; it uses `aria-disabled`, so it stays focusable.
- Caught in testing: MUI `SvgIcon` is `aria-hidden` unless `titleAccess` is set, which would have hidden
  the "Suggested by AI" name from screen readers. Use `titleAccess` on every meaningful icon.

## 2026-10-16 (U0: dev route shell)

- **`/ui` is development-only and outside the login guard.** The router registers `/ui/*` only when
  `process.env.NODE_ENV === "development"`, and lazy-loads `src/ui-dev/`. A production build has
  neither the route nor the chunk, so `/ui` falls to the existing redirect to `/start`. Login, Primo
  and the protected routes are unchanged; there is no production bypass.
- Fixtures are JavaScript with JSDoc typedefs (`frontend/src/mocks/`), matching the repo's stack, not
  TypeScript. Zod is added in I0 for the data contract.
- Contrast test (`src/theme/contrast.test.js`) covers the `--text-muted` pairs from accessibility.md
  plus Baseline `text.primary` / `text.secondary` on the page and card backgrounds.

## 2026-10-16 (build order)

- **UI first, interaction second.** All screens are built as UI with mock fixtures (sessions U0 to U4)
  before any LLM, database or navigation is wired (sessions I0 to I8). F1 to F7 stay the behaviour
  spec; `docs/spec/build-plan.md` says what each session builds. LLM provider, key and the `SavedDoc`
  decision are therefore needed at I0, not before the UI phase.
- **Mockups live in this repo:** the 10 screenshots were copied to `docs/design/` so every UI session
  can open them; the spec wins where a mockup differs (README there lists the known differences).
- **Spec changes** go to the planning document (thesis repo, v27) and to `docs/spec/` together.

## 2026-10-16 (context setup; Telot answered Q1 to Q8)

- **Scoring reasons (Q1 B):** the 5.3 call writes a reasoning sentence only for the chips a card
  shows (each result's top 3 selected directions plus its highest-scoring new direction); others are
  null and generated when `?` is tapped, then stored. (F2)
- **Missing abstract (Q2):** score from title and subjects, flag `lowConfidence`; the `?` text starts
  "Based on title and subjects only". (F2)
- **New-direction label matching (Q3 A):** normalized text plus the LLM told to reuse existing labels
  exactly; no embeddings; revisit if near-duplicates appear in testing. (F4)
- **`SESSION_GAP` is 1 hour** (Q4; was 1 day). Idle longer than 1 hour starts a new session on the next
  search. `IDLE_CAP` stays 5 minutes. (F5)
- **Workspaces list:** Edit Name, Select Color (cosmetic: adds a border) and Archive already exist in
  Baseline; **not specified in this spec** (Q5, Q6). The workspace name is AI-generated at creation and
  editable through Baseline's Edit dialog (replaces "not editable").
- **"Project" and "task" are now "workspace"** everywhere (UI text, data entity `Workspace`, routes).
  The old mockups and screenshot filenames still say "Project"; update the mockup text.
- **Plan Workspace header:** the institution logo as in Baseline (replaces the MINDS wordmark).
- **Non-colour cue for light-blue and saved chips:** left as is for now.
- **Stack (Q7):** MERN kept; see `stack_changed.md`. Spec's Postgres/Supabase, Next.js, Tailwind and
  TypeScript replaced by MongoDB, Express, React + MUI and JavaScript + Zod.
- **Interaction logging added as a feature (Q8):** F7, draft. Baseline's logging had been removed.
- **Stored counters dropped:** `saved_count`, `shown_count`, `opened_count` on directions are derived by
  aggregation, never stored (rule 2; matches Baseline's runtime-computed workspace counts).
- **Scores are integers 0 to 5** everywhere; the old decimal examples (4.5, 4.2) and `numeric(2,1)` are
  gone.
- **Consequences found in review (same day):** `resultscache` (result metadata) never expires, and the
  24 h TTL lives on a separate `primocache`; the on-demand reasoning endpoint is the only LLM call a
  Saved results view may make; the 5.3 call receives `known_scores` so it can pick which new pairs need
  reasoning; reasoning is written only for pairs scoring above 0; `goal_relevance` is an integer; LLM JSON
  is snake_case and mapped to camelCase; `SESSION_GAP` means idle **more than** 1 hour.
- **Primo access works** (Baseline already uses it with the key in server-side `.env`).
- **Spec split:** the 1,326-line `technical-specification-1.md` (frozen, in the papers repo) is replaced
  for building by `docs/spec/`.

## 2026-10-15

- Scores are whole numbers 0 to 5: model returns integers; server floors decimals and clamps.
- Confirmed: one New pill per result; ties go to the selected direction; zero scores appear under
  `>>`; light blue considers selected-direction chips only; `>>` is icon-only (accessible name "Show
  other directions").

## 2026-10-14

- **Scoring by the LLM in one batched call per search** (5.3), not embeddings. Retrieve with Primo, judge
  with the LLM. Anchored rubric, temperature 0, stored scores.
- `CANDIDATE_POOL_SIZE` 30 to **10** (matches Baseline page size; keeps load time short).
- **Chips:** top 3 selected directions by score, **no minimum score, nothing forced**. `MIN_CHIP_SCORE`
  and `STRONG_MATCH_SCORE` removed. Ties by `orderIndex`. Scores of 0 appear only under `>>`.
- **Chip colours:** solid blue = saved; light blue = top chip of a result with the highest chip score
  on the page; neutral otherwise.
- **New directions come from saved results** (5.6): after at least 3 saves, a topic in at least 3
  different saved results, not in the plan, with goal relevance strictly above 2, becomes a suggested
  new direction, scored on later results and shown as a faded fourth "New" pill. `EMERGING_MIN_SCORE`,
  `SUGGEST_WINDOW`, `EMERGING_START_SAVES` removed.
- **`>>` button** reveals the other selected directions on a card.

## Earlier decisions (carried from the old spec section 11)

- Sparkle = AI-generated; no sparkle = custom. Screen 1's faded suggestions are `new` directions,
  selectable. (Superseded 2026-10-16: Screen 1 no longer fades them.)
- Clicking a saved chip undoes the save. The SERP search field is editable. Clicking a faded chip
  adds the direction to the plan and saves under it; each "might explore" row can be dismissed.
- `?` stays on chips (every score has a "why").
- Categorical badges, Plan Strip, Coverage Map, clarity control and recap text are deferred.
- Session badges read `S3, S2, S1`; pale mockup text fixed to meet AA contrast.
- A workspaces landing screen opens a workspace's Your sessions; breadcrumbs start with a clickable
  Workspaces segment. Session tiles are clickable (saved results for that session).
- The saved results view is one view with two optional filters (`direction`, `session`).
- 2026-10-20 Saved results view: cards show only the directions the participant saved under (no grey chips for other scored directions); a chip unsaved in the view stays grey until leaving, for undo.
- 2026-10-21 Plan Workspace: Explore saves every direction on the screen, not only the ticked ones (`subgoals.selected`, `orderIndex` over all). Unticked ones are not searched or shown on the SERP or Your sessions, but come back unticked on Plan Workspace so the participant can tick one later (Explore then replaces the plan). Regeneration still replaces unticked AI suggestions on screen.
- 2026-10-21 I3 backend: chip save/unsave write only `savedresults` link rows in the current session (idempotent; unsave also works on a direction unticked since); `SavedDoc` stays written by Baseline's add/remove calls from the card, as U2 built it. `?` reasoning is generated once if null and stored (first writer wins); `emergingDirectionId` on save and reasoning waits for I4.
- 2026-10-21 Directions are new-only (Orland confirmed). Call 5.1 proposes only angles the student has not thought of and never restates or rephrases what they wrote; the model no longer returns `kind` and the server stamps `kind: 'new'` (API, saved plans and frontend unchanged; `familiar` stays valid in `plan.js` and `subGoalModel.js` for older plans). The familiar-versus-new selection comparison no longer exists, so the study cannot analyse how often participants pick new over familiar directions.
- 2026-10-21 Update workspace keeps saved results: a replace matches directions by label and updates them in place (ids survive); a direction dropped from the plan that has saved results is kept, unselected, after the new ones (`keptSubGoalIds`); others are deleted. Chosen over blocking or asking so a save is never lost (open-questions 9 closed).
- 2026-10-21 I3 frontend: the MINDS SERP is its own route (`/workspace/:id/serp`, `features/mindsSerp/`) fed only by the MINDS endpoints; Baseline's SERP (`/workspace`, `features/search`) stays as the control and `/ui/serp` stays on fixtures. Plan Workspace's Explore opens the new route.
- 2026-10-21 Chips write only `savedresults`; the Baseline `SavedDoc` is not written for MINDS saves (the search API does not carry the Primo record Baseline's save needs, and the Saved results view is built from `savedresults` + `resultscache` in I6). Changes the 2026-10-21 I3 backend line that said SavedDoc was still written from the card. Baseline's saved-documents list therefore does not show MINDS saves until I6.
- 2026-10-21 Page-2 prefetch not done: the search endpoint logs returned results as shown ("reviewed"), so prefetching would mark results the participant never saw as reviewed and spend a scoring call on a page that may never be opened. Load more is a button.
- 2026-10-21 "Add search direction" is built in I3 (F3 says so): `PATCH /api/workspaces/:id/subgoals` with `{add: {label}}`, add only. A direction added after a list loaded shows no chip on that list.
- 2026-10-21 The session response carries the saved counts and per-session segments, and search and save responses carry `savedSegments`, so the "Directions you have explored" bar (one segment per saving session) is real data, not derived on the client.
- 2026-10-21 I3 review (independent subagent against F3 and the 7 rules): no rule violations; fixed three findings: a search answer computed before a chip click no longer overwrites the counts (mutation counter), new cards always take their saved chips from the server even while a save is in flight, and the search field is read-only (not disabled) while searching so keyboard focus stays. Known and accepted: a direction added after a list loaded has no chip on it; a retry or repeat search logs its results as shown again (`sessionresults`, reviewed is distinct per result so counts are unaffected); a direction renamed in an Update workspace is a new direction, and the old one stays unselected if it had saves; the New-pill rule is built but has no live data until I4.
- 2026-10-21 First live failure and its causes. (1) The SERP showed "The search did not finish": the running backend (started Oct 19) predated the sessions route (committed Oct 20), so `POST /api/workspaces/:id/sessions` answered Express's own 404 page; fixed by restarting (`npm run dev` uses nodemon and avoids this). (2) Found by running `scripts/smoke-pipeline.js` against real Gemini and Primo: `scorePool` normalised the scores twice (`generateStructured` returns what `check` returns), so every real scoring call threw and the SERP would have shown unscored results; the unit test mock returned the raw output, so it passed. Fixed, the mock now behaves like the real client, and `scoringWithRealClient.test.js` runs `scorePool` through the real client with only the network mocked. (3) Error messages now name the failed step (session, query, Primo, scoring) with the HTTP status and, for a bare 404, a hint that the server may be an older version; no participant text.
- 2026-10-21 First real measurements (3 runs, invented task): time to first ranked list about 10 s with a new query (5.2 0.8 to 4.8 s, Primo 1.2 to 2.3 s, 5.3 4.1 to 4.5 s) and about 5 s with the stored query; the score spread is wide (best score per result mostly 3 to 5, 14 of 20 pairs scored 0) so light blue is common. **Open: the 5.2 query is sometimes too narrow for Primo: the same task gave 380, 26, 5 and once 0 hits for 7-word queries.** A zero-hit direction shows "returned no results"; consider shorter queries (3 to 5 words) or a fallback.
- 2026-10-21 Call 5.3 failure and speed-up, measured with the new scoring bench (`npm run bench:scoring`, fixed set of 10 records x 8 directions, 10 to 20 runs per variant). **Why 5.3 failed (about 4 of 25 compare runs on the first try, 2 of 25 even after the retry):** the model mistyped a 24-character database id; the check dropped the unknown id and counted the pair as missing. **Fix:** the model gets short opaque ids (`d` or `r` plus 6 hex characters, `utils/shortIds.js`), mapped back on the server. Ordinal ids (`d1`, `r1`) were rejected: they made the model score about 0.8 higher on average (mean 1.96 against 1.2, share of 0s 27% against 48%). Also: `reasoning` is left out instead of `null` (schema optional). Result: scoring median 10.0 s to 7.4 s, prompt 6,100 to 4,600 tokens, output 5,150 to 3,300, 0 failures in 10 compare runs. Level check against the old code (22 runs): mean score 1.24 against 1.43, 1.8 standard errors, inside the noise (accept rule: pairwise differences, chip overlap and mean level all within run-to-run noise). **Rejected:** short output keys (`r`, `d`, `why`, `low`): saved only 4% of output tokens and moved the level again (mean 1.91); a bundle of key renames, dropped empty input fields and no per-result `only` list cut output to 1,400 tokens but lost reasons on chips (33% against 64%), moved the level (1.65, 2.7 standard errors) and failed 1 run in 10, so not adopted. **Finding:** scores are noisy even for identical code: only about 55% of cells agree between two runs, and the mean score of a whole run varies from 0.5 to 2.0 (sd about 0.4). A change smaller than this cannot be seen with 10 runs. Not tried: positional score arrays (a list of 8 numbers per result), which would cut output further but can misalign silently.
- 2026-10-21 Validation failures of any call are now logged with their Zod paths and codes (`issues` in the `[llm]` line, e.g. `results.2.scores.1.score: invalid_type`) or fixed phrases from the 5.3 cross-check (`missing direction score`, `unknown direction id seen`, `duplicate direction score seen`); never values or text (allow-list pattern in `llm/log.js`).
- 2026-10-22 I6 Saved results view is live (`/workspace/:id/saved`, `GET /api/workspaces/:id/saved`): stored rows only, fetched fresh on every visit, built on the U4 screen and model (the screen now takes callbacks; `/ui/saved-results` still runs on fixtures). Entry points wired from the SERP: header toggle, count circle, bar segment. Decided without asking: (1) **undo of a removal saves back into the original session** (optional `sessionId` on the save endpoint, no session created or touched), otherwise the row would move to the current session and the bar, groups and Your sessions would change; the re-saved row has a new `savedAt`, so it sorts last in its group after a reload. (2) A filter that names nothing in the workspace is a 404 page, not an empty list. (3) The workspace-name crumb goes to the SERP until Your sessions has a route (I5, I7). (4) Card titles link to the library record and use Primo's type, as on the SERP; clicking does not mark the result opened. (5) Unselected directions that hold saves appear on the cards; re-saving under one is refused by the save endpoint (message shown). Not checked in a browser, by keyboard or screen reader. I5 (Your sessions) is not built, so "counts on Your sessions match after returning" stays open.
- 2026-10-22 I4 new directions (F4): detection (call 5.6), promote, dismiss, the New pill and the rows of "What you might explore" are built and wired on the live SERP. Choices: (1) `emergingdirections` also stores `reasoning` (the one-line why, rule 4) and `subGoalId` (promote and the later calls find the direction again), plus `normalizedLabel` as the unique key; 02-data-model.md updated. (2) Detection is triggered only when a save wrote a new row, after the answer is sent, with an in-process lock per workspace (one run, one follow-up); a second server process would need a database lock. It is not skipped when 3 suggestions are active, because F4 says it runs after a save and `timesSeen` refreshes. (3) Promote claims the row first (`suggested` to `promoted`), so a double click cannot make two directions; a New pill save promotes and writes the link row in one transaction (F4/03-api said so), and if the plan already has a direction with the same words it is ticked and used instead of duplicated. (4) A New pill click is not optimistic, because the server must add the direction first; the live region says "Saving under X." then the result. (5) Each suggestion row has a "?" showing its reason (F3 listed only label, tag, `+`, `×`; rule 4 needs the why reachable by tap): **Telot to confirm the extra control.** (6) Pills on cards already on screen are decided once per batch (F3), so a suggestion created by the latest save gets pills from the next search. (7) A score written for a suggestion by a scoring call that was already running when it was promoted lands under the old `emergingDirectionId` and is orphaned; the new direction then scores that pair again on the next search (harmless, not fixed).
- 2026-10-22 I4 review (independent subagent against F4 and the 7 rules): no rule broken; thresholds, ownership and logging intact. Fixed: a parallel promote (same pill on two cards, second tab) no longer loses the save or reports failure (the loser reads the row again and saves under the direction it became); dismiss that loses to a promote answers 409 `PROMOTED`; dismiss drops the scores kept for it; workspace delete also removes its `emergingdirections`; labels longer than 3 words are dropped (was 7); the panel row name no longer says "0 saved"; focus goes to the "Directions you have explored" heading after a row is added or dismissed; a full plan on a New pill save says so. **Known, not fixed:** (a) call 5.3 sends suggested directions in the same prompt as the selected ones, so their presence could in principle shift the active direction's scores (ranking code itself reads the active direction only, rule 6), and if 5.3 fails the whole list falls back to Primo order; a separate best-effort call would avoid both but costs a second call: **Telot to decide**; (b) a scoring call already running when a suggestion is promoted or dismissed can write one orphan score row; (c) on a standalone MongoDB (no transactions) a search that scores the new direction between its creation and the re-point can make promote fail on the unique index and retry (Atlas transactions are not affected); (d) the "same words already exist" promote branch does not restore the ticked state if a later write fails on a standalone MongoDB; (e) the "?" and "×" buttons are 32 px like the existing row buttons: check against the target size in accessibility.md.
- 2026-10-22 Call 5.2 queries are shorter: 2 to 4 words (was 3 to 8), the direction's own words plus at most one single anchor word from the goal, nothing taken from the want-to-find or already-know text. Cause of "This direction returned no results": Primo needs every word, and the model combined the direction with several topics from the goal and the want-to-find text (for the custom direction "organizing": `metacognitive scaffolding dyslexia visualization artificial intelligence organization`, 0 hits). Measured with real Primo on the same task and nine directions: old prompt 4 of 7 queries returned 0 hits (6 skipped by LLM timeouts); new prompt 0 of 18 over two passes (hits 3 to 12,901). The stored-query rule is unchanged: queries already stored keep their old text (type a query to replace it; the newest row wins). **Open (Telot):** no automatic fallback when a stored query still returns 0 hits (e.g. a server-side retry with fewer words would change what is searched against what is shown); and a one-word vague custom direction such as "organizing" still gets few hits (3 to 109).
- 2026-10-22 I5 Your sessions is wired (`/workspace/:id/overview`, `GET /api/workspaces/:id/overview`). The endpoint returns stored rows and the existing tested `sessionsModel.js` derives every number (rule 2), instead of the server returning derived pills and segments as 03-api.md first said; one derivation, already covered by tests, and the same shape as the U3 fixtures. 03-api.md and F5 updated. `subgoals.addedInSessionId` added (set on promote) for the New tag. Unselected directions are not cards. Nothing links to the page yet: the entry points are I7. A parallel change to the router and SERP files was in the working tree during this session and is not part of this commit.
- 2026-10-22 Return to Search from the Saved results view no longer reloads the SERP. Before, the SERP remounted and re-ran session, search (stored query, cached Primo, stored scores: no model call expected) and logged the same results as shown again. Now `/serp` and `/saved` share one route and component and the SERP stays mounted (hidden) under the saved view; saved-view chip changes update the SERP's saved state. Telot asked for this.
- 2026-10-22 End Session added (Telot): a text button under "Add search direction" on the SERP ends the session and opens Your sessions. **Reverses 2026-10-18 "a session ends only by the idle gap".** Only the per-direction check-out stays removed. An ended session is never reused (next search starts a new one). Backend `POST /api/sessions/:id/end`; if Your sessions derives "ended" only from the idle gap, it should also treat `endedAt` as ended (the New tag).
- 2026-10-22 Plan Workspace: the "What I want to find" field is removed (Telot). The LLM now gets only the search goal and What I already know (calls 5.1, 5.2 and 5.6; `wantText` is gone from the Workspace model, the generate and plan endpoints, prompts and fixtures; old stored values are ignored). A visible heading "Set your search goal" sits above the first field. Updated F1, F2, F4, 02-data-model, 03-api, stack_changed, design README. **Reverses the three-field plan in F1.** Backend 301 and frontend 333 tests pass.
- 2026-10-22 SERP console timing (Telot): every list load prints one console line per step (1 query, 2 Primo, 3 scoring) with the browser round trip and the whole load. The server measures each step and returns `timings` in the search and scores responses (`frontend/src/features/mindsSerp/serpTimings.js`). Numbers only, no participant text; cost is a few clock reads and about 100 bytes per response.
- 2026-10-22 Plan Workspace "Generate more" (Telot): call 5.1 now asks for `DIRECTION_COUNT` 16 (was 8, schema accepts 8 to 20); the list shows the first 8 and the rest wait in page state as a reserve; the button adds one per click from the reserve, or makes one more 5.1 call when it is empty or the texts changed. `GENERATE_LLM_TIMEOUT_MS` 12 s to 30 s. Measured 2026-10-22 (2 runs per size, noisy): latency is mostly fixed provider time, so a batch costs little more than one direction. Reserve is not saved (reopening the page starts with none). Untested: how good the labels 9 to 16 are.
- 2026-10-22 Plan Workspace "?" (Why?) opens the rationale in a floating popover card (MUI Popover: arrow to the "?", close cross top right, Esc and outside click close) instead of expanding the row (Telot). Plan Workspace only; the SERP and Your sessions "?" buttons are unchanged until Telot says otherwise.
- 2026-10-22 All search directions are editable on Plan Workspace (Telot), not only custom ones. Choice made without asking: editing an AI direction's wording turns it into a custom one (same slot and tick; `source: custom`, no kind or rationale), because its "why" explained the old words and rule 4 says the model is a first draft; regeneration then keeps it like any custom direction. Unchanged confirm = no change. AI directions still cannot be removed (untick them). Say so if an edited AI direction should keep its "?".
- 2026-10-22 Plan Workspace direction cards follow Telot's four-state sheet: blue border and tint when selected, dark border and white when not; every direction (AI too) has Edit and Remove; the "?" is a round badge on the top-right corner shown on hover. **Reverses 2026-10-22 "AI directions cannot be removed".** Added without being asked: the badge also shows on keyboard focus and always on touch screens, because hover alone would hide the explanation from keyboard and touch users (accessibility.md).
- 2026-10-22 Direction card strokes thinned (Telot): 1px, unselected uses the text fields' grey outline, selected stays blue; the 2px dark stroke of the states sheet looked too heavy next to the Search goal field.
- 2026-10-22 The "?" badge moved from the top-right corner to the middle of the card's right edge (Telot): on the corner it covered the card above.
- 2026-10-22 "Add Search directions" moved from below the list to beside "Generate more" under the heading (Telot); Generate more has a sparkle icon, Add has a plus, same outlined style, Add in black. The inline field now opens under the heading row (not below the list), my choice so it appears next to the button. The sparkle is a button icon, not an AI-direction marker (that stays removed, 2026-10-21).
- 2026-10-22 Generate more icon is one outlined star (MUI StarBorder), not the multi-sparkle AutoAwesome (Telot).
- 2026-10-22 Generate more icon is now a Gemini-style four-point gradient star (`GeminiStarIcon` in DirectionRow.jsx), replacing StarBorder (Telot). Still on this button only; it does not mark AI directions.
- 2026-10-22 The "Add Search directions" button is now labelled "Add Custom" (Telot, edited in the code); tests and F1 follow. It was swept into the star-icon commit by mistake, not by design.
- 2026-10-22 One four-step type scale for every MINDS screen (`TYPE_SCALE` in theme/designTokens.js, re-exported from uiTokens.js): title 2rem, heading 1.5rem, body 1.2rem, caption 1rem. Replaces the 0.8 to 2.2rem mix on Plan Workspace, SERP, Your sessions and Saved results; result title/metadata/abstract/link tokens and button/input/chip sizes follow it (Telot).
- 2026-10-23 Workspace Overview header sits in one bordered panel like Plan Workspace (Telot). SERP "Directions you have explored" bars use the Overview's session colours: current session near-black, the one before slate, older light grey with an outline; rank counts all sessions (Telot).
- 2026-10-23 Saved results opened from the Overview carries router state `from: "overview"`: "Return to Search" goes back to the Overview and the disabled search box is hidden. From the SERP nothing changes (Telot).
- 2026-10-23 A session tile shows a chip for every direction with saves in that session, even with no recorded query or shown list for it (`buildSnapshot`). Chips come first from visits, then these, placed by first save.
- 2026-10-23 README.md replaced: MINDS description, simple install steps, a classroom-style walk through the flow (workspace to Saved results), short developer notes. Baseline's README text is gone (Telot).
- 2026-10-23 A running session (newest, last activity within SESSION_GAP) shows a breathing primary-blue dot and "Running" above its minutes on its Overview tile; the dot stops animating under reduced motion (Telot).
- 2026-10-24 Plan Workspace: directions number row by row (1 left, 2 right, ...); Generate more / "or" / Add Custom move into the next free list cell, card height, and Add Custom expands the input in place while Generate more shrinks to a square star; the "N of 7 words" text is screen-reader only (Telot).
- 2026-10-24 A new custom direction starts unticked, like the AI suggestions; the student ticks it (Telot).
- 2026-10-24 + New Workspace has no naming modal (CreateWorkspaceDialog deleted): it creates "Untitled workspace" (numbered if taken) and opens Plan Workspace directly; rename with Edit Name in the list (Telot).
- 2026-10-24 SERP: the Search Direction dropdown is removed. Each direction in the right panel has a search icon that writes its stored query (generated once on first selection) in the search box only; no Primo call until the student presses the search icon in the search box. New endpoint `POST /api/sessions/:id/query` (Telot).
- 2026-10-24 SERP: the direction search icon changes only the search box; the results section keeps the last search until the query is sent (Telot).
- 2026-10-25 SERP search box: "Query generating" while 5.2 runs; the query is then typed out letter by letter (also for stored queries, on every pick), the cursor is placed in the box, caret is primary blue; reduced motion shows it at once (Telot).
- 2026-10-25 Overview: the right column is headed "Directions" with tabs All / Explored (sliding pill) that filter the Selected Directions list; the Explored tab renames the headings to "Explored Directions" and "Unexplored directions" (Telot).
- 2026-10-25 Overview: unticked directions get cards under an "Unselected directions" divider; the arrow on every card is replaced by a tick circle (solid blue when selected, outlined grey with a blue sky-blue hover when not) that toggles the selection and moves the card (new endpoint `PATCH /subgoals/:subGoalId`; the last selected cannot be unticked) (Telot).
- 2026-10-25 Overview: "+ Add search direction" is replaced by Plan Workspace's Generate more / Add Custom (shared `GenerateOrAddBar`); both store the new direction unselected. `PATCH /subgoals` accepts `selected`, `source`, `kind`, `rationale` (Telot).
- 2026-10-25 The "Custom" text tag is replaced by a round user icon on the Overview and on Plan Workspace, after the direction name (Telot).
- 2026-10-25 Overview: the Session tab is removed; only All and Explored for now (Telot).
- 2026-10-25 Overview: the Explored tab splits ALL directions by record (explored above, unexplored below, selected or not), so a ticked direction with no record shows under Unexplored directions; the All tab still splits selected / unselected (Telot).
- 2026-10-25 SERP: a direction added on the page has no score on the cards already shown; every card gets a "?★" chip for it before ">>", its "?" says to press the direction's search icon and then search to get scores (Telot). Promoted directions follow the same rule on cards with no score for them.
- 2026-10-25 SERP chips: no "Best on page" text and no sky-blue accent; the best chip looks like the others with a blue score and star only (accessible name keeps "best match on this page") (Telot).
- 2026-10-25 Plan Workspace: "+ New Workspace" opens Plan Workspace with the workspace name field already open and empty; its hint "Type Workspace name here" is typed out like a SERP query (shown at once with reduced motion). The name field is wider (440px). The router state is cleared after the first render so a refresh does not reopen it (Telot).
- 2026-10-25 Plan Workspace: the screen-reader-only helpers used `width: 1` (MUI = 100%), which caused a sideways scrollbar; now 1px.
- 2026-10-25 Saved results view: a right panel lists the directions that have saved results (plain counts, "All directions" first); choosing a name filters the list to that direction in place (Telot). Replaces "right of the list stays empty" (F6).
- 2026-10-25 Saved chips: the text "Saved" is removed (SERP and Saved results view); the solid blue fill and the check icon stay, the accessible name still says "saved" (Telot).
- 2026-10-25 Your sessions: session tiles show pills only for directions with 1+ saved (no "0 saved" or "+0" pills); F5 and accessibility.md updated (Telot).
- 2026-10-25 Your sessions bar: full at 10 saved (BAR_CAPACITY, was grow-to-largest); beyond 10 the newest session segment shows only what fits and "+N more" sits at the end of the bar, e.g. 18 saved with 9 in the newest = +9, +1, +8 more (Telot, from the professor).
