"""
Extract plain text from .pptx / .docx files so exam-prep can read their content
(Claude Code's Read tool only reads PDF/text/code files directly, not pptx/docx).

Always reads/writes UTF-8 explicitly. This matters a lot for Hebrew content: on a
Hebrew-locale Windows machine, letting Python fall back to a locale-default encoding
(cp1255) instead of UTF-8 silently mangles Hebrew text -- no exception, just wrong
characters -- so every open()/write() below pins encoding="utf-8" rather than relying
on any default.

Requires: pip install python-pptx python-docx

Usage:
    python extract_text.py <file.pptx|file.docx> [-o output.txt]
        Extract one file. Without -o, writes "<file>.extracted.txt" next to the input.

    python extract_text.py <folder> --recursive
        Extract every .pptx/.docx under <folder>, writing "<name>.extracted.txt"
        next to each source file (skips files that already have a newer .extracted.txt).
"""

import argparse
import sys
from pathlib import Path


def _require(module_name, pip_name):
    try:
        return __import__(module_name)
    except ImportError:
        sys.exit(
            f"Missing dependency '{module_name}'. Install it with:\n"
            f"    pip install {pip_name}"
        )


def extract_pptx(path: Path) -> str:
    pptx = _require("pptx", "python-pptx")
    prs = pptx.Presentation(str(path))
    lines = []
    for slide_num, slide in enumerate(prs.slides, start=1):
        lines.append(f"--- Slide {slide_num} ---")
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = "".join(run.text for run in para.runs)
                    if text.strip():
                        lines.append(text)
            if shape.has_table:
                for row in shape.table.rows:
                    lines.append(" | ".join(cell.text for cell in row.cells))
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            notes = slide.notes_slide.notes_text_frame.text
            if notes.strip():
                lines.append(f"[notes] {notes}")
    return "\n".join(lines)


def extract_docx(path: Path) -> str:
    docx = _require("docx", "python-docx")
    doc = docx.Document(str(path))
    lines = []
    for para in doc.paragraphs:
        if para.text.strip():
            lines.append(para.text)
    for table in doc.tables:
        for row in table.rows:
            lines.append(" | ".join(cell.text for cell in row.cells))
    return "\n".join(lines)


def extract_one(path: Path, out_path: Path) -> None:
    suffix = path.suffix.lower()
    if suffix == ".pptx":
        text = extract_pptx(path)
    elif suffix == ".docx":
        text = extract_docx(path)
    else:
        sys.exit(f"Unsupported file type: {path} (only .pptx and .docx are handled)")

    out_path.write_text(text, encoding="utf-8")
    print(f"Wrote {out_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="A .pptx/.docx file, or a folder with --recursive")
    parser.add_argument("-o", "--output", help="Output path (single-file mode only)")
    parser.add_argument(
        "--recursive", action="store_true", help="Process every .pptx/.docx under a folder"
    )
    args = parser.parse_args()

    target = Path(args.target)

    if args.recursive:
        if not target.is_dir():
            sys.exit(f"{target} is not a directory")
        sources = [
            p for p in target.rglob("*") if p.suffix.lower() in (".pptx", ".docx")
        ]
        if not sources:
            print(f"No .pptx/.docx files found under {target}")
            return
        for src in sources:
            out_path = src.with_suffix(src.suffix + ".extracted.txt")
            if out_path.exists() and out_path.stat().st_mtime >= src.stat().st_mtime:
                continue
            extract_one(src, out_path)
    else:
        if not target.is_file():
            sys.exit(f"{target} is not a file")
        out_path = Path(args.output) if args.output else target.with_suffix(
            target.suffix + ".extracted.txt"
        )
        extract_one(target, out_path)


if __name__ == "__main__":
    main()
