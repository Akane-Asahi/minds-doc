# Project Notes

## 2026-09-17 — Session Summary

**Done this session:**
- Reviewed "Telot Thesis Planning Documents v7 - SRL Stripped-1.docx" against Orland's Aug 31
  email feedback and the accompanying `srl-stripping-changes-summary.md` changelog. Confirmed
  the SRL-vs-metacognition fix and the revision-subscale answer were handled correctly; flagged
  that the persona (point 1), screenshots (point 6), broader working-memory literature (point 4),
  and the parallel-track Task List were still unaddressed.
- Produced "Telot Thesis Planning Documents v7 - SRL Stripped-2.docx" (in `Claude outputs/`)
  implementing the three follow-up requests:
  1. Removed "revision" entirely as a metacognitive concept — no longer listed as a fourth
     regulatory activity alongside planning/monitoring/evaluating, and no longer the
     justification for the Suggested Next Step feature (Metacognition section, Note on Scope,
     Research Approach, Prototype Design Overview, Task List, Fall 2026 Goals all edited).
     Left "revisit/revisited" (different word), the doc's own "Project Revised" metadata, and
     "REB revisions" (standard ethics terminology) untouched as out of scope.
  2. Wove the Jamie Chen persona into the Prototype Design Overview — all five MINDS mechanisms
     plus Cross-Session Recap/Resume now ground their explanation in Jamie's situation from the
     Illustrative Scenario, instead of a generic "the searcher."
  3. Reworked the Task List from two parallel tracks (Implementation // Study Design & Ethics)
     into Orland's described sequence: MVP design & build first (through Nov 5) → study design &
     ethics submission grounded in the working MVP (through Dec 5) → heuristic evaluations and
     cognitive walkthroughs during the REB review wait (Dec 5 onward). Fall 2026 Goals rewritten
     to match.
- Wrote `srl-stripped-2-changes-summary.md` documenting every edit in detail (same pattern as the
  existing v1 changelog).
- Validated the new docx against the XSD (`validate.py`), rendered the full 37-page PDF, and
  visually checked every edited section for broken formatting, orphaned bullets, or leftover
  "revision" language.
- Delivered both files into the conversation and committed them into the connected
  `Claude outputs/` folder on the user's machine.

**Why (key decisions):**
- Kept "revisit"/"revisited" and "REB revisions" untouched even though they contain the string
  "revis" — they're unrelated meanings (looking at something again; ethics-board terminology),
  and removing them would either be meaningless or garble standard usage. Flagged this choice to
  the user rather than silently deciding it.
- Did not force the Jamie persona into the two purely technical Implementation Note paragraphs
  (embedding-based relevance scoring, computation/phrasing separation) since those are
  implementation-mechanics arguments where the persona doesn't add anything.
- Compressed the Task List dates to start from "now" (mid-September) rather than the original
  September 1 start, since the document already acknowledges being behind schedule.

**Currently broken / incomplete:**
- Nothing broken. The v2 docx is fully validated and rendered clean.

**Next steps:**
- Broaden the working-memory literature beyond Choi & Arguello (2025) / Choi et al. (2023) —
  flagged as still open since the SRL-Stripped-1 round, not addressed this session either.
- Add screenshots of the prototype design to the Prototype Design Overview once mechanism labels
  are finalized.
- Confirm with Orland (in the reply email) that folding "revision" out entirely — rather than
  keeping it as a sub-concept of evaluation — is what he meant, since his email was slightly
  ambiguous on this point.
- Draft the actual reply email to Orland once the above two items are resolved or explicitly
  deferred.

**Bugs found (not fixed):**
- None found in this session's document work.

**Ideas / revisit later:**
- The Prototype Design Overview intro still says "five linked mechanisms" while six Heading-3
  mechanism sections exist (Goal Decomposition, Query Generation, Relevance Visualization,
  Goal-Linked Saving, Suggested Next Step, Recap & Resume) plus the Implementation Note — this
  pre-existing count mismatch wasn't part of this session's ask but is worth reconciling before
  the document goes back to Orland.
