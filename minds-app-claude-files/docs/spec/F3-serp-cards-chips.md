# F3 SERP result cards, direction chips, and the right-hand panels

**Problem it solves:** with low working memory, a participant cannot hold in mind which direction
a result serves or what they have already filed. Each card shows, in low-text form (star plus
number, chips), why it may help; one click files it under a direction; a side panel shows what has
been explored.
**Challenges it answers:** dense text is slow to read; hard to tell relevant results; organizing
found information; losing the thread.
**Load with:** 01-core.md, accessibility.md, F2 (scores and reasons come from there).
**Status:** UI in progress (U2, on the Baseline SERP copy at `/ui/serp`): Search Direction dropdown, the three-row right panel and direction chips (with `>>` and `?`) are built; the header Saved Results toggle and the promote / add behaviour are not. Wired in I3 (2026-10-21): the live SERP at `/workspace/:id/serp` (see "As built (I3)" below and in F2). Not yet checked in a browser, by keyboard or with a screen reader. Wired in I4 (2026-10-22): the New pill from real scores, the rows of "What you might explore", promote, dismiss and the New-pill save (F4 "As built (I4)"). The Saved results view and the header toggle were wired in I6.

## Result card (top to bottom)

1. Title.
2. Meta line: resource type, year, authors, e.g. `Article · 2022 | Authors: Name01, Name02`. From Primo.
3. `Description:` abstract from Primo, clamped to about two lines. None: "No description available".
   Never generated.
4. Up to `CHIP_COUNT` (3) direction chips, plus an optional 4th **New pill**, then the `>>` button.

## Which pills a card shows by default

1. **Up to 3 chips from selected directions.** Sort the selected directions by their score for this
   result, highest first, show the first three. **No minimum score and nothing forced:** the active
   direction's chip appears only if it is in the top three. Ties: `orderIndex`. A direction scored 0
   gets no chip in the default view, so fewer than three show only when fewer than three score
   above 0.
2. **Optionally a 4th New pill.** Suggested new directions (F4) are scored with the selected ones.
   Show the pill of the card's highest-scoring suggested new direction when its score is **within
   the top three scores of all directions** (selected plus new); on a tie the selected direction
   ranks ahead. Example: scores a 4, b 2, c 2, d 1, e 0 and new x 3 give "4★ a", "3★ x New",
   "2★ b", "2★ c". If x scored 2 it ties b and c, ranks behind them, and no New pill shows. A new
   direction scored 0 is never shown. **At most one New pill per result.**
3. **Order:** all shown pills by score, highest first; on a tie a selected direction before a new
   one, then `orderIndex`.

## `>>` "Show other directions"

A small icon-only button after the last pill (accessible name "Show other directions",
`aria-expanded`), collapsed by default. Pressing it shows the remaining **selected** directions as
normal chips, highest score first (ties `orderIndex`), each with score, `?` and save, **including
directions scored 0** (a result whose scores are all 0 shows no default pill, only this button). It
opens and closes per card, keeps saved states, and never changes ranking. Icon only for now; test
whether participants understand it in Phase 3 testing.

## Chip anatomy and behaviour

Each chip shows a star, the score number, and the direction label, followed by a separate `?` button.

- **Clicking a chip saves the result under that direction.** It is the only way to save; no opening
  or reading first. One result can be saved under several directions. **Clicking a saved chip
  again undoes the save.**
- A saved chip shows a check icon and the text "Saved", a visual change, and `aria-pressed="true"`.
- `?` is its own button (`aria-expanded`), never nested in the chip. It toggles the one-sentence
  reason in place and never saves. If the reason is null, fetch it (F2 "Reasoning on demand").
- Save and unsave update the UI immediately (optimistic), call the endpoints, and roll back with a
  visible message on failure. Saving announces in a polite live region, e.g. "Saved under Public
  parks. 3 results saved."
- **Clicking the faded New pill** first adds that direction to the plan (promote, F4), then saves
  the result under it; afterwards it behaves as any chip.

## Chip colours (three states)

| State | Rule |
|---|---|
| **Solid blue = saved** | the participant saved the result under this direction. Saved results are found again on Your sessions via the circle or a bar segment. |
| **Light blue = suggested** | the chip is the top chip of its result (the first of the three after sorting; the New pill is never light blue) **and** its score equals the highest chip score of any result on the page (the batch of 10 scored together). A tie for the page maximum makes every tied result's top chip light blue. Computed once when the batch is scored; never changes after. A saved chip shows solid blue, not light blue. Considers selected-direction chips only. The stars still show the real score, so a weak page highlights its best chip without calling it strong. |
| **Neutral** | every other unsaved chip |

The score never decides colour; only "saved" and "best on this page" do. The New pill is faded
("not in your plan, but this result talks about it"), carries a visible "New" tag, and must still
meet contrast. Light blue and solid blue must not rely on colour alone: they need a non-colour cue
and an accessible name such as "best match on this page". The exact cue is **not chosen; leave as
is for now** (see open-questions.md).

## Right panel (one card in the right rail, three rows)

Always fixed, it does not scroll. Sits in Baseline's right rail, outside the scrolling result list, so it stays in view. Design: `02-serp-a.png`.

**Row 1: "Directions you have explored".** One row per selected direction in `orderIndex` order: a circle with the saved
count, the label, and under it a bar. Count = distinct results in `savedresults` for that
direction: a plain count, never a percentage or ratio. Count 0 = outlined circle and muted label, 1 or more = filled
circle; the number is always shown (never colour alone). The bar is a grey ruler (never labelled, never a target) with
one dark `+N` segment per session that saved under the direction, oldest first, alternating two dark shades; each
segment is a native button named like "Session 2, Aug 12, 2026: 1 saved under Physical health benefits. Open these
results". Bar units follow Your sessions (`BAR_MIN_CAPACITY`, `MIN_SEGMENT_PX`). Saving or unsaving updates the count
and the current session's segment at once. The circle and the segments open the Saved results view (F6) for that
direction (and session).

**Row 2: "What you might explore".** Every New pill on the page comes from here: the suggested new directions (F4), most
seen first, up to `SUGGESTION_LIMIT` (3). A dashed, faded row per suggestion: label, the "New" tag, a `+`
(promote) and a `×` (dismiss). No circle (the design drops it). If there are none, **hide the row** (no
empty header).
- Activating a row (the label or the `+`) promotes it (`POST /api/emerging-directions/:id/promote`): it moves into row 1,
  joins the Search Direction dropdown, and is included in future scoring. Results already on screen keep their scores
  and gain chips for it only where a score already exists.
- `×` dismisses it (`.../dismiss`); its New pills disappear from the cards too.
- Faded style: same contrast and text-cue treatment as faded chips (text at least 4.5:1).

**Row 3: "Add search direction".** A dashed full-width button that lets the searcher type their own search direction
(same rules as the Plan Workspace Add field: at most `DIRECTION_LABEL_MAX_WORDS` words). Not in the old spec; added from
the design (Telot, 2026-10-17). Behaviour is built in I3.

## Header: Saved Results toggle

A pill button, always visible, opening the Saved results view (F6) with **no filter** (everything
saved anywhere in the workspace). While that view is open it reads **Return to Search**.

## Acceptance criteria

- Default pills follow the top-3 rule with no minimum score and nothing forced; ties by `orderIndex`.
- The New pill appears only when its score is within the top three of all directions, never beats a
  tied selected direction, at most one per card, never when its score is 0.
- `>>` lists every other selected direction including 0-scored, per card only, no ranking change.
- Light blue computed once per batch; saved chips are solid blue; colour is never the only cue.
- Save and undo are optimistic with rollback and a visible failure message.
- Counts in "Directions you have explored" equal distinct `savedresults` per direction and update at once; the bar has one segment per saving session.
- "What you might explore" is absent when there are no suggestions, and every New pill on the page is one of its rows.
- Chips are native buttons with `aria-pressed`; `?` is a separate button.

## UI notes (U2)

- Heading wording "Directions you have explored" follows the mockup and Telot's 2026-10-17 request (Your sessions
  still says "What you have explored").
- Chips live in a footer row of the card (MINDS copy of `ResultCardShell`). Baseline's bookmark button is **removed**
  from MINDS cards: a chip does exactly what the bookmark did. The first chip saved under a result saves the document
  (Baseline's save call); unsaving the last chip removes it (Baseline's unsave call). So the nav-bar Saved Results
  button lists every result with at least one saved chip, and unsaving a result on that view clears its chips here.
  On the Saved results view the card has no bookmark either: its footer shows a solid-blue chip for each direction the
  result is saved under, and a chip does what the bookmark did (unsave under that direction; unsaving the last chip
  removes the result from the list, dimmed while it leaves, with a visible message if the call fails).
  Which direction a saved result is filed under is the `savedresults` link row (SavedDoc vs `savedresults`, open-questions.md 3).
- Light blue = 2px blue border + the text "Best on page" + the accessible-name suffix "best match on this page";
  solid blue = check icon + "Saved". Provisional (open-questions.md 4).
- The Search Direction dropdown is beside the workspace breadcrumb, right-aligned. Choosing a direction re-runs the
  search with that direction's stored query; mock results are not re-ranked (ranking is I2).

## As built (I3)

- **Chips** come from the real scores through `buildPills` (top three above 0, `>>` for the rest including 0, light blue once per batch of 10). A direction with no score for a result shows no chip. `?` shows the stored reason at once, or fetches it once (`POST .../reasoning`, stored by the server, so the same words show next time); a failed fetch says so and opening `?` again tries again. A card with no description says "No description available" (the text is never generated); the meta line is `Article · 2022 | Authors: Name01, Name02`.
- **Save and unsave** are optimistic: chip, count, bar segment and the polite live region ("Saved under Public parks. 3 results saved.") change at once; a failed call puts that chip back with a visible message ("Could not save the result under X. Try again."). Calls for one chip run in the order clicked. **Chips write only `savedresults`**: the Baseline `SavedDoc` is not written (the Saved results view, I6, is built from `savedresults` + `resultscache`), so Baseline's saved-documents list does not show MINDS saves. Clicking a title marks the result opened (`POST /api/results/:id/open`, logging only).
- **Add search direction** (row 3) opens an inline field with Plan Workspace's rules (7 words at most, a typed 8th word ignored, "N of 7 words", Enter adds, Escape cancels and focus returns to the button). `PATCH /api/workspaces/:id/subgoals` appends it last and selected; it joins the dropdown and the panel with a count of 0, and the live region says to choose it in Search Direction. A failure keeps the field open with a message.

## Out of scope

Categorical badges, Plan Strip, Coverage Map, clarity control (deferred.md).

*Source: old spec 8.2 (header toggle, card, chips, panels) and the chip/`>>` decisions in 11.*
