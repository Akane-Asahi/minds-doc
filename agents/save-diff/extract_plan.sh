#!/usr/bin/env bash
# Turn the planning document (.docx) into readable markdown plus its figures.
#
# Usage: extract_plan.sh <plan.docx> <outdir>
#
# Writes   <outdir>/plan.md      text with tracked changes and comments kept
#          <outdir>/media/       the figures (image1.png ...)
# Prints   headings, figure/caption pairs, tracked-change and comment counts, and every line that mentions
#          saving or the Saved results view (line numbers refer to plan.md).
# Needs pandoc; without it, falls back to python-docx plus unzip (no tracked changes or comment text).

set -uo pipefail

DOCX="${1:?usage: extract_plan.sh <plan.docx> <outdir>}"
OUT="${2:?usage: extract_plan.sh <plan.docx> <outdir>}"
[ -f "$DOCX" ] || { echo "ERROR: no such file: $DOCX" >&2; exit 2; }
DOCX="$(cd "$(dirname "$DOCX")" && pwd)/$(basename "$DOCX")"   # absolute: pandoc runs from inside the output folder
mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"
rm -rf "$OUT/media" "$OUT/plan.md"

if command -v pandoc >/dev/null 2>&1; then
  # --extract-media writes to <outdir>/media; run from OUT so the markdown refers to media/imageN.png
  ( cd "$OUT" && pandoc "$DOCX" -t markdown --wrap=none --track-changes=all --extract-media=. -o plan.md ) \
    || { echo "ERROR: pandoc failed" >&2; exit 1; }
else
  echo "pandoc not found; using python-docx fallback (no tracked changes or comments)" >&2
  mkdir -p "$OUT/media"
  python3 - "$DOCX" "$OUT" <<'PY' || exit 1
import sys, zipfile, re
from pathlib import Path
try:
    import docx
except ImportError:
    sys.exit("ERROR: neither pandoc nor python-docx is installed (pip install --break-system-packages python-docx)")
src, out = sys.argv[1], Path(sys.argv[2])
d = docx.Document(src)
lines = []
for p in d.paragraphs:
    style = (p.style.name or "") if p.style is not None else ""
    m = re.match(r"Heading (\d)", style)
    text = p.text.strip()
    if not text:
        lines.append("")
    elif m:
        lines.append("#" * int(m.group(1)) + " " + text)
    else:
        lines.append(text)
    if "graphic" in p._p.xml and "<pic:pic" in p._p.xml:
        lines.append("![](media/figure)")
(out / "plan.md").write_text("\n".join(lines), encoding="utf-8")
with zipfile.ZipFile(src) as z:
    for n in z.namelist():
        if n.startswith("word/media/"):
            (out / "media" / Path(n).name).write_bytes(z.read(n))
PY
fi

# pandoc's --extract-media=. puts files in ./media/ ; make sure the folder exists for the summary below
[ -d "$OUT/media" ] || mkdir -p "$OUT/media"

PLAN="$OUT/plan.md"
echo "== extracted: $PLAN ($(wc -l < "$PLAN") lines), media: $(ls "$OUT/media" | wc -l) files =="
echo
echo "== headings (line: heading) =="
grep -n -E '^#{1,4} ' "$PLAN" | cut -c1-140
echo
echo "== figures and captions (image line -> caption line) =="
awk '
  /!\[[^]]*\]\([^)]*\)/ { match($0, /\(([^)]*)\)/); img=substr($0, RSTART+1, RLENGTH-2); imgline=NR; next }
  imgline && /^\*?Fig/   { printf "%d -> %d  %s  %s\n", imgline, NR, img, substr($0,1,110); imgline=0 }
' "$PLAN"
echo
echo "== tracked changes / comments in the plan =="
ins=$(grep -c -E '\{\.insertion' "$PLAN" || true)
del=$(grep -c -E '\{\.deletion' "$PLAN" || true)
com=$(grep -c -E '\{\.comment-start' "$PLAN" || true)
echo "insertions: $ins   deletions: $del   comments: $com"
echo "(if any are non-zero, read the affected passages in plan.md and say in the brief whether they touch saved results)"
echo
echo "== lines mentioning saving or the Saved results view =="
grep -n -i -E 'saved result|saved view|saved-result|Saved Results|saving into|saves? (a )?result|bookmark|file[sd]? (the )?result|filing|Screen [0-9]|Fig [0-9]' "$PLAN" | cut -c1-210
