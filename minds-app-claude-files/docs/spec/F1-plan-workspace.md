# F1 Plan Workspace (Screen 1) and direction generation (call 5.1)

**Problem it solves:** people with dyslexia are unsure what to search for and favour familiar
angles. Before searching, the participant states the task and chooses from LLM-proposed
directions, **every one an angle they had not thought of** (Orland confirmed, 2026-10-21; the generator never restates what they wrote). Choosing is an active
decision: that is the planning step of metacognition.
**Challenges it answers:** unsure what to search; favouring familiar sources; spelling and
query formulation (via F2).
**Load with:** 01-core.md, 03-api.md (generate + create workspace), accessibility.md.
**Depends on:** LLM key only, plus Baseline's workspace create and `GET /api/workspaces/:id`. No Primo needed.
**Status:** wired (I1, 2026-10-19). Real route `/workspace/:workspaceId/plan` (protected); the dev preview `/ui/plan-workspace` still uses fixtures. Not yet looked at in a browser; see the acceptance list below.

## How the participant gets here (Telot, 2026-10-19)

1. `/start`: participant ID (Baseline, unchanged).
2. `/workspaces`, **+ New Workspace**: Baseline's **Create New Workspace** dialog asks for the Workspace Title (unchanged Baseline code).
3. **Create** runs Baseline's `POST /api/workspaces {title, color}` as before, so the workspace has the participant's own title. The only change:
   instead of opening the SERP with the title as the query, the app goes to **Plan Workspace for that workspace**, `/workspace/:workspaceId/plan`.
   The id is in the URL (not in `WorkspaceContext`) so a refresh keeps it; the page loads the workspace with `GET /api/workspaces/:id`,
   which only returns the signed-in participant's own workspaces.
4. Fields, generation (5.1), picking directions.
5. **Explore does not create a workspace.** It saves the two texts and **every direction on the screen, ticked or not** (each with its `selected` flag), onto the existing workspace
   (`PUT /api/workspaces/:id/plan`) and then opens Baseline's SERP for it (`openWorkspace(ws, navigate, "serp")`).

**A workspace that already has a plan** (Explore answered 409) shows one wrapping row: "This workspace already has a plan.  [Open workspace]  Or
  [Update workspace]" (the "Or" is plain text between two real buttons, read in that order). **Open workspace** opens the SERP. **Update workspace**
  loads the saved texts and the saved directions (ticked or not as saved, in saved order) into this screen without calling 5.1; the participant can edit, add, drag
  and tick, then press Explore, which sends `replace: true` and **replaces** the old plan (`PUT /plan`, one transaction). Only this explicit choice
  sends `replace`. A replace keeps directions that have saved results: they keep their `_id`; one the participant removed comes back unticked (open-questions 9).

**Clicking a workspace, and a workspace that already has a plan (Telot, 2026-10-19):** on `/workspaces`, clicking any workspace opens its Plan Workspace
page (Baseline opened the SERP); the three-dots menu has **Edit Workspace** for the same page. If the workspace already has a plan, the page **shows the
full saved plan by default**: the two texts and the saved directions in saved order, ticked as saved (**an unticked one comes back unticked**, so the participant can tick it later), loaded with one `GET /plan` lookup and no call to 5.1. The
participant can edit, add, drag and tick, then press **Explore**, which replaces the old plan (`replace: true`, one transaction) and opens the SERP. If nothing was
changed, Explore just opens the SERP and writes nothing (so the directions keep their ids). If the participant had already started typing before the lookup came
back, nothing is overwritten and the row "This workspace already has a plan. [Open workspace] Or [Update workspace]" shows at the top instead. The same row also
shows at the bottom if Explore answers 409 (a plan saved from elsewhere); **Open workspace** opens the SERP and **Update workspace** loads the saved plan. An empty or
failed lookup shows no row and the page works as for a new plan.

Workspaces created before this keep opening the SERP. **Open item for I7:** a workspace with no directions yet should reopen Plan Workspace.

## Layout (top to bottom)

Header (the institution logo at left and the participant icon at right, as in Baseline; the "MINDS"
wordmark is dropped; the icon is the account control once login is integrated), a **breadcrumb** `Workspaces › {workspace title}` (as on Your sessions: `Workspaces` links back to the list, the title is plain text), **no visible page title or helper line** (Telot, 2026-10-21; the page keeps a visually hidden `h1`
"Plan Your New Workspace" for assistive tech, and the mockup still shows the old title and helper), a visible heading **"Set your search goal"** (an `h2`, Telot 2026-10-22) above the first field, a three-row form, then a full-width **Explore** button. Every box (the two fields, direction rows, the Add box and inline inputs, the error box, Explore) is a rectangle with the SERP result card corner radius (`CARD_BORDER_RADIUS`, 12px), not a pill.

| Row | Control | Notes |
|---|---|---|
| Search goal | text input | e.g. "Explore academic literature on how green spaces affect human well-being" |
| What I already know | multi-line text area | feeds the "do not restate what they know" rule in 5.1 |
| Search directions | two-column checkbox list + **Add Custom** | **No sparkle or star icon anywhere** (Telot, 2026-10-21; the mockups still show it). **States (Telot's sheet, 2026-10-22):** selected = blue 1px border, light-blue tint, blue checkbox; unselected = the same thin grey 1px outline as the text fields, white, dark checkbox (2px dark strokes were tried and looked heavy, Telot 2026-10-22). **Every item has Edit and Remove** (AI ones too; removing an AI one just takes it off the list). AI items have the "?" (Why?) button as a round badge centred on the card's right edge (it first sat on the top-right corner and covered the card above, Telot 2026-10-22), drawn in the card's border colour, **shown on hover, on keyboard focus anywhere in the card, while its popover is open, and always on touch screens** (no hover there). (Older wording follows:) **every item has Edit** (Telot, 2026-10-22: editing an AI direction's wording keeps its slot and tick but makes it a custom one, so the "?" goes and Remove appears; confirming unchanged words changes nothing); custom items also have Remove and no tag. **One mixed list across two columns:** the AI suggestions in the order the model returns them (all are new to the student; there is no tag, no fading and no column of its own), then custom directions as added at the end. The list fills column 1 top to bottom (the first half, rounded up), then column 2. It is one `<ul>`; the two columns are a layout only. Each column is exactly half the width (`minmax(0, 1fr)`), so a long label can never push column 2 out of the window. All rows are selectable and deselectable. **Word limit:** every direction label is at most `DIRECTION_LABEL_MAX_WORDS` (7) words, so it stays on one line like a bullet point. AI labels are asked for 2 to 5 words and validated to at most 7. When the participant types a custom or edited direction, a typed 8th word is ignored, a pasted longer text is cut to 7 words, and a visible "N of 7 words" count shows under the field. If a row is still too narrow (very large text, narrow window) the label is cut with an ellipsis and the full text stays in the tooltip (`title`) and the accessible name; this is only a safety net. Columns stack on narrow screens (column 1 then column 2). **Row numbers:** each row shows its list position (1, 2, 3 ... down column 1, then continuing down column 2), the same order as `orderIndex` + 1; the number is plain text beside the row, not part of the label. The section heading "Search directions" has a decorative three-arrow icon (arrows to the left, right and up, meaning several directions; `aria-hidden`). |

## Generation trigger (blur)

1. Listen for `blur` on each of the two fields; any order.
2. On every blur, if either is empty after trimming: do nothing (no request, no error).
3. If both are filled, hash the two normalized texts (trimmed, whitespace collapsed). If equal to the
   hash of the last successful or in-flight generation, do nothing.
4. Otherwise call `POST /api/search-directions/generate`. Abort any in-flight request
   (`AbortController`) and ignore stale responses (request counter).

**Regeneration when inputs change:** generate again, but keep every selected and every custom
direction; replace only AI suggestions that are still unselected. Send kept labels as
`keepLabels` so the model does not duplicate them. **Exact rule (the list is one ordered list):** selected and custom cards keep their
slots; each unselected AI card is a hole, filled top to bottom by the next new suggestion in the model's order (repeats of a kept label
are skipped); leftover new suggestions go to the end; holes left unfilled are removed (the only case where a card moves, and only the
cards below it move up). A batch that arrives **while a card is being dragged** is held back and applied when the drag ends; until then
existing rows stay and "Updating search directions…" shows. A reorder never triggers generation, and the hash check is unaffected.

## Reordering (drag and drop; Telot, 2026-10-19)

- Any card (AI or custom, selected or not) can be dragged to a new place; it works across the column break because the list is one ordered
  list. The **row numbers are fixed slot labels** (1 to n) and are not part of the card: after a drop, slot 1 shows whichever card is now first.
- A mouse drag starts after 6px, so the checkbox, label and "?" still click normally. A finger needs a short press-and-hold
  (about 250 ms), because a swipe over the cards is page scrolling.
- While dragging: a see-through copy of the card (no number) follows the pointer and the old slot shows a faint outline. Over the top or
  bottom half of a card a 3px solid black line shows just above or below it; releasing inserts the card exactly there. A light-grey rounded
  end slot appears in the **next available position**, right after the last card with no gap: with an odd number of cards it fills the
  empty cell at the bottom of column 2; with an even number (both columns full) it sits directly under the last card of column 2 (in the row
  below the list, in column 2 of the row that used to hold the Add box); on a narrow screen it comes right after the last card. It is shown only while dragging and
  never moves a card between columns; releasing on it makes the card last. Releasing anywhere else cancels.
- After a drop the cards close up with no gaps and the numbers stay put. The Explore payload follows the list order (selected cards only), so
  the first selected card is the SERP default. No new endpoint; the payload is unchanged.
- **Keyboard: not provided yet** (dnd-kit's keyboard sensor needs extra insertion-point code); see accessibility.md and STATUS.md.

## Picking and creating directions

- AI suggestions start **unselected**. The "?" opens its `rationale` in a **floating popover card** (Telot, 2026-10-22): rounded card, soft shadow, a small arrow pointing at the "?", a cross at the top right. The cross, Esc or a click outside closes it and focus returns to the "?"; the "?" keeps `aria-expanded`, the card is `role="dialog"` named "Why <label>". One card open at a time. (Not applied to the "?" buttons on the SERP yet.)
- **Buttons beside the "Search directions" heading (Telot, 2026-10-22):** **Generate more** (a Gemini-style four-point star icon with a blue-to-violet gradient, decorative) and **Add Custom** (plus icon, same outlined shape, black). The star is on this button only; it does not mark AI directions (01-core.md). Add Custom is disabled while its field is open.
- **Add Custom** opens an inline field (directly under the heading row, above the list; it used to sit below the list): Enter confirms, Escape cancels. A custom
  direction is `source: "custom"`, starts **selected**, can be edited or removed in
  one tap, and can be added any time (including before generation or if it fails).
- AI directions are all new to the student: same row, border, checkbox and label colour, with no "New" tag and no fading.
  All are fully selectable. After Explore, a selected one is an ordinary direction (`source: "ai"`, `suggestionKind: "new"`;
  `familiar` stays a valid value so plans saved before 2026-10-21 still load).

## States

| State | Behaviour |
|---|---|
| Idle (fewer than 3 fields filled) | empty-state hint in the directions area; Add button still works |
| Loading | skeleton placeholders; fields stay editable; announce "Generating search directions" |
| Ready | suggestions shown; announce "Search directions ready" |
| Error / timeout | non-blocking inline message with Retry; participant can continue with custom directions only |

## Generate more (Telot, 2026-10-22)

An outlined **Generate more** button sits beside the "Search directions" heading (same style as Retry). Each click adds **one** AI direction at the end of the list, unticked, with a polite live-region message ("Added a search direction: ...").
- **Why a reserve:** a 5.1 call costs 5 to 14 s of fixed provider time whatever its size (measured 2026-10-22: 1 direction 5 to 11 s, 16 directions 12 to 15 s, tokens about 40 per direction), so one call per click would be slow. Call 5.1 asks for 16; the first 8 fill the list and the other 8 are kept in page state as a **reserve**.
- A click takes the next reserve item that is not already on the list (case-insensitive): no model call. The reserve is valid only for the exact texts it was made for; if either text changed, or the reserve is empty, one 5.1 call is made with **every label on the list** as `keepLabels` (last 40), the first new direction is added and the rest become the new reserve.
- The reserve lives only in page state (not saved; lost on reload). A blur-triggered regeneration replaces it.
- Disabled while either text is empty, while generating, while Explore is saving, and at 30 directions (the plan limit). A failed request shows a message and leaves the list unchanged.

## Explore button

- Enabled only when both fields are non-empty **and** at least one direction is selected.
  Otherwise disabled with a visible reason.
- On press: `PUT /api/workspaces/:id/plan`; disable the button while running (no double submit; it reads "Saving your plan…"); on
  success open the SERP for the workspace. A 409 (the workspace already has a plan) shows "This workspace already has a plan." with an
  **Open workspace** button; any other failure shows a message and re-enables the button. If a field was still focused, its blur runs first; the click
  proceeds with the current selection and any late generation result is discarded after routing.
- `orderIndex` is 0 to n-1 over the **selected** directions in Screen 1 list order (the AI suggestions as returned, then custom
  directions as added; column 1 top to bottom, then column 2), over **all** saved directions, ticked or not (Telot, 2026-10-21: Explore saves every generated direction, so coming back to Plan Workspace shows them again). Only `selected` ones are searched, ranked, listed on the SERP dropdown and shown on Your sessions; an unticked one waits here until ticked, then Explore replaces the plan with it selected. The first **selected** direction in that order is the SERP default. Explore still needs at least one selected.
- **Workspace name:** there is no name field and 5.1 does not return one. The workspace keeps the title the participant typed in the Create New Workspace dialog; Plan Workspace never shows or changes it.
- Nothing about the plan is saved before Explore (the empty workspace already exists, created by the dialog).

## Call 5.1: search direction generation

Stateless: reads the two fields, returns suggestions, writes nothing (the workspace is created
only on Explore). May run many times per draft.

**Input:** `goalText`, `knownText` (both required, non-empty); on regeneration also the
labels already selected or created.

**Prompt requirements:**
- About `DIRECTION_COUNT` (16) directions (the client shows the first 8; see Generate more), **all new** (Orland, 2026-10-21): angles the student has not thought of, not in `goalText` and not covered by `knownText`, but helpful (e.g. "Mechanisms & Environmental Pathways", "Accessibility, Equity & Environmental
  Justice"). Never restate, rephrase or narrow anything the student wrote.
- Each direction is a distinct angle. Labels are short plain-language noun phrases (2 to 5 words; the server rejects more than `DIRECTION_LABEL_MAX_WORDS` = 7).

**Output schema (validate with Zod):**
```json
{
  "sub_goals": [
    { "label": "string, 2-5 words (hard max 7)",
      "rationale": "one sentence: why searching this direction helps the goal" }
  ]
}
```
The model returns no `kind`; the server stamps `kind: "new"` on every direction in the API result (`toDirectionsResult`), so the response shape, saved plans and the frontend are unchanged.
Server rate limits this endpoint per user. Target a few seconds; never block typing.

## Acceptance criteria

`[x]` met and tested; `[~]` built and tested in jsdom, still to confirm by hand in a browser. Status stays "wired" until those are checked.

- [x] Blur with fewer than 3 fields filled sends no request; unchanged hash sends no request.  (automated test)
- [x] A stale or aborted response never overwrites a newer one.  (automated test)
- [x] Regeneration keeps selected and custom directions and replaces only unselected AI ones.  (automated test)
- [x] Generate more adds one unticked direction from the reserve without a request; an empty or outdated reserve makes one request that avoids every label on the list.  (automated tests)
- [x] AI suggestions start unselected; custom start selected; Explore is disabled until both fields are filled  (automated tests)
  fields are filled and one direction is selected, and shows why when disabled.
- [x] Double-clicking Explore saves the plan once. Nothing about the plan is persisted before Explore.  (automated test)
- [x] Every direction is persisted with `selected` and `orderIndex` in list order (unselected ones too); the search uses only selected ones; a plan with none selected is 400.  (automated tests (backend + frontend))
- [x] A saved unticked direction comes back unticked; ticking it and pressing Explore saves it as selected; an unchanged Explore writes nothing.  (automated tests)
- [x] The workspace keeps the participant's own title; Explore never renames or creates a workspace.  (by design: the plan endpoint never touches the title (backend test))
- [~] No direction label exceeds 7 words (typing, paste and AI output); a typed 8th word is ignored; column 2 never leaves the window.  (U1 + backend tests; the column-2 part needs a browser check)
- [~] Live-region messages are announced and focus never moves when suggestions appear.  (messages: automated test; "focus never moves" is tested in jsdom, to confirm with a screen reader)
- [x] Generation failure still allows custom directions and Explore.  (automated test)
- [x] Any card can be dragged to a new place, across the column break; the numbers stay at their slots; the cards close up with no gaps.  (automated tests drive dnd-kit's handlers; a real drag needs a browser check)
- [x] Dropping on the end slot makes a card last; the end slot is drawn in the next available position (no gap after the last card) and never moves a card between columns (8 and 7 cards, wide and narrow).  (structure tested; layout needs a browser check)
- [x] A reorder sends no request; Explore sends the selected cards in list order; regeneration keeps selected and custom cards in their slots; a batch that arrives mid-drag waits for the drop.  (automated tests)
- [x] A workspace that already has a plan shows its full saved plan on arrival (texts and directions in saved order, ticked as saved, no generation); an unchanged Explore opens the SERP without writing; a changed one replaces the plan. The Open/Update row remains for the 409 case and when the participant typed first.  (automated tests)
- [x] (earlier wording) A workspace that already has a plan offers "Open workspace  Or  Update workspace"; Update loads the saved texts and directions in saved order without a generation request, and Explore then replaces the plan (`replace: true`); a normal Explore never replaces.  (automated tests; row wrap and focus ring need a browser check)
- [~] Mouse drag feel, the black line, the end slot and a finger on a tablet.  (browser check)
- [ ] Keyboard reordering: not built (open-questions.md 8).

## Out of scope

Editing directions after Explore; a name field; the 👍/😐/👎 clarity control.

*Source: old spec 1, 1.1, 5.1, 7 (generate, create), 8.1.*
