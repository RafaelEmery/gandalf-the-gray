from sentence_transformers import SentenceTransformer
from typing import List
from .settings import settings


class EmbeddingModel:
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embeds a list of texts into vectors.
        Returns list of vectors (python floats)
        """
        embeddings = self.model.encode(
            texts, show_progress_bar=False, convert_to_numpy=True
        )
        # ensure python lists
        return [emb.tolist() for emb in embeddings]

    def embed_query(self, text: str) -> List[float]:
        """Embeds a single query text into a vector."""
        return self.model.encode(text, convert_to_numpy=True).tolist()
