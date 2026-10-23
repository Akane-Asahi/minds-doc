# 02 Data model (MongoDB / Mongoose)

Translated from the original Postgres design (see /stack_changed.md). Collection and field
names below are the logical model; match Baseline's camelCase Mongoose style when writing
schemas. Every screen is a different view over one `Workspace`; do not let directions,
coverage and saved items drift into separate structures.

Mongo has no foreign keys or multi-field CHECK constraints: enforce relations in code (ObjectId
refs + indexes), enforce "exactly one of" with a schema validator, and cover both with tests.
Use a Mongo transaction (Atlas replica set) for the two multi-document operations:
save the plan (texts + directions; `runInTransaction`, which falls back to a compensated plain write on a standalone local MongoDB), and promote a new direction + save.

## Collections

| Collection | Fields (logical) | Notes |
|---|---|---|
| `users` | Baseline `User` (participant id login) | unchanged |
| `workspaces` | `userId`, `title`, `color`, `goalText`, `knownText`, timestamps | **Baseline `Workspace` extended** with the two texts. `title` is the participant's own title, typed in Baseline's Create New Workspace dialog (the unique `{userId, title}` index and its duplicate check stay as they are). The three texts are written by Explore (`PUT /api/workspaces/:id/plan`), not at creation. Editing the title, color and archive already exist in Baseline. Counts are computed at runtime, not stored (Baseline rule, keep it). |
| `subgoals` | `workspaceId`, `label`, `source` (`ai`\|`custom`), `suggestionKind` (`familiar`\|`new`\|null), `rationale` (null for custom), `selected` (default true), `addedInSessionId` (the session a promoted new direction was added in; null otherwise; drives the F5 "New" tag), `orderIndex`, `clarity` (reserved, deferred) | Explore saves every direction on Plan Workspace, ticked or not (`selected`); only selected ones are searched, ranked and shown elsewhere (queries use `selected: {$ne: false}`, so older rows count as selected). `suggestionKind` is `new` for every AI direction generated from 2026-10-21 (5.1 is new-only); `familiar` stays valid for plans saved before that. It is null for custom and for promoted new directions. The familiar-versus-new selection comparison no longer exists. **No stored counters** (saved/shown/opened are derived). |
| `emergingdirections` | `workspaceId`, `label`, `normalizedLabel`, `status` (`suggested`\|`promoted`\|`dismissed`), `timesSeen`, `goalRelevance` (integer 0 to 5, set once), `reasoning` (the one-line why), `subGoalId` (null until promoted), `firstSeenAt`, `lastSeenAt` | Unique on `{workspaceId, normalizedLabel}` (lowercase, trimmed, whitespace collapsed). Created only by call 5.6. `candidate` status no longer used. `reasoning` and `subGoalId` added in I4 (rule 4 needs the why stored; promote needs to find the direction again). No saved counts here: a new direction has none until promoted. |
| `sessions` | `workspaceId`, `startedAt`, `endedAt`, `lastActivityAt`, `activeSeconds`, `activeSubGoalId` (the direction selected on the SERP; updated whenever the selection changes or a search runs) | Created lazily when the participant first searches after a gap (> `SESSION_GAP`), never by merely viewing Your sessions. Each API call belonging to a session does `activeSeconds += min(now - lastActivityAt, IDLE_CAP)`; then `lastActivityAt = now`. Session number ("Session 3") = rank of `startedAt` within the workspace, computed on read. |
| `queries` | **Baseline `Queries` extended**: `workspaceId`, `userId`, `query`, plus `sessionId`, `subGoalId`, `source` (`ai`\|`user`), `totalHits` | One row per query run. A direction's first `source: 'ai'` row is its **stored AI query**: written once, on the direction's first selection (5.2), never regenerated. The newest row for a direction (AI or user-typed) is the one shown when the participant switches back or returns. `totalHits` is the Primo total shown as "Results: N". |
| `resultscache` | `primoRecordId` (unique), `title`, `authors`, `venue`, `keywords`, `abstract`, `resourceType`, `identifiers`, `raw`, `cachedAt` | Shared across users. Result metadata that scores, saves and sessions point to. **No expiry:** deleting it would break saved cards and the Saved results views (which make no Primo calls). |
| `primocache` | `queryKey` (normalized query string + paging, unique), `response` (raw Primo JSON), `totalHits`, `cachedAt` | Query-keyed response cache that protects the Primo quota. **TTL index on `cachedAt` (about 24 h).** Safe to expire. |
| `resultscores` | `workspaceId`, `resultId`, `subGoalId` **or** `emergingDirectionId` (exactly one), `score` (integer 0 to 5), `reasoning` (nullable), `lowConfidence` (bool), `scoredAt` | Output of call 5.3. Unique partial indexes on `{workspaceId, resultId, subGoalId}` and on `{workspaceId, resultId, emergingDirectionId}`. When a new direction is promoted, its rows are re-pointed to the new `subGoalId` so scores are kept. |
| `sessionresults` | `sessionId`, `queryId`, `resultId`, `subGoalId` (the active direction), `rank`, `opened`, `shownAt`, `openedAt` | Per-session log of what was shown. Source of "reviewed". |
| `savedresults` | `workspaceId`, `sessionId`, `resultId`, `subGoalId`, `savedAt` | One row per (result, direction). Unique on `{workspaceId, resultId, subGoalId}`. Unsave deletes the row (so a bar segment shrinks). **Source of truth for every saved count.** |
| `interactionevents` | see F7-logging.md | append-only study log |

## Derived values (always computed by aggregation, never stored)

- Saved count per direction = rows in `savedresults` grouped by `subGoalId`.
- Per-session bar segments = grouped by `{sessionId, subGoalId}`; only sessions with at least
  one save under that direction get a segment. Segments sum to the circle number.
- Reviewed per direction = distinct `resultId` in `sessionresults` with that `subGoalId`.

## Decided: `SavedDoc` and `savedresults` (Telot, 2026-10-19)

Baseline `SavedDoc` stores one row per result per workspace (unique on `externalId`, soft delete via `isRemoved`, keeps
full `docdata`). MINDS needs the same result saved under several directions. So:

- `SavedDoc` stays the **document record** (metadata, dedupe, Baseline saved-results code).
- `savedresults` holds the per-direction **link rows** and drives every saved count (rule 2).
- Join: `SavedDoc.externalId` = `resultscache.primoRecordId`. `savedresults.resultId` is the `resultscache` `_id`, because
  scores (5.3) exist before anything is saved and are keyed by `resultId` too. `resultscache` arrives in I2.
- Saving under a first direction creates the `SavedDoc` (or revives a soft-deleted one) and the link row; removing the last
  link row soft-deletes the `SavedDoc` (as U2 describes for the chips).

Built in I0: `Workspace` (two texts added), `SubGoal` (`subgoals`), `SavedResult` (`savedresults`), in `backend/models/`.
Their `sessionId` and `resultId` refs point at models that arrive in I2 and I5.
