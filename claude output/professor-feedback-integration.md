# Professor Feedback Integration Log
**Date:** 2026-08-30  
**Source:** Granola Meeting Notes (Generated)

---

## Core Feedback Themes

### 1. Research Scope & Minimalism Principle
**Feedback:**
- Every UI feature must map to a specific problem, constraint, or user need
- If a feature can't be justified, it shouldn't exist
- This is how minimalist interfaces are built

**Status:** ⏳ REQUIRES DESIGN AUDIT  
**Action Items:**
- [ ] Audit wireframe for every feature; document justification for each
- [ ] Remove features without clear problem mapping
- [ ] Document design rationale in presentation

---

### 2. UI Design for Dyslexia: Text Minimization + Categorization
**Feedback:**
- Minimize text; maximize visual indicators
- **Numbers consume cognitive resources just like words** — this is key
- Replace similarity percentages with ordered classifier:
  - Categories: Excellent / Good / Possible / No Match
  - Map to color intensity (light to dark green)
  - Thresholds need justification through experimentation
- Goal: maximize readability by minimizing unnecessary text, not by removing information

**Current Implementation:**
- Wireframe shows direction-confidence percentages (e.g., "72% Environmental Justice")
- Presentation uses percentages throughout

**Status:** 🔴 CRITICAL - REQUIRES REDESIGN  
**Action Items:**
- [ ] Replace all percentages in wireframe with category labels + color intensity
- [ ] Define threshold mapping (e.g., 0.85+ = Excellent, 0.65–0.84 = Good, 0.40–0.64 = Possible, <0.40 = No Match)
- [ ] Justify thresholds through experimentation (or state as "to be validated")
- [ ] Update presentation slides to remove percentage language
- [ ] Update all explainability modals to reference categories, not percentages

---

### 3. Metacognition: Terminology & Separation of Concerns
**Feedback:**
- Metacognition is a **solution, not a problem**: planning, monitoring, evaluating, revising
- It places a burden on **cognitive resources** (working memory), not searching itself
- Scaffolds are UI features around the primary task; users engage or ignore them
- **CRITICAL:** Keep metacognitive scaffolding separate from cross-session scaffolding
  - Metacognitive scaffolding: planning, monitoring, strategy *during* search
  - Cross-session scaffolding: reacquaintance and resumption
  - Do not conflate the two
- Features to support: planning and monitoring confirmed; evaluation and others need individual justification
- Don't try to support everything; do a few things well

**Current Implementation:**
- Presentation mixes both concerns; wireframe shows session recap + suggested next step
- "Metacognitive scaffold" framing may be too broad

**Status:** 🟡 REQUIRES RESTRUCTURING  
**Action Items:**
- [ ] Explicitly define which features support metacognitive scaffolding vs. cross-session scaffolding
- [ ] Create two separate design matrices showing feature → scaffold type → problem mapping
- [ ] Revise presentation to cleanly separate the two concerns
- [ ] Limit scope: confirm which evaluation/revising features are in scope (not everything)

---

### 4. Presentation Structure: Persona + Task First
**Feedback:**
- Always open with persona and realistic task before any demonstration
- Persona: one-page description of hypothetical representative user (not a scenario)
- Task: include context, motivation, situation — not just "searching for X"
- Prepare detailed persona for thesis + abbreviated version for presentations
- Explain exploratory search from first principles (assume audience doesn't know)
- Spent too long on details of other studies; focus on key takeaways and design justification

**Current Implementation:**
- Presentation does not open with persona
- No explicit task scenario before UI walkthrough

**Status:** 🔴 CRITICAL - REQUIRES RESTRUCTURING  
**Action Items:**
- [ ] Create detailed persona (use ChatGPT as starting point, rewrite in own words with academic references)
- [ ] Create one abbreviated persona for presentations
- [ ] Restructure presentation: Persona → Task → Exploratory Search 101 → Problem → Solution → Design Walkthrough
- [ ] Add slide numbers (current/total format, e.g., 5/18)
- [ ] Trim related-work details; keep only key takeaways that justify design

---

### 5. Terminology Accuracy
**Feedback:**
- Don't rename other authors' models (e.g., "LVSIP")
- If author didn't name it, describe as they did
- Be specific about AI use: distinguish generative AI from other ML (e.g., BERT-based similarity)

**Current Implementation:**
- Presentation uses "LVSIP" as shorthand for Hoeber et al.'s framework
- AI use not clearly contextualized upfront

**Status:** 🟡 REQUIRES REVISION  
**Action Items:**
- [ ] Check each author's original terminology; use theirs or describe accurately
- [ ] Contextualize generative AI use upfront: where is it used, how, why (vs. other ML)
- [ ] Be specific: LLM for summarization? Reranking? Semantic matching?

---

### 6. Working Memory Claims Review
**Feedback:**
- Check working memory claims from presentation for accuracy/completeness
- Urgo and Arguello are key references for metacognition
- Become expert-level on their work before writing

**Current Implementation:**
- Presentation references Choi & Arguello 2025, Zhu et al. 2026 on working memory
- Not all claims have been fact-checked against source material

**Status:** 🟡 REQUIRES VERIFICATION  
**Action Items:**
- [ ] Read Urgo and Arguello papers on metacognition; document key concepts
- [ ] Verify each working memory claim in presentation against source
- [ ] Correct any inaccuracies before next session
- [ ] Read top 5 most-cited papers on scaffolds in information retrieval (Google Scholar)
- [ ] Ground scaffold definition in these papers; add to thesis introduction

---

### 7. Academic Writing Principles
**Feedback:**
- Anticipate every likely question; answer it before it's asked, in right order
- Follow standard structure: intro, literature review, approach, methodology, results, discussion, conclusion
- Explain what a scaffold is explicitly before using the term
- Don't assume shared vocabulary

**Current Implementation:**
- Presentation assumes knowledge of exploratory search, scaffolding, etc.

**Status:** 🟡 REQUIRES REVISION  
**Action Items:**
- [ ] Add explicit definitions for: exploratory search, scaffolding, metacognition, working memory
- [ ] Reorder information to answer likely questions early
- [ ] Check thesis structure against standard academic arc

---

## Action Priority

### Immediate (Before Next Session)
1. **Persona creation** (cascades to all other changes)
   - Detailed persona with academic references
   - Abbreviated presentation version
2. **Replace percentages with categories** in wireframe and slides
3. **Verify working memory claims** against sources
4. **Add slide numbers** to presentation
5. **Read Urgo/Arguello** on metacognition

### Short-term (Next 1-2 weeks)
6. Restructure presentation: Persona → Task → Exploratory Search 101 → etc.
7. Separate metacognitive scaffolding from cross-session scaffolding
8. Read top-cited papers on scaffolds; ground definition
9. Feature audit: map every UI element to specific problem

### Medium-term (Before Thesis Defense)
10. Revise full thesis for terminology accuracy and structure
11. Contextualize all AI use upfront
12. Expand citations for Urgo/Arguello/scaffolding papers

---

## Notes for Next Session
- Professor emphasized: **minimalism is justified by problems, not aesthetics**
- Key insight: **percentages are cognitive load** — categories with color are better for dyslexia
- Must be expert-level on Urgo & Arguello before writing about metacognition
- Persona-first framing is non-negotiable for both presentation and thesis
