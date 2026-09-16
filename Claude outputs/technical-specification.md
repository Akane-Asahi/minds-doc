# Technical Specification: AI-Assisted Metacognitive Search Scaffold

*A build-ready spec, written so any AI coding assistant (or developer) can implement
this system directly from this document. It consolidates the design in
`thesis-scope-llm-metacognitive-serp.md`, the persona in `final-persona.md`, the AI
goals in `ai-goals-in-system.md`, and the tech stack discussion, into one reference.*

---

## 1. What this system does, in one paragraph

A user starts a research task by stating a goal, what they already know, and what they
want to find out. An LLM proposes sub-goals to decompose that task, and generates the
actual search queries behind whichever sub-goals the user selects. Results come back
from the University of Regina's library search API (Ex Libris Primo, branded "Quick
Find"), get classified by the LLM against the user's sub-goals, and are shown with a
categorical match badge that lets the user decide whether to save something without
reading it. All of this state (sub-goals, coverage, saved items, session history)
persists across sessions, so returning after a gap of days reinstates the user's mental
context instead of forcing them to reconstruct it from scratch.

The target user is someone with dyslexia and/or low working memory (see
`final-persona.md`, Jamie Chen), for whom the expensive resource is not time, it is
working memory itself. Every design and technical decision below optimizes for that.

---

## 2. Architecture overview

```
Browser (Next.js/React frontend)
        |
        v
Next.js API routes (orchestration layer)
        |
        +--> Ex Libris Primo Search API   (external, University of Regina's index)
        |
        +--> LLM API (Claude or GPT, structured output)
        |
        v
Postgres via Supabase (persistence)
```

Recommended stack, sized for a one person thesis build with a working prototype and a
user study, not a production system:

- **Frontend:** Next.js (React + TypeScript), Tailwind CSS.
- **Orchestration/backend:** Next.js API routes in the same codebase. This layer is
  the actual novel engineering in this project, it is what turns a plain search box
  into the four AI behaviors described in `ai-goals-in-system.md`.
- **LLM:** Claude or GPT-4o-mini, called with structured/tool-calling output, not free
  text, so responses parse reliably into the JSON shapes defined in section 5. Default
  to a cheaper/faster model; escalate to a stronger one only where testing shows the
  cheaper model's classification quality is not good enough.
- **External data source:** Ex Libris Primo Search API, University of Regina's
  instance. See section 4, this is the one dependency outside your control.
- **Database:** Postgres via Supabase (auth, persistence, and hosting in one place,
  minimal ops overhead for a thesis timeline).
- **Hosting:** Vercel for the Next.js app, Supabase cloud tier for the database.

---

## 3. The shared state model

Every screen in this system is a different view over one underlying object per task.
This is the single most important modeling decision in the whole system, do not let
sub-goals, coverage, and recap drift into separate data structures.

```
Task
  goal_text, known_text, want_text
  sub_goals: [
    {
      id, label,
      shown_count, opened_count, saved_count,   // behavioral, bounded to results actually shown
      clarity: "clear" | "so_so" | "unclear" | null   // subjective, set only by the user, never inferred
    },
    ...
  ]
  unopened_leads_count
```

Two rules that must not be violated by any implementation shortcut:

- **Coverage counts are never a percentage of the full result set.** The denominator
  is always "results shown so far under this sub-goal," never the size of the
  underlying Primo index. A query with 128 hits does not make coverage "3 of 128."
- **Clarity is never LLM-inferred.** It is a one-tap 👍/😐/👎 the user sets themselves,
  in exactly two places (the Session Overview sub-goal card, and the matching Plan
  Strip chip), always showing the same value. Before the user sets it, render it as
  unrated, never as a fabricated default.

---

## 4. External dependency: Primo Search API

University of Regina's Archer Library search tool ("Quick Find") runs on Ex Libris
Primo. This is an institution-gated API, not self-serve, so before writing the
integration code, someone at the library has to register the application in the Ex
Libris Developer Network and issue an API key scoped to their Primo instance (or, on
older deployments, allowlist your server's IP under the XServices access model
instead). Confirm the following with the library before finalizing the integration:

- Whether returned records reliably include an abstract/description field, or mostly
  citation-level metadata only. This directly determines classification quality.
- The institution code, the correct regional REST API base URL, and the `vid` (view
  id) to scope searches correctly.
- Daily/hourly call quota. This system makes more calls per user search than a person
  typing into Quick Find would (one query per selected sub-goal, potentially several
  sub-goals at once), so budget for that multiplier.

**Per-result fields this system needs from Primo:** title, author(s), venue ("Is Part
Of"), keywords, abstract/description, resource type, identifiers (DOI/ISSN/PMID). No
full text is fetched or needed anywhere in this system.

**Caching:** cache raw Primo responses keyed by normalized query string, with a TTL on
the order of 24 hours. Scholarly metadata for a given query does not change minute to
minute, and this protects the daily quota during both development and the live study.

**Fallback while access is pending:** build and test against mocked JSON fixtures
shaped like a Primo response, so the frontend and LLM orchestration work are not
blocked on the library's turnaround time.

---

## 5. LLM calls: prompts and structured output schemas

All four calls below use structured/tool-calling output. Do not parse free text.

### 5.1 Sub-goal generation

Called once, when a task is created.

**Input:** `goal_text`, `known_text`, `want_text`.

**Output schema:**
```json
{
  "sub_goals": [
    { "label": "string, 2-5 words" }
  ]
}
```

### 5.2 Query generation

Called after the user selects which sub-goals to pursue.

**Input:** `goal_text`, the selected sub-goal labels.

**Output schema:**
```json
{
  "queries": [
    { "sub_goal_id": "string", "query_text": "string, sent to Primo as-is" }
  ]
}
```

### 5.3 Result classification (batched, not per-result)

Called once per search, over the full merged/deduped result set from all Primo calls
in that search. Batching is a cost and latency requirement, not an optimization detail.

**Input:** the user's sub-goal list, and for each result: title, authors, venue,
keywords, abstract, resource type; plus the user's already-saved item ids for that
task, to allow the "similar to something you saved" and "possible duplicate" badges.

**Output schema:**
```json
{
  "classifications": [
    {
      "result_id": "string",
      "sub_goal_id": "string | null",
      "badge": "new | seen_before | similar_to_saved | fills_gap | possible_duplicate",
      "reasoning": "one sentence, shown on tap-to-expand"
    }
  ]
}
```

### 5.4 Session recap generation

Called when a session ends (on check-out), generating the recap shown at the start of
the *next* session.

**Input:** the task's shared state (section 3) as it stood at session end, plus the
check-out reason.

**Output schema:**
```json
{ "recap_text": "2-3 sentences, plain language" }
```

### 5.5 Cross-session history recap

Called when rendering Session History (component 6) for a task with 2+ sessions.

**Input:** all past sessions' recaps and their per-sub-goal saved-count deltas.

**Output schema:**
```json
{ "overall_recap": "string", "per_session_recaps": [{ "session_id": "string", "recap": "string" }] }
```

**Non-negotiable UX requirement on every LLM output that reaches the UI:** it must be
editable or dismissible in one tap (sub-goal chips, classifications), and it must carry
a one-line "why" reachable by tap-to-expand (badges). The LLM is a first draft of the
user's own thinking, never presented as an authority on it.

---

## 6. Database schema (Postgres)

```sql
users            (id, email, created_at)

tasks            (id, user_id, goal_text, known_text, want_text, created_at)

sub_goals        (id, task_id, label, clarity, shown_count, opened_count,
                   saved_count, order_index, created_at)

sessions         (id, task_id, started_at, ended_at,
                   checkout_reason)  -- 'done' | 'break' | 'stuck' | 'need_help' | null

queries          (id, session_id, sub_goal_id, query_text, created_at)

results_cache    (id, primo_record_id, title, authors, venue, keywords,
                   abstract, resource_type, identifiers, raw_json, cached_at)
                   -- shared across users/sessions, keyed by primo_record_id

session_results  (id, session_id, result_id -> results_cache.id, sub_goal_id,
                   badge, badge_reasoning, opened boolean, saved boolean,
                   shown_at, opened_at, saved_at)
                   -- the per-session log; this is what Session Detail reconstructs
                   -- from, and what sub_goals' cumulative counts aggregate over

session_recaps   (id, session_id, recap_text, generated_at)
```

`session_results` is the source of truth for both the cumulative counts on `sub_goals`
(recompute or increment transactionally on save/open) and the read-only Session Detail
reconstruction (component 7), which is just this table filtered to one session_id.

---

## 7. API endpoints

| Endpoint | Purpose |
|---|---|
| `POST /api/tasks` | Create task from goal/known/want text; calls 5.1; returns candidate sub-goals |
| `PATCH /api/tasks/:id/subgoals` | User accepts/edits/removes sub-goals before first search |
| `POST /api/tasks/:id/sessions` | Start a session; if a prior session exists, returns the recap (5.4 output) and Session Overview data |
| `POST /api/sessions/:id/search` | Body: selected sub-goal ids. Runs 5.2, calls Primo per sub-goal, merges/dedupes, runs 5.3 once over the full set, returns enriched result list |
| `POST /api/results/:id/save` | Marks saved. No read/open required first. |
| `POST /api/results/:id/open` | Marks opened (for badge/coverage purposes only, no detail page in scope) |
| `PATCH /api/subgoals/:id/clarity` | User sets 👍/😐/👎 — never written by any other caller |
| `POST /api/sessions/:id/checkout` | Records check-out reason, triggers 5.4 for the next session's recap |
| `GET /api/tasks/:id/overview` | Session Overview data (component 0) |
| `GET /api/tasks/:id/history` | Session History (component 6): runs 5.5, returns per-sub-goal saved-count trace |
| `GET /api/sessions/:id/detail` | Session Detail (component 7), read-only reconstruction from `session_results` |

---

## 8. Screens and components

Maps directly onto the eight components in `thesis-scope-llm-metacognitive-serp.md`.

| Screen/route | Components rendered |
|---|---|
| `/task/new` | Goal/known/want input, then sub-goal proposal and selection (feeds 5.1) |
| `/task/:id/serp` (fresh, no prior session) | Component 1 (Plan Strip, pinned top), Component 2 (Coverage Map, sidebar), Component 3 (Evaluation Badges, per result card), Component 4 (Check-out Chip, on exit/idle) |
| `/task/:id/serp` (resumed) | All of the above, plus Component 5 (Session Recap Capsule, shown first) |
| `/task/:id/overview` | Component 0 (Session Overview) — one card per sub-goal: coverage ring + clarity control + unopened leads + recommended next sub-goal |
| `/task/:id/history` | Component 6 (Session History) — cross-session recap, per-session recap, saved-count trace as a stacked horizontal bar (not a percentage, see section 3) |
| `/session/:id/detail` | Component 7 (Session Detail) — read-only: queries issued, opened/saved items, sub-goal state at that session's end |

Evaluation Badges use exactly these five labels (do not invent new ones): *New*, *Seen
before*, *Similar to something you saved*, *Fills a gap in [sub-goal]*, *Possible
duplicate*. Check-out Chip uses exactly these four: *Done*, *Taking a break*, *Stuck*,
*Need to ask someone*.

---

## 9. Frontend/accessibility requirements

These are technical requirements, not visual polish, they follow directly from the
persona in `final-persona.md`.

- Typeface: Atkinson Hyperlegible or Lexend (both designed for reading-differences
  legibility), with generous line spacing.
- Match badges and any other status indicator: color plus icon plus text label, never
  color alone. Three-tier badge palette must pass WCAG AA contrast.
- Never render a raw percentage as the headline number for coverage or the
  cross-session trace (section 3, section 8). Categorical or count-based framing only.
- Session Recap Capsule text renders in an ARIA live region so a screen reader
  announces it immediately on page load, the user should not have to hunt for it.
- Save action is a single control, reachable and triggerable by keyboard alone, no
  read/expand step required first.
- Respect `prefers-reduced-motion` for any progress-ring or transition animation.
- State management: React Query (or equivalent) for server state (tasks, results,
  overview data), lightweight context/Zustand for local UI state (which sub-goals are
  currently expanded, etc).

---

## 10. Non-functional requirements

- **Batch, don't loop:** result classification (5.3) is one LLM call per search, over
  the full result set, never one call per result. This is both a cost control and a
  latency requirement, looping would make the SERP feel broken.
- **Cache Primo responses** (section 4) to protect the institution's call quota.
- **Cost control on the LLM:** default to a cheap/fast model; only escalate for
  quality reasons found in testing, not by default.
- **Secrets:** Primo API key and LLM API key live server-side only (Vercel
  environment variables), never shipped to the browser.

---

## 11. Open dependencies before implementation can start end-to-end

1. Primo Search API access from Archer Library (in progress, see the email drafts
   already sent/prepared to library systems staff and to Milad Momeni).
2. Confirmation of whether Primo's returned records for this institution include a
   usable abstract field across the disciplines the study will cover.
3. Confirmation of the daily/hourly Primo call quota, to size the caching strategy.
4. An LLM provider API key and a cost budget for the study period.
5. Supabase and Vercel project setup (can be done immediately, not blocked on
   anything above).

Everything except item 1-3 can be built and tested today against mocked Primo
fixtures shaped per section 4.
