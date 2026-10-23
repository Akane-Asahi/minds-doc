# STATUS.md

Read this first in every session. Update it at the end of every session (done / next / blocked).
Last updated: 2026-10-22 (I5 Your sessions wired).

## Where we are

Planning and context setup are done. The repo started as the Baseline code (React 18 + MUI v5 +
Express + Mongoose); no MINDS feature code exists yet. The spec is split into `docs/spec/`.

## Done

- Decisions A1 to A4 settled; repo created; Primo access works (Baseline uses it).
- U0: typed fixtures (`frontend/src/mocks/`), dev-only `/ui` index and per-screen state switcher
  (`frontend/src/ui-dev/`), contrast test (`npm test` in `frontend/`). `/ui` exists only in development.
- U1: Plan Workspace UI at `/ui/plan-workspace` (`frontend/src/features/planWorkspace/`), all four states
  plus long text and many items; 10 render tests and the new contrast pairs pass. Not yet looked at in a
  browser (no browser tools in that session): check it against `docs/design/01-plan-workspace-*.png`.
- U3: Your sessions UI at `/ui/sessions` (`frontend/src/features/yourSessions/`), rebuilt 2026-10-17 exactly as
  `03-your-sessions.png` (Workspace Overview: header, breadcrumb, Continue Last Activity, three summary cards,
  SESSIONS pills, direction cards with bars, New tag, Add search direction). States: default, returned (New tag
  gone), none, one, many, twentySaves, longNames, loading, error. Model tests and render tests pass. Checked in
  headless Chrome against the mockup; not yet checked with a screen reader or keyboard by hand.
- I0: LLM client (`backend/llm/`, Gemini over REST, structured output, one retry, safe errors and logs), Zod schemas for
  calls 5.1 and 5.3 (`backend/schemas/`), Mongoose models `SubGoal`, `SavedResult` and the three Workspace texts, backend Jest +
  Supertest (31 tests), `server.js` exports `configureApp`. `node backend/scripts/smoke-llm.js` passed 8 of 8 calls with the real
  model; scores are not repeatable at temperature 0, so they are stored and never re-requested (DECISIONS.md 2026-10-19).
  Not built (moved to I1): rate-limit factory, React Query provider, the `/generate` route.
- U4: Saved results view at `/ui/saved-results` (`frontend/src/features/savedResults/`): all sessions grouped by session, one direction, one session, both; SERP header in saved mode, three counts, grey and solid chips, empty/loading/error. Reached from Your sessions in `/ui` (button, tiles, circles, segments). Model and render tests pass; not yet checked by keyboard or screen reader.
- I1: Plan Workspace is wired (status "wired" in F1: not yet checked in a browser). Flow: Create New Workspace dialog (Baseline) ->
  `/workspace/:workspaceId/plan` -> blur generation (`POST /api/search-directions/generate`, per-user rate limit) -> Explore
  (`PUT /api/workspaces/:id/plan`) -> Baseline SERP. React Query added. Backend 70 tests, frontend 185 tests pass. Startup warning
  for a Baseline-looking database name. See DECISIONS.md 2026-10-19 (I1).
- I1 follow-up: drag and drop reordering of search directions on Plan Workspace (F1 "Reordering"): fixed slot numbers, black insertion line,
  grey end slot, regeneration keeps selected/custom cards in their slots, new batch held during a drag. Frontend 209 tests pass; real
  pointer dragging not yet checked in a browser. **Known gap: no keyboard reordering** (accessibility.md, open-questions.md 8).
- I1 follow-up: a workspace that already has a plan offers "Open workspace Or Update workspace"; Update loads the saved plan and Explore replaces it
  (`replace: true`, one transaction; `GET /plan`). Backend 80 and frontend 222 tests pass.
- I1 follow-up: Workspaces list menu has **Edit Workspace** (opens the plan page; the Open/Update row shows at the top for a workspace that already has a plan). Frontend 225 tests pass; the menu item itself has no automated test (check by hand).
- I1 follow-up: clicking a workspace on `/workspaces` opens its Plan Workspace page (not the SERP); Open workspace there opens the SERP. No automated test for the list click (check by hand).
- I1 follow-up: a workspace with a plan now shows the full saved plan by default (no click on Update); an unchanged Explore writes nothing. 228 frontend tests pass.
- I2: search pipeline, backend only (F2 "As built"): Primo service with 24 h cache and `resultscache`, call 5.2 stored query (one `ai` row per direction),
  call 5.3 one batched call for unscored pairs only, ranking by the active direction, sessions (`POST /api/workspaces/:id/sessions`, SESSION_GAP, capped active
  time), `POST /api/sessions/:id/search`. Backend 136 tests (no network). Run against real Primo and Gemini on 2026-10-21 (`scripts/smoke-pipeline.js`: works after the scorePool fix, DECISIONS 2026-10-21); the Primo record shape is taken from
  Baseline's `pnx` fields and mocks, and whether records carry abstracts is still unmeasured (04-primo.md). No frontend change; U2 is still open.
- I1 follow-up (2026-10-21): Explore saves all directions with a `selected` flag; unticked ones return unticked on Plan Workspace. Backend 138 and frontend 233 tests pass. **I3/I4/I5 must list only `selected` directions** (the I2 search already does); not checked in a browser.
- Update workspace keeps saved results (2026-10-21, open-questions 9 closed): ids survive, a dropped direction with saves is kept unticked. Backend 164 tests.
- I3 backend (2026-10-21): `POST/DELETE /api/results/:id/save`, `POST /api/results/:id/open`, `POST /api/workspaces/:id/results/:resultId/reasoning`, `PATCH /api/workspaces/:id/subgoals` (add), saved counts and per-session segments on the session, search and save responses (03-api.md). Backend 171 tests (no network).
- **U2 / I3 frontend (2026-10-21): the live MINDS SERP** at `/workspace/:id/serp` (`frontend/src/features/mindsSerp/`), fed by the MINDS endpoints only (F2 and F3 "As built"). Done: search on arrival, stored query reuse, typed query, direction switch with kept lists, chips from real scores, optimistic save/unsave with rollback message and live region, server counts and bar segments, `?` reason on demand, title click marks opened, load more, F2 states, Add search direction. Reviewed by an independent subagent against F3 and the 7 rules (DECISIONS 2026-10-21); its three findings are fixed. Frontend 271 tests pass. **Not checked by hand: a browser, keyboard use, a screen reader, the real backend, Primo or model** (everything above is jsdom with a mocked API). **Not done:** page-2 prefetch (reason in F2), promote / dismiss / New pill (I4, still mock), Saved results view and header toggle (I6, still mock), chips write only `savedresults` so Baseline's saved list does not show them (DECISIONS 2026-10-21).
- **SERP speed (2026-10-21):** the cards now show as soon as Primo answers, with loading chips, and scores arrive in a second call (`POST /api/sessions/:id/scores`); the first page is re-ordered once when they do (DECISIONS 2026-10-21, **Telot to confirm the re-order**). Measured before the change by the perf suite (`backend/scripts/perf-serp.js`, report in `perf-report/`, untracked): scoring was about 72% of a 9.6 s first visit. Backend 178 and frontend 281 tests pass. **Not timed again and not checked by hand: a browser, keyboard, screen reader, the real backend.**
- **Call 5.3 failure and speed (2026-10-21):** the intermittent "validation" failure was a mistyped 24-character id; the model now gets short opaque ids and no `null` reasoning (DECISIONS 2026-10-21). Scoring median 10.0 s to 7.4 s, 0 failures in 10 compare runs (earlier about 1 in 6 on the first try). `npm run compare` now shows the Primo call and save/map separately (save/map is a steady ~190 ms; the Primo call is what Baseline waits for). New `npm run bench:scoring` (fixed set, noise-aware accept rule). Backend 215 tests pass. **Not done:** the scripts `perf-serp.js`, `smoke-pipeline.js` and `smoke-llm.js` still build their own 5.3 prompt with database ids (their 5.3 timings are the old, slower format); scores vary a lot between identical runs (see DECISIONS), which is a study-validity question for Telot and Orland, not fixed here.
- **I6 (2026-10-22): Saved results view is live** at `/workspace/:id/saved?direction=&session=` (`features/savedResults/SavedResultsPage.jsx`, `GET /api/workspaces/:id/saved`, F6 "As built"). Reached from the SERP header toggle, count circles and bar segments. Grouped by session, three plain counts, chip removal with undo into the original session (`sessionId` on save), `?` stored reason or one on-demand request, title links to the library record. Backend 233 and frontend 295 tests pass (mocked models and API). **Not checked: a browser, keyboard, screen reader, the real backend.** **Open:** "counts on Your sessions match after returning" (needs I5); the workspace-name crumb goes to the SERP until Your sessions has a route (I7); no independent subagent review of this diff yet.
- **I4 (2026-10-22): new directions** (F4 "As built (I4)"). Backend: model `emergingdirections`, call 5.6 detection after a save (background, one run per workspace plus one follow-up, thresholds 3 distinct valid ids and relevance above 2, max 3 active, dismissed never recreated), suggestions scored with the selected directions in call 5.3 (never used for ranking), `POST /api/emerging-directions/:id/promote` and `/dismiss`, save and `?` reason accept `emergingDirectionId`. Frontend: the live SERP shows the real rows of "What you might explore" (`+` promote, `×` dismiss, "?" why) and the New pill; a New pill click adds the direction and saves in one step. Backend 285 and frontend 314 tests pass (mocked models and API). **Not checked: the real model for call 5.6 (no smoke run yet, so label quality and how often topics recur are unknown), a browser, keyboard, screen reader.** **Telot to confirm:** the extra "?" on each suggestion row (DECISIONS 2026-10-22). Independent subagent review done (see DECISIONS).
- **I5 (2026-10-22): Your sessions is wired** at `/workspace/:id/overview` (`features/yourSessions/YourSessionsPage.jsx`, `GET /api/workspaces/:id/overview`, F5 "As built (I5)"). Stored rows, derived on the page; New tag via `subgoals.addedInSessionId`. Backend 295 tests and the Your sessions frontend tests (61) pass (mocked). **Not linked from anywhere** (I7) and the route line in `frontend/src/app/router/index.js` plus the crumb line in `SavedResultsPage.jsx` sit in files that also hold someone else's uncommitted work, so they are not in the I5 commit. **Not checked: a browser, keyboard, screen reader, the real backend.**
- **Plan Workspace two fields (2026-10-22):** "What I want to find" removed end to end; the LLM gets only goal + already-know; heading "Set your search goal" added (DECISIONS 2026-10-22). Not checked in a browser.
- **Generate more (2026-10-22):** button beside "Search directions"; 5.1 asks for 16, shows 8, keeps 8 as a page-state reserve (F1 "Generate more", DECISIONS 2026-10-22). Not checked in a browser, and the quality of directions 9 to 16 is unmeasured.
- Directions are new-only (2026-10-21, Orland): call 5.1 returns only angles the student has not thought of; the server stamps `kind: 'new'`.
- Context system: `CLAUDE.md`, `docs/spec/` (per-feature files), `DECISIONS.md`, `stack_changed.md`,
  `docs/templates/feature-brief.md`.

## Next (in order; details in docs/spec/build-plan.md)

**Phase 1, UI with mock data:** all done (U2 SERP built on the Baseline copy, now also live).
(Each replaces its placeholder in `frontend/src/ui-dev/UIDevRoutes.jsx`.)
**Phase 2, interaction:** I2 done (backend; real-service check pending);
I3 done in code (check by hand); I4 done in code (check by hand, real-model check pending); I5 done in code (check by hand; needs the route lines above); I6 done in code (check by hand); I7 navigation between screens; I8 F7 logging.

Also before or alongside:
- Subagents: spec-reviewer and a11y-checker in `.claude/agents/`.
- Invariant tests for the 7 rules (01-core.md), starting in I0.
- Scoring validation plan and a latency measurement (open-questions.md).

## Blocked or needs Telot

- **Decide keyboard reordering** of search directions (not built; open-questions.md 8).
- `backend/.env` `MONGO_URI` points at `minds-dev` (checked 2026-10-21 with `node backend/scripts/show-db-name.js`: "looks like a MINDS database"; 5 small collections). Re-check before any manual try.
- **Real check written, not run:** `node backend/scripts/smoke-pipeline.js` (5.1, 5.2, one real Primo search, 5.3; counts and timings only; no database, writes nothing; invented task text). Run it to measure abstracts, time to first ranked list and the score spread.
- I7 must reopen Plan Workspace for a workspace with no directions yet (open-questions.md 7).
- Study LLM provider and budget (development uses Gemini on prepaid credit with made-up data only; ethics must name the study provider).
- Logging plan (F7): ethics coverage and Baseline's original event names.

## Notes

- Never commit `.env`, keys, database URIs or participant data (public repo).
- Use a separate MongoDB database from Baseline's study database.
