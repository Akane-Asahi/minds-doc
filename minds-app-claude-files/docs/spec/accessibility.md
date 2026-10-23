# Accessibility requirements (requirements, not polish)

They follow from the persona (Jamie Chen, 19, first-year, has dyslexia) and the study population.
Baseline already went through a WCAG 2.2 AA pass; reuse its tokens and patterns where they fit and
re-measure every new mockup.

## Global

- Typeface: Atkinson Hyperlegible or Lexend, generous line spacing. Baseline's theme already uses
  **Lexend Deca** (`frontend/src/theme/theme.js`); keep it.
- Status is never colour alone: colour plus icon plus text label. All chip emphasis tiers pass WCAG
  AA (4.5:1 text, 3:1 large text and meaningful non-text such as borders, icons, outlined circles).
- Never render a raw percentage as a headline coverage number; counts or categories only.
- Never lighten text to mean "quiet", "faded", "empty" or "disabled". Use the surface (lighter or
  dashed border, flatter fill, paler icon) **plus a text cue** ("New", "0 saved", "No Session
  Record"). Text stays at `--text-muted` or darker.
- Respect `prefers-reduced-motion` for any ring or transition animation.
- Save is a single control, operable by keyboard alone, no read or expand step first.
- State management: React Query (or equivalent) for server state; Context for local UI state.

## Required contrast fix (rule for the whole product)

1. One muted text token `--text-muted: #5c5647` for all secondary text. It measures 4.75:1 on the
   grey field `#d6d0c2`, 5.70:1 on page background `#e7e3da`, 6.47:1 on tile background `#f3f1ec`.
   No lighter colour for text that carries meaning.
2. Non-text parts that carry meaning (checkbox outlines, outlined zero-count circles, chip borders)
   reach 3:1 against their background.
3. Add a build test that computes the ratio for every text/background token pair and fails under
   4.5:1 (3:1 for large text and non-text).
4. Re-measure on the final designs.

Mockup failures measured in the original audit (fix in the designs): Screen 3 "No Session Record" and
"0 saved — N reviewed" (1.54; now hidden text, see below), Screen 3 name line (1.85, line removed), Screen 3 duration and placeholder (3.38),
Screen 1 unselected "new" labels (2.08), SERP "What you might explore" labels (2.08), SERP description
text (2.97). Faded chips are the same grey family and are assumed to fail until re-measured.

## Per screen

- **Plan Workspace (F1):** directions list updates asynchronously, so announce in a `polite` live
  region ("Generating search directions", then "Search directions ready" or the error); **focus never
  moves on its own** when suggestions appear. Direction items are real checkboxes with labels. There
  is no sparkle or star icon; AI items have the "?" button (accessible name "Why? <label>"), every item has Edit ("Edit <label>") and Remove ("Remove <label>"); the "?" badge appears on hover, on focus within the card, while open, and always on touch screens (Your sessions also tags custom ones with text). Directions can be reordered by **mouse drag and by touch (press-and-hold)** only; **there is no keyboard way to reorder yet** (a known gap, Telot to decide: dnd-kit's keyboard sensor needs extra code to find an insertion point, and move buttons or a move mode were scrapped for simplicity). Everything else on the screen is keyboard-operable and order does not have to be changed (the AI order is a valid order). The drop-position line is solid black 3px (3:1 against the page and the cards, in the contrast test); dnd-kit's own announcements are switched off because they would read meaningless text for a mouse drag. All text meets AA. Directions are one `<ul>` (the two columns are layout only, so reading order is the list order). Each label is at most 7 words and one line; if it is still cut with an ellipsis, the full text stays in the accessible name and `title`. The "N of 7 words" count under the Add field is visible text.
- **SERP (F2, F3):** chips are native `<button>` with `aria-pressed` and an accessible name including
  direction and score as text, e.g. "Save under Mental / emotional well-being, score 4 out of 5" (never
  stars alone). `?` is its own button with `aria-expanded`. Saving announces in a polite live region
  ("Saved under Public parks. 3 results saved."). The New pill's name states it: "New direction, not in
  your plan: Children, score 5 out of 5. Adds it to your plan and saves this result". The search field
  is a labelled input; the icon is a real button; Enter submits; results replace the list **without
  moving focus**; the live region announces "Loading results" then the new count. Faded chips, grey
  chips, the "What you have explored" circles and "What you might explore" rows all meet AA.
- **Your sessions (F5):** each bar segment is a native `<button>` named with session, date, count and
  direction ("Session 2, Aug 9, 2026: 4 saved under Green Space. Open these results"). `+N` is always
  visible; the grey track is `aria-hidden`. The card's main action is a link named "Search {direction}";
  segments and the count circle are **not nested** inside it. The count circle is a button named "{n} saved
  under {direction}. Open these results". Focus order: header, breadcrumb, Continue Last Activity, tiles, then
  each card's circle, link and segments. Pills carry the full direction label as text for screen readers (the
  visible two-word form is `aria-hidden`) and the saved mark as text ("+4 saved", "0 saved"). **A card with 0
  saved shows an empty track and no visible text (Telot, 2026-10-17, overriding the visible-text-cue rule for
  this one case); it keeps hidden text for screen readers: "0 saved — N reviewed" or "No Session Record".** The
  count circle's number is always visible text, so its light outline is decorative. The New tag is text. Hover
  linking also works on keyboard focus, visibly without colour alone (3px outline). Session list is newest
  first while bars run oldest first (intentional; badges and linking connect them). Grey text on cards and
  tile secondary text meet AA (`text.secondary` on card 4.5:1).
- **Saved results views (F6):** same as SERP cards. The header is the SERP's (search box disabled, Return to
  Search). The scope heading is an `h1`, visually hidden because the breadcrumb ends in the same scope. Each
  session group heading is an `h2` (card titles are `h2` too, as on the SERP). The three counts are visible
  numbers with screen-reader labels ("9 saved results"); icons are decorative. Chips are native buttons with
  `aria-pressed` and names like "Save under Physical health benefits, score 4 out of 5, saved"; saved is solid blue
  with the text "Saved", unsaved is grey, so state is never colour alone.

## Deferred (do not build now)

Session Recap Capsule text in an ARIA live region (deferred with the recap feature).
