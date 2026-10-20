#!/usr/bin/env python3
"""Pick the latest thesis planning document in a folder (default: "Claude outputs").

Usage:
    python3 find_latest_plan_doc.py [folder]

Prints JSON: {"chosen": ..., "reason": ..., "candidates": [...], "ignored": [...], "warnings": [...]}

Rule (version number in the file name decides, never the file date, because a git
checkout gives every file the same date):
  1. Only .docx files whose name contains "planning document(s)" and "v<number>" count.
  2. Lock files such as "~$lot Thesis ...docx" and anything else are ignored.
  3. Highest version number wins (v27 beats v7).
  4. Within one version number, the highest trailing "-<number>" wins
     ("... v7 - SRL Stripped-3.docx" beats "... v7 - SRL Stripped.docx").
  5. If two files still tie, the choice is reported as a tie in "warnings"; the
     caller must say so in its report instead of guessing silently.
"""
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"planning\s+documents?\s*v\s*(\d+)(.*)\.docx$", re.IGNORECASE)
TRAILING_NUM_RE = re.compile(r"-\s*(\d+)\s*$")


def main() -> int:
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "Claude outputs")
    if not folder.is_dir():
        print(json.dumps({"chosen": None, "reason": f"folder not found: {folder}",
                          "candidates": [], "ignored": [], "warnings": []}))
        return 2

    candidates, ignored, warnings = [], [], []
    for p in sorted(folder.iterdir()):
        if not p.is_file():
            continue
        name = p.name
        if name.startswith("~$"):
            ignored.append({"name": name, "why": "Word lock file"})
            continue
        m = NAME_RE.search(name)
        if not m:
            if p.suffix.lower() == ".docx" and "plan" in name.lower():
                warnings.append(f"'{name}' looks like a plan file but has no 'v<number>' in its name; not considered")
            ignored.append({"name": name, "why": "not a versioned planning document"})
            continue
        version = int(m.group(1))
        t = TRAILING_NUM_RE.search(m.group(2))
        trailing = int(t.group(1)) if t else 0
        candidates.append({"name": name, "version": version, "trailing": trailing,
                           "bytes": p.stat().st_size})

    if not candidates:
        print(json.dumps({"chosen": None, "reason": "no versioned planning document found",
                          "candidates": [], "ignored": ignored, "warnings": warnings}, indent=2))
        return 3

    candidates.sort(key=lambda c: (c["version"], c["trailing"]), reverse=True)
    best = candidates[0]
    ties = [c for c in candidates if (c["version"], c["trailing"]) == (best["version"], best["trailing"])]
    if len(ties) > 1:
        warnings.append("tie between: " + "; ".join(c["name"] for c in ties))
    reason = f"highest version number v{best['version']}"
    if best["trailing"]:
        reason += f" with highest suffix -{best['trailing']}"

    print(json.dumps({"chosen": best["name"], "reason": reason, "candidates": candidates,
                      "ignored": ignored, "warnings": warnings}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
