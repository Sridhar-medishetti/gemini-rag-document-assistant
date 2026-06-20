# AI Document Q&A Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to ask questions about PDF and DOCX documents using semantic search and Google Gemini.

## Features

- PDF and DOCX document ingestion
- Recursive text chunking
- Vector embeddings using Sentence Transformers
- ChromaDB vector database
- Semantic similarity search
- Gemini-powered answer generation
- Source citations
- Streamlit web interface

## Tech Stack

- Python
- Streamlit
- ChromaDB
- Sentence Transformers
- Google Gemini
- PyPDF
- python-docx

## Workflow

1. Load documents from the data folder
2. Extract text
3. Chunk content
4. Generate embeddings
5. Store vectors in ChromaDB
6. Retrieve relevant chunks
7. Generate grounded answers with Gemini

## Installation

```bash
pip install -r requirements.txt
```

## Build Vector Database

```bash
python src/ingest.py
```

## Run Application

```bash
streamlit run app.py
```

## Future Improvements

- Document upload through UI
- Conversation memory
- Hybrid retrieval
- Cloud deployment
- Multi-user support
