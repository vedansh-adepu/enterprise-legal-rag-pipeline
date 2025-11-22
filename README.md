# Enterprise Legal RAG Pipeline

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

## Overview
End-to-end **Retrieval-Augmented Generation (RAG)** system for summarizing legal contracts using Llama-3 architecture concepts and FAISS vector search.

## Architecture
- **Ingestion:** Apache Spark optimized PDF parsing.
- **Vector Store:** FAISS (CPU optimized).
- **API:** FastAPI for low-latency inference (<300ms).

## Quick Start
```bash
pip install -r requirements.txt
python src/ingest.py
uvicorn src.main:app --reload