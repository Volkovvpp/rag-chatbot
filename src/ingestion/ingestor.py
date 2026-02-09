import logging
from src.ingestion.file_loader import FileLoader
from src.ingestion.splitter import Splitter
from src.vector_db.base_vector_store import BaseVectorStore

logger = logging.getLogger(__name__)

class DocumentIngestor:
    def __init__(self, store: BaseVectorStore):
        self.loader = FileLoader()
        self.splitter = Splitter()
        self.store = store
        logger.info("Initialized DocumentIngestor")

    def add_files(self, paths: list[str]):
        for path in paths:
            logger.info(f"Adding file: {path}")
            try:
                docs = self.loader.load(path)
                logger.info(f"Loaded {len(docs)} documents from file: {path}")

                chunks = self.splitter.split(docs)
                logger.info(f"Split into {len(chunks)} chunks")

                for chunk in chunks:
                    chunk.metadata["source"] = path

                self.store.add_documents(chunks)
                logger.info(f"Added {len(chunks)} chunks to vector store from file: {path}")
            except Exception as e:
                logger.error(f"Failed to ingest file {path}: {e}", exc_info=True)

    def delete_files(self, paths: list[str]):
        for path in paths:
            logger.info(f"Deleting documents from vector store for file: {path}")
            try:
                self.store.delete_documents_by_path(path)
                logger.info(f"Deleted documents for file: {path}")
            except Exception as e:
                logger.error(f"Failed to delete documents for {path}: {e}", exc_info=True)

    def update_files(self, paths: list[str]):
        logger.info(f"Updating files: {paths}")
        try:
            self.delete_files(paths)
            self.add_files(paths)
            logger.info("Update complete.")
        except Exception as e:
            logger.error(f"Failed to update files {paths}: {e}", exc_info=True)

    def search(self, query: str, k: int = 3):
        logger.info(f"Searching for top {k} similar documents for query: '{query}'")
        try:
            results = self.store.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} matching documents")
            return results
        except Exception as e:
            logger.error(f"Search failed: {e}", exc_info=True)
            return []

