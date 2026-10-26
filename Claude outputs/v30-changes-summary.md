# v30 changes summary

v30 is v29 plus text edits that bring the planning document in line with the minds-app code at commit 209f0cd (2026-10-25). The edits come from running plan-diff, serp-diff, sessions-diff and save-diff against v29. Only text changed: no figure, table, reference or heading was touched. The file passes the docx validator against v29.

## What changed in the text

**Front matter**
- "Project Revised" date: Oct 15, 2026 → Oct 25, 2026.

**1.1 Planning: Goal Decomposition**
- The LLM generates sixteen candidates in one call, shows eight and keeps eight in reserve (was "about eight").
- "Add search direction" is now **Add Custom**; new **Generate more** takes the next suggestion from the reserve and asks for a new batch only when the reserve is empty; 30 sub-goals at most; both buttons add the sub-goal unselected.
- The Workspace Overview lists unselected sub-goals too, with a tick to select or unselect (at least one stays selected). Before: "only the selected sub-goals are shown on the Workspace Overview".
- "Why?" card opens above the candidate with an arrow (was "beside").
- The reason is kept with every proposed sub-goal, selected or not (was "each sub-goal that Jamie selects").
- New sentence on the origin mark (added after plan-diff on minds-app a52ed50): a blue four-pointed star after the label for a sub-goal the LLM proposed, a round person icon for one Jamie added or edited; always visible, unlike the "Why?" button. First screen only: the Overview shows the person icon but no star on proposed sub-goals.

**1.2 Planning: Query Generation**
- The system now writes the query in the search box instead of running it. Applies to the first query for a sub-goal, the "mental health greenspace" example, and returning to a sub-goal.

**2.1 Evaluation: Relevance and Usefulness**
- Best-on-page tag is no longer "light blue": it is a plain tag with a blue rating and star. Saved tag is solid blue with a check mark.
- New sentence on "?★": a sub-goal added after a result was rated shows "?★", and its "(?)" says how to get a rating.

**2.3 Switching and Adding Sub-Goals**
- Each sub-goal in the right panel has a search icon. Pressing it types that sub-goal's last query into the search box and leaves the cursor there; the results stay until Jamie searches. What is sent from the box is stored under the sub-goal whose icon was pressed last. The results page searches the start sub-goal's query at once when it opens.
- A sub-goal added later is rated from the next search on.
- New workspace: the first screen opens with the title field ready, and the title can be left empty (was "with its own title").

**Stars and numbers removed from the results page (2026-10-25, commit 349a106; Telot: removed for good, for the CHIIR demo paper)**
- Fit is now shown by order only. The tag order on each result runs from best fit to weaker fit, and the results are ordered by fit to the sub-goal being searched, best at the top. Ratings (0 to 5) are still computed and stored but never shown.
- Rewritten in: Abstract; 2.1 (three paragraphs); 2.2 and its closing line; 2.3; 3; 5; Keeping the Searcher in Control; Implementation Note; Task List (relevance ordering). The best-on-page blue score and the "?★" chip are gone from the text.
- Accuracy note: the first page of results is sorted once by the active sub-goal's rating; each "Load more" page of 10 is sorted among itself and added below, so "best at the top, falling down the page" holds within each page of 10, and the text says so.
- Still true and kept: the Plan-screen star after AI-proposed sub-goals (a different star).

**New directions (2026-10-25, Telot's description)**
- No "What you might explore" panel on the results page. A suggestion shows as a "New" tag on result cards, placed in the tag order by its fit, and in a "New directions" section on the Overview with "?" (how it came to be suggested), plus (adds it to the unselected list) and cross (dismiss).
- Rewritten in 2.2 (two paragraphs), 5 and Keeping the Searcher in Control.
- Code mismatch to settle: the plus button currently adds the direction as selected (`emergingService.js:233`). The text says unselected.
- Figures: Fig 2.3 still shows the panel; Fig 5 has no "New directions" section.

**The "?" explanation on a result tag (2026-10-25, commit 0fbd7d9)**
- 2.1 now says what the sentence does and how it is made. Three steps: name the sub-goal in its own words, say what in the record (title, subject terms, abstract) addresses that exact topic by quoting or paraphrasing a phrase, say how that helps the goal. About 20 words, no hedging, no rating shown. Content follows the rating (high: how it covers it; middle: which part; low: loosely related; 0: what the result is about instead). It must match the sub-goal's specific topic, not only its wider field; no abstract gives "Based on title and subjects only".
- How it is fetched: written with the ratings for the shown tags (top three above 0, plus the New tag); any other sub-goal gets its sentence the first time "(?)" is selected ("Loading the reason…", retry by closing and opening). Stored with the rating, so the same words show every time.
- Implementation Note: the scoring paragraph now mentions the reason's three parts and the stricter rubric (a shared general word earns 0, a match to only the wider field earns at most 1).
- The example sentence in 2.1 is an illustration written for Jamie's goal, not output from the app.
- Sentences already stored keep their old wording until `npm run scores:reset` is run (stored ratings are final).
- Figures: the inset in Fig 2 shows an older sentence.

**3 Organization**
- Saved tag shows a check mark.
- New right panel "Directions with saved results" with counts and an in-place filter; Return goes back to the Overview (no search box) when the view was opened from the Overview.

**4 Monitoring**
- Panel heading "Directions You Have Explored" → "Directions for this session".
- Segment colours are the same on the results page and the Overview (newest near black, then slate, then light grey with outline).
- Overview: header card, breathing blue "Running" status, six-pill cap with "+N more", All/Explored filter with Selected / Unselected / Explored / Unexplored lists, tick circle, person icon on custom sub-goals, Generate more and Add Custom.

**5 Cross-Session Support**
- Directions panel wording follows the search icon; "Add search direction" → "Add Custom or Generate more".

## Not changed in the text, for Telot to decide or fix

Doc and code disagree, and the right side is not clear:
1. **Model for each task.** The doc says a capable model for sub-goals and a lighter one for queries (1.1, 1.2, Implementation Note). The code uses one model (`LLM_MODEL`) for every call. Change one side.
2. **"Reason" call.** A "?" on a saved-view chip with no stored reason makes a model call (`SavedResultCard.jsx:50-55`); the doc's list of AI components does not include it.
3. **Last-activity cards.** The doc says last sub-goal searched, last result saved, last query run. The code uses the direction selected at session end and its newest stored query (2026-10-18 decision, "Last Query" still to confirm).
4. **Bars past 10 saved on the results page.** The v30 text says "+N more" at the right end of the name line. That is now true only on the Overview. Since commit bdac003 the results-page panel shows "+N" inside the right end of the bar, with no "more" text. Reword §4, or make the two screens match.
5. **Edit and remove behaviour.** Editing a sub-goal that has saved results creates a new custom one and leaves the old one unticked; a removed sub-goal with saves returns unticked at the end. Not described in the doc.
6. **Keyboard reordering** of sub-goals does not exist (drag by mouse or touch only); the doc says "drag any sub-goal".

Code defects found by the agents (not doc edits):
- Overview: an ended session still shows "Running", and a New tag stays up to an hour (`overviewController.js:49` ignores the stored `endedAt`).
- Saved results: choosing a name in the right panel drops the router state (`SavedResultsPage.jsx:90`), so the search box probably returns and Return goes to the SERP. Needs a click-through to confirm.

## Commits after v30's first push that the text does not cover yet

Found by reading minds-app a52ed50 (2026-10-25). Not edited, because they go beyond the star change:
- **"What you might explore" panel is gone from the results page** (2973394). A suggested direction now shows only as a "New" tag on result cards. v30 still describes the panel in 2.2, in 5 (Cross-Session Support) and in Keeping the Searcher in Control, and Fig 2.3 shows it.
- **Opening an unselected direction on the Overview** asks first ("Direction not selected … Move it to Selected directions and continue search?"), then selects it and opens the results page. Continue Last Activity does the same when the last direction is unticked. This fixes the earlier defect where it opened the first selected one.
- **Return button** reads "Return to Overview" when Saved results was opened from the Overview (was "Return to Search"). v30 describes the behaviour but not the label.
- **Workspaces list**: each card keeps only a round "Open plan" button and a menu button; the stats were removed (7bde993). The planning document does not describe the list, so nothing to edit unless you want it added.
- **Fixed in code, no doc change needed:** the Plan screen error text now says "Fill both fields"; Add Custom at 30 directions on the Overview shows a limit message.

## Figures are out of date and need new screenshots

The text edits above are not matched by the images. Replace these:
- **Fig 2.1 to 2.3, 3 and 4**: chips still show "5★ …" scores. Re-take them without scores.
- **Fig 1**: shows "Plan your new project", three fields, a sparkle on every row (including Jamie's own sub-goals, which now carry a person icon instead), a dashed "Add search direction" and no Edit/Remove. Code has two fields, three bordered panels, Edit and Remove on every row, Generate more and Add Custom.
- **Fig 2.1 to 2.3**: still show the Search Direction dropdown, "DIRECTIONS YOU HAVE EXPLORED", light blue best chips and a sparkle on AI sub-goals.
- **Fig 3 and Fig 4**: right side empty; two counts shown, code has three; "Description:" label and "Journal article" type label that the code does not have.
- **Fig 5**: S3/S2/S1 badges, a "Community access +0" pill, arrows instead of tick circles, no Unselected list, no Running status, no header card, dashed "Add search direction".

## Run of 2026-10-26: all four diff agents against minds-app 2f08f2c

Text edited in v30 (26 edits, code treated as current wherever it carries a dated decision by Telot):
- **1.1**: marks are black and follow a direction's name on every screen; generation starts when a field is left with both texts filled and replaces only unticked proposed directions; Generate more is hidden while Add Custom is open; a direction with saved results comes back unticked at the end if removed or renamed.
- **2.1**: saved tag is solid blue, no check mark. **2.2**: New tag can sit anywhere (up to four tags); the Overview explanation names up to three saved titles, says the topic kept appearing and looks highly relevant, then one sentence on how it helps; a cross on the New tag dismisses it. **2.3**: from the Overview search icon the query is only typed, not searched; Add search direction on the results page starts selected.
- **3**: right panel has no "All directions" row, several names can be chosen, Reset clears; saved cards show tags in planning order; title card, breadcrumb and one Return button ("Return to Workspace" / "Return to Search"); one view with two filters; "?" on a saved tag can write its sentence on first use.
- **4**: panel rewritten to what is shown: name, mark, search icon, one plain bar with the count inside, grey name until something happened, "10+" past 10, name or bar opens saved results; no circle, no session segments, no session colours, no "+N more" on bars. Overview: header card says "Workspace" and holds Saved Results; tick circle, marks, name and search icon behaviour, the "Direction not selected" question; tile entries are per visit (fixes the "at most six sub-goals" slip); "saved or shown".
- **5**: the Saved Results button is in the Overview header card; name or bar (not circle or segment) opens a direction's results; Workspace button on the results page leads back. **Task List**: "per-session progress bars" now "progress bars".
- Ledger: the six pending entries are closed as v30; a new entry covers e1506e3, f5672f1, c1c940b, 6280091, 6e38937, 81aec93, 2f08f2c. Sync marker moved to 2f08f2c.

Not edited, waiting for Telot (each was found by the agents):
1. Plus button and New-tag click add the direction **selected** in code; v30 says unselected for the plus button. The New-tag click has to stay selected (the results page lists selected directions only).
2. **One model for every call** (`LLM_MODEL`); 1.1, 1.2 and the Implementation Note still say a capable model for sub-goals and a lighter one for queries.
3. Session segments and the number circle are "hidden for now" by two flags. v30 now follows the shipped look; switch the flags back on and the old text would need restoring.
4. "The rubric is set empirically against searchers' own judgments" (Implementation Note): the scoring bench compares prompt variants against run-to-run noise only.
5. Screen readers hear "score N out of 5" on tags and "best match on this page", against "the searcher never sees these numbers".
6. Return after choosing a name in the Saved results panel probably loses "opened from the Overview" (search box returns, Return goes to the results page). Return to Search goes to the first chosen direction, not the one left.
7. Ticking a direction on the Overview moves it in the saved order, so ties no longer follow only the Plan-screen order.
8. No keyboard way to reorder directions (mouse and touch only).
9. End Session link on the results page (cuts sessions in the study logs); after End Session the tile still reads "Running" for up to an hour (`overviewController.js:59`).
10. Last Query card shows the newest stored query for the last direction, which may never have been run.
11. Cards on the first page appear in library order and re-sort when ratings arrive (a few seconds).
12. Implementation Note counts four AI components; the code also has the on-demand reason call (5.3r).
13. Overview h1 is "Workspace" in code; v30 prose still calls the screen "Workspace Overview".

Figures still show the 2026-10-20 design and need new screenshots from 2f08f2c: Fig 1; Figs 2.1 to 2.3 (dropdown, scores, "Why this may help" line, circles, segments, the "What you might explore" list in 2.3); Figs 3 and 4 (header button, scores, no title card, no right panel, two counts); Fig 5 (Project Overview title, S badges, circles, segments, no Unselected list, no New directions section). Fig 1 caption could read "Plan Workspace".

## Method

Four read-only diff agents compared v29 with minds-app 209f0cd by reading the code. Nothing was run, and nothing was checked in a browser, by keyboard or with a screen reader. The planning document's v29 text came from the minds-doc repo (commit 5c08af8).
