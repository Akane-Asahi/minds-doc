# SRL Stripped-2: What Changed

Three edits on top of SRL Stripped-1, per your instructions.

## 1. Removed "revision" entirely

Went back through the whole document and removed every instance where "revision" appeared as
a metacognitive concept (a fourth regulatory activity alongside planning/monitoring/evaluating,
or as the justification for the Suggested Next Step feature):

- **Metacognition section**: the regulatory-activities paragraph now names only planning,
  monitoring, and evaluation (Crescenzi et al. 2021). It no longer enumerates revision as a
  fourth activity.
- **Note on Scope section**: the paragraph that reframed revision as "a refinement within
  evaluation" is gone. It now just states that evaluation support is grounded, and that the
  Suggested Next Step feature is this thesis's contribution to evaluation — full stop, no
  revision framing at all.
- **Research Approach**: "(planning, monitoring, evaluating, and revising)" → "(planning,
  monitoring, and evaluating)".
- **Evaluation: Suggested Next Step** (Prototype Design Overview): dropped "supporting revision
  as part of evaluation, the specific refinement..." → now just "this thesis's own concrete
  mechanism for evaluation support, the specific gap...".
- **Task List**: "the Suggested Next Step revision mechanism" → "the Suggested Next Step
  mechanism"; "extended with a new revision subscale" → dropped entirely (the whole Task List
  was rebuilt anyway, see below); the Fall 2026 Goals line that said "revision features
  implemented" is gone.
- A handful of sentences elsewhere used "revise" as a plain verb describing general searcher
  behavior (Problem Statement, Cross-Session Search, Visualization-Based Scaffolding) — these
  were reworded to "adjust" or "change" so no trace of the word remains tied to the
  metacognition/SRL discussion.

**Left untouched, deliberately**: "revisit"/"revisited" (a different word — "look at again" —
appears describing documents/evidence, not the metacognitive activity), "Project Revised" (the
document's own revision-date metadata), and "Address any requested REB revisions" (standard
research-ethics terminology for ethics-board feedback, unrelated to Crescenzi's framework).
Flagging these so you can override if you want them gone too, but changing them would either be
meaningless (metadata) or garble unrelated, standard terminology.

## 2. Wove Jamie Chen into the Prototype Design Overview

Previously the persona lived only in the Illustrative Scenario; the five-mechanism design
walkthrough talked about a generic "the searcher." Now every mechanism section opens or closes
with a concrete tie-back to Jamie's situation from the scenario:

- **Intro paragraph**: explicitly says the mechanisms below are illustrated by returning to
  Jamie.
- **Planning: Goal Decomposition**: Jamie's green-space topic becomes the worked example, and
  the "add the policy dimension partway through" moment ties directly to the scenario's
  "gradually realizing... policy dimension" beat.
- **Planning: Query Generation**: ties directly to Jamie rereading/rewording queries in the
  scenario.
- **Monitoring and Evaluation: Relevance Visualization**: ties to Jamie skimming a dozen
  results.
- **Organization: Goal-Linked Saving**: a concrete example (a tree-canopy/mental-health source
  auto-filed under Jamie's mental-health direction).
- **Evaluation: Suggested Next Step**: Jamie's coverage-tallying example.
- **Cross-Session Reacquaintance: Recap and Resume**: opens with Jamie's two-day interruption
  from the scenario — the most natural fit of the five.
- **Implementation Note**: one added sentence ties the "capable generative model" design
  decision back to the risk of Jamie's policy dimension never surfacing if sub-goal generation
  is weak.

Left the two purely technical Implementation Note paragraphs (embedding-based relevance
scoring; the computation/phrasing separation on the Recap page) without a forced Jamie mention —
those are implementation-mechanics arguments, not places where the persona adds anything.

## 3. Reworked the Task List to match Orland's described process

Replaced the two-parallel-track structure (Implementation running alongside Study Design &
Ethics) with the sequential process Orland described: build an MVP first to validate the
research questions, then design and submit the study, then use the REB waiting period for
heuristic evaluations and cognitive walkthroughs rather than sitting idle.

New structure:
- **Phase 1: MVP Design & Build** (Sept 17 – Nov 5) — design freeze, then build all five MINDS
  mechanisms into a working MVP, ending with informal use to confirm the mechanisms behave as
  intended and the research questions still hold up.
- **Phase 2: Study Design & Ethics Application** (Nov 5 – Dec 5) — protocol decisions, instrument
  adoption, population strategy, then the protocol itself and REB submission — now explicitly
  grounded in how the MVP actually behaves, not written in parallel from the original design
  intent.
- **Phase 3: Heuristic Evaluation & Cognitive Walkthroughs (While REB Review Is Pending)**
  (Dec 5 onward) — heuristic evaluations and cognitive walkthroughs on the MVP, defect fixes,
  REB-revision response, recruitment materials.

The Fall 2026 Goals list and the Task List intro paragraph were rewritten to match. Dates are
compressed relative to the original plan (single sequence instead of two tracks) and start from
today (mid-September) rather than September 1, since the intro paragraph already flags you're
behind; the intro also keeps the existing "scope may need to be trimmed if it runs behind"
caveat, now attached to the MVP build specifically, since everything downstream now depends on
it finishing.

## Verified before sending

- XML/XSD validation passed (`validate.py`), diffing against the SRL Stripped-1 original.
- Rendered the full 37-page PDF and visually checked every edited section: Abstract, Problem
  Statement, Metacognition, Note on Scope, Research Approach, all five Prototype Design Overview
  mechanisms plus the Implementation Note, the full rebuilt Task List (all three phases, no
  orphaned bullets or broken numbering), and the Fall 2026 Goals.
- Grepped the full document for every remaining instance of "revis*" and confirmed only benign,
  unrelated uses remain (see "left untouched" note above).

## Still open (not touched in this pass)

- Broadening the working-memory literature beyond Choi & Arguello (2025) / Choi et al. (2023).
- Screenshots of the prototype design.
- Whether folding revision fully out (rather than into evaluation) changes how the "Evaluation:
  Suggested Next Step" mechanism should be pitched to Orland when you send this back — worth a
  sentence in your reply email confirming this is what you meant.
