"""Vector store abstraction over ChromaDB for semantic search."""

import chromadb
from chromadb.utils import embedding_functions

# Use the same embedding model as rag/embeddings.py for consistency
_embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_collection(name="rag_collection", db_path="./chroma_db"):
    """Get or create a ChromaDB collection with our standard configuration.
    
    Args:
        name: Collection name.
        db_path: Where ChromaDB stores its data on disk.
    
    Returns:
        A ChromaDB collection object configured for cosine similarity.
    """
    client = chromadb.PersistentClient(path=db_path)
    return client.get_or_create_collection(
        name=name,
        embedding_function=_embedding_fn,
        metadata={"hnsw:space": "cosine"}
    )


def add_chunks(collection, chunks, source, base_id=None):
    """Add a list of text chunks to a collection with consistent metadata.
    
    Args:
        collection: A ChromaDB collection (from get_collection).
        chunks: List of text strings to add.
        source: Source identifier (e.g., filename) — stored as metadata.
        base_id: Optional ID prefix. If None, uses source as prefix.
    """
    if base_id is None:
        base_id = source
    
    ids = [f"{base_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {"source": source, "chunk_index": i}
        for i in range(len(chunks))
    ]
    
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas,
    )


def search(collection, query, n_results=5, where=None):
    """Search for chunks most semantically similar to the query.
    
    Args:
        collection: A ChromaDB collection.
        query: The user's question or search string.
        n_results: How many results to return.
        where: Optional metadata filter (e.g., {"source": "doc1.txt"}).
    
    Returns:
        A list of dicts, each containing: document, metadata, distance.
        Sorted by similarity (closest first).
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where,
    )
    
    # Flatten the nested structure into a clean list of dicts
    return [
        {
            "document": doc,
            "metadata": meta,
            "distance": dist,
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]