from pathlib import Path

from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader, PyPDFLoader
from langchain_core.documents import Document

from src.ingestion.excel_load import XLSXQALoader


class FileLoader:
    def load(self, path: str) -> list[Document]:
        ext = Path(path).suffix.lower()
        print(ext)
        match ext:
            case ".txt":  return TextLoader(path).load()
            case ".md":   return UnstructuredMarkdownLoader(path).load()
            case ".pdf":  return PyPDFLoader(path).load()
            case ".xlsx": return XLSXQALoader(path).load()
            case _: raise ValueError(f"Unsupported extension: {ext}")
