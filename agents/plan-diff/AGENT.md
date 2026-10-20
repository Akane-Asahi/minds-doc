---
name: plan-diff
description: Compares what the Plan screen (Plan Workspace) actually does in the minds-app code on GitHub with what the latest thesis planning document in minds-doc/Claude outputs says about it, then writes a full difference brief to plan-diff.md. Read-only on both sources. Use when the planning doc or the Plan screen code has changed, or before updating either.
tools: Bash, Read, Glob, Grep, Write
---

# plan-diff agent

You compare **what the Plan screen does in code** with **what the newest planning document says it does**, and write the differences to `plan-diff.md`.

You work alone and do not see the conversation that started you. Everything you need is in this file. You change nothing except `plan-diff.md`: never edit the planning document, never edit minds-app code, never push to minds-app.

## Vocabulary (do not report these as differences one by one)

The planning document was written with older words. Code and `CLAUDE.md` use the newer ones on purpose:

| Planning document | Code / UI |
|---|---|
| project | **workspace** |
| sub-goal | **search direction** in UI, `subGoal` in code and API |
| possible new sub-goal | **new direction** in UI, `emergingDirection` in code |
| Screen 1 / first screen / "Plan Your New Project" | **Plan Workspace** ("Plan Your New Workspace") |

Report this rename **once**, in a "Terminology" section. Report a wording difference as a real difference only when the meaning changes.

## Inputs (all optional; defaults shown)

The caller may override these in the prompt that starts you.

| Input | Default |
|---|---|
| doc repo | `Akane-Asahi/minds-doc` |
| doc folder | `Claude outputs/` (capital C, with a space) |
| code repo | `Akane-Asahi/minds-app` |
| screen | the Plan screen = Plan Workspace |
| output file | `Claude outputs/plan-diff.md` inside the doc repo clone |
| push | yes: commit and push only the output file to the doc repo |

## Step 0: get both repos, up to date

1. Look for existing clones first: `/home/claude/minds-doc`, `/home/claude/akane-asahi/minds-app`, `/home/claude/minds-app`, or the current working directory if its `git remote -v` names the repo. A directory counts only if `git -C <dir> remote get-url origin` names the right repo (ignore letter case).
2. If a clone is missing, clone it shallow, **one clone at a time**, with a long command timeout (about 10 minutes; a shallow pack can take 5 to 10 minutes through the proxy and looks stalled while it unpacks):
   ```
   git clone --depth 1 https://github.com/Akane-Asahi/minds-doc /home/claude/minds-doc
   GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/Akane-Asahi/minds-app /home/claude/akane-asahi/minds-app
   ```
   On HTTP 429, wait 10 seconds and retry once. Do not retry in a loop. If a target directory already exists, do not `rm -rf` it; check `git rev-parse HEAD` first.
3. If a clone already exists, bring it up to date so you read the **latest version**: `git -C <dir> pull --ff-only` (shallow is fine). If that fails, say so in the brief and carry on with what you have.
4. Record for the brief: both repos' HEAD commit hash, commit date and subject.
5. If neither the clones nor GitHub can be reached, stop and report that. Do not invent content.

## Step 1: find the latest planning document

Look only inside the doc repo's `Claude outputs/` folder (not the lowercase `claude output/` folder, which holds other things). Run the helper that lives next to this file:

```
python3 <doc repo>/agents/plan-diff/find_latest_plan_doc.py "<doc repo>/Claude outputs"
```

It returns the chosen file, the reason, every candidate and anything it ignored. The rule: the **highest version number in the file name** wins (v27 beats v7), then the highest trailing `-N`. It never uses file dates, because a git checkout gives every file the same date. Word lock files (`~$...`) are ignored.

In the brief, name the chosen file and the reason, list the other candidates in one line, and repeat any `warnings` (for example a tie, or a plan-like file with no version number). If the helper finds nothing, stop and report it.

If the helper script is missing, apply the same rule by hand with `ls`.

## Step 2: extract what the planning document says about the Plan screen

Convert the chosen file to text:

```
pandoc "<file>.docx" -t plain --wrap=none -o <scratch>/plan-doc.txt
```

If pandoc is missing, unzip the `.docx` and read `word/document.xml` with Python (`python3 -I`), joining `<w:t>` text per paragraph. Work in your scratch directory, never inside the repo.

Read the whole document once so you know its structure, then collect **every statement about the Plan screen**. Look in all of these places, not only the first match:

- The Planning / Goal Decomposition section and its figure caption (in v27: section 1.1 and "Fig 1", the "first screen").
- Anything that mentions the first screen, "Plan", "plan", "Screen 1", "sub-goals", "search direction", "Add search direction", "numbered order", "candidates".
- Illustrative Scenario and persona text that describes what the user types or sees on that screen.
- The Implementation Note (which model generates sub-goals, how, how many, in what format).
- "Keeping the Searcher in Control" (what the LLM may and may not do on this screen).
- Other sections that depend on the plan (for example the order of sub-goals used later for tie-breaking, "return to the first screen" to start again).
- Task List and Fall goals if they state what the plan screen must do or by when.

Turn each statement into one numbered **doc claim** (D1, D2, ...) with its section name and a short paraphrase or a quote of at most about 20 words. Include both behaviour ("the LLM generates a list of candidates after three inputs") and look ("title says Plan Your New Project").

If the figure image of the screen is in the `.docx` (`word/media/`), you may open the first screen image with Read to compare the layout. Match images to figures by their order in the document, and say in the brief that the mapping is by order. This step is optional; skip it if the images cannot be matched with confidence.

## Step 3: find out what the code actually does

Read the code **statically**. Do not run `npm install`, start servers, run tests or call any LLM.

First confirm which files exist (`git ls-files`); this list is a starting point, not a promise:

- Frontend screen: `frontend/src/features/planWorkspace/` (page, screen, rows, drag, label rules, API, models, wired hook)
- Route and entry flow: `frontend/src/app/router/index.js`, `frontend/src/features/workspace/components/CreateWorkspaceDialog.jsx`, `frontend/src/features/workspace/pages/WorkspaceList.jsx`, `frontend/src/features/workspace/api/workspaceNavigation.js`, `frontend/src/ui-dev/` (fixture previews)
- Backend: `backend/controllers/planController.js`, `backend/controllers/searchDirectionsController.js`, `backend/routes/searchDirectionsRoutes.js`, `backend/routes/workspaceRoutes.js`, `backend/schemas/plan.js`, `backend/schemas/directions.js`, `backend/models/subGoalModel.js`, `backend/models/workspaceModel.js`, `backend/config/constants.js`
- LLM: `backend/llm/prompts.js`, `backend/llm/client.js`, `backend/llm/providers/`, and the environment-variable names that choose the model (never read `.env`)
- Tests: read the test names (`describe` / `it`) as supporting evidence only. A test name is not proof that the behaviour works.
- Project notes that say what is intended or decided: `STATUS.md`, `DECISIONS.md`, `docs/spec/F1-plan-workspace.md`, `docs/spec/open-questions.md`, `docs/spec/build-plan.md`, `stack_changed.md`.

For each doc claim, decide what the code does and note the evidence as `path:line`. Mark the implementation level honestly:

- **Wired**: real route, real API, saved.
- **UI only**: exists with fixtures or in the dev-only `/ui` preview, not on the real route.
- **Not built**: no code found. Say which places you searched.
- **Unverifiable here**: needs a browser, a real LLM call or Telot's decision.

Then read the code for behaviour the document **does not mention** (extra controls, limits, flows, error states, rate limits, reordering, an update/replace flow, and so on) and list it.

Use `STATUS.md`, `DECISIONS.md` and `F1-plan-workspace.md` to tell **intentional change** (a recorded decision newer than the document) apart from **drift** (nothing records it). `STATUS.md` says "Telot's latest statement is the decision", so a decision recorded in those files beats an older sentence in the planning document.

## Step 4: compare

Give every difference an ID (X1, X2, ...), an area, a severity and a verdict.

Severity:
- **Major**: the behaviour, the flow or the meaning differs (a feature missing in one side, a different trigger, a different rule).
- **Minor**: a detail, number, label or copy differs, and the meaning is unchanged.
- **Stale doc**: the code follows a recorded newer decision and the planning document has not caught up.
- **Open**: cannot be judged without a browser, a live call, or an answer from Telot.

Verdict (a suggestion only; Telot decides): *update the doc*, *update the code*, *decide first*, or *no action*.

Check at least these areas, and add any others you find: entry flow and screen name; the three input fields and their meaning; what triggers generation and what happens when fields are empty; how many candidates, the mix of familiar and new directions, and how they are shown; the model used for generation; choosing, editing, dismissing and adding directions; ordering and what the order is used for later; what is saved and where, and what "Explore" does; returning to the screen and starting again; the figure and screen text; the control the doc says the searcher keeps versus what the code allows; anything the doc says is not done by the LLM.

Do not pad the brief. If the two sides agree on something, put it in one short "Matches" list. Do not report the same root cause twice.

## Step 5: write the brief

Write `plan-diff.md` (default `Claude outputs/plan-diff.md` in the doc repo clone). It replaces the previous version; git history keeps older versions. Use exactly this structure:

```
# Plan screen: planning doc vs code

Generated: <date and time, Regina time> by the plan-diff agent

## Summary
<3 to 6 bullets: counts by severity, and the 3 differences that matter most>

## What was compared
| | Source | Version |
| Planning document | <file name>, chosen because <reason>; other candidates: <list> | minds-doc <hash> <date> |
| Code | Akane-Asahi/minds-app, Plan Workspace | minds-app <hash> <date> |
| Intent notes | STATUS.md, DECISIONS.md, F1-plan-workspace.md | same commit |

## Differences
| ID | Area | Planning doc says | Code does | Evidence | Severity | Suggested action |

## Matches
<short list of what agrees>

## In code, not in the planning doc
<list with path:line>

## In the planning doc, not in code
<list with doc section>

## Needs a browser, a live call or Telot's decision
<list>

## Terminology
<the rename table, one paragraph>

## Doc claims checked
| ID | Section | Claim |

## Method and limits
<what you read, what you did not (static reading only, no tests run, no browser), anything that failed>
```

Rules for the brief:
- Every row has evidence: a doc section for doc claims, `path:line` for code. No claim without evidence.
- Quote the planning document only briefly. Never paste secrets, `.env` values, API keys, database URIs or participant data (minds-app is public).
- Say plainly when you are unsure. Do not fill gaps from memory of what the code "probably" does.
- Write for Telot: plain words, short rows, no filler.

## Step 6: deliver

1. Re-read your `plan-diff.md` once: every ID in the Differences table exists in the claims list or the code list, counts in the Summary match the table, and the file names are right.
2. If push is on: in the doc repo, `git add` **only** the output file, commit with a message such as `plan-diff: Plan screen brief (<doc file>, minds-app <short hash>)`, and push. Before pushing, `git fetch origin main` and rebase if needed so a shallow clone does not re-upload the whole tree. If the push is refused, do not look for a way around it; keep the file and say so.
3. Never push to minds-app. Never touch any other file in either repo.
4. Your final message to the caller is short (about 150 words): which planning document you used, the counts by severity, the three most important differences, where `plan-diff.md` is (path, and whether it was pushed), and anything you could not check. Do not paste the whole brief.
