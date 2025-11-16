from typing import List, Tuple
from .settings import settings
from rich import print


def chunk_text(
    text: str,
    chunk_size: int = settings.CHUNK_SIZE,
    overlap: int = settings.CHUNK_OVERLAP,
) -> List[Tuple[str, Tuple[int, int]]]:
    """Split text into chunks by characters (a simple, robust approach).

    Returns list of tuples: (chunk_text, (start_char, end_char))
    """
    text = text.strip()

    if not text:
        print("[yellow]Chunker:[/yellow] No text provided to chunk.")
        return []

    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append((chunk, (start, min(end, length))))
        # advance with overlap
        start = end - overlap

    return chunks
