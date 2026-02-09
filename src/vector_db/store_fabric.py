from src.vector_db.base_vector_store import BaseVectorStore
from src.vector_db.db_store import QdrantStore
from src.core.config import settings

def create_vector_store() -> BaseVectorStore:
    store_type = settings.VECTOR_STORE_TYPE.lower()

    if store_type == "qdrant":
        return QdrantStore(collection_name=settings.QDRANT_COLLECTION)
    # elif store_type == "...":
    else:
        raise ValueError(f"Unsupported vector store type: {store_type}")
