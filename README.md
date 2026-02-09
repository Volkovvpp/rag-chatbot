# Document QA Chatbot with LLM + RAG

This project is a **Document Question Answering (QA) Chatbot** that leverages **Retrieval-Augmented Generation (RAG)** using a local or remote **LLM** (e.g. LLama 3 via Ollama), **embedding models** (e.g. Sentence Transformers), and a **vector database** (e.g. Qdrant). It provides an interactive UI for secure question-answering over your private documents.

---

## Features

- Upload and process your own text files
- Ask natural language questions about document content
- Use local LLMs (e.g. Ollama)
- Fast semantic search with vector store (Qdrant)
- Password-protected UI
- Configurable via `.env` file

---

## Setup Instructions

1. Init project
```commandline
uv init 
```
2. Create venv
```commandline
uv venv
```
3. Add dependencies
```commandline
uv sync
```
4. Load LLM model
```commandline
ollama pull llama3
ollama serve
```
5. Install docker image of Qdrant database
```commandline
docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```
6. Load file to vector knowledge database from ./data directory
```commandline
python -m src.main add ./data/<filename>.<ext>
```
You can use commands: add, delete, update to manage files
7. Run application 
```commandline
python -m src.ui.ui
```
Running on local URL:  http://127.0.0.1:7860
8. Run tests
```commandline
pytest .\test
```
9. Check errors using mypy
```commandline
mypy .
```

## Description of Architecture and Components
- Centralized configuration management via .env file and Settings class (based on pydantic-settings).
- src/ingestion - Document Ingestion located
- src/rag - LLM Integration with RAG pipline
- src/ui - UI Layer based on Gradio framework, entry point
- src/core/ — project configuration
- test - Unit tests
- src/main.py - CLI functionality

## Security/privacy handling notes
1. Authentication

Password protection is implemented at the UI level using a hardcoded or .env-configured admin password (ADMIN_PASSWORD).
2. Data Privacy

User-uploaded documents are embedded and stored locally (Qdrant).

3. Environment Configuration

Sensitive values are managed via .env and pydantic_settings.

## Usage instruction 
- Open your browser and go to the address shown in the console (usually http://127.0.0.1:7860).
- Enter the password to access the chatbot.
- Ask questions.
- Get answers and a list of sources.