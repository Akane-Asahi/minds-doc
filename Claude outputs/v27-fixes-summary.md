# v27 fixes: what changed in the planning document (2026-10-20)

Source: the four diff briefs (`plan-diff.md`, `serp-diff.md`, `save-diff.md`, `sessions-diff.md`), checked against `minds-app` @ ba707ba (DECISIONS.md, `docs/spec/`). Edited in place in `Telot Thesis Planning Documents v27.docx`; the previous version is in git history (commit fc321d4 and earlier). Only text in `word/document.xml` changed; figures, styles and references are untouched. 26 paragraphs edited, no tracked changes.

## 1. Task List and Fall 2026 Goal 2

| Where | Change |
|---|---|
| Task List, Oct 5 – Nov 5, "Set up the project…" | Adds LLM query generation the first time a sub-goal is opened. |
| Same list, "Implement the planning screen…" | Now sub-goal generation and selection only (query generation moved up). |
| Same list, "Implement the SERP relevance visualization…" | Embedding cosine similarity → a generative model rates each result against each selected sub-goal 0 to 5 with a written rubric; "thresholds" → "rubric". |
| Same list, "Implement goal-linked saving…" | The searcher files a result by selecting a sub-goal tag; saved results viewable by sub-goal and by session. Coverage tracking and Suggested Next Step removed (deferred in `deferred.md`). |
| Same list, "Implement session logging…" | Recap and Resume screens → the Workspace Overview screen (last-activity cards, Continue Last Activity, Sessions panel, per-session bars). LLM-phrasing clause removed (recaps are deferred). |
| Phase 3, "Validate the similarity thresholds…" | Now "Validate the rubric behind the star ratings…". |
| Fall 2026 Goal 2 | Suggested Next Step and Recap and Resume replaced by "the Workspace Overview and saved results screens". The 5 November date is unchanged (decision below). |

## 2. Plan screen (Abstract, 1.1, 2.3)

- Abstract and 1.1: about eight candidates, roughly half of them angles the searcher has not mentioned; Jamie's six-item list is marked as shortened for illustration.
- 1.1: the searcher can drag sub-goals to set the order; the numbered order of the *selected* sub-goals is kept; Explore saves the texts and the selected sub-goals in order and opens the results page on the first; unselected candidates are not kept; a saved plan can be reopened and changed, and Explore then replaces it.
- 1.1: the sub-goals stay in view "in the directions panel of the results page" (the Plan screen is not shown again).
- 2.3: starting again = go to the workspaces list, create a workspace with its own title, then plan it.

## 3. Results page (2.2, 4)

- 2.2: the New tag is "an extra tag", at most one per result, ordered by rating (can sit second or third). Selecting it adds the facet as a sub-goal and files the result under it (`F3` spec).
- 4: the bars on the results page are also split into one segment per session (as Fig 2.2 already draws).

## 4. Saved results (3, 5)

- 3: a row of three counts (results, sub-goals, sessions); unsaving keeps the card on screen with a grey tag until Jamie leaves the view (`F6`).
- 5: the whole-workspace view is grouped by session, newest first; a count circle opens one sub-goal, a bar segment opens one sub-goal in one session, a session tile opens one session.

## 5. Sessions screen (4, 5)

- "A version of this panel" replaces "the same panel" (the two are separate components).
- 5: the "New" tag stays on a direction Jamie added from a suggestion during the latest session until that session ends; an unadded suggestion is not in the list (DECISIONS 2026-10-17; `F5`). The old example "urban planning tradeoffs" was dropped because it is one of Jamie's original six.

## 6. Wording

- "Project" → "workspace" wherever it means the MINDS unit: 1.1, 2.2, 2.3 (including "starting a new workspace"), 3, 4, 5, the section 5 title ("Resuming a Workspace") and its two cross-references, and "Project Overview" → "Workspace Overview" (text and Fig 5 caption), Fig 1 caption → "Plan Your New Workspace".
- Left as "project": the course project in the persona and scenario, "Set up the project" (the software project), and the "Project Revised" line.
- "Sub-goal" is kept: the thesis defines it as its own term for what the UI calls a search direction (1.1).

## Not changed, because the answer is yours to give

- Two models (strong for sub-goals, light for queries) vs one cheap model: 1.1 and the Implementation Note still describe two.
- `(?)` window vs in-place sentence; whether right-panel rows switch direction or only the dropdown; whether results are re-ordered by the active direction's score.
- Saved cards: all scored directions vs top 3 with ">>".
- Last Query meaning (still "Telot to confirm" in DECISIONS.md); Sessions-panel pill text ("0 saved", two-word labels) and the encoding-specificity wording that depends on it.
- Labels: "What I want to find out" vs "What I want to find"; "Add search direction" vs "Add Search directions".
- The 5 November MVP date.
- Where returning searchers land (Plan Workspace vs overview).
- `technical-specification.md`: not edited. `minds-app/CLAUDE.md` calls the original spec frozen ("do not edit"); say if you want a "superseded by docs/spec/" line added.

## Figures that still need redrawing by hand (images cannot be edited as text)

- Fig 1: title still reads "Project"; six rows vs about eight (fine if kept as illustration).
- Fig 2.2: header says "Projects ›"; shows an always-visible "Why this may help" line (removed 2026-10-17).
- Figs 3 and 4: two counts (should be three); search text differs from Fig 5's last query; "Description:" label has no code behind it.
- Fig 5: tiles with S3/S2/S1 badges, "Community access +0" and Session 2 with 0 saved (Session 2 now saves one result under Community access); "Project" wording.
- The figure captions now use the new names, so they will not match the images until those are redrawn.

## Second pass (2026-10-20): the "Why?" button on generated sub-goals

plan-diff (focused run) found that v27 never mentioned the "Why?" button on AI-proposed directions on Plan Workspace; the only "why" features in the document were the "(?)" icons on result tags (2.1). The code and `01-core.md` rule 4 have it. Added:

- **1.1 Planning: Goal Decomposition**, paragraph "The LLM proposes the candidates, and the searcher decides…" (after the Fig 1 caption), a passage saying each LLM-proposed candidate has a sparkle icon and a "Why?" button; selecting it shows one sentence under the candidate saying why searching that direction helps with the goal; it is written in the same step as the candidate; sub-goals Jamie adds have no sparkle and no reason; the reason is kept with selected sub-goals and shown again on reopening; the button only shows the reason and does not select the candidate. It reuses the two guidance citations already used in 2.1 (Amershi et al. 2019; Weisz et al. 2024), each placed right after its own claim. The community-access sentence is an illustration worded after a real generated reason.
- **Keeping the Searcher in Control**, paragraph "This division shows at each step…": one clause saying each candidate comes with a "Why?" button showing the reason it was proposed.
- **1.1**, paragraph "On the first screen (Fig 1)…": reworded "so the list is not limited to what the searcher already knows" to "so the list reaches beyond what the searcher already knows" (R41, say what it does).

Still open: Fig 1 shows the sparkle but no "Why?" button (needs redrawing by hand); the new passage cites in the document's author-year style, while `.agents/rules/citation-precision.md` asks for numbered [n] citations only (the whole document is author-year today).
