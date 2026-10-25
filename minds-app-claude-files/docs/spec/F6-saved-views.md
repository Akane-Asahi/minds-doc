# F6 Saved results views (by workspace, direction, or session)

**Problem it solves:** a participant must be able to get back to what they saved, narrowed the way
they think about it (everything; one direction; one session; one direction in one session), without
re-searching and without extra reading.
**Challenges it answers:** reacquainting after a break; organizing found information.
**Load with:** 01-core.md, F3 (same card component and chip rules), 02-data-model.md.
**Status:** wired (I6, 2026-10-22): live at `/workspace/:id/saved?direction=<id>&session=<id>` (`features/savedResults/SavedResultsPage.jsx`); the UI also stays at `/ui/saved-results` on mock data. Not yet checked in a browser, by keyboard or with a screen reader.

## One view, two optional independent filters

`direction` and `session` are each optional. Omitting a filter widens the scope; omitting both shows
every result saved anywhere in the workspace. The view **looks the same as the SERP** (F3 cards) but
without the search field and the right-hand panels. It makes **no Primo calls** in any
state and **no LLM calls except one**: tapping `?` on a chip whose stored reason is null calls the
on-demand reasoning endpoint (F2), which reads stored metadata only and stores the result. Scores and
reasons otherwise come from the stored values.

| Entry point | Filters set |
|---|---|
| SERP header **Saved Results** toggle (F3), Your sessions header **Saved Results** | neither (whole workspace, grouped by session) |
| Circle badge (SERP panel or Your sessions) | `direction` only |
| Black bar segment (Your sessions) | `direction` and `session` |
| Session tile (Your sessions) | `session` only |

## Page layout (decided by Telot 2026-10-19; mockups `04-*`, `05-*`, `06-*`)

- **Header: the SERP's `MainHeader` in saved mode:** logo; the search box **disabled**, showing the last query
  (the same text as Last Query on Your sessions); account icon; **Return to Search** button (to the SERP).
  There is no Back button: Return to Search and the breadcrumb are the ways out.
- **Breadcrumb:** `Workspaces › {workspace name} › {scope}`. `Workspaces` links to the Workspaces list, the
  workspace name links to Your sessions, the last segment is the current page (not a link): `All Saved Results`
  (no filter), the direction label (`direction`), `Session {n}` (`session`), `{direction} · Session {n}` (both).
- **h1:** visually hidden (the breadcrumb is the visible cue): "All saved results", "Saved under {direction}",
  "Saved in Session {n}", "Saved under {direction} · Session {n}".
- **Counts row:** three plain counts, each an icon and a number (no percentages, rule 1): **saved results**
  (distinct results saved here; document icon), **search directions** (distinct directions present here;
  three-arrows icon) and **sessions** (distinct sessions present here; history icon). The mockups' "8" and "3"
  were wrong (they listed 6 cards and had no sessions count); the counts must agree with Your sessions: the
  all-sessions view shows the sum of the tile totals, a direction view equals that direction's circle, a session
  view equals that session's tile. Each has a screen-reader label ("9 saved results"). They update when a chip
  is toggled in this view.
- **Right panel (Telot, 2026-10-25; it was empty before):** "Directions with saved results" lists, by name with a plain
  saved count (distinct results, rule 1), "All directions" first and then every direction that has saved results in the
  session scope, in `orderIndex` order. Choosing a name filters the list to results saved under it (the `direction`
  filter, set in the URL with `replace`; no new request, chips toggled here are kept); choosing it again or "All
  directions" clears the filter. The chosen button is solid blue with white bold text (no hover change) and `aria-pressed` (not colour alone);
  the other names stay listed while one is chosen. A `session` filter from the URL still narrows what the panel lists.
  The list takes the rest of the width (the panel is the SERP's right-column width); on narrow screens it stacks below.
  The page asks the server for the session scope only and applies the direction filter itself; a `direction` that is
  not a direction of the workspace shows "Saved results not found".

## Cards, groups and order

- **Card:** the SERP card chrome (type icon and label, title, `year · authors`, Primo description) with the
  chips under it, **only the directions the participant saved it under** (solid blue, score and a check icon, no "Saved" text,
  ordered as the directions are). Other scored directions are never shown here. `?` opens the one-line reason in
  place. No "Why this may help" label.
- **Groups by session:** unless a `session` filter is set, results are **grouped under a heading per session,
  newest session first**: `SESSION 3 · SEP 23` (small grey uppercase, letter spacing) with a thin rule across.
  Only sessions with saved results in scope get a group (a session with nothing saved has no heading). With
  `session` set there is one list and no heading.
- **Order inside a group:** by save time, earliest first (the order they were saved in that session).
- **Which results:** with `direction` set, only results saved under it (05 shows Walkability in Session 3, two
  results in Session 1: 3, the circle). With `session` set, everything saved that session (06: 6, the tile total).
  Both together: the bar segment's results.
- **Chips work as on the SERP.** Clicking a saved chip undoes the save; the card stays visible with the chip grey (the only time a grey chip appears)
  until the participant leaves the view, so a mis-click can be reversed. Your sessions counts and bars refresh
  when they go back.

## Empty state

"Nothing saved here now" (when nothing matches, or everything shown was unsaved). The counts row shows zeros.

## States

Loading: skeleton cards, `aria-busy`. Error: message with Retry.

## Acceptance criteria

- [x] Each of the four filter combinations returns exactly the matching `savedresults` rows (backend test, mocked models). A card also carries the other directions saved on the same result in the same session (they are its other chips).
- [x] No Primo call is made by this view; the only LLM call is the on-demand reasoning on a `?` tap with a null stored reason (backend and page tests).
- [x] Undoing a save leaves the card visible, with the chip reset, until the participant leaves.
- [ ] Counts on Your sessions match this view after returning. (Needs Your sessions wired, I5; the page loads fresh on every visit and the server derives both from `savedresults`.)
- [x] Counts agree with Your sessions for the mock data (all = tile totals, direction = circle, session = tile).
- [x] Results are grouped by session, newest session first, earliest save first inside a group; no heading with a session filter.
- [x] The header is the SERP's with a disabled search box and Return to Search; the breadcrumb ends in the scope; h1 is correct for each combination.

## As built (I6)

- **Data:** `GET /api/workspaces/:id/saved?subGoalId=&sessionId=` (03-api.md) returns the workspace's directions (also unselected ones, which can hold saves) and sessions (numbers by rank of `startedAt`), the saved rows in scope, the Primo metadata and stored scores for them, and `lastQuery`. A filter naming something that is not in the workspace is a 404 ("Saved results not found"), not an empty list. The page fetches fresh on every visit.
- **Entry points:** SERP header toggle (no filter), count circle (`direction`), black bar segment (`direction` and `session`). The workspace-name crumb goes to the SERP until Your sessions has a route (I5, I7). Return to Search keeps the `direction` filter as the SERP's starting direction.
- **No reload on return:** `/workspace/:id/serp` and `/saved` are one route and one component (`MindsSerpPage`); the SERP stays mounted (hidden) under the saved view, so Return to Search shows the lists as they were: no session call, search, Primo, scoring or "reviewed" log. A chip removed or re-saved in the saved view is pushed into the SERP's saved state. Opening `/saved` directly does not start a search; the first one runs when the SERP is first shown. Return to Search from a direction view selects that direction (its list is kept, or searched once).
- **Undo:** a chip click is applied at once; on a refusal the chip goes back and a visible message says so. Removing calls `DELETE /api/results/:id/save`; clicking the grey chip saves again **into the session it came from** (`sessionId` on `POST /api/results/:id/save`), so the group, the bar segment and Your sessions do not move. Its save time is new, so after a reload it sorts last in its group.
- **Card:** title links to the library record, Primo's own type icon, `?` shows the stored reason or asks the server once (loading and error text in place; a second tap after an error retries).
- **Not done:** re-saving under a direction that was unticked on Plan Workspace after the save is refused by the save endpoint (only selected directions can be saved under), so the message shows and the chip stays grey. Clicking a title does not mark the result opened here.

*Source: old spec 8.4, 8.5, 7 (saved endpoint), 9 (saved view accessibility), decisions in 11.*
