# Urgo & Arguello: Metacognition & Self-Regulated Learning in Search
## Critical Learning Guide for Your Thesis

**Your professor emphasized:** "Urgo and Arguello are key references for metacognition. Become expert-level on their work before writing about this."

This document summarizes what you *must* understand from their research to ground your thesis and avoid errors that will reflect on your advisor's name in publication.

---

## Part 1: Kelsey Urgo — Self-Regulated Learning Framework

### The Core Model: Winne & Hadwin's SRL (Self-Regulated Learning)

**CRITICAL CONCEPT:** Metacognition IS self-regulated learning (SRL). They're not separate. SRL has four phases:

1. **Goal-Setting** — Establishing clear, measurable learning objectives *before* searching
2. **Strategy Selection** — Choosing appropriate search approaches based on the goal
3. **Monitoring** — Tracking progress toward those goals *during* search
4. **Evaluation** — Assessing whether goals were achieved and adjusting tactics

**Why this matters to you:** Your thesis mentions metacognition as "planning, monitoring, evaluating, revising." That's SRL language. You must ground it in Urgo's framework and cite it correctly.

### Key Finding: Goal Quality Matters More Than You Think

**From "The Effects of Goal-Setting on Learning during Information" (CHIIR 2026):**

Well-formed goals have four characteristics:
- **Action** (what will you do?)
- **Information** (what will you learn?)
- **Success criteria** (how will you know you succeeded?)
- **Timeframe** (when?)

**Real-world impact:** Participants given goal-setting tools (Subgoal Manager):
- Spent only ~5 minutes on initial goal-setting
- Produced shorter, more selective notes (= deeper cognitive processing, not copying)
- Requested focused, specific information rather than open-ended suggestions
- Achieved better learning outcomes *without extending task time*

**What you need to change in your design:** 
- Your setup screen asks for "search goal," "what I already know," "what I want to find" — this is good, but you're not explicitly guiding users to form *success criteria* and *timeframes*
- Add language like: "How will you know you've found enough?" and "How long do you expect this to take?"

### Key Finding: Task Complexity Drives Metacognition

**From "Search as Learning" (Foundations & Trends 2025):**

- **Fact-finding** ≠ **Conceptual learning** tasks
- Complex tasks (requiring analysis, evaluation, or creation) generate more diverse search strategies and require *greater metacognitive engagement*
- Learners must actively connect new information with existing knowledge — a constructivist process requiring constant metacognitive monitoring
- Strategy adaptation happens at **session endpoints** — when learners stop and reflect on what they learned

**What you need to understand:**
- Your persona (Jamie, researching environmental justice + green space) is a *conceptual learning task*, not a fact lookup
- This means Jamie *must* continuously ask: "How does this fit with what I already know?" and "Do I understand how X connects to Y?"
- Your AI metacognitive scaffolding must *surface these connections*, not just list what was found
- This is different from helping someone find a phone number

---

## Part 2: Jaime Arguello — Working Memory Constraints in Search

### The Core Problem: Working Memory Severely Limits Metacognition

**From "The Effects of Working Memory during a Search and Sensemaking Task" (CHIIR 2025 — Choi & Arguello):**

**Key finding:** Working memory capacity directly constrains:
- How many search goals a user can hold in mind simultaneously
- Ability to track progress across multiple search directions
- Capacity to recognize when you're going off-track
- Ability to integrate new findings with prior results

**Concrete numbers (from your presentations):**
- Typical working memory span: 3–4 items held simultaneously
- Dyslexia-specific constraint: working memory deficits are a core feature
- ADHD overlap: frequently co-occurs; compounds the problem

**CRITICAL IMPLICATION:** Users with low working memory cannot use search interfaces designed for users with *typical* working memory. They will:
- Lose track of what they were looking for mid-session
- Open the same paper twice, not recognize it
- Forget why they clicked a link
- Abandon the search because "I feel lost"

**This is NOT a reading-speed problem.** It's not about dyslexia fonts. It's about *holding multiple cognitive threads at once.*

### What Arguello Found About Effective Interfaces

**For users with constrained working memory:**
1. **Minimize the number of simultaneous goals** — don't show 10 possible next steps; show 1–3
2. **Externalize the search state** — what was I doing? what have I found? what's next? *must* be visible, not in memory
3. **Surface relationships explicitly** — don't assume users will *notice* that Paper A cites Paper B; show it
4. **Reduce decision overhead** — every interaction should have a clear purpose
5. **Persistent context** — information should be available across sessions without requiring users to remember or re-search

---

## Part 3: What You MUST Fix or Clarify in Your Thesis

### 1. **Metacognition ≠ just "thinking about your thinking"**

**Wrong framing:** "Metacognition is self-awareness during search"  
**Correct framing (Urgo):** Metacognition IS the four-phase SRL cycle: goal-setting → strategy selection → monitoring → evaluation

**In your presentation:** When you say "metacognitive scaffold," you must mean "a scaffold supporting the SRL cycle," not just "helping people reflect."

**Fix in your slides:** Define SRL explicitly before using "metacognition." Show the four phases. Show how your design supports each.

### 2. **Working Memory Claims Must Be Precise**

**Your current statement:** "People with dyslexia have working memory deficits"  
**What Arguello found:** "Working memory deficits *specific to* holding multiple phonological/linguistic items affect search performance"

**The difference:** You can't just say "Jamie has low working memory." You need to describe *what* Jamie can't hold: "Jamie can hold a task goal + search query in memory, but adding 'what papers I've already found' causes overload."

**Fix:** In your persona, specify what Jamie's working memory span is. In your design, show how you *externalize* the items that would overflow Jamie's span.

### 3. **"Scaffolding" Needs a Precise Definition**

**Your professor said:** "Read top 5 most-cited papers on scaffolds in information retrieval — use these to ground the definition"

**Urgo's perspective on scaffolding:** 
- Graduated support that *fades* as users demonstrate competence
- Not a tool; it's *support around the primary task*
- Should enable independence, not create dependency

**Your current design:**
- Session History (shows prior work) ✅ scaffolding
- Session Recap (AI synthesizes what happened) ✅ scaffolding
- Suggested Next Step (AI proposes three options) ⚠️ *might* be too prescriptive — is this scaffolding or automation?
- Direction-confidence tags (AI labels relevance) ✅ scaffolding

**Fix:** For "Suggested Next Step," include *why* the AI is proposing each option, so users can make informed choices, not just follow suggestions.

### 4. **Separating Metacognitive Scaffolding from Cross-Session Scaffolding**

**Your professor's exact feedback:** "Keep metacognitive scaffolding and cross-session scaffolding as two separate concerns. Do not conflate the two."

**Metacognitive scaffolding** = supporting the SRL cycle *during a single session*
- Goal-setting support: "What are you trying to learn in this session?"
- Strategy guidance: "Try searching for X angle, then Y angle"
- Monitoring: "You've found 4 papers on topic A, 1 on topic B — should you explore B more?"
- Evaluation: "Does this collection of papers cover your question?"

**Cross-session scaffolding** = enabling re-entry after a break
- Reacquaintance: "Last time you were focused on X; here's what you found"
- Session history: Visual timeline of where you were
- Progress replay: "You went from not knowing X to understanding X"

**Your current design conflates them:**
- Session History panel mixes "what I did overall" (cross-session) with "how to continue strategically" (metacognitive)
- Suggested Next Step doesn't distinguish: "Is this proposing a new search strategy [metacognitive] or just showing what's next chronologically [cross-session]?"

**Fix in your presentation:** Create two separate design matrices:
1. Metacognitive scaffolding features (planning, monitoring, evaluation, revising *within* a session)
2. Cross-session scaffolding features (reacquaintance, continuity, progress replay *across* sessions)

Show how your design supports *each* concern separately.

### 5. **Planning & Monitoring Are Confirmed; Evaluation Needs Justification**

**Your professor said:** "Features to support planning and monitoring are confirmed; evaluation and others need individual justification."

**What this means:**
- ✅ Goal-setting (planning) — Urgo confirms this works; cite it
- ✅ Progress tracking (monitoring) — Urgo confirms this works; cite it
- ⚠️ Evaluation prompts ("How well do these papers answer your question?") — needs *your own* justification, not just citation
- ⚠️ Revision prompts ("Should you change direction?") — needs *your own* justification and grounding in Arguello's work on working memory

**Fix:** For evaluation and revision features, explicitly state:
- *Why* you're including them (cite Urgo's SRL model, then extend)
- *How* your design supports them without overloading working memory (cite Arguello's findings on constraint)
- *What* user study or heuristic validation supports them

---

## Part 4: What to Say in Your Presentation

### When Introducing Metacognition:
"Metacognition in search isn't just reflection—it's self-regulated learning. Urgo's research, based on Winne & Hadwin's framework, shows that effective search learning requires four phases: setting clear goals, selecting appropriate strategies, monitoring progress, and evaluating results. [CITE: Urgo 2025]. Our design scaffolds these four phases without automating them."

### When Discussing Working Memory:
"Working memory constraints directly limit search effectiveness. Arguello's research shows that users with limited working memory struggle to hold multiple search goals, track progress, and recognize relationships between results simultaneously [CITE: Choi & Arguello 2025]. This is especially acute for users with dyslexia, where working memory deficits are a core feature [CITE: Arguello 2024]. Our interface externalizes this cognitive state—what you're searching for, what you've found, what you've decided—so users don't have to hold it all in memory."

### When Describing Your Design:
"Our metacognitive scaffolding supports three of Urgo's SRL phases: planning (setup screen guides goal-setting with success criteria), monitoring (session overview shows progress per direction), and evaluation (rating system lets users assess coverage). We separate this from cross-session scaffolding, which enables reacquaintance after a break. Together, they respect Arguello's finding that constrained working memory requires externalized task state."

---

## Part 5: Specific Reading Recommendations

### **Must Read (this week):**
1. **"Search as Learning" (Urgo, Foundations & Trends 2025)** — Winne & Hadwin SRL model, task complexity effects
2. **"The Effects of Working Memory during a Search and Sensemaking Task" (Choi & Arguello, CHIIR 2025)** — Working memory constraints on search

### **Should Read (next week):**
3. **"The Effects of Goal-setting on Learning during Information" (Urgo, CHIIR 2026)** — Goal quality, Subgoal Manager design
4. **Arguello's earlier work on cognitive abilities:** "The effect of cognitive abilities on information search" — sets foundation for working memory research

### **Reference (as needed for citations):**
- Winne & Hadwin (2008) — the original SRL model (Urgo cites this)
- Tulving & Thomson (1973) — encoding specificity (you already cite this correctly)

---

## Summary: What Your Professor Needs to See

In your thesis and presentations, your professor will look for:

✅ **Accurate grounding in Urgo's SRL framework** — metacognition IS the four-phase cycle, not just reflection  
✅ **Precise working memory language** — citing Arguello, not just asserting constraints  
✅ **Separated concerns** — metacognitive scaffolding ≠ cross-session scaffolding  
✅ **Feature-by-feature justification** — each design element maps to Urgo's SRL phases or Arguello's findings  
✅ **Avoiding overclaim** — you're *scaffolding* metacognition (supporting it), not *teaching* it  

**The stakes:** Any error in interpreting Urgo or Arguello will reflect poorly on your advisor's name in publication. Get this right, and your thesis will be publishable.
