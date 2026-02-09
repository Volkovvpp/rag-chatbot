import logging
from typing import List, Tuple

from langchain_core.documents import Document

from src.core.config import settings
from src.ingestion.ingestor import DocumentIngestor
from src.rag.llm import answer_prompt
from src.vector_db.store_fabric import create_vector_store

logger = logging.getLogger(__name__)
store = create_vector_store()
ingestor = DocumentIngestor(store=store)
threshold = settings.SOURCES_THRESHOLD

def answer_question_with_context(question: str, k: int = 3) -> Tuple[str, List[str]]:
    logger.info(f"Received question: '{question}'")
    logger.info(f"Searching top {k} relevant documents for context...")

    result: list[tuple[Document, float]] = ingestor.search(question, k=k)

    logger.info(f"Found {len(result)} documents for the question.")

    relevant_docs = []
    for doc, score in result:
        logger.info(f"Score: {score:.3f} of the document {doc.metadata.get("source")}")
        if score > threshold:
            relevant_docs.append(doc)

    sources = set([
        source for doc in relevant_docs
        if (source := doc.metadata.get("source")) is not None
    ])
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    try:
        logger.info("Generating answer using LLM with provided context...")
        answer = answer_prompt(question, context=context)
        logger.info(f"Answer generated. Sources used: {sources}")
        return answer, list(sources)
    except Exception as e:
        logger.error(f"LLM error during answer generation: {e}", exc_info=True)
        return "", []

