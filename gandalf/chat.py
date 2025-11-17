from .embeddings import EmbeddingModel
from .vector_repository import VectorRepository
from .ollama_client import OllamaClient
from .settings import settings
from .helper import farewell, initial_context, some_error_happened
from textwrap import shorten
from rich import print


def build_prompt(question: str, retrieved_chunks: dict) -> str:
    """Compose a prompt for the LLM that includes retrieved evidence and a user question.

    We instruct the model to answer based only on the provided sources.
    """
    pieces = []
    metadatas = retrieved_chunks.get("metadatas", [])
    documents = retrieved_chunks.get("documents", [])

    if metadatas and isinstance(metadatas[0], list):
        metadatas = metadatas[0]
    if documents and isinstance(documents[0], list):
        documents = documents[0]

    for idx in range(len(documents)):
        meta = metadatas[idx] if idx < len(metadatas) else {}
        doc_text = documents[idx] if idx < len(documents) else ""
        src = meta.get("source", "unknown")
        span = f"[{meta.get('start', '?')}..{meta.get('end', '?')}]"

        pieces.append(
            f"SOURCE {idx + 1}: {src} {span}\n{shorten(doc_text, width=800, placeholder='...')}"
        )

    context = "\n\n".join(pieces)
    prompt = (
        f"{initial_context()}\n\n"
        f"CONTEXT:\n{context}\n\nQUESTION: {question}\n\n"
        "Answer using only the CONTEXT. If you must, cite the source number."
    )

    return prompt


def get_question() -> str | None:
    """Get a question from user input. Returns None if user wants to exit."""
    try:
        question = input("\nAye Frodo Baggins! What do you wish to ask Gandalf?\n> ")
    except (KeyboardInterrupt, EOFError):
        return None

    if not question or question.strip().lower() in ("exit", "quit"):
        return None

    return question


def interactive_chat() -> None:
    print(
        "\n[bold blue]Hello from Gandalf! Type 'exit' or 'quit' to leave.[/bold blue]\n"
    )

    embedder = EmbeddingModel()
    repository = VectorRepository()
    ollama = OllamaClient()

    print(
        "[italic green] I am ready to answer your questions based on "
        "the indexed documents from the data/files/ folder, "
        f"and my wisdom is from the Ollama model {settings.OLLAMA_MODEL}.[/italic green]"
    )

    while True:
        question = get_question()
        if question is None:
            print(f"[italic yellow]{farewell()}[/italic yellow]")
            return

        try:
            print("\n[italic blue] Let me think...[/italic blue]")
            embed_query = embedder.embed_query(question)

            # # response is a dict-like structure with 'ids', 'distances', 'metadatas', 'documents'
            response = repository.query(embed_query, top_k=settings.TOP_K)

            prompt = build_prompt(question, response)
            answer = ollama.generate(prompt)

            print("\n[italic green] I have an answer for you.[/italic green]")
            print(answer)
        except Exception as e:
            print(f"[italic red]{some_error_happened()} |[/italic red] {e}")
            break


if __name__ == "__main__":
    interactive_chat()
