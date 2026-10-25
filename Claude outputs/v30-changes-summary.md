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

**1.2 Planning: Query Generation**
- The system now writes the query in the search box instead of running it. Applies to the first query for a sub-goal, the "mental health greenspace" example, and returning to a sub-goal.

**2.1 Evaluation: Relevance and Usefulness**
- Best-on-page tag is no longer "light blue": it is a plain tag with a blue rating and star. Saved tag is solid blue with a check mark.
- New sentence on "?★": a sub-goal added after a result was rated shows "?★", and its "(?)" says how to get a rating.

**2.3 Switching and Adding Sub-Goals**
- Each sub-goal in the right panel has a search icon. Pressing it types that sub-goal's last query into the search box and leaves the cursor there; the results stay until Jamie searches. What is sent from the box is stored under the sub-goal whose icon was pressed last. The results page searches the start sub-goal's query at once when it opens.
- A sub-goal added later is rated from the next search on.
- New workspace: the first screen opens with the title field ready, and the title can be left empty (was "with its own title").

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
4. **Doc says bars are full at 10 saved with "+N more" on the results page.** Only the Overview does this; the SERP panel does not clip (`DirectionsPanel.jsx:101-135`). Fix the code, or make the doc say Overview only.
5. **Edit and remove behaviour.** Editing a sub-goal that has saved results creates a new custom one and leaves the old one unticked; a removed sub-goal with saves returns unticked at the end. Not described in the doc.
6. **Keyboard reordering** of sub-goals does not exist (drag by mouse or touch only); the doc says "drag any sub-goal".

Code defects found by the agents (not doc edits):
- Overview: an ended session still shows "Running", and a New tag stays up to an hour (`overviewController.js:49` ignores the stored `endedAt`).
- Overview: clicking an unselected card, or Continue Last Activity when the last sub-goal is unticked, opens the SERP on the first selected one (`MindsSerpPage.jsx:127-136`).
- Saved results: choosing a name in the right panel drops the router state (`SavedResultsPage.jsx:90`), so the search box probably returns and Return goes to the SERP. Needs a click-through to confirm.
- Header button still reads "Return to Search" when it goes to the Overview (`MainHeader.jsx:240`).
- "Fill the three fields" error text on the Plan screen; there are two fields (`useWiredPlanModel.js:61`, `planController.js:106`).
- Add Custom at 30 sub-goals on the Overview shows the 7-word message instead of a limit message (`YourSessionsPage.jsx:48`).

## Figures are out of date and need new screenshots

The text edits above are not matched by the images. Replace these:
- **Fig 1**: shows "Plan your new project", three fields, sparkles, a dashed "Add search direction" and no Edit/Remove. Code has two fields, three bordered panels, Edit and Remove on every row, Generate more and Add Custom.
- **Fig 2.1 to 2.3**: still show the Search Direction dropdown, "DIRECTIONS YOU HAVE EXPLORED", light blue best chips and a sparkle on AI sub-goals.
- **Fig 3 and Fig 4**: right side empty; two counts shown, code has three; "Description:" label and "Journal article" type label that the code does not have.
- **Fig 5**: S3/S2/S1 badges, a "Community access +0" pill, arrows instead of tick circles, no Unselected list, no Running status, no header card, dashed "Add search direction".

## Method

Four read-only diff agents compared v29 with minds-app 209f0cd by reading the code. Nothing was run, and nothing was checked in a browser, by keyboard or with a screen reader. The planning document's v29 text came from the minds-doc repo (commit 5c08af8).
