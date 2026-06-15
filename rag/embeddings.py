"""Embedding generation and similarity computation."""

import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model ONCE at module level — avoids reloading on every call
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text):
    """Generate an embedding for a single piece of text.
    
    Args:
        text: A string to embed.
    
    Returns:
        A numpy array of 384 floats representing the text's meaning.
    """
    return _model.encode(text)


def embed_texts(texts):
    """Generate embeddings for a list of texts (batched, efficient).
    
    Args:
        texts: A list of strings.
    
    Returns:
        A numpy array of shape (len(texts), 384).
    """
    return _model.encode(texts)


def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two embedding vectors.
    
    Args:
        vec1, vec2: Numpy arrays from embed_text.
    
    Returns:
        Float between -1 and 1; higher = more semantically similar.
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)