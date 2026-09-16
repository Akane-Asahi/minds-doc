# Persona & Task Scenario for Cross-Session Exploratory Search Research

---

## Detailed Persona: Jamie Chen, Third-Year Environmental Science Undergrad

### Demographics & Background
- **Name:** Jamie Chen
- **Age:** 21 years old
- **Program:** Third-year Bachelor of Environmental Science, State University
- **Diagnosis:** Dyslexia (identified age 8; mild to moderate; uses screen reader + text-to-speech)
- **Experience:** Competent searcher; has adapted to digital tools over 13 years

### Cognitive Profile

**Working Memory (Grounded in Research)**
- Working memory span: approximately 3–4 items held simultaneously (typical for dyslexia; Choi & Arguello 2025)
- Cannot reliably hold task goals + search query + found results + prior searches in mind at once
- Requires external aids to track: "What was I looking for?" and "Did I already read this?"
- Loses search thread after ~30 minutes of browsing or after interruption (Li et al. 2020)

**Reading & Processing**
- Reads at ~60% of typical speed but with high accuracy (Duranovic 2018)
- Text-heavy screens cause fatigue; color-coding and visual categorization reduce cognitive load
- Prefers sans-serif fonts with increased spacing (Rello & Baeza-Yates 2016)
- Numbers read as text: "72%" takes same cognitive effort as "seventy-two percent" (working memory research)
- Benefits from reduced visual clutter; high data-ink ratio preferred (Morris et al. dyslexia accessibility study)

**Metacognitive Capacity**
- Strong metacognitive awareness when supported: can articulate search goals, recognize off-topic results, identify gaps
- Metacognition becomes effortful when also holding search state in memory (dual-task interference)
- Thrives when interface externalizes metacognitive state (planning, monitoring) so working memory is freed for actual search decisions (Crescenzi et al. 2021)

### Motivation & Task Characteristics

**Typical Search Scenario**
- Conducting research for a term paper on "environmental justice in urban green space access"
- Topic is genuinely complex: requires integrating perspectives from ecology, urban planning, sociology, policy
- Not a simple lookup; requires multiple sessions to understand the landscape (Hoeber 2025)

**Real-World Search Pattern**
- **Session 1 (Monday, 90 min):** Finds 12 papers, reads 3 abstracts, saves 5 promising results, realizes: "I don't understand how policy works here"
- **2-day break** (Tuesday/Wednesday: other coursework, life)
- **Session 2 (Thursday, 60 min):** Returns and must spend 15 minutes re-orienting: "What was my question? Did I already read this? Where should I look next?" (reacquaintance cost; Li et al. 2020)
- **Session 3 (Friday, 120 min):** Focuses on policy angle; cross-references with earlier findings; completes draft
- **Total time wasted on re-orientation:** ~20% of search time (Hoeber, Islam et al. 2024)

### Pain Points with Current Tools

1. **Search history is just a list:** Browser history shows 47 links; no context about *why* each was visited
2. **Folder/tag systems require overhead:** Jamie used Zotero to tag papers, but labeling took mental effort; abandoned after Session 1
3. **No way to externalize metacognitive state:** Browser doesn't show: "You were deciding between X and Y" or "You were exploring the policy angle"
4. **Working memory overload on return:** Reacquaintance requires holding: previous search goals + what was already read + what gaps remain, all at once
5. **Text-heavy screenshots/notes:** Jamie's own notes are dense paragraphs; re-reading them is cognitively taxing

### Strengths & Capabilities
- Highly motivated; researches thoroughly when supported
- Strong visual-spatial reasoning; benefits from visualizations and color-coding
- Aware of own working memory limits; proactively uses external tools (notes, screen reader, accessibility features)
- Comfortable with technology; uses multiple research tools weekly

### Session Characteristics (For Design Validation)
- Searches typically 60–120 min per session
- Often interrupted (notifications, roommate, class) — needs graceful pause/resume
- Reviews 8–15 results per session
- Saves/bookmarks ~4–6 per session; later realizes 2–3 were useful
- Frequently pivots direction based on abstracts ("Oh, I didn't know X was a thing")
- Rarely re-reads own notes; prefers interface-provided context

---

## Task Scenario: "Environmental Justice and Green Space Access" (Realistic Situation)

### Context & Motivation
Jamie is in Environmental Science 301 (Senior Seminar). The assignment: write a 4,000-word research paper on one aspect of environmental justice. Jamie chose "How does green space access relate to environmental justice in North American cities?"

**Why this matters:** 
- Not a simple definition lookup
- Requires Jamie to integrate multiple disciplinary perspectives
- Will involve real cross-session exploratory search (Hoeber 2025)
- Represents authentic undergraduate research workflow

### Session Breakdown

**Session 1: Initial Exploration (Monday 2–3:30 PM)**
- **Starting knowledge:** "Green space is healthy, environmental justice is about fairness, but are they connected?"
- **Goal (vague):** "Find papers that talk about this. Figure out if it's even a real thing."
- **Search path:**
  1. Query: "environmental justice green space" → 127 results, overwhelmed
  2. Query: "urban green space equity" → 34 results, better, but mix of urban planning + ecology + sociology
  3. Saved 5 papers: 3 on green-space-access in cities, 2 on environmental justice definitions
- **Ending state:** Confused about how it all fits together, realizes there's a policy/regulation angle Jamie didn't expect
- **What Jamie did:** Bookmarked papers in browser; closed laptop, went to class

**Reacquaintance Gap (Tuesday–Wednesday)**
- Jamie does other homework, goes to lab, forgets specifics of the search
- Thursday morning: "What was I researching?" Must re-discover: the theme was urban green space + justice

**Session 2: Pivot & Depth (Thursday 3–4 PM)**
- **Starting state:** Can't remember which papers covered what; re-reads all 5 saved abstracts to understand the landscape again (~8 min cognitive overhead)
- **New realization:** "It's really about *access* — who gets to use green space, who has to travel far, who decides where it gets built"
- **Searches:** "green space access urban poor" → finds 12 new results, saves 3 more
- **Outcome:** Now understands the framing; ready to focus on policy angle in Session 3

**Session 3: Policy Angle & Integration (Friday 7–9 PM)**
- **Starting goal:** "Find papers on policy/regulation for green space in cities; connect to what I found before"
- **Searches:** "urban green space policy" + "environmental justice policy" → finds case studies
- **Key moment:** Realizes one paper (Session 2) directly cites a policy paper Jamie just found → aha moment about how arguments connect
- **Outcome:** Completes research phase; has 11 core papers, understands debate

### What the Interface Needs to Support

1. **Session 1 (initial exploration):** Show Jamie that search is multi-directional, help recognize overlapping themes
2. **Reacquaintance (2-day gap):** Externalize session 1's goals and saved papers *in context* so re-orientation takes 2 min, not 8
3. **Session 2 (pivot):** Show Jamie what was searched before, what was found, how to pick a new angle without starting over
4. **Session 3 (integration):** Show Jamie how new papers relate to old ones; surface the citation connection Jamie discovered

### Specific Challenges for Dyslexia
- Reading all 5 abstracts again (Session 2) was tiring; a visual summary would help
- "12 new results" are all text; hard to rapidly see which are relevant; color-coded categories (Excellent / Good / Possible) would be faster than reading
- Holding three goals at once (prior work + new direction + integration point) exceeds working memory; needs externalized list
- Paper titles and snippets are text-heavy; numbers ("72% confidence in X topic") feel like more text, not clarity

---

## Abbreviated Persona for Presentations/Defenses

### One-Page Summary: Jamie Chen

**Who:** Third-year undergrad, environmental science major, dyslexia (mild–moderate), competent digital-tool user.

**Search Profile:** Cross-session exploratory research (60–120 min sessions, 2–7 day gaps, 8–15 results reviewed, 4–6 saved per session). Topic: complex and multi-disciplinary (environmental justice + green space). Requires multiple sessions to develop understanding.

**Working Memory Constraint:** Holds ~3–4 items simultaneously (Choi & Arguello 2025). Loses search thread after interruption or 30-min browsing (Li et al. 2020). Cannot simultaneously hold task goals + prior results + new queries in mind.

**Pain Points:** 
- Reacquaintance overhead: ~15 min re-reading old results after 2-day gap (20% of session time)
- Text-heavy interfaces cause fatigue (Rello & Baeza-Yates 2016)
- Search history doesn't show *why* results were visited; folder systems require overhead
- Numbers consume cognitive load like text (working memory constraint, not reading speed)

**Strength:** Highly motivated; responds well to visual structure and external metacognitive scaffolds that free working memory.

**Design Implication:** Interface should externalize search goals, prior results, and topic connections so working memory is freed for actual search decisions.

---

## Task Scenario (Short Version)

**Paper assignment:** "Environmental justice and green space access in North American cities"

**Session progression:**
- Session 1: Initial exploration, saves 5 papers, confused about how it all connects
- Reacquaintance gap (2 days)
- Session 2: Re-reads old papers to re-orient (~8 min lost), pivots to policy angle, saves 3 more
- Session 3: Integrates new findings with old ones; recognizes citation connection

**What fails:** Reacquaintance takes 8 minutes; abstract re-reading is tedious; can't hold "where I was" + "where I'm going" at once.

**What succeeds:** Visual categorization (Excellent/Good/Possible topics per paper) beats percentages; session recap showing prior goals + saved papers helps re-orient; connections between papers are visible.

---

## Academic References Grounding This Persona

### Working Memory
- **Choi & Arguello (2025):** Working memory deficits in dyslexia; working memory load during search decision-making
- **Zhu et al. (2026):** ADHD and working memory; working memory in information seeking

### Dyslexia & Accessibility
- **Rello & Baeza-Yates (2016):** Font, spacing, color preferences for dyslexia
- **Duranovic (2018):** Reading speed and accuracy in dyslexia; visual processing
- **Morris et al. (dyslexia clutter study):** Visual clutter and data-ink ratio preferences

### Cross-Session Search
- **Li et al. (2020):** Reacquaintance cost; multi-session exploration; stopping reasons (6 categories: goals achieved, satisfaction, interruption, cannot find, consult sources, low task knowledge)
- **Hoeber, Islam, et al. (2024):** Timeline visualization for cross-session search; what users need to re-orient
- **Hoeber (2025):** Exploratory search definition and why it requires multiple sessions

### Metacognition in Search
- **Crescenzi et al. (2021):** Metacognitive activities (planning, monitoring, evaluating, revising); scaffolding definition; OrgBox tool
- **[Urgo & Arguello — to be read]:** Deep metacognition framework

### Search Behavior
- **Gomes et al. (2022):** Cognitive load and lost-track behavior in exploratory search
