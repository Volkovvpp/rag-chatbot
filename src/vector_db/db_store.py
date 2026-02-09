import logging
from typing import List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    MatchValue,
    Filter,
    FieldCondition,
)
from src.core.config import settings

from src.vector_db.base_vector_store import BaseVectorStore

logger = logging.getLogger(__name__)

class QdrantStore(BaseVectorStore):
    def __init__(
        self,
        collection_name: str,
        embedding_model: str = settings.EMBEDDING_MODEL,
    ):
        self.collection_name = collection_name
        self.embedder = HuggingFaceEmbeddings(model_name=embedding_model)
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

        logger.info(f"Initializing QdrantStore with collection: '{self.collection_name}'")
        self._ensure_collection()

        self.vectorstore = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embedder,
        )
        logger.info("Qdrant vector store initialized")

    def _ensure_collection(self) -> None:
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            logger.info(f"Creating new Qdrant collection: '{self.collection_name}'")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_SIZE,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")
        else:
            logger.info(f"Collection '{self.collection_name}' already exists")

    def add_documents(self, documents: List[Document]) -> None:
        logger.info(f"Adding {len(documents)} documents to collection '{self.collection_name}'")
        self.vectorstore.add_documents(documents)
        logger.info("Documents successfully added")

    def delete_documents_by_path(self, path: str) -> None:
        logger.info(f"Deleting documents with source path = '{path}' from collection '{self.collection_name}'")
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="metadata.source",
                        match=MatchValue(value=path),
                    )
                ]
            ),
        )
        logger.info("Documents successfully deleted")

    def similarity_search(self, query: str, k: int = 3) -> list[tuple[Document, float]]:
        logger.info(f"Performing similarity search for query: '{query[:50]}...' with top {k} results")
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        logger.info(f"Search returned {len(results)} results")
        return results
