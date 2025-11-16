from .pdf_loader import extract_text_from_pdf
from .chunker import chunk_text
from .embeddings import EmbeddingModel
from .vector_repository import VectorRepository
from .settings import settings
from rich import print
from pathlib import Path


def _ensure_directories() -> None:
    """Ensure that index and files directories exist."""
    settings.INDEX_DIR.mkdir(parents=True, exist_ok=True)
    settings.FILES_DIR.mkdir(parents=True, exist_ok=True)


def prepare_chunks(pdf: Path, text: str) -> tuple[list[str], list[dict], list[str]]:
    """
    Divide the extracted text into chunks and prepare ids, metadatas, and texts lists.
    """
    print(f"[blue]Indexer: Preparing chunks for {pdf.name}[/blue]")

    chunks = chunk_text(text)
    ids, metadatas, texts = [], [], []

    for i, (chunk_text_str, (start, end)) in enumerate(chunks):
        doc_id = f"{pdf.stem}_{i}"
        meta = {
            "source": pdf.name,
            "start": start,
            "end": end,
            "text": chunk_text_str[:1000],
        }

        ids.append(doc_id)
        metadatas.append(meta)
        texts.append(chunk_text_str)

    return ids, metadatas, texts


def index_pdf(
    pdf: Path, embedder: EmbeddingModel, vector_repository: VectorRepository
) -> None:
    """
    Extract text from a PDF, chunk it, generate embeddings, and add to the vector repository.
    """
    print(f"[blue]Indexer: Indexing {pdf.name}[/blue]")

    text = extract_text_from_pdf(pdf)
    ids, metadatas, texts = prepare_chunks(pdf, text)

    print(f"[green]Indexer: Generating embeddings for {len(texts)} chunks...[/green]")
    embeddings = embedder.embed_documents(texts)
    vector_repository.add_documents(ids=ids, metadatas=metadatas, embeddings=embeddings)

    print(f"[green]Indexer: Indexed {len(texts)} chunks from {pdf.name}.[/green]")


def build_index(force_reset: bool = False) -> None:
    """
    Build or refresh the vector index from all PDFs in the files directory.
    """
    _ensure_directories()
    repository = VectorRepository(persist_directory=str(settings.INDEX_DIR))

    if force_reset:
        print("[red]Indexer: Resetting existing index...[/red]")
        repository.reset()

    embedder = EmbeddingModel()
    pdf_paths = list(settings.FILES_DIR.glob("*.pdf"))

    if not pdf_paths:
        print(
            f"[yellow]Indexer: No PDFs found in {settings.FILES_DIR}. Put your PDF files there.[/yellow]"
        )
        return

    for pdf in pdf_paths:
        index_pdf(pdf, embedder, repository)

    print("[green]Indexer: Indexing finished.[/green]")


if __name__ == "__main__":
    import argparse

    print("[bold purple]Indexer: Starting the indexing process...[/bold purple]")

    parser = argparse.ArgumentParser(
        description="Build or refresh the Gandalf index from PDFs"
    )
    parser.add_argument(
        "--force-reset", action="store_true", help="Reset index before building"
    )
    args = parser.parse_args()

    build_index(force_reset=args.force_reset)
