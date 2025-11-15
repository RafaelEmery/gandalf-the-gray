from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Directories
    ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = ROOT / "data"
    FILES_DIR: Path = DATA_DIR / "files"
    INDEX_DIR: Path = DATA_DIR / "index"

    # Chunking
    CHUNK_SIZE: int = 2000
    CHUNK_OVERLAP: int = 200

    # Embedding model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Chroma
    CHROMA_COLLECTION: str = "gandalf_manuals"

    # Ollama
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_TIMEOUT: int = 60

    # Retrieval
    TOP_K: int = 6

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
