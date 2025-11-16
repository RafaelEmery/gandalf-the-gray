import pdfplumber
from typing import List
from pathlib import Path
import re
from rich import print


def extract_text_from_pdf(path: Path) -> str:
    """Extracts text from PDF using pdfplumber and does light cleaning."""
    text_parts: List[str] = []
    with pdfplumber.open(path) as pdf:
        print(
            f"[blue]PDF Loader:[/blue] Extracting text from PDF: {path} | "
            f"Number of pages: {len(pdf.pages)}"
        )
        for page in pdf.pages:
            try:
                page_text = page.extract_text() or ""
            except Exception:
                print(
                    f"[red]PDF Loader:[/red] Failed to extract text"
                    f" from page {page.page_number} of {path} |"
                    f" skipping this page."
                )
                page_text = ""
            if page_text:
                text_parts.append(page_text)
    raw = "\n\n".join(text_parts)
    return _clean_extracted_text(raw)


def _should_join_lines(new_lines: list, current_line: str) -> bool:
    """
    Heuristic to decide if the current line should be joined to the previous one.

    Returns True if:
    - There is at least one previous line in new_lines,
    - The last line in new_lines is not empty,
    - The last line ends with a lowercase letter, digit, comma, or period.

    This suggests that the line break was likely introduced by the PDF layout,
    not because the sentence actually ended. In these cases, lines are joined
    to reconstruct sentences that were artificially split.
    """
    return new_lines and new_lines[-1] and re.match(r"[a-z0-9,.]$", new_lines[-1], re.I)


def _clean_extracted_text(text: str) -> str:
    """Performs simple cleanup of headers/footers and repeated whitespace.

    This is intentionally conservative — for production you may tailor to your PDFs.
    """

    # remove multiple hyphenated linebreaks
    text = re.sub(r"-\n", "", text)
    # join lines that appear wrapped (heuristic): if a line ends with a lowercase letter or digit, join
    lines = text.splitlines()
    new_lines = []
    for i, ln in enumerate(lines):
        ln = ln.strip()
        if not ln:
            new_lines.append("")
            continue
        if _should_join_lines(new_lines, ln):
            new_lines[-1] = new_lines[-1] + " " + ln
        else:
            new_lines.append(ln)
    joined = "\n".join(new_lines)
    # collapse repeated blank lines
    joined = re.sub(r"\n{2,}", "\n\n", joined)
    return joined
