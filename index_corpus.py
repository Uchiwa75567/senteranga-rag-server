import os
import sys
import pickle
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

CHUNK_SIZE = 1000  # characters per chunk (simple heuristic)
OUTPUT_DIR = 'index_data'

def read_files(root: Path, patterns=None):
    patterns = patterns or ["**/*.md", "**/*.ts", "**/*.html", "**/*.js", "**/*.json"]
    files = []
    for pat in patterns:
        for f in root.glob(pat):
            # skip node_modules, dist, .git, .venv, __pycache__
            if any(part in ("node_modules", "dist", ".git", ".venv", "__pycache__", "models") for part in f.parts):
                continue
            if f.is_file():
                files.append(f)
    return files

def chunk_text(text: str, size: int = CHUNK_SIZE):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end
    return chunks

def main(repo_root: str = '.'):
    repo = Path(repo_root)
    print(f"Indexing files under: {repo.resolve()}")

    files = read_files(repo)
    print(f"Found {len(files)} files to consider")

    # Load embedding model
    print("Loading embedding model (sentence-transformers/all-MiniLM-L6-v2)")
    embed = SentenceTransformer('all-MiniLM-L6-v2')

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    documents = []
    metadatas = []
    
    for f in files:
        try:
            text = f.read_text(encoding='utf-8')
        except Exception:
            continue
        chunks = chunk_text(text)
        for i, c in enumerate(chunks):
            metadatas.append({"source": str(f.relative_to(repo)), "chunk": i})
            documents.append(c)

    print(f"Total chunks: {len(documents)}")
    if len(documents) == 0:
        print('No documents to index, exiting.')
        return

    # compute embeddings
    print('Computing embeddings...')
    embeddings = embed.encode(documents, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    # Create FAISS index
    print('Creating FAISS index...')
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save FAISS index and metadata
    print('Saving index and metadata...')
    faiss.write_index(index, f'{OUTPUT_DIR}/faiss_index.bin')
    with open(f'{OUTPUT_DIR}/documents.pkl', 'wb') as f:
        pickle.dump(documents, f)
    with open(f'{OUTPUT_DIR}/metadata.json', 'w') as f:
        json.dump(metadatas, f, indent=2)

    print(f'✓ Indexing complete. Saved to {OUTPUT_DIR}/')
    print(f'  - faiss_index.bin ({len(documents)} chunks)')
    print(f'  - documents.pkl')
    print(f'  - metadata.json')

if __name__ == '__main__':
    root = '.'
    if len(sys.argv) > 1:
        root = sys.argv[1]
    main(root)
