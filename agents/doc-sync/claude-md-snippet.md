## Docs sync (added 2026-10-25)

- Every commit that touches `frontend/src` or `backend` (not tests, mocks, ui-dev) needs a `doc-impact:` line in its message. A git hook checks it. `doc-impact: none` is allowed.
- After a functional change run `/done`. It updates `docs/spec/`, `DECISIONS.md`, `STATUS.md`, the change ledger in minds-doc and the backup copy in `minds-doc/minds-app-claude-files/`.
- The planning document is never edited by `/done`. Its sync point is `Claude outputs/doc-sync.json` in minds-doc; the ledger (`Claude outputs/change-ledger.md`) lists what is still pending.
- To bring the planning document up to date, follow `agents/doc-sync/README.md` in minds-doc.
