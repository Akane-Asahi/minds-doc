# SRL Language Stripped: What Changed

Per your decision to drop SRL entirely (the project stays scoped to the SERP and never
follows the searcher into full-document reading), I went through the whole planning
document and made these changes. Nothing else in the document was touched — I diffed
the full extracted text before and after, and the only differences are the ones below.

## 1. Literature review: the "self-regulated learning (SRL)" paragraph

Rewrote the paragraph that introduced SRL (Winne & Hadwin 1998's goal-setting →
strategy → monitoring → adaptation cycle) as the framework for this thesis. It now
says plainly that because the thesis stops at the search results page rather than
following the searcher into document reading, it adopts Crescenzi et al.'s three
measurable activities, planning, monitoring, evaluating, and deliberately does not
adopt SRL. Urgo & Arguello (2024) is kept, but rescoped to a single, narrower role:
supporting evidence that goal quality matters, cited specifically under Planning, not
as a theoretical framework for the thesis as a whole. Urgo & Arguello (2025) ("Search
as Learning") is no longer cited anywhere, since it was explicitly framed around
search-as-learning, and dropped from the reference list. Winne & Hadwin (1998) is also
no longer cited anywhere and was dropped from the reference list.

## 2. "Note on Scope" section

- The general description of "metacognitive scaffolding" no longer lists "revising" as
  a fourth activity alongside planning/monitoring/evaluating, and no longer cites Urgo
  & Arguello there (kept only in the Planning-specific paragraph, see above).
- The paragraph about revision being underexplored no longer proposes writing a new
  revision subscale for the study instrument. It now frames the Suggested Next Step
  feature as a contribution to evaluation, to be measured with Crescenzi et al.'s
  existing evaluation items rather than a new subscale.

## 3. Prototype Design Overview: mechanism headings and text

- Renamed **"Strategy Selection: Query Generation"** → **"Planning: Query Generation"**
  (query/strategy formulation folds under Planning, consistent with Crescenzi's
  definition of planning as "establishing search objectives and identifying possible
  strategies").
- Renamed **"Revision: Suggested Next Step"** → **"Evaluation: Suggested Next Step"**
  and reworded its justification: it's now framed as a way of supporting revision
  *within* evaluation, not as a separate fourth process.
- The Goal Decomposition mechanism's text no longer cites Winne & Hadwin or frames
  itself as "central to self-regulated learning." It now cites Crescenzi et al. for the
  planning framing, and separately notes that Urgo & Arguello's goal-quality finding
  supports the Implementation Note's design decision.
- The Implementation Note no longer says sub-goal generation "influences downstream
  self-regulated learning outcomes" — now just "influences a searcher's downstream
  outcomes."

## 4. Task List

- The Track summary no longer says the literature review was "restructured around the
  SRL framework" — now says it was restructured around "core metacognitive activities
  (planning, monitoring, and evaluating)."
- The study-design bullet that said "map each MINDS feature to the specific SRL phase
  it targets (goal-setting, strategy, monitoring, evaluation, revision), verifying
  against Urgo and Arguello's framework" now says "map each MINDS feature to the
  specific metacognitive activity it targets (planning, monitoring, or evaluating)."
- Dropped the plan to write new revision-subscale items and pilot-test them; the bullet
  now just says the study will use Crescenzi et al.'s instrument as-is.

## 5. References

Removed two now-uncited references (Winne & Hadwin 1998; Urgo & Arguello 2025, "Search
as Learning") and renumbered [20]–[24] down to [19]–[22] so there are no gaps. Nothing
else in the reference list changed.

## What I did NOT change

- The four regulatory activities (planning, monitoring, evaluating, revising)
  attributed to **Crescenzi et al.** earlier in the Metacognition section — that's an
  accurate description of Crescenzi's own paper, not SRL language, so I left it alone.
- Descriptions of *other papers'* own frameworks (e.g., Zhu et al.'s use of
  "self-regulation" to describe their own ADHD study) — rewriting those would
  misrepresent those papers, so they're untouched.
- "Revision" as a plain-English word describing the Suggested Next Step feature (e.g.,
  in the Fall 2026 Goals list) — that's just naming the feature, not an SRL claim.

## Verified before sending

- XML/XSD validation passed (`validate.py`).
- Rendered the full 36-page PDF and visually checked every section I edited: the
  literature-review paragraph, Note on Scope, all five Prototype Design Overview
  headings, the Task List bullets (confirmed no orphaned empty bullet where I removed
  the pilot-test item), and the renumbered reference list.
- Diffed the full extracted text (before vs. after) and confirmed the only differences
  are the ones listed above — nothing else moved.

## Next steps (from your earlier bullet-point plan, not yet done)

- Weave the Jamie Chen persona into the "Illustrative Scenario" section and the
  prototype design walkthrough.
- Add screenshots of the prototype design once mechanism labels are finalized.
- Broaden the working-memory literature beyond Choi & Arguello (2025).
- Draft the reply email to Orland confirming the SRL decision and answering his
  revision-subscale question.
