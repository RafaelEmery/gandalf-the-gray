import chromadb
from typing import List, Dict, Any
from .settings import settings
from rich import print


class VectorRepository:
    def __init__(self, persist_directory: str = None):
        print(
            f"[blue]VectorRepository: Initializing with persist_directory={persist_directory}[/blue]"
        )

        persist_directory = persist_directory or str(settings.INDEX_DIR)

        self._client = chromadb.PersistentClient(path=persist_directory)
        self._collection = self._client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION
        )

    def add_documents(
        self,
        ids: List[str],
        metadatas: List[Dict[str, Any]],
        embeddings: List[List[float]],
    ) -> None:
        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=[m.get("text", "") for m in metadatas],
        )

    def query(self, query_embedding: List[float], top_k: int = 5) -> Dict[str, Any]:
        results = self._collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )
        # results contains ids, distances, metadatas, documents
        return results

    def reset(self) -> None:
        """Deletes and recreates the collection, effectively resetting the index."""
        print(
            f"[red]VectorRepository: Resetting collection {settings.CHROMA_COLLECTION}[/red]"
        )
        try:
            self._client.delete_collection(name=settings.CHROMA_COLLECTION)
        except Exception:
            pass
        self._collection = self._client.create_collection(
            name=settings.CHROMA_COLLECTION
        )
