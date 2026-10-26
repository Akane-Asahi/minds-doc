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
- Doc status: pending | vNN | n/a
```

Entries below the line marked SEEDED were rebuilt from minds-app commit history on 2026-10-25, not written at the time, so "Why" is mostly not stated. Fill it in from DECISIONS.md where you know it.

---

### 2026-10-25 · 349a106 · SERP chips: score and star removed; order shows fit
- Change: tags on a result show no score or star; the left-most tag is the best fit and the rest follow. Results are ordered by the active sub-goal's score, best first (each page of 10 on its own). Scores are still computed and kept (code is commented out, not deleted).
- Why: Telot, 2026-10-25: the star idea is gone for good; the order of the tags and of the results tells the user what fits best (for the CHIIR demo paper)
- Affects: plan Abstract, §2.1 to 2.3, §3, §5, Keeping the Searcher in Control, Implementation Note, Task List; Figs 2.1 to 2.3, 3, 4; spec F3
- Doc status: v30

### 2026-10-25 · 6195d45, 40f4e09 · Directions panel and Overview cards: total bar with count thumb; session segments and number circle hidden
- Change: (from the commit subjects, not re-read) the SERP panel and the Overview cards show one total bar with a count thumb, a search icon on the left and a grey name for never-searched directions; session segments and the number circle are hidden.
- Why: not stated
- Affects: plan §4 (describes circles and per-session segments), Figs 2 and 5; spec F3, F5
- Doc status: pending

### 2026-10-25 · 7d91ee4, ca96c3e, d32df64, f6bb349, aad78da, 5de1dd6 · Header and title-card changes on the Overview and Saved results
- Change: (from the commit subjects, not re-read) Saved Results button moves before Continue Last Activity; Saved results gets the Overview's title card; Overview button (eye icon) in the header; workspace name on the Overview links to its Plan page.
- Why: not stated
- Affects: plan §3, §4, §5; Figs 3, 4, 5; spec F5, F6
- Doc status: pending

### 2026-10-25 · 8c79d63, 1e6f305 · New-direction explanation reworded; New tag blue everywhere
- Change: (from the commit subjects, not re-read) the explanation names the saved results, says the topic kept appearing, then how it helps the goal; "?" beside the New tag opens it on the Overview.
- Why: not stated
- Affects: plan §2.2; spec F4
- Doc status: pending

### 2026-10-25 · bdac003 · SERP panel: bar overflow shows as "+N" inside the bar
- Change: past 10 saved, the results-page directions panel clips the bar and shows "+N" inside the right end of the bar, with no "more" text. The Overview still shows "+N more" in the title row.
- Why: not stated
- Affects: plan §4 (text says "+N more" at the right end of the name line), Fig 2; spec F3
- Doc status: pending

### 2026-10-25 · 2973394 · "What you might explore" panel removed from the results page
- Change: a suggested new direction now shows only as a "New" tag on result cards. The panel and its add and dismiss rows are gone from the SERP right panel.
- Why: not stated
- Affects: plan §2.2, §5 (Cross-Session Support), Keeping the Searcher in Control, Fig 2.3; spec F3, F4
- Doc status: pending

### 2026-10-25 · 2973394 · Overview asks before opening an unselected direction
- Change: opening an unselected direction, or Continue Last Activity when the last direction is unticked, shows "Direction not selected … Move it to Selected directions and continue search?"; "Yes, select and search" selects it and opens the results page.
- Why: the results page lists selected directions only
- Affects: plan §4 and §5; spec F5
- Doc status: pending

### 2026-10-25 · 2973394 · Return button reads "Return to Overview" from the Overview
- Change: the Saved results header button says "Return to Overview" when the view was opened from the Overview (was "Return to Search").
- Why: not stated
- Affects: plan §3 (Return behaviour is described, the label is not); spec F6
- Doc status: pending

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
