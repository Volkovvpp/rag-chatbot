from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LLM_MODEL_NAME: str = "llama3"
    LLM_API_BASE: str = "http://localhost:11434"

    VECTOR_STORE_TYPE: str = "qdrant"
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "default_collection"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64
    EMBEDDING_SIZE: int = 384

    SOURCES_THRESHOLD: float = 0.2

    PORT: int = 8501
    DEBUG_MODE: bool = False
    ADMIN_PASSWORD: str = "admin123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
