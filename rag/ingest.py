"""The end-to-end ingestion pipeline: load → chunk → embed → store."""

from rag.loader import load_document
from rag.chunking import chunk_smart
from rag.vector_store import get_collection, add_chunks


def ingest_document(file_path, collection=None, chunk_size=300, overlap=50):
    """Ingest a single document into the vector store.
    
    The pipeline:
        1. Load the document from disk
        2. Split it into semantic chunks
        3. Embed each chunk (done implicitly by ChromaDB via its embedding function)
        4. Store chunks + metadata in the vector store
    
    Args:
        file_path: Path to the document on disk.
        collection: Optional pre-existing collection. If None, gets/creates the default.
        chunk_size: Target characters per chunk.
        overlap: Characters of overlap between chunks.
    
    Returns:
        A dict with summary stats: file_path, num_chunks, total_chars.
    """
    if collection is None:
        collection = get_collection()
    
    # Load
    text = load_document(file_path)
    
    # Chunk
    chunks = chunk_smart(text, chunk_size=chunk_size, overlap=overlap)
    
    # Embed + store (one step in ChromaDB — its embedding_function handles embedding internally)
    # We use the filename as the source identifier
    source_name = file_path.split("/")[-1].split("\\")[-1]  # works on Windows and Unix paths
    add_chunks(collection, chunks, source=source_name)
    
    return {
        "file_path": file_path,
        "source": source_name,
        "num_chunks": len(chunks),
        "total_chars": len(text),
    }


def ingest_documents(file_paths, collection=None, chunk_size=300, overlap=50):
    """Ingest multiple documents into the same collection.
    
    Args:
        file_paths: List of paths to documents.
        collection: Optional collection; created if not provided.
        chunk_size, overlap: Chunking parameters.
    
    Returns:
        A list of summary dicts (one per document) and the collection.
    """
    if collection is None:
        collection = get_collection()
    
    results = []
    for path in file_paths:
        try:
            result = ingest_document(path, collection=collection, 
                                     chunk_size=chunk_size, overlap=overlap)
            results.append(result)
            print(f"  ✓ Ingested {result['source']}: "
                  f"{result['num_chunks']} chunks, {result['total_chars']} chars")
        except Exception as e:
            print(f"  ✗ Failed to ingest {path}: {e}")
            results.append({
                "file_path": path,
                "error": str(e),
            })
    
    return results, collection