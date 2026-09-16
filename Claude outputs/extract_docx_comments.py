#!/usr/bin/env python3
"""
extract_docx_comments.py

Pulls the body text of a .docx alongside every Word comment, matched to the
exact text each comment is anchored to (the text you'd see highlighted when
you click a comment bubble in Word).

No external libraries required, just the Python standard library.

Usage:
    python extract_docx_comments.py "User Persona.docx"
    python extract_docx_comments.py "User Persona.docx" -o report.md

This writes a Markdown report next to the input file (or to the path given
with -o) listing, in document order: each comment's author, date, the exact
text it's anchored to, and the comment body itself. It also prints the same
report to the terminal.

Notes / limitations:
  - Handles comments anchored to a text range (the normal case: you select
    text, right-click, "New Comment"). A comment with no visible anchor
    (attached to an image or an empty selection) is reported with
    "[no anchored text found]".
  - Handles threaded replies if the file has them (commentsExtended.xml),
    showing replies indented under their parent comment.
  - Does not attempt to resolve resolved/unresolved status, since that's
    stored inconsistently across Word versions; all comments are shown.
"""

import sys
import argparse
import zipfile
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"
W15_NS = "http://schemas.microsoft.com/office/word/2012/wordml"


def qn(tag: str, ns: str = W_NS) -> str:
    return f"{{{ns}}}{tag}"


def read_xml_from_docx(docx_path: str, member: str):
    with zipfile.ZipFile(docx_path) as z:
        names = z.namelist()
        if member not in names:
            return None
        with z.open(member) as f:
            return ET.parse(f).getroot()


def paragraph_text(p_elem) -> str:
    """Flatten all text runs in a <w:p> into a single string."""
    parts = []
    for node in p_elem.iter():
        tag = node.tag
        if tag == qn("t"):
            parts.append(node.text or "")
        elif tag in (qn("tab"),):
            parts.append("\t")
        elif tag in (qn("br"), qn("cr")):
            parts.append("\n")
    return "".join(parts)


def load_comments(docx_path: str):
    """Returns {comment_id: {"author":..., "date":..., "text":...}}."""
    root = read_xml_from_docx(docx_path, "word/comments.xml")
    comments = {}
    if root is None:
        return comments
    for c in root.findall(qn("comment")):
        cid = c.get(qn("id"))
        author = c.get(qn("author")) or "Unknown"
        date = c.get(qn("date")) or ""
        text = "\n".join(
            paragraph_text(p) for p in c.findall(qn("p")) if paragraph_text(p).strip()
        )
        comments[cid] = {"author": author, "date": date, "text": text}
    return comments


def load_comment_replies(docx_path: str):
    """
    Reads commentsExtended.xml, if present, to find parent/child threading.
    Returns {comment_paraId: parent_paraId}. Modern Word comments use a
    w15:paraId on each comment's paragraph to link replies to their parent.
    """
    root = read_xml_from_docx(docx_path, "word/commentsExtended.xml")
    parent_of = {}
    if root is None:
        return parent_of
    for entry in root.findall(qn("commentEx", W15_NS)):
        para_id = entry.get(qn("paraId", W15_NS))
        parent_id = entry.get(qn("paraIdParent", W15_NS))
        if para_id and parent_id:
            parent_of[para_id] = parent_id
    return parent_of


def comment_para_ids(docx_path: str):
    """
    Maps comment_id -> its paragraph's w14:paraId, to resolve threading.
    Note: comments.xml paragraphs carry a w14:paraId (same attribute Word uses
    on ordinary body paragraphs), NOT a w15:paraId, even though the linking
    entries in commentsExtended.xml are themselves named w15:paraId/
    w15:paraIdParent. The values line up across both namespaces.
    """
    root = read_xml_from_docx(docx_path, "word/comments.xml")
    mapping = {}
    if root is None:
        return mapping
    for c in root.findall(qn("comment")):
        cid = c.get(qn("id"))
        for p in c.findall(qn("p")):
            para_id = p.get(qn("paraId", W14_NS))
            if para_id:
                mapping[cid] = para_id
                break
    return mapping


def extract_anchored_text_and_order(docx_path: str):
    """
    Walks word/document.xml in document order, tracking which comment
    ranges are open, and accumulates the text under each open range.
    Returns (anchored_text: {comment_id: str}, order: [comment_id, ...]).
    """
    root = read_xml_from_docx(docx_path, "word/document.xml")
    if root is None:
        raise RuntimeError("word/document.xml not found, is this a valid .docx?")

    anchored_text = {}
    order = []
    open_ranges = {}  # comment_id -> list of text chunks

    def walk(elem):
        tag = elem.tag
        if tag == qn("commentRangeStart"):
            cid = elem.get(qn("id"))
            open_ranges[cid] = []
            if cid not in order:
                order.append(cid)
            return
        if tag == qn("commentRangeEnd"):
            cid = elem.get(qn("id"))
            if cid in open_ranges:
                anchored_text[cid] = "".join(open_ranges.pop(cid))
            return
        if tag == qn("t"):
            text = elem.text or ""
            for chunks in open_ranges.values():
                chunks.append(text)
        elif tag in (qn("tab"),):
            for chunks in open_ranges.values():
                chunks.append("\t")
        elif tag in (qn("br"), qn("cr")):
            for chunks in open_ranges.values():
                chunks.append("\n")

        for child in list(elem):
            walk(child)

    walk(root)

    # Any range that never closed (shouldn't normally happen) still counts.
    for cid, chunks in open_ranges.items():
        anchored_text[cid] = "".join(chunks)

    return anchored_text, order


def extract_full_body_text(docx_path: str) -> str:
    root = read_xml_from_docx(docx_path, "word/document.xml")
    if root is None:
        return ""
    body = root.find(qn("body"))
    paragraphs = []
    for p in body.findall(qn("p")):
        paragraphs.append(paragraph_text(p))
    return "\n\n".join(paragraphs)


def build_report(docx_path: str) -> str:
    comments = load_comments(docx_path)
    anchored_text, order = extract_anchored_text_and_order(docx_path)
    para_ids = comment_para_ids(docx_path)
    parent_of = load_comment_replies(docx_path)

    # Figure out, for each comment id, its parent comment id (if a reply).
    id_by_para_id = {v: k for k, v in para_ids.items()}
    parent_comment_of = {}
    for cid, para_id in para_ids.items():
        parent_para_id = parent_of.get(para_id)
        if parent_para_id and parent_para_id in id_by_para_id:
            parent_comment_of[cid] = id_by_para_id[parent_para_id]

    lines = []
    body_text = extract_full_body_text(docx_path)
    lines.append("# Document text\n")
    lines.append(body_text.strip() or "*(no body text found)*")
    lines.append("\n\n---\n\n# Comments\n")

    if not comments:
        lines.append("*(no comments found in this document)*")
    else:
        # Only iterate top-level comments in document order, print replies nested under them.
        top_level_order = [cid for cid in order if cid not in parent_comment_of]
        for cid in top_level_order:
            _append_comment_block(lines, cid, comments, anchored_text, parent_comment_of, order, depth=0)

    return "\n".join(lines)


def _append_comment_block(lines, cid, comments, anchored_text, parent_comment_of, order, depth):
    info = comments.get(cid, {"author": "Unknown", "date": "", "text": "(missing comment body)"})
    anchor = anchored_text.get(cid, "").strip()
    indent = "  " * depth
    lines.append(f"{indent}**Comment {cid}** — {info['author']} ({info['date']})")
    lines.append(f"{indent}Anchored text: \"{anchor}\"" if anchor else f"{indent}Anchored text: [no anchored text found]")
    lines.append(f"{indent}Comment: {info['text']}")
    lines.append("")

    children = [c for c, p in parent_comment_of.items() if p == cid]
    children_in_order = [c for c in order if c in children]
    for child_id in children_in_order:
        _append_comment_block(lines, child_id, comments, anchored_text, parent_comment_of, order, depth + 1)


def main():
    parser = argparse.ArgumentParser(description="Extract text and comments from a .docx file.")
    parser.add_argument("docx_path", help="Path to the .docx file")
    parser.add_argument("-o", "--output", help="Output Markdown file path (default: <input>_comments.md)")
    args = parser.parse_args()

    report = build_report(args.docx_path)

    out_path = args.output or (args.docx_path.rsplit(".", 1)[0] + "_comments.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\n\n(Report also written to: {out_path})", file=sys.stderr)


if __name__ == "__main__":
    main()
