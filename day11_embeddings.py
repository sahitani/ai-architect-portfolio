import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model ONCE at module level
# This avoids reloading the 80MB model on every function call
print("Loading embedding model...")
_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model ready.")


def embed_text(text):
    """Generate an embedding for a single piece of text.
    
    Args:
        text: A string to embed.
    
    Returns:
        A numpy array of 384 floats representing the text's meaning.
    """
    return _model.encode(text)


def embed_texts(texts):
    """Generate embeddings for a list of texts (efficient batch processing).
    
    Args:
        texts: A list of strings to embed.
    
    Returns:
        A numpy array of shape (len(texts), 384) — one embedding per text.
    """
    return _model.encode(texts)


def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two embedding vectors.
    
    Args:
        vec1, vec2: Numpy arrays (embeddings from embed_text).
    
    Returns:
        A float between -1 and 1. Higher means more similar in meaning.
        Typical rough ranges:
            > 0.7 : very similar
            0.4-0.7 : related  
            < 0.2 : essentially unrelated
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)


# --- Demo ---
if __name__ == "__main__":
    sentences = [
        "The cat sat on the mat.",
        "A feline rested on the rug.",
        "Python is a popular programming language.",
        "Many developers love coding in Python.",
    ]

    # Batch-embed all four
    embeddings = embed_texts(sentences)
    print(f"\nGenerated {len(embeddings)} embeddings of dimension {embeddings.shape[1]}\n")

    # Pairwise similarity
    print("Pairwise similarity scores:")
    labels = ["A", "B", "C", "D"]
    print(f"{'Pair':<10}{'Similarity':<12}Sentences")
    print("-" * 70)
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            print(f"{labels[i]} <-> {labels[j]}   {sim:>6.3f}      "
                  f"'{sentences[i][:25]}...' vs '{sentences[j][:25]}...'")

    # Quick demo of querying — find which sentence is most similar to a NEW one
    print("\n\n=== Querying with a new sentence ===")
    query = "What language do programmers use?"
    query_embedding = embed_text(query)
    
    print(f"Query: '{query}'\n")
    print("Similarity to each sentence:")
    for i, sentence in enumerate(sentences):
        sim = cosine_similarity(query_embedding, embeddings[i])
        print(f"  {labels[i]} ({sim:.3f}): '{sentence}'")