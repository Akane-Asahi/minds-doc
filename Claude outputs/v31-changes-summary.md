# v31 changes summary

v31 is v30 plus text edits that bring the planning document in line with the minds-app code at commit 533d618 (2026-10-27). The edits come from running plan-diff, serp-diff, save-diff and sessions-diff against v30 on 2026-10-28; their briefs are in this folder. Made at Telot's request ("fix everything the code does"), starting from the copy of v30 in this repo, not the one in Downloads. Only text changed: no figure, table, reference or heading was touched. The file passes the .docx validator.

## Two edits that go against Telot's own earlier decisions

The code does these, so v31 says them. If the decisions below still stand, fix the code and revert the passage.

- **Score and star are shown on the results page again.** v30 said they were removed for good (2026-10-25, commit 349a106). The code (`DirectionChip.jsx`) says the SERP shows them again since 2026-10-26. Saved results still hides them.
- **The Overview plus button adds a suggestion as selected** (`emergingService.js:233`). v30 said unselected, following Telot's 2026-10-25 description.

## What changed in the text

**Front matter and Abstract**
- "Project Revised": Oct 25, 2026 → Oct 28, 2026.
- Abstract: a returning searcher can "reopen the last sub-goal, resume any earlier session, or switch to any sub-goal" (was "continue the last activity").

**1.1 Planning: Goal Decomposition**
- The first screen asks for a workspace name; Explore stays off until the name, both texts and one selected sub-goal are in place.
- "About sixteen" candidates (the server accepts 8 to 20); the reserve is lost on reload.
- A draft of the plan is autosaved a moment after each change; Explore saves everything.
- Removing a sub-goal that has saved results asks first and deletes those results; renaming still keeps them.
- Reordering is mouse or touch only (no keyboard way yet).
- The Overview is one list in plan order; ticking does not move a card; cards can be dragged.
- A proposal Jamie reworded shows the person icon beside the star; a sub-goal added from a suggestion carries no mark.
- Sub-goal generation: "the step where the quality of the model matters most" (was "its most capable model").

**1.2 Query Generation**
- The prototype uses the same model for queries as for everything else.

**2.1 Relevance and Usefulness**
- Every tag shows its rating as a number and a star (for example 4★).
- Every sub-goal rated above 0 is a tag; no cap of three; no ">>" button; a sub-goal rated 0 has no tag, so a result cannot be filed under it from the results page.
- The best-rated tag on the page has its number and star in blue and is announced as the best match to screen readers (was "no tag is marked as the best match").
- Cards first appear in library order, with placeholders, and are reordered once when the ratings arrive.
- "(?)" sentences are written with the ratings for the three highest-rated tags and the New tag; any later tag gets its sentence on first selection. A sub-goal added after rating shows "?★".

**2.2 Discovering New Direction**
- The New tag shows whenever the suggestion is rated above 0 (was "among the three highest"; "four tags in all" removed).
- Overview section renamed "New sub-goals"; the plus button adds the suggestion as selected.

**2.3 Switching and Adding Sub-Goals**
- "Add search sub-goal" button; the new-workspace name is required and a name already in use is refused (was "can be left empty").
- The results page opens on the last sub-goal from the Last Sub-goal card; continuing a session from its saved results restores it without a new search.

**3 Organization**
- Tags are every sub-goal rated above 0 (no ">>").
- Saved results: each sub-goal has its own pastel colour (saved tags and selected panel name); the unsaved tag is white with a grey outline; panel is "Sub-goals with saved results" and greys the session's other sub-goals with a 0; the sub-goals count can include other sub-goals a shown result is saved under; a session view is titled "Saved Results for Session N", the workspace name links to the Overview, and the button reads "Continue searching" and restores that session's search.

**4 Monitoring**
- Panel heading "Sub-goals for this session". Session tiles shorten each name to its first two words.
- Overview: no Continue Last Activity button; one "Sub-goals" list with an Explore button that starts a new session; the All/Explored filter and its four named lists are gone from the text (the code hides them behind `SHOW_DIRECTION_TABS`).

**5 Cross-Session Support and Keeping the Searcher in Control**
- Cards: Last Sub-goal (a button that reopens it with its stored query), Last Query (the newest stored query, which may never have been run), Last Saved.
- Every "Continue Last Activity" is now the Last Sub-goal card; "New directions" is "New sub-goals"; the plus button adds as selected.

**Implementation Note and Task List**
- One model setting serves every call; a small, fast Gemini model is used in development and the study model is open.
- Ratings are shown on the tags; every sub-goal rated above 0 becomes a tag. Task List: Continue Last Activity removed from the Overview item; ratings are shown as a number and a star.

## Not changed

- **Figures 1, 2.1, 2.2, 2.3, 3, 4 and 5 are still the old screenshots** and now disagree with the text (Fig 5 still says "Project Overview", shows count circles and session segments). They need new screenshots from the running app. Retake them once, after the open decisions below.
- Plan-screen title: the Fig 1 caption says "Plan Your New Workspace"; the visible heading is "Plan your search" (hidden h1 has the old name). No action.
- Wording: the screen mixes "sub-goal" and "search direction" ("Sub-Goals" headings beside "Search directions ready" messages). Telot to choose one word, then make the screen consistent.
- Left out on purpose (edge cases and bugs, not design): Saved results cannot be opened when no sub-goal is selected (`MindsSerpPage.jsx:139-141`); undo for a sub-goal unticked afterwards is refused (`resultsController.js:27`); the SERP header's Saved Results button is built but hidden; dev-only mock routes.
- Not checked: nothing was run in a browser; code facts come from reading the files at 533d618. A test title (`PlanWorkspaceScreen.test.jsx:14`, "no icon marks them as AI") contradicts the code.

## Decisions still open (Telot)

1. Score and star on the results page: shown (v31) or removed (v30)?
2. Overview plus button: selected (v31, as coded) or unselected?
3. One model or two tiers (and which model for the study)?
4. Keyboard reordering of sub-goals before the study?
5. "Sub-goal" or "search direction" on screen?
6. Whether the Overview should bring back the All/Explored tabs (Orland's 2026-10-27 one-list change favours the code).
