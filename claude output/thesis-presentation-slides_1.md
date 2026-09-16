# Presentation Slide Content
### LLM-Assisted Metacognitive Scaffolding for Cross-Session Exploratory Search

*Slide-by-slide content draft. Each "Page" below is one slide — titles are slide titles, bullets are slide body content (keep bullets short when building the actual deck; speaker notes can carry the fuller explanation).*

---

## Page 1: Title

- **[Working title]** An LLM-Assisted Exploratory Search Framework for Metacognitive Scaffolding and Working-Memory-Conscious Cross-Session Search
- [Your name]
- [Program / department, University of Regina]
- Thesis proposal presentation
- Advisor: Dr. Orland Hoeber

---

## Page 2: The Setup — What Is Exploratory Search?

- Exploratory search ≠ simple lookup — it can't be answered by one query or one result (Hoeber 2025)
- It requires the searcher to, continuously and iteratively:
  - Formulate and refine goals
  - Evaluate evidence
  - Construct interpretations
  - Decide what to do next, as understanding evolves
- Inherently **iterative** (Katz et al. 2024), **non-linear** (Hoeber and Shukla 2022), and **multi-faceted** (Hoeber, Pirmoradi, et al. 2024)
- Because of this, it rarely fits in one sitting — it spans **multiple sessions**: sometimes an interruption of minutes (Gomes et al. 2022), sometimes a gap of days or weeks (Hoeber, Islam, et al. 2024)

---

## Page 3: The Problem — Picking Up Where You Left Off Is Hard

- Every time a searcher returns to a paused task, they must reconstruct:
  - What was I trying to do?
  - What have I already found?
  - What's still unresolved?
  - What should I do next?
- This reconstruction work happens **before** the searcher can even continue — it's pure overhead
- It places heavy demand on **working memory**, on top of the demands of the search itself
- The interruption gap can be minutes (Gomes et al. 2022) or days/weeks (Hoeber, Islam, et al. 2024) — the reconstruction cost doesn't go away either way

---

## Page 4: Theoretical Grounding — Why Returning Is Genuinely Hard

- **Encoding specificity principle** (Tulving and Thomson 1973): memory retrieval depends on having the *same contextual cues* that were present when the memory was formed
  - Implication: giving someone their old documents back isn't enough — they need the cues that let them reconstruct *why* those documents mattered
- **Distributed cognition** (Hutchins 1995): cognition isn't confined to what's in your head — it happens through interaction with external artifacts and representations
- **Cognitive artifacts** (Norman 1993): well-designed external structures reduce the need to internally hold complex information
- Together, these argue that the *interface itself* can (and should) carry part of the cognitive load of resuming a task

---

## Page 5: The Catch — Cognitive Offloading Is a Double-Edged Sword

- **Cognitive offloading** (Risko and Gilbert 2016): people naturally use external tools to reduce mental effort — but doing so *changes* how they process, remember, and engage with information
- This creates a direct design tension for any AI-assisted system:
  - Too little support → searchers stay overloaded, especially across sessions
  - Too much automation → searchers stop doing their own reasoning, reflection, and sensemaking
- The goal isn't to remove cognitive work — it's to remove the *unnecessary* overhead (remembering *where you were*) while preserving the *valuable* work (evaluating, deciding, understanding)

---

## Page 6: Who Feels This Most

- Working memory capacity shapes how well someone can monitor, evaluate, and make sense of information mid-search (Choi and Arguello 2025)
- Populations for whom this is especially acute:
  - Users with **reduced working memory capacity**
  - Users with **dyslexia** — a condition research links specifically to working-memory deficits (Choi and Arguello 2025)
  - Users with **ADHD** (Zhu et al. 2026), which frequently co-occurs with dyslexia in the same person (Zhu et al. 2026)
  - Neurodivergent students more broadly, who report similar task-management strain (Jamshed et al. 2025)
- But this isn't a niche problem — **any** searcher doing a long-running research task juggles goals, evidence, uncertainty, and evolving understanding at once
- Low-WM/dyslexic searchers are simply the population where the *interface's* failure to help becomes the deciding factor in whether the task gets finished
- Critically, this population can least afford to *manually* build or maintain any external structure — the more upkeep a tool demands, the sooner it gets abandoned under working-memory load (Choi and Arguello 2025)

---

## Page 7: Where Current Tools Fall Short

- Traditional cross-session support = browser history, bookmarks, saved documents, query logs
- These preserve **artifacts** — not the **reasoning** behind them (Gomes et al. 2022)
- Prior HCI work has improved this significantly — organizing information (Crescenzi et al. 2021), visualizing relationships (Li et al. 2021), prompting reflection (Orin and Hoeber 2025) — but the *searcher* still has to:
  - Monitor their own progress
  - Evaluate their own evidence
  - Notice their own knowledge gaps
  - Decide, unaided, when to change direction
- **The gap:** nothing externalizes the *plan → progress → evaluation* loop itself, persistently, across sessions, without requiring manual upkeep

---

## Page 8: Why an LLM — Not Just a Better Visualization

- Fair question: Page 7's gap could, in principle, be attacked with a better dashboard or a smarter workspace. So why reach for an LLM at all?
- Look at what the two existing approach classes actually give you, against what the gap requires:

| Capability the gap requires | Interface-based (e.g., OrgBox) | Visualization-based (e.g., Search Timelines, Visual Keyword Linking) | LLM-based |
|---|---|---|---|
| Externalizes *some* structure | ✅ | ✅ | ✅ |
| Reconstructs **why**, not just **what** (the reasoning/plan behind actions) | ❌ — structure is just containers/labels the user made | ❌ — a timeline shows sequence, not intent (Page 12) | ✅ — can synthesize a plan/progress narrative from existing signals |
| Works **without manual authoring** | ❌ — the user must build and maintain it (Crescenzi et al. 2021) | ✅ (automatic) | ✅ (automatic) |
| Adapts explanation to the reader (e.g., simplified for dyslexia) | ❌ — fixed spatial/label format | ❌ — fixed visual schema, still requires interpretation | ✅ — natural-language output can be shaped to reading needs |
| Handles semantic content (keywords/abstracts), not just structure | ❌ | ⚠️ partial (keyword links only) | ✅ |

- **The synthesis:** visualization makes structure *visible* — it doesn't generate *meaning*. Interface tools like OrgBox require the searcher to build the very structure this thesis is trying to stop asking them to build. Neither approach class can look at raw session signals (queries, opens, saves, metadata) and hand back "here's what you were doing and why it mattered" in plain language — that specific capability is what an LLM adds that the other two categories structurally cannot
- This isn't a purely novel idea — GenAI-based prior work (Zhu et al. 2026; Yang et al. 2025 *Search+Chat*; An 2025 *Cognitive Workspace*; Katz et al. 2024 *Knowledge Navigator*, detailed next) already points this direction; the gap is that none of them combine it with true cross-session persistence, preserved agency, and an accessibility-first design (Page 15)
- **The honest tradeoff, acknowledged up front:** an LLM can infer the *wrong* plan or progress state — this is exactly the over-automation risk from Page 5. That risk is why the design keeps behavioral **Coverage** and self-reported **Clarity** strictly separate, and why every AI-generated suggestion stays editable and dismissible (Page 16) rather than authoritative

---

## Page 9: Research Question / Thesis Statement

> **How can an LLM-assisted exploratory search interface scaffold metacognition and preserve cross-session continuity, while minimizing working-memory demand — without replacing the searcher's own reasoning?**

- This thesis proposes an LLM-assisted exploratory search framework that:
  1. Externalizes evolving search context (so it doesn't have to live in the searcher's head)
  2. Preserves contextual continuity across sessions
  3. Provides interactive scaffolding for planning, monitoring, and evaluation
  4. Keeps the searcher in control — the system proposes, the searcher decides
- **Expected outcome:** a set of design principles + an interactive prototype demonstrating this approach

---

## Page 10: Related Work — Roadmap

Three interconnected areas motivate this research, each reviewed through three lenses:

| Area | Interface-based | Visualization-based | GenAI-based |
|---|---|---|---|
| **Metacognition** | OrgBox | OrgBox, Visual Keyword Linking | Zhu et al., Search+Chat, Knowledge Navigator |
| **Cross-Session Continuity** | Bookmarks/history, OrgBox | Search Timelines, Visual Keyword/Result Linking | Cognitive Workspace, Knowledge Navigator, Search+Chat |
| **Working Memory** | OrgBox, knowledge representation tools | Search Timelines, Visual Keyword Linking | Cognitive Workspace, Search+Chat |

- Recurring theme: interface & visualization approaches externalize *structure*; GenAI approaches newly enable externalizing *reasoning* — but risk over-automating it

---

## Page 11: Related Work — Metacognition in Exploratory Search

- **Metacognition** = awareness and regulation of one's own thinking during a task
- Four regulatory activities (Crescenzi et al. 2021):
  - **Planning** — setting objectives, choosing a strategy
  - **Monitoring** — tracking progress and open questions
  - **Evaluating** — judging relevance/usefulness of what's found
  - **Revising** — changing strategy when it isn't working
- Exploratory search interfaces should support this *investigative process*, not just ranked retrieval (Hoeber 2025)
- Maintaining metacognitive awareness is itself cognitively demanding — and that demand scales with working memory capacity (Choi and Arguello 2025)

---

## Page 12: Related Work — Metacognitive Scaffolding

- **Interface-based:** OrgBox (Crescenzi et al. 2021) — a spatial workspace where users manually create containers, labels, and groupings to externalize their own emerging structure. Requires sustained manual effort — exactly what's hardest to sustain for low-WM/dyslexic users across sessions
- **Visualization-based:** OrgBox's spatial layout (see above) is one example; two more directly relevant systems:
  - **Visually Linked Keywords** (Hoeber and Shukla 2022) — *Contribution:* a controlled study (32 participants) found that visually linking shared keywords across results, plus an interactive workspace, measurably improved exploratory browsing over a standard "10 blue links" baseline, on both subjective and behavioural measures. *Falls short:* validated within a single sitting only — it reveals relationships *among the documents in front of you*, not your own plan or progress, and nothing persists once the session ends
  - **Visual Keyword/Result Linking** (Hoeber, Pirmoradi, et al. 2024) — *Contribution:* extended the idea by aggregating keywords across the whole SERP and dynamically linking them back to their source results, again validated in a controlled study, showing the approach helps regardless of how the keywords are laid out. *Falls short:* also a single-session lab study scoped specifically to browsing tasks — by the authors' own admission this limits how far the findings generalize, and like its predecessor, nothing carries over between sessions
  - **The shared gap:** both visualize connections *among documents* — never the searcher's own plan, monitoring, or evaluation of what's been covered — and neither was built or tested for returning to a task after a break
- **GenAI-based:**
  - Zhu et al. (2026) — AI-generated prompts helping ADHD students set goals, monitor progress, and reconsider strategy
  - Yang et al. (2025), *Search+Chat* — conversational AI that helps formulate follow-ups without replacing the searcher's judgment
  - An (2025), *Cognitive Workspace* — LLM maintains goals/findings/context as external memory (conceptual)
  - Katz et al. (2024), *Knowledge Navigator* — LLM clusters literature into thematic structures
- **Common thread:** structure without removing agency — but none combine LLM-driven scaffolding *with* persistence across sessions

---

## Page 13: Related Work — Cross-Session Search

- Interruptions are the **norm**, not the exception, in exploratory search (Li et al. 2020)
- Resuming isn't just re-accessing old material — it's **reconstructing the reasoning** behind it (Gomes et al. 2022)
- Ties directly back to encoding specificity (Tulving and Thomson 1973) — access to documents ≠ access to the cues needed to interpret them
- Session boundaries reflect real **cognitive state changes**, not just technical pauses (Li and Capra 2024)
- **Search Timelines** (Hoeber, Islam, et al. 2024) — visualizes session history as an interactive timeline, helping searchers see where they left off
- Even so: a timeline shows **what you did** — it doesn't reconstruct **what you were thinking** (your plan, your sense of progress, your open questions)

---

## Page 14: Related Work — Working Memory & Its Limits

- Working memory = limited capacity to hold and manipulate task-relevant information while processing new input
- Exploratory search continuously taxes it: goals, evaluations, comparisons, prior decisions, next steps — all at once (Choi and Arguello 2025)
- Individual differences matter: users respond differently to the *same* knowledge-representation tool depending on cognitive ability (Choi et al. 2023) → one-size-fits-all scaffolding is the wrong assumption
- When working memory is exceeded: searchers repeat failed paths or fail to connect new findings to existing understanding (Choi and Arguello 2025); they can also lose the thread of what they were doing entirely once interrupted (Gomes et al. 2022)
- Scaffolding approaches (interface, visualization, GenAI) all aim to *externalize* what would otherwise have to be held in the head — but each stops short of full cross-session, LLM-driven, agency-preserving support

---

## Page 15: Why This Is a Real Gap

| System | Metacognitive scaffolding | Cross-session persistence | LLM-driven | Preserves agency | Accessibility-first |
|---|---|---|---|---|---|
| OrgBox | ✅ (manual) | ⚠️ partial | ❌ | ✅ | ⚠️ general |
| Search Timelines / Dilex | ❌ (action history only) | ✅ | ❌ | ✅ | ⚠️ general |
| Knowledge Navigator | ⚠️ (clustering only) | ❌ (single-session) | ✅ | ✅ | ❌ |
| Search+Chat | ⚠️ (conversational) | ⚠️ partial | ✅ | ✅ | ❌ |
| Cognitive Workspace | ⚠️ (conceptual) | ✅ (conceptual) | ✅ | ⚠️ unclear | ❌ |
| **Proposed system** | ✅ | ✅ | ✅ | ✅ (by design) | ✅ (dyslexia/low-WM) |

- No existing system combines **all four**: LLM-inferred plan/progress/evaluation state, true cross-session persistence, preserved user agency, and a design targeted at dyslexic/low-WM searchers
- That combination — scoped to the SERP, using only lightweight metadata — is the thesis-sized, publishable gap
- Positions this work as a natural extension of the advisor's own **LVSIP** framework (Hoeber, CHIIR '25) against a harder case: a searcher whose barrier isn't *finding* information, but *holding onto their own thinking about it*

---

## Page 16: The Proposed Solution — Overview

- An **LLM-assisted, SERP-scoped metacognitive scaffold** — no document detail page, no full text required
- Built from metadata the search API already returns: title, authors, venue, keywords, abstract, resource type, identifiers
- Three things the system tracks and externalizes as one shared state, rendered on multiple screens:
  - **Plan** — the searcher's sub-goals/search directions
  - **Coverage** — behavioral progress per direction (saved / opened-not-saved / shown-not-opened)
  - **Clarity** — the searcher's *own* self-rated sense of how well-covered a direction feels
- Rather than replacing the searcher's reasoning, the system **externalizes context** so they can review, evaluate, and decide — not just remember

---

## Page 17: Design Principles

- Grounded in Hoeber's **LVSIP** framework (CHIIR '25):
  - **Lightweight** — additions that don't disrupt the core ranked-list search pattern
  - **Visual** — icon-forward, low-text representations over dense paragraphs
  - **Scrutable** — the searcher can see *why* the system labeled/grouped something the way it did
  - **Interactive** — every AI suggestion is editable, dismissible, correctable
  - **Persistent** — state survives across sessions, not just within one
- Plus one construct-validity discipline unique to this design:
  - **Coverage (behavioral) and Clarity (self-reported) are never conflated.** The LLM tracks what was *shown/opened/saved* — it never infers whether the searcher "understood" something. That judgment is made by the searcher, one tap, always
  - Coverage denominators are always "results shown so far for this direction" — never the full index — so numbers stay meaningful instead of rounding to a misleading 0%

---

## Page 18: Scope

- **In scope:** everything on/around the SERP — pre-query planning, browsing, and post-session resumption
- **Out of scope:** the document detail page (reading/annotating full text is *cognition*, not *metacognition* — a different, already-studied problem)
- **Population:** searchers with dyslexia and/or low working memory doing cross-session academic exploratory search
- **Mechanism:** LLM working only from lightweight per-result metadata + session-level interaction logs
- Sized to fit a 1-year thesis: no new platform, no new psychometric instrument (reusing Kuo et al.'s validated planning/monitoring/evaluation subscales), no new study methodology (adapting Dilex's cross-session protocol)

---

## Page 19: Walkthrough — New Project Setup

- Before any searching happens: a 3-field planning screen —
  - *Search goal* — what are you trying to accomplish?
  - *What I already know* — prior context, so the LLM doesn't start from zero
  - *What I want to find* — the target
- The LLM generates a starting set of **search directions** (editable, addable, removable at any time) plus **one AI-generated suggestion** highlighting an angle the searcher may not have considered
- This is the **planning** metacognitive process, made explicit and externalized from the very first moment — not something the searcher has to hold in their head from the start

---

## Page 20: Walkthrough — On the SERP Itself

- **Goal & Plan Strip** — pinned at the top: the searcher's directions as compact chips, each with a tap-to-rate 👍/😐/👎 clarity control
- **Coverage Map** — sidebar view of the same directions' saved/opened/shown counts — monitoring, always visible, never requiring a separate screen
- **Evaluation Badges** — every result card is tagged: *New*, *Seen before*, *Similar to something saved*, *Fills a gap in [direction]*, or *Possible duplicate*
- All three are different views of **one shared state** — not three separate features to keep in sync manually
- Directly externalizes the *evaluating* process that's normally invisible and left entirely to the searcher

---

## Page 21: Walkthrough — Session Overview (Before You Search)

- A dedicated pre-SERP screen, shown automatically when resuming a task
- One card per search direction: a coverage ring (saved / opened-not-saved / shown-not-opened) + a self-rating control (well-covered / some, but thin / barely started)
- Explicit **"what this ring shows (and doesn't)"** panel — the ring is *never* framed as "how much you understand," only as triage progress on what's been shown so far
- Surfaces **unopened leads** — results seen but never opened in a past session
- Recommends where to continue, based on lowest coverage / lowest self-rating — but always lets the searcher choose differently

---

## Page 22: Walkthrough — Session History (Multi-Session Traceability)

- The landing screen once a task has 2+ sessions — answers "how did I get here?"
- **Overall recap** — compact, dot-coded status per direction (well-covered / thin / not started / flagged)
- **Last actions + Suggested next step** — grounded directly in your own problem framing: coming back usually means one of three things —
  1. **Continue** where you left off (AI's specific top pick)
  2. **Try a different direction** — a related but different piece of the same task
  3. **Start a new project** entirely
- **Cross-session progress trace** — a stacked bar per direction, one segment per session, colour = recency — shows *when* progress happened, not just *how much*
- A **Compact / Detailed** text toggle — short tagged fact-lines by default, full sentences on demand — because dense paragraphs are a real barrier for the target population, but some readers still want the fuller explanation

---

## Page 23: Walkthrough — Session Detail (Re-Examining a Past Session)

- Reached via "view this session in full" from Session History — a read-only snapshot of one closed session
- **Action view** (default): grouped by action type — queries issued, results opened, results saved, direction state at session's end
- **Time view** (toggle): the *same* events, reordered chronologically — a browser-history-style timeline showing the actual sequence: search → open → save → search → open → review, etc.
- Two different monitoring aids for two different recall styles — some people reconstruct "what did I do" more easily by category, others by sequence

---

## Page 24: How the Design Answers the Literature

- Every feature you just saw exists because a specific prior study identified a specific gap — several of them naming the exact feature that was still missing, without building it
- The next slides pair each feature with: the problem it answers (and its source), and how the design closes it
- A few of these are literally future-work items other papers called for — this thesis is where they become an interactive design, not just a recommendation

---

## Page 25: AI-Generated Search Directions (New Project Setup)

- **Problem:** manual, hand-built organization (OrgBox, Crescenzi et al. 2021) requires the searcher to invent their own categories from nothing — exactly the sustained effort that's hardest to sustain under working-memory load
- Li et al. 2020 named this specific gap as a "spawning" resumption need: *"show the user related concepts and sub-topics related to the task"* — identified, not built
- **How this design answers it:** from three short setup fields, the LLM proposes a starting set of directions plus one suggested angle the searcher may not have considered — planning starts externalized, not hand-built

---

## Page 26: Session Recap (the "Welcome Back" Capsule)

- **Problem:** resuming isn't just re-opening old material, it's reconstructing the reasoning behind it — work traditional tools never do for you (Gomes et al. 2022)
- Li et al. 2020 named this the "answer lost" resumption need: *"remind user of previously found information and sources"*
- **How this design answers it:** the moment a session resumes, a plain-language recap states what you were focused on, what you saved, and what you rated — the reconstruction is done for you, not by you

---

## Page 27: Last Actions (Session History's Middle Row)

- **Problem:** reconstructing "what exactly was I just doing" is the first, most disorienting step of resuming (Gomes et al. 2022)
- Grounded in the encoding specificity principle (Tulving and Thomson 1973): recent, concrete actions are cues closer to the mental state you left in than an aggregate summary is
- **How this design answers it:** shows the last few concrete actions, not just a rolled-up total — a direct cue trail back into where your head was

---

## Page 28: Suggested Next Step

- **Problem:** Li et al. 2020 found people resume in one of three ways — continue, try a different angle, or start fresh — but flagged that *"future work should investigate ways to detect when users are in these modes and to evaluate methods to provide assistance"*
- Also answers a gap Yang et al. 2025 (*Search+Chat*) named directly: their Chat AI wasn't designed to prompt planning, goal-setting, monitoring, or judging understanding — they proposed enhancing it to do so, as future work
- **How this design answers it:** turns that detection problem into one AI-recommended, one-tap choice among exactly those three options, instead of leaving the searcher to self-diagnose which mode they're in

---

## Page 29: Cross-Session Progress Trace

- **Problem:** Li et al. 2020's "transmuting" resumption need calls for a feature to *"help users track how the problem evolved and the relationships of information found"* — again named, not built
- Also answers Choi et al. 2023's finding that a single static display doesn't serve searchers of differing cognitive abilities equally well — a one-size-fits-all history view is the wrong assumption
- **How this design answers it:** a stacked bar per direction, one segment per session, shows evolution across the whole task at a glance — not just today's snapshot

---

## Page 30: Overall Session Summaries

- **Problem:** the "evaluating" metacognitive activity (Crescenzi et al. 2021) — judging what was found — has to be redone from scratch every time a searcher revisits a past session's raw action log
- The same reconstruction-cost problem as Page 26, here at the level of a whole session rather than a single action (Gomes et al. 2022)
- **How this design answers it:** every past session gets its own plain-language "what happened and why it mattered" recap, so evaluating an old session doesn't mean re-reading the raw log

---

## Page 31: Action View vs. Time View — Why Not Just a Browser-Style Timeline

- **Problem:** a chronological log — like Search Timelines (Hoeber, Islam, et al. 2024) or plain browser history — shows sequence, but still leaves the *regrouping into meaning* to the searcher, which is exactly the reconstruction cost this thesis targets (Page 13)
- Grouping by action type instead organizes the log along categories searchers already think in — planning/monitoring/evaluating/revising (Crescenzi et al. 2021) — rather than raw chronology
- **How this design answers it:** **Action view** (grouped by type) is the default; **Time view** (chronological) stays one tap away, because individual differences in recall style are real (Choi et al. 2023) — some readers do reconstruct better by sequence

---

## Page 32: "Continue on This Direction" Button

- **Problem:** Li and Capra (2024) cite Urgo and Arguello's finding that helping searchers set up sub-goals improves task performance and resumption — but that help has to be surfaced at the moment of return, not left as a general principle
- Also operationalizes Li et al. 2020's "anticipated" resumption need: *"help the user save information in order to use it in the future"*
- **How this design answers it:** rather than the searcher deciding from scratch where to resume, the AI computes the lowest-coverage, lowest-self-rated direction and offers one specific, one-tap resumption path

---

## Page 33: Per-Result Direction-Confidence Tags

- **Problem:** Katz et al. 2024 (*Knowledge Navigator*) cluster documents into themes on the backend, but name their own limitation directly: *"the development of a UI that leverages Knowledge Navigator's capabilities and optimizes the user experience is crucial for its practical application"* — the clustering existed; the interactive layer didn't
- **How this design answers it:** each result shows the AI's confidence that it belongs to each of the searcher's directions, and a single tap accepts it — the missing interactive layer Katz et al. named, built as LVSIP's **Scrutable** + **Interactive** principles (Page 17) in practice
- **Why it matters for the scaffold as a whole:** this tap and the plain 💾 save both update the *same* Coverage Map, Plan Strip, and Overview rings — so planning, monitoring, and evaluating are never separate, hand-maintained lists (the OrgBox problem, Crescenzi et al. 2021) — they're one continuously updated model of progress

---

## Page 34: AI Tips and Suggestions Throughout

- **Problem:** Zhu et al. 2026's ADHD participants specifically asked for "cognitive scaffolding to enhance task and self-awareness" and support for "reflective task execution for building metacognitive abilities" — a need identified in interviews, not yet a specific interface
- Also answers Yang et al. 2025's future-work call for prompts that encourage a searcher to reflect on whether their understanding improved, rather than leaving reflection unprompted
- **How this design answers it:** short, contextual explanations sit next to the decision they explain (why a result is flagged, why a direction is prioritized) instead of living in a separate help screen — and per LVSIP's **Scrutable** principle, every AI suggestion says why, which is what keeps this from becoming the over-automation risk raised on Page 5

---

## Page 35: Accessibility Is Not an Afterthought

- Visual identity ("MINDS") built around: warm, low-glare palette; **Lexend** typeface (chosen for spacing and sans-serif properties research has linked to easier reading — detail on Page 36); icon-forward labeling throughout
- Every text-heavy surface has a **compact-by-default** mode — because low working memory and dyslexia both make dense paragraphs a genuine barrier, not just a preference
- But accessibility ≠ removing detail entirely — every compact view has a **Detailed** fallback, because under-explaining is its own failure mode
- This tension (minimal-text editorial aesthetic vs. icon-forward data density) was navigated deliberately, screen by screen, rather than applying one rule everywhere

---

## Page 36: Visual Design Choices — Checked Against the Literature

- **Cream background, not stark white:** Rello and Bigham (2017) tested 10 background colors on dyslexic and non-dyslexic readers — warm tones (peach, orange, yellow) produced significantly faster reading than cool tones (blue, blue-grey, green), consistently across both groups. *Caveat:* pure white wasn't one of the tested colors, so this is evidence for "warm over cool," not literally "cream over white" — but it's the closest available evidence, and it points the same direction
- **Lexend typeface:** chosen for its wide, variable letter/word spacing and plain sans-serif form — the two specific typographic factors research has actually linked to easier reading for dyslexic readers (spacing: Duranovic et al. 2018; sans-serif over serif/italic: Rello and Baeza-Yates 2016). *Caveat:* Lexend itself has no independent peer-reviewed validation for dyslexia — its design principle matches what's been shown to help, but the typeface as a named product hasn't been tested against controls the way OpenDyslexic and Dyslexie have been (and neither of those was found to help)
- **Low visual clutter (data-ink ratio, the "squint test"):** a general information-design heuristic (Tufte, 1983) for cutting anything on screen that isn't carrying information — paired here with a dyslexia-specific finding, not just a general design preference: Morris et al.'s study (cited in Choi and Arguello 2025) found dyslexic searchers specifically prefer less-cluttered content with more structural elements like lists and tables
- **The honest framing for all three:** none of these is a "solved problem" backed by a dyslexia-specific controlled trial of this exact design — they're the best available evidence, chosen deliberately over less-grounded defaults, and presented here as such rather than oversold

---

## Page 37: Expected Contributions

1. A set of **design principles** for LLM-assisted, SERP-scoped metacognitive scaffolding — extending Hoeber's LVSIP framework to a new, harder case
2. A working **interactive prototype** demonstrating cross-session continuity + metacognitive scaffolding + working-memory-conscious design, together, for the first time
3. A **construct-validity pattern** (Coverage vs. Clarity, never conflated) that other GenAI-search researchers can reuse to avoid overclaiming what an LLM can validly assess
4. Empirical evidence (via evaluation) on whether this approach measurably improves planning/monitoring/evaluation (via Kuo et al.'s validated instrument) and reduces resumption cost for low-WM/dyslexic searchers specifically

---

## Page 38: Evaluation Plan (Brief)

- Adapts Dilex's cross-session protocol: initial session → ~1 week gap → resumed session
- Baseline: visually-identical SERP without the scaffolding components, isolating the contribution
- Measures: UES-SF engagement, Kuo et al.'s planning/monitoring/evaluation subscales, task-resumption time, qualitative interviews ("did this feel like picking up where you left off?")
- Participants screened via self-reported dyslexia and/or a standard working-memory span task (e.g., OSPAN)

---

## Page 39: Timeline (12 Months)

- **Months 1–2:** Design finalization, prompt design, heuristic evaluation against LVSIP
- **Months 3–5:** Prototype build (scaffolded + baseline versions)
- **Month 5:** Pilot study + cognitive walkthrough
- **Months 6–9:** Main cross-session study
- **Months 9–11:** Analysis + thesis writing
- **Months 11–12:** Defense prep + CHIIR submission

---

## Page 40: Thank You / Questions

- **Thesis statement, restated:** an LLM-assisted exploratory search framework that scaffolds metacognition and preserves cross-session continuity while minimizing working-memory demand — without replacing the searcher's own reasoning
- Questions?
- [Contact info]

---

*End of slide content draft — 40 slides. Trim, merge, or split any slide to fit your actual time budget; Pages 11–14 (related work), 19–23 (design walkthrough), and 25–34 (feature-by-feature literature justification) are the easiest to compress or cut down to a few representative examples if you're running long.*
