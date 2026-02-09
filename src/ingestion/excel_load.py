from pathlib import Path
from typing import List
import pandas as pd
import logging
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

class XLSXQALoader:
    def __init__(self, path: str):
        self.path = Path(path)
        if not self.path.exists():
            logger.error(f"File not found: {self.path}")
            raise FileNotFoundError(f"File not found: {self.path}")
        logger.info(f"Initialized XLSX loader for file: {self.path}")

    def load(self) -> List[Document]:
        try:
            df = pd.read_excel(self.path, header=3)
            logger.info(f"Successfully read file: {self.path.name} with {len(df)} rows")
        except Exception as e:
            logger.exception(f"Error while reading file {self.path}: {e}")
            raise

        df.columns = [str(col).strip().lower() for col in df.columns]
        logger.debug(f"Normalized column names: {df.columns}")

        if "вопрос" not in df.columns or "ответ" not in df.columns:
            logger.error(f"Missing required columns 'вопрос' and/or 'ответ' in file: {self.path.name}")
            raise ValueError("Expected columns 'вопрос' and 'ответ'")

        documents = []
        skipped = 0

        for idx, row in df.iterrows():
            question = row.get("вопрос", "")
            answer = row.get("ответ", "")

            if pd.isna(answer) or not str(answer).strip():
                skipped += 1
                continue
            if pd.isna(question):
                question = ""

            doc = Document(
                page_content=f"Вопрос: {question}\nОтвет: {answer}".strip(),
                metadata={
                    "question": str(question).strip(),
                    "source": str(self.path),
                }
            )
            documents.append(doc)

        logger.info(f"Loaded {len(documents)} question-answer documents")
        if skipped:
            logger.info(f"Skipped {skipped} rows due to missing answers")

        return documents
