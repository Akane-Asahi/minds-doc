# Open questions and assumptions

Move an item to DECISIONS.md only when Telot confirms it. Telot's latest statement is the decision;
if a mockup or message conflicts with the spec, say so and update the spec.

## Needs a decision

1. **LLM provider for the study, and budget.** Development provider decided 2026-10-19: Gemini `gemini-3.5-flash-lite`,
   prepaid/free tier, **made-up data only** (a free tier may use prompts to improve the provider's products). The
   provider for the study is still open and the ethics application must name it (participant text goes to a third
   party). Provider and model are environment variables behind one module (`backend/llm/`), so it can change.
2. **Logging and study data (F7).** Event list, ethics coverage, Baseline's original event names,
   retention, whether prompts/outputs are stored.
3. ~~`SavedDoc` vs `savedresults`~~ **Decided 2026-10-19:** keep `SavedDoc`, add `savedresults` link rows (02-data-model.md).
4. **Non-colour cue for light-blue and solid-blue chips.** A second cue is required (accessibility); the
   exact one is **not chosen. Leave as is for now** (Telot, 2026-10-16).
5. **Route names** for the new screens (`/workspace/:id/...`): align with Baseline's router.
6. **Hosting** for the study deployment. Baseline ships an nginx config; decide when deploying (stack_changed.md).

7. **Reopening Plan Workspace (for I7).** A workspace created before I1, or one whose participant left Plan Workspace before
   pressing Explore, has no directions yet and opens the SERP. I7 should send a workspace with no directions back to
   `/workspace/:id/plan`. A way back now exists: clicking a workspace in the list, and the menu item **Edit Workspace**, both open the plan page (2026-10-19). Automatic reopening elsewhere (for example from a SERP link) is still I7.

8. **Keyboard reordering of search directions.** Mouse and touch drag are built; there is no keyboard path (dnd-kit's keyboard sensor
   needs insertion-point code). Options: add a small coordinate getter for the keyboard sensor, or accept that order is optional.
   Recorded in accessibility.md and STATUS.md; decide before the study.

9. **Replacing a plan once results are saved: decided and built (2026-10-21).** "Update workspace" no longer deletes and re-inserts directions. Each direction in the
   new plan that matches an old one by label (case-insensitive) is **updated in place**, so its `_id` (and its saved results, stored query, scores, sessions) survive.
   An old direction the new plan no longer lists is deleted **unless it has saved results**: then it is **kept, unselected**, after the new ones (not searched, still on
   Plan Workspace to tick again), and the response lists it in `keptSubGoalIds`. Chosen over blocking the removal or asking, because a save must never be lost and the
   participant can always see and re-tick it. Still open: whether Plan Workspace should say that a removed direction was kept (it simply reappears unticked).
   Orphaned `queries` and `resultscores` of a deleted direction are left in place (harmless).

## Assumptions (defaults used; change if wrong)

- Scoring rubric anchors (5 main topic, 4 substantial, 3 partly, 2 in passing, 1 tangential, 0 unrelated)
  and temperature 0 are used as written; validate empirically (item below).
- A stored new direction stays after unsaves until dismissed or promoted.
- Detection may suggest at most 3 directions at a time; "page" means the batch of 10 scored together.
- Plan Workspace: AI suggestions start unselected; AI directions carry no tag and no fading;
  all of them are new to the student (Orland, 2026-10-21); `DIRECTION_COUNT` about 8.
- First search runs automatically when the SERP loads; default direction = first selected in Screen 1 order.
- Your sessions is mockup-exact (2026-10-17). Open: where **Start New Workspace** lives (Workspaces list assumed).
- Saved results view: the Back control, scope heading and score ordering are proposals.
- Primo: abstract availability, quota and maximum page size not yet confirmed.

## To measure or schedule

- **Latency** of scoring a page of 10: measured 2026-10-19 with the Gemini dev model on mock metadata, **3.5 to 6 s per call**
  (call 5.1: 1.6 to 2 s). Repeat with a real Primo response in I2.
- **Scores are not repeatable** even at temperature 0 (2026-10-19 smoke test: 5 to 20 of 70 scores changed between identical
  runs; call 5.1 returned completely different labels each run). So scores are stored once and never re-requested.
- **Scoring validation:** compare LLM scores against an embedding baseline using two raters on about 60
  results (Phase 3 threshold validation; not scheduled). Expect Orland to challenge LLM-only scoring.
- **Re-measure contrast** on every new mockup.
- **Light-blue chips** and the **`>>` icon-only button**: test whether participants understand them.
- **Duplicate new-direction labels:** watch for near-duplicates in testing; add embedding matching only if they appear.
