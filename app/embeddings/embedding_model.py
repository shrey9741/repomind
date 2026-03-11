from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL
from typing import List
import numpy as np
import os

# Force offline mode - use cached model, don't try to connect to HuggingFace
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

# Load model once globally (avoids reloading on every call)
_model = None


def get_model() -> SentenceTransformer:
    """Load and cache the embedding model."""
    global _model
    if _model is None:
        print(f"📦 Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        print(f"✅ Embedding model loaded!")
    return _model


def embed_text(text: str) -> np.ndarray:
    """Embed a single text string into a vector."""
    model = get_model()
    return model.encode(text, convert_to_numpy=True)


def embed_batch(texts: List[str], batch_size: int = 64, show_progress: bool = True) -> np.ndarray:
    """
    Embed a list of texts in batches.
    Returns a 2D numpy array of shape (len(texts), embedding_dim)
    """
    model = get_model()
    print(f"🔢 Embedding {len(texts)} chunks in batches of {batch_size}...")
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=show_progress,
        convert_to_numpy=True,
    )
    print(f"✅ Embeddings created! Shape: {embeddings.shape}")
    return embeddings