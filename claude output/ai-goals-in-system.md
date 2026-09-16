# Goals of the AI in the System

This document captures the four specific roles the AI plays in the exploratory-search
tool, and the working-memory rationale behind each one. This is the "what is the AI
actually *for*" layer that sits underneath the SERP scaffolding design (sub-goal chips,
coverage map, session recap, etc.) described in the main scope document.

---

## 1. Helping the user come up with better sub-goals

At the start of an exploratory search session, the user provides three things:

- **Search goal** — what they want to learn
- **What they already know**
- **What they want to find out**

**Example.**

- Search goal: *"Explore academic literature on how green spaces affect human well-being."*
- What I already know: *"Green spaces include parks, gardens, tree-lined streets, and
  conservation areas. Well-being can include physical, mental, and social dimensions."*
- What I want to find out: *"How do green spaces affect different aspects of human
  well-being?"*

From this, the AI proposes candidate sub-goals — for this example, something like:

- Mental / emotional well-being
- Social engagement
- Mechanisms & environmental pathways
- Different types of green spaces

The user reviews the proposed sub-goals, selects the ones that matter to them, and hits
**Explore**.

**Why this matters:** coming up with the right decomposition of a broad goal into
focused sub-goals is itself a planning task, and planning is exactly the kind of
executive-function work that's hardest to sustain for someone who already has low
working memory going into the session. Handing the user a first draft to react to
(accept, remove, edit) is far cheaper on working memory than generating the
decomposition from nothing.

This also lines up with a concrete empirical finding: Urgo & Arguello's goal-setting
study found that participants given a structured goal-setting tool spent only ~5 minutes
on upfront planning, and that investment produced shorter, more selective notes (deeper
processing rather than copying) and better learning outcomes — **without extending total
task time**. In other words, a little more time spent planning up front is better than
a lot of extra time spent later chasing down mediocre results.

> Urgo, K., & Arguello, J. (2024). *The Effects of Goal-Setting on Learning Outcomes and
> Self-Regulated Learning Processes.* Proceedings of the 2024 ACM SIGIR Conference on
> Human Information Interaction and Retrieval (CHIIR '24).

---

## 2. Generating the actual search queries behind each sub-goal

Once the user selects which sub-goals to pursue and hits **Explore**, the AI uses its
own prompt-design step to turn each sub-goal into strong search queries — the user never
has to write the query themselves.

**Why this matters:** in ordinary search, a user who doesn't know how to phrase a good
query simply gets worse results. That's already a real cost for anyone. For a user who
is already working with constrained working memory, query formulation is one more
executive task competing for the same limited resource — and a bad query is a failure
mode they are the least equipped to notice or self-correct in the moment. Letting the AI
own query construction removes that entire failure point.

---

## 3. Save without reading first

Every result on the SERP carries an AI-generated percentage-match score against the
user's selected sub-goals.

The score is **not** there to help the user skim faster after a quick read. It's there
so the user doesn't have to read the result *at all* to decide whether to save it — the
AI-generated score stands in for that initial read entirely.

**Why this matters:** for a user with dyslexia, reading itself — not deciding, not
navigating — is what consumes working memory. So the design move isn't "reduce reading
time," it's "defer reading entirely" until the user sits down later to actually work
through their saved papers. During the search/collection phase, working memory stays
free for the search task itself (where to look next, whether a direction is panning
out), instead of being spent parsing dense text under time pressure.

---

## 4. Resume without hiccups

After being away from a search for a while — a few days, a week — the AI-generated
summaries and visualizations act as reinstatement cues: what the goal was, what had
already been found, and why.

**Why this matters:** this mirrors context-dependent memory — you recall something more
easily when you're back in the environment where you originally learned it. Reinstating
the right cues brings the memory back directly, rather than forcing the user to
reconstruct their own train of thought by rereading everything from scratch. With those
cues in place, the user picks up mid-thought instead of starting cold.

---

## Summary

| # | AI role | Working-memory problem it targets |
|---|---|---|
| 1 | Propose sub-goals from the stated search goal | Planning / decomposition effort |
| 2 | Generate the search queries per sub-goal | Query-formulation effort |
| 3 | Score results so saving doesn't require reading | In-session reading load |
| 4 | Summarize/visualize state to reinstate context on return | Cross-session memory reconstruction |
