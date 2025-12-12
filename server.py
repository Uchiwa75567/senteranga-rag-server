import os
import json
import pickle
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai

SENTERANGA_CONTEXT = """
Tu es Jokko, l'assistant IA intelligent de SENTERANGA, la plateforme agricole digitale du Sénégal.
Réponds en français et utilise le contexte fourni pour donner des réponses précises et utiles.
"""

app = FastAPI()

# Add CORS middleware to allow requests from Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for FAISS index
# Get the absolute path to the index directory
SCRIPT_DIR = Path(__file__).parent
INDEX_DIR = SCRIPT_DIR / 'index_data'
faiss_index = None
documents = None
metadata = None
embed_model = None

# Gemini API setup
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY not set in environment")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini API configured")

"""
Senteranga RAG Server
---------------------
This module implements a FastAPI server for the Senteranga Retrieval-Augmented Generation (RAG) system.
It exposes endpoints to:
1. Check service health (/health)
2. Chat with the AI using context from the local project files (/chat)

Dependencies:
- FastAPI: specific web framework
- FAISS: efficient similarity search
- Google Gemini: LLM for generation
"""

# ... imports ...

def load_faiss_index():
    """
    Loads the FAISS index, document chunks, and metadata from the disk.
    
    Expected files in INDEX_DIR:
    - faiss_index.bin: The FAISS vector index
    - documents.pkl: Pickled list of text chunks
    - metadata.json: JSON list of metadata (source filenames)
    
    Returns:
        bool: True if successful, False if files are missing.
    """
    global faiss_index, documents, metadata, embed_model
    
    if faiss_index is not None:
        return  # Already loaded
    
    print(f"Loading FAISS index from {INDEX_DIR}/...")
# ... rest of function
    index_path = f'{INDEX_DIR}/faiss_index.bin'
    docs_path = f'{INDEX_DIR}/documents.pkl'
    meta_path = f'{INDEX_DIR}/metadata.json'
    
    if not all(Path(p).exists() for p in [index_path, docs_path, meta_path]):
        print(f"⚠ Index files not found. Run: python index_corpus.py .")
        return False
    
    faiss_index = faiss.read_index(index_path)
    with open(docs_path, 'rb') as f:
        documents = pickle.load(f)
    with open(meta_path, 'r') as f:
        metadata = json.load(f)
    
    print(f"✓ Loaded FAISS index with {len(documents)} chunks")
    return True

# Load embedding model
try:
    print("Loading embedding model (sentence-transformers/all-MiniLM-L6-v2)...")
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Embedding model loaded")
except Exception as e:
    print(f"Error loading embedding model: {e}")

# Load FAISS index
try:
    load_faiss_index()
except Exception as e:
    print(f"Warning: Failed to load FAISS index: {e}")

class ChatReq(BaseModel):
    message: str
    userContext: Optional[dict] = None

@app.get('/health')
def health():
    index_ok = faiss_index is not None and documents is not None
    gemini_ok = GEMINI_API_KEY is not None
    return {
        "status": "OK",
        "service": "local-rag-jokko",
        "index_loaded": index_ok,
        "index_chunks": len(documents) if documents else 0,
        "gemini_configured": gemini_ok,
        "backend": "gemini"
    }

@app.post('/chat')
def chat(req: ChatReq):
    """
    Process a chat request from the user.
    
    Flow:
    1. Validate input and server state (index loaded, API key set).
    2. Embed the user message using the local SentenceTransformer model.
    3. Search the FAISS index for the 4 most relevant document chunks.
    4. Construct a prompt with the context and user question.
    5. Send the prompt to Google Gemini for generation.
    6. Return the response and the list of sources used.
    """
    if not req.message:
        raise HTTPException(status_code=400, detail='message is required')
    
    if faiss_index is None or documents is None:
        raise HTTPException(status_code=503, detail='FAISS index not loaded. Run: python index_corpus.py .')

    if not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail='Gemini API key not configured')

    # 1) embed query
    if embed_model is None:
        raise HTTPException(status_code=503, detail='Embedding model not loaded')
    
    q_emb = embed_model.encode([req.message]).astype('float32')
    
    # 2) search FAISS
    distances, indices = faiss_index.search(q_emb, k=4)
    
    # 3) retrieve documents
    retrieved_docs = []
    sources_set = set()
    for idx in indices[0]:
        if idx >= 0 and idx < len(documents):
            retrieved_docs.append(documents[idx])
            sources_set.add(metadata[idx]["source"])
    
    sources = sorted(list(sources_set))
    context_text = "\n---\n".join(retrieved_docs)

    # Build context string from user metadata
    user_info = ""
    if req.userContext:
        u_type = req.userContext.get("userType", "")
        u_region = req.userContext.get("region", "")
        if u_type or u_region:
            user_info = f"Profil utilisateur: {u_type or 'Inconnu'} | Région: {u_region or 'Inconnue'}"

    prompt = f"""{SENTERANGA_CONTEXT}

Contexte du projet SENTERANGA (Extrait):
{context_text}

Information sur l'utilisateur:
{user_info}

Question de l'utilisateur: {req.message}

Réponds en français, avec un ton professionnel et empathique (comme Jokko). 
Si la question porte sur des fonctionnalités, des politiques ou des données techniques, base-toi strictement sur le contexte fourni. 
Si l'utilisateur a un profil spécifique (ex: agriculteur), adapte ta réponse à ses besoins potentiels.
"""

    try:
        # Call Gemini API - use latest gemini-2.5-flash model
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        text = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

    return {
        "response": text,
        "sources": sources,
        "backend": "gemini"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
