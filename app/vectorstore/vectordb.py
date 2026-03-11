import os
import json
import faiss
import numpy as np
from typing import List, Dict
from app.config import VECTOR_DB, VECTOR_DB_DIR
from app.embeddings.embedding_model import embed_text, embed_batch


# ─── File paths for saving ───────────────────────────────────────────────────
def _get_paths(repo_name: str):
    base = os.path.join(VECTOR_DB_DIR, repo_name)
    os.makedirs(base, exist_ok=True)
    return {
        "faiss_index": os.path.join(base, "index.faiss"),
        "metadata":    os.path.join(base, "metadata.json"),
        "chroma_dir":  os.path.join(base, "chroma"),
    }


# ─── FAISS Operations ─────────────────────────────────────────────────────────
def build_faiss_index(chunks: List[Dict], repo_name: str) -> faiss.Index:
    """Embed all chunks and build a FAISS index."""
    texts = [c["content"] for c in chunks]
    embeddings = embed_batch(texts)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))

    # Save index and metadata
    paths = _get_paths(repo_name)
    faiss.write_index(index, paths["faiss_index"])

    # Save metadata (chunk info without content for speed)
    metadata = [{
        "relative_path": c["relative_path"],
        "language":      c["language"],
        "chunk_type":    c["chunk_type"],
        "start_line":    c["start_line"],
        "end_line":      c["end_line"],
        "content":       c["content"],
    } for c in chunks]

    with open(paths["metadata"], "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ FAISS index saved! {index.ntotal} vectors indexed.")
    return index


def load_faiss_index(repo_name: str):
    """Load a previously saved FAISS index and metadata."""
    paths = _get_paths(repo_name)

    if not os.path.exists(paths["faiss_index"]):
        raise FileNotFoundError(f"No FAISS index found for repo: {repo_name}")

    index = faiss.read_index(paths["faiss_index"])

    with open(paths["metadata"], "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"✅ Loaded FAISS index with {index.ntotal} vectors.")
    return index, metadata


def search_faiss(query: str, repo_name: str, k: int = 5) -> List[Dict]:
    """Search FAISS index for most relevant chunks."""
    index, metadata = load_faiss_index(repo_name)

    query_vector = embed_text(query).astype(np.float32).reshape(1, -1)
    distances, indices = index.search(query_vector, k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        chunk = metadata[idx].copy()
        chunk["score"] = float(dist)
        results.append(chunk)

    return results


# ─── ChromaDB Operations ──────────────────────────────────────────────────────
def build_chroma_index(chunks: List[Dict], repo_name: str):
    """Embed all chunks and store in ChromaDB."""
    import chromadb

    paths = _get_paths(repo_name)
    client = chromadb.PersistentClient(path=paths["chroma_dir"])

    # Delete existing collection if rebuilding
    try:
        client.delete_collection(repo_name)
    except Exception:
        pass

    collection = client.create_collection(repo_name)

    texts = [c["content"] for c in chunks]
    embeddings = embed_batch(texts).tolist()

    metadatas = [{
        "relative_path": c["relative_path"],
        "language":      c["language"],
        "chunk_type":    c["chunk_type"],
        "start_line":    c["start_line"],
        "end_line":      c["end_line"],
    } for c in chunks]

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    print(f"✅ ChromaDB index saved! {len(chunks)} chunks stored.")
    return collection


def search_chroma(query: str, repo_name: str, k: int = 5) -> List[Dict]:
    """Search ChromaDB for most relevant chunks."""
    import chromadb

    paths = _get_paths(repo_name)
    client = chromadb.PersistentClient(path=paths["chroma_dir"])
    collection = client.get_collection(repo_name)

    query_vector = embed_text(query).tolist()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
    )

    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        chunks.append({
            "content":       doc,
            "relative_path": meta["relative_path"],
            "language":      meta["language"],
            "chunk_type":    meta["chunk_type"],
            "score":         results["distances"][0][i],
        })

    return chunks


# ─── Unified Interface ────────────────────────────────────────────────────────
def build_index(chunks: List[Dict], repo_name: str):
    """Build index using configured vector DB."""
    if VECTOR_DB == "chroma":
        return build_chroma_index(chunks, repo_name)
    else:
        return build_faiss_index(chunks, repo_name)


def search_index(query: str, repo_name: str, k: int = 5) -> List[Dict]:
    """Search index using configured vector DB."""
    if VECTOR_DB == "chroma":
        return search_chroma(query, repo_name, k)
    else:
        return search_faiss(query, repo_name, k)