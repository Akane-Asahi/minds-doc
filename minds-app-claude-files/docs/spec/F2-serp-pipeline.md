# F2 SERP pipeline: search controls, query (5.2), scoring (5.3), ranking

**Problem it solves:** a participant with dyslexia cannot easily tell which results fit which
part of the task, and writing good queries (spelling, wording) is hard. The system writes a query
per direction, fetches results, and scores each result against every direction so ranking and
chips reflect the active direction.
**Challenges it answers:** query formulation; telling relevant from non-relevant; unsure results
are good enough.
**Load with:** 01-core.md, 03-api.md (search, reasoning), 04-primo.md. Card UI is in F3.
**Depends on:** F1 (workspace and directions exist). Primo proxy exists in Baseline.
**Status:** backend built (I2, 2026-10-20; frontend wiring is I3): Primo service and cache, call 5.2 stored query, call 5.3 batched scoring, ranking, sessions, `POST /api/sessions/:id/search`. Frontend built in I3 (2026-10-21, see "As built (I3)"). Not built yet: the real Primo and LLM end to end check (script written, not run), page-2 prefetch (deliberately not done, see below), new-direction scoring is built (I4: suggested directions are scored with the selected ones, F4). Route: `/workspace/:id/serp` (optional `?direction=<id>`).

## Search controls (SERP main column)

**Search field.** Shows the active direction's query with a search icon (a real button). It is
**editable**.
- On arrival and on each direction change it shows that direction's **stored query**: the newest `queries` row
  for it, which is the 5.2 query (generated once, on the direction's first selection) until the participant
  submits a typed one, then that typed query. Switching never calls the LLM again (**stored query rule**, below).
- Submit (Enter or the icon) sends the text to Primo **exactly as typed**
  (`POST /api/sessions/:id/search` with `queryText`; 5.2 is not called), then scores and ranks the
  new pool for the active direction. Stored as a `queries` row with `source: 'user'`. The
  Results count updates.
- Empty submit does nothing. Blur does not search; only explicit submit does. A typed query
  applies to the active direction only.

**Meta bar.** Left: `Results: N` (Primo's total hit count, `totalHits`); informational only,
never a denominator for anything. Right: **Search Direction** dropdown.

**Search Direction dropdown.** Options = all selected directions in `orderIndex` order; the first
is selected on arrival. Choosing another reuses its stored query, or generates it (5.2) if this is the first time
that direction is selected, then searches Primo, scores, and re-renders the field, count and list (skeleton cards while loading).
Lists already loaded this session are kept, so switching back is instant. Switching never changes
saved results or the right-panel counts. Keyboard-operable (native `<select>` or accessible
listbox).

## Ranking flow (per search)

**On arrival** the SERP automatically searches the **first selected direction only** and shows the
loading state until results return (first search runs without a click; assumed default, see
open-questions.md).

1. Get the active direction's stored query; generate it (5.2) only if the direction has none yet.
2. Fetch a pool of `CANDIDATE_POOL_SIZE` (10) from Primo, merge, dedupe.
3. Score the whole pool in one batched call (5.3) against every selected direction and every
   suggested new direction (skipping pairs already in `resultscores`).
4. Sort by the **active direction's score**, highest first; ties by Primo's original order.
   New directions play no part in ranking.
5. Render. Cards already on screen never reorder.

Ranking orders a pool of 10, not all N hits (a better match at Primo position 11 is not pulled
up; the main value is the direction chips). **Load more:** when the participant reaches the end of
the list, fetch the next pool with `cursor`, score and rank it the same way, append below.
**Prefetch:** while the participant reads page 1, fetch and score page 2 in the background so it
appears instantly. Measure real time-to-first-ranked-list with a real Primo response and the chosen
model before changing the pool size (latency not yet measured).

## Call 5.2: query generation (one direction at a time)

**Stored query rule (Telot, 2026-10-18).** The LLM writes a direction's query **once**, the first time that
direction is selected (the first selected direction on arrival, or the first switch to another one). The query is
stored in `queries` (`source: 'ai'`) and reused every time after that: switching back, returning in a later
session, opening the direction from Your sessions, Continue Last Activity. It is **never regenerated**, because
(1) generating takes tokens and time, and (2) the LLM can word the same direction differently each time, which
confuses a participant who is relying on seeing the same phrase. A typed query is stored as another row
(`source: 'user'`); the newest row for a direction is the one shown, and the AI row stays stored.

**Input:** `goalText`, `knownText`, the direction's label. Nothing else (no query history, no saved
titles: there is no "better query" regeneration).

**Output:** `{ "query_text": "string" }` sent to Primo as-is and shown in the search field.

**Query length (2026-10-22):** 2 to 4 plain keywords (never more than 5). Primo's keyword search returns only records that contain every word, so a long query that mixes the direction with several parts of the goal finds nothing (seen: 4 of 7 queries of 5 to 7 words returned 0 hits). The query starts from the direction's own words, adds at most one single anchor word from the goal (usually "dyslexia"), and never takes words from `already_know` or `want_to_find` that the direction does not name.

## Call 5.3: result scoring (batched, one call per search)

Batching is a cost and latency requirement. Primo is the first-stage retriever; the LLM is the
second-stage judge. Scoring uses the LLM, **not embeddings** (embedding similarity measures topical
closeness, not whether a result helps a direction; short labels embed poorly; per-set calibration
forces a spread even on a weak page).

**Input:** selected directions (id + label, in `orderIndex` order), the active direction id,
stored suggested new directions (id + label), and for each result: title, authors, venue, keywords,
abstract/description, resource type, and `known_scores` (scores already stored for that result,
read-only context). Only pairs **without** a stored score are scored. Primo metadata only.

**Casing:** LLM JSON uses snake_case as shown in the schemas; the server maps it to camelCase for the
API and Mongo.

**The model:**
1. Scores every result against **each selected direction and each suggested new direction**, whole
   numbers 0 to 5, using an absolute anchored rubric: 5 = the result's main topic is this direction;
   4 = a substantial part of it; 3 = relevant but only partly; 2 = mentioned in passing; 1 =
   tangential; 0 = unrelated. Temperature 0. **A score is 0 unless the metadata names or clearly addresses the direction's
   topic** (a shared general word such as "community" or "access" is not enough).
2. Writes one reasoning sentence (about 20 words max) **only for the chips a card will show**. The
   model ranks each result's directions using the new scores **plus `known_scores`**, then writes
   reasoning for the newly scored pairs that fall in the result's top `CHIP_COUNT` selected directions
   **with a score above 0** (ties: earlier in the given order), or that are its highest-scoring suggested
   new direction (score above 0). Every other newly scored pair has no `reasoning` (the model leaves the field out; the server stores null). Pairs already
   stored keep their stored reasoning (text or null).
3. Each reasoning must rest on something actually in the record's metadata (a phrase from the
   abstract, subjects or title) and may not add claims the metadata does not support.
4. If a record has no abstract, scores from title and subjects, sets `low_confidence: true`, and begins
   each reasoning with "Based on title and subjects only".

**Output schema (validate with Zod):**
```json
{ "results": [ {
    "result_id": "string",
    "low_confidence": "boolean",
    "scores": [ { "sub_goal_id": "selected or suggested new direction id",
                  "score": "integer 0-5",
                  "reasoning": "one short sentence; the field is left out when there is none" } ] } ] }
```

**Ids on the wire (2026-10-21):** the model is given short opaque ids (`d` or `r` plus 6 hex characters, `utils/shortIds.js`) for directions
and results and answers with them; the server maps them back before storing. Reason: a mistyped 24-character database id counted as a
missing score and failed the call. The ids must not be ordinal (`d1`, `d2`): that made the model score noticeably higher (DECISIONS 2026-10-21).
A failed check is logged with fixed phrases (`missing direction score`, `unknown direction id seen`, ...), never ids or values.

**Scores are not repeatable** (measured 2026-10-19: even at temperature 0, 5 to 20 of 70 scores changed between identical runs),
so a stored score is final and is never re-requested; only unscored pairs are ever sent.

**Server after the call (plain code, not the LLM):** floor any decimal and clamp to 0 to 5 so a
malformed value never reaches the screen; store scores in `resultscores`; build each card's pills
(F3). Stored scores are reused if the same result appears under another direction's query, so a
result never gets two scores for the same direction. Only unscored pairs are sent.

**Reasoning on demand:** when `?` is tapped on a chip whose reasoning is null (for example one
revealed under `>>`), call `POST /api/workspaces/:id/results/:resultId/reasoning`; the server
generates one sentence from the stored score and the record's metadata, stores it and returns it.
If the result is `low_confidence`, the text shown starts "Based on title and subjects only".

## States

| State | Behaviour |
|---|---|
| Loading (first load, direction switch, load more) | skeleton cards with the same structure as a real card; container `aria-busy="true"`; live region "Loading results", then the new result count |
| No results | message that this direction returned nothing, hint to try another direction |
| Primo error | inline error with Retry; already-loaded lists and saved counts stay visible |
| Scoring error, Primo OK | show results in Primo's original order without chips, a message that they could not be ranked, and Retry |

## As built (I2)

- **Order of work in `POST /api/sessions/:id/search`:** touch the session (active time, active direction) -> query (typed as typed, else the
  stored one, 5.2 only if none) -> Primo (cache by normalized query + paging) -> score the pool -> rank -> log `sessionresults` -> read saved state.
- **`cursor`** is the Primo offset to start from (a string of digits); `nextCursor` is `null` on the last page. `totalHits` is stored on the
  query row from the first page only.
- **Response:** `queryText`, `queryGenerated`, `activeSubGoalId`, `totalHits`, `scored`, `results` (each with `rank`, Primo `abstract` or `null`,
  `lowConfidence`, `scores` for **every selected direction in `orderIndex` order**, `savedSubGoalIds`), `savedCounts` per direction (derived from
  `savedresults`), `suggestions` (always `[]` until I4), `nextCursor`. The card's default pills (top 3, `>>`) are chosen in the frontend from `scores` (F3).
- **Failures:** Primo -> 502 `PRIMO_UNAVAILABLE`; the query could not be written -> 502 `QUERY_UNAVAILABLE` (nothing stored, the next selection tries
  again; the participant can type a query); scoring -> 200 with `scored: false`, Primo order, `scores: []`. Never a 401 or 403 from a provider.
- **Scoring batch:** only results that lack a stored pair are sent; each carries `known_scores` and `score_directions` (the ids to score). A stored
  score is never overwritten (upsert with `$setOnInsert`). A result with no abstract is forced to `lowConfidence` and its reason is prefixed
  "Based on title and subjects only." even if the model forgot.
- **One `ai` query row per direction** is enforced by a unique partial index, so two quick first selections cannot generate twice.
- Sessions are created by `POST /api/workspaces/:id/sessions` (get or create). I5 builds the overview and the rest of F5 on the same service.

## As built (I3, frontend: `frontend/src/features/mindsSerp/`)

- **Route** `/workspace/:workspaceId/serp` (protected; Plan Workspace's Explore goes here). The Baseline SERP at `/workspace` and `features/search` are untouched (the control); `/ui/serp` still runs on fixtures. The page loads the workspace and `GET /plan` (selected directions only, `orderIndex` order; none selected: a message and a link to Plan Workspace).
- **Data:** every search is `POST /api/sessions/:id/search`, preceded by `POST /api/workspaces/:id/sessions` (get or create, so a session that idled out starts a new one). Baseline's Primo fetch is not used. `MindsSerpContext` is provided by `useLiveSerp` with the same value the chips and panel read from the fixture provider.
- **Arrival** searches the first selected direction (or `?direction=` if it is selected) with no `queryText`: the stored query. Choosing a direction searches it once (stored query, or 5.2 on its first selection); its list is kept, so switching back is instant and calls nothing. A typed query goes as `queryText` exactly as typed (trimmed; an empty submit does nothing; blur never searches) and replaces that direction's list. The chosen direction is kept in `?direction=`.
- **States:** skeleton cards with `aria-busy` and the live text "Loading results", then `Results: N.`; Primo or query failure: inline error with Retry (saved counts stay, they come from the session call); scoring failure (`scored: false`): the list in Primo order, no chips, a notice with Retry; no results: a message.
- **The list first, the scores second (2026-10-21).** Measured: scoring (5.3) was about 72% of the wait for the first cards (6.9 s of 9.6 s with 8 directions; the library alone about 0.9 s). The page now sends `scoring: "later"`, so the search answers when Primo has the list; the cards show at once in the library's order with **loading chips** (grey placeholder shapes in the chip row, wave animation off under `prefers-reduced-motion`, hidden from screen readers; the page's live region says "Scoring the results against your search directions."). The page then calls `POST /api/sessions/:id/scores` for those results; the chips replace the placeholders and the list is **ordered once** by the active direction (live region: "Scores are ready. Results ordered by <direction>."). A "Load more" batch only reorders itself, so cards already read never move. A pool whose pairs are all stored arrives scored at once (no placeholders, no second call). Scoring failure: the cards stay in the library's order with the ranking notice and Retry. Logged "reviewed" ranks (`sessionresults.rank`) are the library's order at the time of showing.
- **Load more** is a button at the end of the list ("Load more results"): the next pool (`cursor`) is appended below, cards on screen never reorder, a pool that repeats a result adds only the new ones. **Page-2 prefetch is not done**: the search endpoint logs the results it returns as shown (`sessionresults`, "reviewed"), so fetching page 2 in the background would count results the participant never saw, and would spend a scoring call on a page they may never open.
- **Counts** in "Directions you have explored" are the server's per-direction counts and per-session segments (search, session and save responses); a save or unsave updates them at once and the server's numbers then replace ours.
- **An added direction** (see F3) has no score on lists loaded before it was added, so it shows no chip there (not a made-up 0); results loaded after it carry its score. Switching to it searches it like any direction.

## Acceptance criteria

- One Primo call and one scoring call per search; zero scoring calls when every pair is stored.
- Scores returned as 2.7 become 2; 9 becomes 5; -1 becomes 0 (server enforced).
- A user-typed query skips 5.2 and is stored with `source: 'user'`.
- 5.2 runs at most once per direction: selecting a direction a second time, in the same or a later session, or from
  Your sessions, makes no LLM call and shows the same query.
- Ranking uses the active direction's score only; ties keep Primo order; new directions never
  change order.
- A result with no abstract is flagged low confidence and its reason says so.
- Switching direction twice reuses the stored query and loaded list; no extra Primo call.
- Page 2 prefetch does not delay page 1; cards on screen never reorder on load more.
- The first cards show without waiting for scoring: chips are loading placeholders until the scores arrive, and the list is ordered once, then.
- Scoring failure degrades to Primo order with a Retry; Primo failure keeps saved counts visible.

## Out of scope

Embedding-based scoring; full-text fetching; categorical badges (deferred).

*Source: old spec 4 (use), 5.2, 5.3, 8.2 (search field, meta bar, dropdown, ranking, latency, states).*
