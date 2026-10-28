# MINDS change ledger

One entry per functional change in minds-app, newest first. `/done` adds entries; the person updating the planning doc reads them.

**Doc status** says where the change stands in the planning document:
- `pending`: the planning-doc text, a figure or both do not cover it yet
- `v30` (or later version): covered in that version's text (figures may still be old; see the version's changes summary)
- `n/a`: no planning-doc impact (code-only fix, screen the plan does not describe)

Entry format:

```
### YYYY-MM-DD · <commit> · <short title>
- Change: what is different for the participant
- Why: the reason, in Telot's words; "not stated" if nobody said
- Affects: planning-doc sections and figures; spec files
- Doc status: v30 (rewritten 2026-10-26 to match 2f08f2c; figures still old) | vNN | n/a
```

Entries below the line marked SEEDED were rebuilt from minds-app commit history on 2026-10-25, not written at the time, so "Why" is mostly not stated. Fill it in from DECISIONS.md where you know it.

---

### 2026-10-26 to 2026-10-27 · up to 533d618 · SERP shows score and star again, no tag cap, Continue Last Activity gone, one Overview list, pastel colours on Saved results, name required, draft autosave
- Change: (read from the code at 533d618 by the four diff agents, 2026-10-28) tags on the results page print a number and a star again and every sub-goal rated above 0 is a tag (no cap of three, no ">>", a 0 shows nothing); the New tag shows whenever the suggestion is rated above 0; the Overview has no Continue Last Activity button, one "Sub-goals" list in plan order (ticking never moves a card, cards can be dragged, the All/Explored tabs are hidden behind `SHOW_DIRECTION_TABS`) and an Explore button that starts a new session; "where you left off" cards are Last Sub-goal (a button), Last Query, Last Saved; the Overview plus button adds a suggestion as selected; Saved results gives each sub-goal its own pastel colour, titles a session view "Saved Results for Session N" and shows "Continue searching" for a session; the panel reads "Sub-goals with saved results"; the Plan screen requires a workspace name, autosaves a draft, and asks before removing a sub-goal that has saved results (the removal deletes its saved results); one model setting serves every LLM call.
- Why: Telot (2026-10-26) and Orland (2026-10-27) in code comments; no reasons recorded except Orland's "hiding information that is valuable makes for poor UI design" (tag cap)
- Affects: plan Abstract, 1.1, 1.2, 2.1, 2.2, 2.3, 3, 4, 5, Keeping the Searcher in Control, Implementation Note, Task List; Figs 1, 2.1 to 2.3, 3, 4, 5 (still old); spec F1 to F6
- Doc status: v31 (text rewritten 2026-10-28 to match 533d618, at Telot's request; figures still old)
- CODE VS EARLIER DECISIONS: v31 follows the code. Two code behaviours contradict Telot's own 2026-10-25 decisions in this ledger: the results-page tags show score and star again (349a106 said removed for good), and the Overview plus button adds the suggestion as selected (the 2026-10-25 entry below says unselected). If those decisions stand, change the code and revert these two passages in the text.

### 2026-10-25 · e1506e3, f5672f1, c1c940b, 6280091, 6e38937, 81aec93, 2f08f2c · Marks on every screen, plain total bars, saved-results filter and title card
- Change: (read from the code at 2f08f2c by the four diff agents) direction marks are black (star = LLM, person = own) and follow the name on every screen; the number circle and per-session bar segments are switched off (`SHOW_COUNT_CIRCLE`, `SHOW_SESSION_BAR` = false, "hidden for now") and every bar is one plain blue bar with the count inside, "10+" past 10; the name and the bar open that direction's saved results; the saved tag has no check mark; Saved results has a multi-select direction filter with Reset (no "All directions" row), the Overview's title card, and one "Return to Search" / "Return to Workspace" button; the results-page header has a "Workspace" button, no Saved Results button; Add Custom hides Generate more.
- Why: Telot's dated decisions in code comments (2026-10-25); no reasons recorded
- Affects: plan 1.1, 2.1, 2.2, 2.3, 3, 4, 5, Task List; Figs 1, 2.1 to 2.3, 3, 4, 5
- Doc status: v30 (text rewritten 2026-10-26; figures still old)

### 2026-10-25 · 0fbd7d9 · Result-tag "?" explanation: names the sub-goal, the matching phrase and how it helps the goal; stricter topic match
- Change: the one-sentence reason behind a tag's "?" now follows three steps (sub-goal in its own words, the phrase in the record that addresses it, how that helps the goal). A result that only covers the sub-goal's wider field is rated at most 1 and its sentence says so plainly. Sentences are written with the ratings for the shown tags; any other sub-goal gets its sentence when "?" is first selected, and it is stored. `scores:reset` clears stored ratings so old wording can be regenerated.
- Why: Telot, 2026-10-25: the explanation is "better fetched" now
- Affects: plan 2.1 ("?" paragraph), Implementation Note (scoring paragraph); Fig 2 inset; spec F2, F3
- Doc status: v30

### 2026-10-25 · 1e6f305, 8c79d63 · Overview "New directions" section: plus, cross and "?" (Telot's description, 2026-10-25)
- Change: suggested new directions appear as a tag in the order of chips on result cards (placed by score) and in a "New directions" section on the Overview, each with New tag, "?" (explains how it came to be suggested), plus and cross. Telot: the plus adds it to the UNSELECTED list.
- Why: no separate suggestions list on the results page; the participant decides on the Overview
- Affects: plan §2.2, §5, Keeping the Searcher in Control; Fig 2.3 (panel), Fig 5 (no section); spec F4, F5
- Doc status: v30
- CODE MISMATCH: `promoteEmerging` (backend/services/emergingService.js:233) creates the direction with `selected: true` and flips an existing unselected one to selected, and YourSessionsPage.jsx:102 says "Add puts the suggestion in the plan (selected)". The text follows Telot's description (unselected). Fix the code or the text.

### 2026-10-25 · 349a106 · SERP chips: score and star removed; order shows fit
- Change: tags on a result show no score or star; the left-most tag is the best fit and the rest follow. Results are ordered by the active sub-goal's score, best first (each page of 10 on its own). Scores are still computed and kept (code is commented out, not deleted).
- Why: Telot, 2026-10-25: the star idea is gone for good; the order of the tags and of the results tells the user what fits best (for the CHIIR demo paper)
- Affects: plan Abstract, §2.1 to 2.3, §3, §5, Keeping the Searcher in Control, Implementation Note, Task List; Figs 2.1 to 2.3, 3, 4; spec F3
- Doc status: v30

### 2026-10-25 · 6195d45, 40f4e09 · Directions panel and Overview cards: total bar with count thumb; session segments and number circle hidden
- Change: (from the commit subjects, not re-read) the SERP panel and the Overview cards show one total bar with a count thumb, a search icon on the left and a grey name for never-searched directions; session segments and the number circle are hidden.
- Why: not stated
- Affects: plan §4 (describes circles and per-session segments), Figs 2 and 5; spec F3, F5
- Doc status: v30 (rewritten 2026-10-26 to match 2f08f2c; figures still old)

### 2026-10-25 · 7d91ee4, ca96c3e, d32df64, f6bb349, aad78da, 5de1dd6 · Header and title-card changes on the Overview and Saved results
- Change: (from the commit subjects, not re-read) Saved Results button moves before Continue Last Activity; Saved results gets the Overview's title card; Overview button (eye icon) in the header; workspace name on the Overview links to its Plan page.
- Why: not stated
- Affects: plan §3, §4, §5; Figs 3, 4, 5; spec F5, F6
- Doc status: v30 (rewritten 2026-10-26 to match 2f08f2c; figures still old)

### 2026-10-25 · 8c79d63, 1e6f305 · New-direction explanation reworded; New tag blue everywhere
- Change: (from the commit subjects, not re-read) the explanation names the saved results, says the topic kept appearing, then how it helps the goal; "?" beside the New tag opens it on the Overview.
- Why: not stated
- Affects: plan §2.2; spec F4
- Doc status: v30 (explanation described in 2.2; the blue colour of the tag is not mentioned)

### 2026-10-25 · bdac003 · SERP panel: bar overflow shows as "+N" inside the bar
- Change: past 10 saved, the results-page directions panel clips the bar and shows "+N" inside the right end of the bar, with no "more" text. The Overview still shows "+N more" in the title row.
- Why: not stated
- Affects: plan §4 (text says "+N more" at the right end of the name line), Fig 2; spec F3
- Doc status: v30 (rewritten 2026-10-26 to match 2f08f2c; figures still old)

### 2026-10-25 · 2973394 · "What you might explore" panel removed from the results page
- Change: a suggested new direction now shows only as a "New" tag on result cards. The panel and its add and dismiss rows are gone from the SERP right panel.
- Why: not stated
- Affects: plan §2.2, §5 (Cross-Session Support), Keeping the Searcher in Control, Fig 2.3; spec F3, F4
- Doc status: v30 (text; Fig 2.3 still shows the panel)

### 2026-10-25 · 2973394 · Overview asks before opening an unselected direction
- Change: opening an unselected direction, or Continue Last Activity when the last direction is unticked, shows "Direction not selected … Move it to Selected directions and continue search?"; "Yes, select and search" selects it and opens the results page.
- Why: the results page lists selected directions only
- Affects: plan §4 and §5; spec F5
- Doc status: v30 (rewritten 2026-10-26 to match 2f08f2c; figures still old)

### 2026-10-25 · 2973394 · Return button reads "Return to Overview" from the Overview
- Change: the Saved results header button says "Return to Overview" when the view was opened from the Overview (was "Return to Search").
- Why: not stated
- Affects: plan §3 (Return behaviour is described, the label is not); spec F6
- Doc status: v30 (rewritten 2026-10-26 to match 2f08f2c; figures still old)

### 2026-10-25 · 2973394 · Plan screen error text says "Fill both fields"
- Change: the 400 error text said "three fields"; there are two.
- Why: wording bug
- Affects: none
- Doc status: n/a

### 2026-10-25 · 7bde993 · Workspaces list card keeps only Open plan and menu buttons
- Change: stats removed from workspace cards; round Open plan button and a menu button.
- Why: not stated
- Affects: none (the planning document does not describe the workspaces list)
- Doc status: n/a

### 2026-10-25 · a52ed50 · Plan screen: Gemini star after AI-proposed directions
- Change: AI-proposed directions show a star after the label; directions the participant added or edited show a person icon. Overview shows the person icon only.
- Why: tell AI-proposed directions from the participant's own at a glance
- Affects: plan §1.1, Fig 1; spec F1
- Doc status: v30

### 2026-10-25 · 209f0cd · Overview bar is full at 10 saved, "+N more" in the title row
- Change: all direction bars share one scale and are full at 10 saved; beyond that the newest segment shows what fits.
- Why: professor's request (2026-10-25)
- Affects: plan §4; spec F5
- Doc status: v29

### 2026-10-25 · 695de4e · Session tiles show pills only for directions with saved results
- Change: no pill list when nothing was saved in the session.
- Why: not stated
- Affects: plan §4; spec F5
- Doc status: v29

### 2026-10-25 · a5a142d · Saved results right panel "Directions with saved results"
- Change: lists All directions and each direction with its saved count; picking one filters the list in place.
- Why: not stated
- Affects: plan §3, Figs 3 and 4 (right side empty in the figures); spec F6
- Doc status: v30

### 2026-10-25 · 0c39fe2 · Saved chips drop the word "Saved"
- Change: check icon and solid blue stay; the accessible name still says saved.
- Why: not stated
- Affects: plan §2.1, §3; spec F3
- Doc status: v30

### 2026-10-25 · 7a0b0e7 · Overview: Generate more, Add Custom, tick circle, All/Explored filter
- Change: the Overview lists unselected directions too; tick circle selects or unselects (the last selected one cannot be unticked); Generate more and Add Custom as on the Plan screen; 30 directions at most.
- Why: not stated
- Affects: plan §1.1, §4, Fig 5; spec F5
- Doc status: v30

### 2026-10-25 · 7e3042e · New workspace opens Plan with the name field ready
- Change: the title can be left empty and renamed later.
- Why: not stated
- Affects: plan §1.1, §2.3, Fig 1; spec F1
- Doc status: v30

### 2026-10-25 · f78ec5b · SERP: search icon per direction, dropdown removed, ?★ chip
- Change: each direction in the right panel has a search icon that types its stored query into the search box; the Search Direction dropdown is gone; a direction added after a result was rated shows "?★"; the best-on-page chip is plain with a blue score and star.
- Why: not stated
- Affects: plan §1.2, §2.1, §2.3, §5, Figs 2.1 to 2.3 (still show the dropdown); spec F2, F3
- Doc status: v30

### 2026-10-24 · 7e8d120 · Plan: row-by-row numbering, Generate more and Add Custom in the next free cell
- Change: numbers run across the rows; the new buttons fill the next free cell.
- Why: not stated
- Affects: plan §1.1, Fig 1; spec F1
- Doc status: v30

### 2026-10-23 · 2097fe8 · Overview header card; SERP bars use Overview session colours
- Change: breadcrumb, title and Continue Last Activity sit in one card; saved-only directions count in session chips; same session colours on both screens.
- Why: not stated
- Affects: plan §4, Fig 5; spec F5
- Doc status: v30

### 2026-10-23 · df19aa1 · Running session tile shows a breathing blue "Running" status
- Change: newest session, last activity within the past hour.
- Why: not stated
- Affects: plan §4, Fig 5; spec F5
- Doc status: v30

### 2026-10-23 · 2ef1eb4 · Saved results from the Overview: Return goes back to the Overview, no search box
- Change: see title.
- Why: not stated
- Affects: plan §3; spec F6
- Doc status: v30

<!-- SEEDED ends here. New entries go above the first entry, under the "---" line. -->
