# F4 New direction detection (call 5.6)

**Problem it solves:** the participant's own saved results reveal a topic they did not plan but
keep finding. Surfacing it lets them widen the plan without having to notice the pattern
themselves (working-memory load), while keeping them in control of whether to adopt it.
**Challenges it answers:** new facets missed; hard to refocus after a tangent.
**Load with:** 01-core.md, 02-data-model.md (`emergingdirections`), F3 (where it appears).
**Status:** wired (I4, 2026-10-22): detection, promote, dismiss, New-pill save and the live SERP rows and pills (see "As built (I4)"). Backend 285 and frontend 314 tests (mocked models and API). **Not run against the real model or in a browser.**

## When it runs

In the background after a save (`POST /api/results/:id/save`), never in the search path, so it adds
no time to loading the SERP. Runs only when the workspace has at least `SUGGEST_MIN_COUNT` (3)
saved results. One run at a time per workspace; if more saves arrive meanwhile, run once more
afterward.

## Input

The Search goal and What I already know; the selected direction labels; every
existing new-direction label (including dismissed ones); and for each saved result: id, title,
keywords, abstract (Primo metadata only, no full text).

## What the model does

Finds topics that recur in **at least three different saved results** and are not covered by any
selected direction or existing new direction. For each it returns: a label (1 to 3 words, plain noun
phrase), the ids of the saved results it appears in, `goal_relevance` 0 to 5 (relevance to the
Search goal), and one sentence of reasoning.

**Label reuse (decided 2026-10-16):** the model is told to reuse an existing label **exactly**
where one fits. The server matches labels by **normalized text** (lowercase, trimmed, whitespace
collapsed). No embeddings. If testing shows near-duplicates (e.g. "green gentrification" vs
"gentrification near parks"), revisit then.

**Output schema (validate with Zod):**
```json
{ "new_directions": [ { "label": "string, 1-3 words",
                        "saved_result_ids": ["string"],
                        "goal_relevance": "integer, 0 to 5 (server floors and clamps)",
                        "reasoning": "one short sentence, about 20 words max" } ] }
```

## After the call (server code)

Keep a topic only if at least `SUGGEST_MIN_COUNT` (3) **distinct, valid** saved result ids support
it **and** `goal_relevance` is **strictly greater than** `EMERGING_GOAL_MIN` (2). Create an
`emergingdirections` row with status `suggested` (at most `SUGGESTION_LIMIT` (3) active at once)
and `timesSeen` = number of distinct saved results that mention it. Dismissed labels are never
created again. A stored topic stays until dismissed or promoted, even if results are later unsaved
(assumed; Telot to confirm). From the next search on, call 5.3 scores every suggested new direction
together with the selected ones, and F3 decides whether a card shows the New pill.

## Promote and dismiss

- **Promote** (row in "What you might explore", or clicking a New pill): create a `subgoal`
  (`source: 'ai'`, `suggestionKind: null`, next `orderIndex`), mark the emerging direction
  `promoted`, re-point its `resultscores` to the new `subGoalId`. It then appears in "What you have
  explored" and is scored as a normal direction.
- **Dismiss:** mark `dismissed`; never suggested again.
- Every suggestion is optional and dismissible in one tap, with its reasoning available (rule 4).

## Acceptance criteria

(All met in code and tests, 2026-10-22; none checked against the real model or by hand.)

- No detection run with fewer than 3 saved results; never in the search request path.
- Concurrent saves cause at most one run at a time, plus one follow-up run.
- A topic supported by only 2 distinct saved results is discarded; relevance exactly 2 is discarded.
- At most 3 suggested directions active; dismissed labels never recreated; labels deduplicated by
  normalized text.
- Promote creates a `subgoal` and keeps earlier scores for that direction.
- New directions never influence ranking (rule 6).

## As built (I4)

- **Model** `emergingdirections` (`models/emergingDirectionModel.js`): the fields in 02-data-model.md plus `normalizedLabel` (the unique key) and `reasoning` (the one-line why, rule 4) and `subGoalId` (set when promoted).
- **Detection** (`services/emergingService.js`, `runDetection`): triggered by `scheduleDetection(workspaceId)` after the save answer is sent, only when the save wrote a new row (a repeated click does not). In this process, one run per workspace; saves meanwhile cause exactly one follow-up. It needs `SUGGEST_MIN_COUNT` distinct saved results (a result saved under two directions counts once). The model sees short opaque ids, Primo metadata only, the three texts, the selected labels and every existing label including dismissed ones. The server then keeps a topic only if at least 3 distinct, valid ids support it and `goal_relevance` is strictly above 2 (decimals floored); drops a label equal (normalized) to any direction of the plan, ticked or not; never recreates a dismissed or promoted label; only refreshes `timesSeen` and `lastSeenAt` of a suggested one (relevance and reasoning are set once); and fills at most `SUGGESTION_LIMIT` active slots, best supported first. Failures log a kind only. The lock is not shared between server processes.
- **Scoring**: call 5.3 now scores the active suggestions with the selected directions (`suggested` in `scorePool`; stored under `emergingDirectionId`, unique partial index). Search and `/scores` answers carry `suggestions` (`{_id, label, timesSeen, reasoning}`) and, per result, `newScores` (only pairs that exist). Ranking reads the active direction only (rule 6; tested).
- **Promote** (`POST /api/emerging-directions/:id/promote`): one transaction. It first claims the row (`suggested` to `promoted`, so a double click or a second tab cannot promote twice), then creates the `subgoals` row (`source: 'ai'`, `suggestionKind: null`, the why as `rationale`, last `orderIndex`), re-points the `resultscores`, and records `subGoalId`. If a direction with the same words is already in the plan (typed meanwhile) it is ticked and used instead, and the suggestion's own scores are dropped (that direction owns its pairs). Already promoted: the same direction is returned (200). Dismissed: 409 `DISMISSED`. Lost claim: 409 `NOT_SUGGESTED`. A full plan: 400 `TOO_MANY`.
- **Dismiss** (`.../dismiss`): `dismissed`; idempotent; a promoted one is 409 `PROMOTED`. Both answers carry the suggestions that remain.
- **New pill save**: `POST /api/results/:id/save` with `emergingDirectionId` promotes and writes the link row in the same transaction (the row is written with the transaction session; on a standalone MongoDB a failed save undoes the promote). A suggestion already promoted saves under the direction it became; a dismissed one is 404.
- **`?` on a New pill**: `.../reasoning` with `emergingDirectionId` (stored reason, or generated once and stored); after promotion the same call is answered through the direction it became.
- **Live SERP** (`features/mindsSerp/useLiveSerp.js`): the rows of "What you might explore" are the server's suggestions; the `+` or the row promotes (the direction joins the panel with a count of 0 and the cards already on screen follow it: a New pill becomes an ordinary chip in the same place, a card that had a score but no pill gets it under `>>`, a card with no score is untouched); `×` dismisses at once and puts the row back with a message if the server cannot record it; a search answer computed before a dismiss cannot bring it back. A New pill click is not optimistic (the server must add the direction first) and says so in the live region. Each row has a "?" ("Why? <label>") that shows the suggestion's reason; the New pill's own `?` explains its score. The cards' New pills are decided once per batch from the suggestions known then, so a suggestion created later gets pills from the next search on (F4: "from the next search on").

## Out of scope

Embedding-based label matching; per-result emerging directions in the scoring call (removed).

*Source: old spec 5.6, 6 (emerging_directions), 8.2 (What you might explore), decisions in 11.*
