# AI Document Q&A Bot using RAG

## Overview

A Retrieval-Augmented Generation (RAG) based document question-answering system that enables users to query information from PDF and DOCX documents using semantic search and Large Language Models.

The system extracts document content, generates vector embeddings, stores them in ChromaDB, retrieves relevant context, and generates grounded responses with source citations.

## Features

* PDF and DOCX document ingestion
* Automatic text chunking with metadata preservation
* Semantic search using vector embeddings
* ChromaDB persistent vector storage
* Gemini-powered answer generation
* Source citation support
* Streamlit web interface
* Retrieval-Augmented Generation architecture

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Vector Database

* ChromaDB

### Embeddings

* Sentence Transformers (all-MiniLM-L6-v2)

### LLM

* Google Gemini 2.5 Flash

### Document Processing

* PyPDF
* python-docx

## Project Structure

document-qa-bot/
├── app.py
├── data/
├── db/
├── src/
│   ├── config.py
│   ├── ingest.py
│   └── query.py
├── requirements.txt
├── .env
└── README.md

## Installation

pip install -r requirements.txt

## Run Ingestion

python src/ingest.py

## Run Application

streamlit run app.py

## Workflow

1. Upload documents to data folder
2. Run ingestion pipeline
3. Generate embeddings
4. Store vectors in ChromaDB
5. Ask questions through Streamlit UI
6. Retrieve relevant chunks
7. Generate grounded answers with citations

## Future Improvements

* Multi-user support
* Document upload through UI
* Hybrid search
* Re-ranking
* Conversation memory
* Cloud deployment
