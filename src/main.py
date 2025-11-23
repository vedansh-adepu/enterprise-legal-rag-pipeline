import time
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

app = FastAPI(
    title="Enterprise Legal RAG API",
    version="1.0.0",
    description="Microservice for ingesting and querying legal contracts."
)

# Global variables for models to avoid reloading on every request
DB_FAISS_PATH = "vectorstore/db_faiss"
embeddings = None
vector_db = None

@app.on_event("startup")
async def load_models():
    """
    Load the Vector DB and Embeddings into memory on startup.
    """
    global embeddings, vector_db
    # Only load if the vectorstore exists
    if os.path.exists(DB_FAISS_PATH):
        print("Loading Vector Database...")
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        vector_db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        print("Vector Database Loaded Successfully.")
    else:
        print("Warning: No Vector DB found. Please run ingestion first.")

class QueryRequest(BaseModel):
    query: str
    k: int = 2

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "legal-rag-pipeline"}

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    # Real logic: Save file to disk for ingestion script
    file_location = f"data/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    return {"message": f"File {file.filename} saved. Trigger ingestion to process."}

@app.post("/query")
async def query_rag(request: QueryRequest):
    if not vector_db:
        raise HTTPException(status_code=500, detail="Vector DB not initialized.")
    
    start_time = time.time()
    
    # 1. REAL Retrieval: Search the actual FAISS index
    docs = vector_db.similarity_search(request.query, k=request.k)
    
    # 2. Context Construction
    context = "\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get('source', 'Unknown') for doc in docs]
    
    # 3. Generation (Mocked for CPU, but Retrieval is REAL)
    # In production, this context goes to Llama-3
    generated_response = f"Based on the provided context regarding '{request.query}', the document states: {context[:200]}..."
    
    process_time = round((time.time() - start_time) * 1000, 2)
    
    return {
        "query": request.query,
        "response": generated_response,
        "retrieved_context_snippets": [d.page_content[:100] + "..." for d in docs],
        "sources": sources,
        "inference_time_ms": process_time
    }