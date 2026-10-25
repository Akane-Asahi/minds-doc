#!/usr/bin/env python3
"""Which diff agents, spec files and planning-doc sections does the work since the last sync touch?

Usage:
  python3 which-diff.py [--from <commit>] [--app <minds-app path>] [--doc <minds-doc path>] [--files]

--from  defaults to minds_app_commit in "Claude outputs/doc-sync.json" (the commit the planning doc was last synced to)
--app   defaults to $MINDS_APP, else the current directory
--doc   defaults to the minds-doc repo this script sits in
--files print every changed functional file under its area

Read-only. It runs git log / git diff on minds-app and reads doc-map.json and the change ledger.
"""
import argparse, json, os, re, subprocess, sys


def git(app, *args):
    r = subprocess.run(["git", "-C", app, *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip())
    return r.stdout


def pending_entries(ledger_path):
    """Ledger entries start with '### ' and carry '- Affects:' and '- Doc status:' lines.
    Lines inside ``` code blocks (the format example) are skipped. Returns [(title, affects)] for status 'pending'."""
    if not os.path.exists(ledger_path):
        return []
    out, head, affects, fenced = [], None, "", False
    for line in open(ledger_path, encoding="utf8"):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("### "):
            head, affects = line[4:].strip(), ""
            continue
        m = re.match(r"-\s*Affects:\s*(.+)", line.strip())
        if m:
            affects = m.group(1).strip()
        m = re.match(r"-\s*Doc status:\s*(.+)", line.strip())
        if m and head:
            if m.group(1).strip().lower().startswith("pending"):
                out.append((head, affects))
            head = None
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    doc_default = os.path.abspath(os.path.join(here, "..", ".."))
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="frm")
    ap.add_argument("--app", default=os.environ.get("MINDS_APP", "."))
    ap.add_argument("--doc", default=doc_default)
    ap.add_argument("--files", action="store_true")
    a = ap.parse_args()

    out_dir = os.path.join(a.doc, "Claude outputs")
    marker = {}
    mp = os.path.join(out_dir, "doc-sync.json")
    if os.path.exists(mp):
        marker = json.load(open(mp, encoding="utf8"))
    frm = a.frm or marker.get("minds_app_commit")
    if not frm:
        sys.exit("No --from given and no minds_app_commit in doc-sync.json.")
    cfg = json.load(open(os.path.join(here, "doc-map.json"), encoding="utf8"))
    functional, ignore = re.compile(cfg["functional"]), re.compile(cfg["ignore"])

    try:
        git(a.app, "cat-file", "-e", frm + "^{commit}")
    except RuntimeError:
        sys.exit(f"Commit {frm} is not in {a.app}. If the clone is shallow, run: git fetch --depth=200 origin")

    head = git(a.app, "rev-parse", "--short", "HEAD").strip()
    commits = [l for l in git(a.app, "log", "--format=%h %ad %s", "--date=short", f"{frm}..HEAD").splitlines() if l]
    changed = set(git(a.app, "diff", "--name-only", frm).splitlines())
    changed |= set(git(a.app, "ls-files", "--others", "--exclude-standard").splitlines())
    files = sorted(f for f in changed if functional.search(f) and not ignore.search(f))

    by_area, unmapped = {}, []
    for f in files:
        hit = False
        for area in cfg["areas"]:
            if any(re.search(p, f) for p in area["paths"]):
                by_area.setdefault(area["name"], []).append(f)
                hit = True
        if not hit:
            unmapped.append(f)
    area_cfg = {x["name"]: x for x in cfg["areas"]}

    agents, specs, sections = [], [], []
    for name in by_area:
        c = area_cfg[name]
        agents += [x for x in c["agents"] if x not in agents]
        specs += [x for x in c["spec"] if x not in specs]
        sections += [x for x in c["planSections"] if x not in sections]

    pend = pending_entries(os.path.join(out_dir, "change-ledger.md"))

    print(f"Since {frm[:7]} ({marker.get('planningDoc', '?')} sync point): {len(commits)} commits, {len(files)} functional files changed, minds-app HEAD {head}")
    if not files and not pend:
        print("Nothing to sync.")
        return
    print("\nRun these diff agents:", ", ".join(agents) if agents else "none (no agent covers the changed files)")
    for name, fs in by_area.items():
        c = area_cfg[name]
        tag = ", ".join(c["agents"]) or "no agent"
        print(f"  {name}  [{tag}]  {len(fs)} file(s)")
        if a.files:
            for f in fs:
                print(f"      {f}")
    print("\nSpec files to check:", ", ".join(specs) or "none")
    print("Planning-doc sections to re-read:")
    for s in sections:
        print(f"  - {s}")
    if unmapped:
        print("\nChanged but not in doc-map.json (add them):")
        for f in unmapped:
            print(f"  {f}")
    print(f"\nLedger entries with Doc status: pending: {len(pend)}")
    for h, aff in pend:
        print(f"  - {h}")
        if aff:
            print(f"      affects: {aff}")
    if commits:
        print("\nCommits in range:")
        for c in commits:
            print(f"  {c[:110]}")


if __name__ == "__main__":
    main()
