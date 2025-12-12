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

# Try llama-cpp-python first, fallback to gpt4all if model path not set
try:
    from llama_cpp import Llama
    HAS_LLAMA_CPP = True
except ImportError:
    HAS_LLAMA_CPP = False

try:
    from gpt4all import GPT4All
    HAS_GPT4ALL = True
except ImportError:
    HAS_GPT4ALL = False

SENTERANGA_CONTEXT = """
Tu es Jokko, l'assistant IA intelligent de SENTERANGA, la plateforme agricole digitale du Sénégal.
Réponds en français et utilise le contexte fourni.
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
INDEX_DIR = './server/local_rag/index_data'
faiss_index = None
documents = None
metadata = None
embed_model = None

# LLM model initialization - try multiple backends
MODEL_PATH = os.environ.get('LOCAL_LLM_MODEL_PATH')
llm = None
llm_backend = None

def load_faiss_index():
    global faiss_index, documents, metadata, embed_model
    
    if faiss_index is not None:
        return  # Already loaded
    
    print(f"Loading FAISS index from {INDEX_DIR}/...")
    index_path = f'{INDEX_DIR}/faiss_index.bin'
    docs_path = f'{INDEX_DIR}/documents.pkl'
    meta_path = f'{INDEX_DIR}/metadata.json'
    
    if not all(Path(p).exists() for p in [index_path, docs_path, meta_path]):
        print(f"⚠ Index files not found. Run: python server/local_rag/index_corpus.py .")
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

# Initialize LLM
if MODEL_PATH and HAS_LLAMA_CPP:
    try:
        llm = Llama(model_path=MODEL_PATH)
        llm_backend = 'llama-cpp-python'
        print(f'✓ Loaded llama-cpp-python with model: {MODEL_PATH}')
    except Exception as e:
        print(f'Warning: Failed to load llama-cpp model: {e}')

# Fallback to GPT4All ONLY if explicitly enabled via env var
if os.getenv('ENABLE_GPT4ALL_DOWNLOAD') and llm is None and HAS_GPT4ALL:
    try:
        llm = GPT4All(model_name='mistral-7b-openorca.Q4_0.gguf')
        llm_backend = 'gpt4all'
        print('✓ Loaded GPT4All model (mistral-7b-openorca). Downloading if needed...')
    except Exception as e:
        print(f'Warning: Failed to load GPT4All: {e}')
        llm = None

if llm is None:
    print('⚠️ Note: No LLM backend loaded. Server will use retrieval-only mode (sources + stub response).')
    print('   To enable LLM: set LOCAL_LLM_MODEL_PATH=/path/to/model.gguf OR ENABLE_GPT4ALL_DOWNLOAD=1')

class ChatReq(BaseModel):
    message: str
    userContext: Optional[dict] = None

@app.get('/health')
def health():
    index_ok = faiss_index is not None and documents is not None
    return {
        "status": "OK",
        "service": "local-rag-jokko",
        "index_loaded": index_ok,
        "index_chunks": len(documents) if documents else 0,
        "llm_loaded": llm is not None,
        "llm_backend": llm_backend
    }

@app.post('/chat')
def chat(req: ChatReq):
    if not req.message:
        raise HTTPException(status_code=400, detail='message is required')
    
    if faiss_index is None or documents is None:
        raise HTTPException(status_code=503, detail='FAISS index not loaded. Run: python server/local_rag/index_corpus.py .')

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

    if llm is None:
        # Retrieval-only mode: return context + stub response
        return {
            "response": f"[Retrieval Mode - No LLM Loaded]\n\nBased on the project documentation, here are the relevant sources for your question: '{req.message}'\n\nSources: {', '.join(sources) if sources else 'No sources found'}\n\nTo enable full AI responses, set LOCAL_LLM_MODEL_PATH=/path/to/model.gguf or ENABLE_GPT4ALL_DOWNLOAD=1",
            "sources": sources,
            "backend": "retrieval-only"
        }

    prompt = f"{SENTERANGA_CONTEXT}\n\nContexte récupéré:\n{context_text}\n\nQuestion:\n{req.message}\n\nRéponds en français, concis et indique les sources si possible."

    try:
        if llm_backend == 'gpt4all':
            # GPT4All generate method
            resp = llm.generate(prompt=prompt, max_tokens=512, temp=0.2)
            text = resp
        else:
            # llama-cpp-python __call__ method
            resp = llm(prompt=prompt, max_tokens=512, temperature=0.2)
            text = resp['choices'][0]['text']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    return {"response": text, "sources": sources, "backend": llm_backend}
