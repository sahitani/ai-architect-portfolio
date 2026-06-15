"""Run sample search queries against the RAG vector store.

Usage:
    python -m scripts.run_search
"""

from rag.vector_store import get_collection, search


def main():
    collection = get_collection(name="rag_collection")
    
    chunk_count = collection.count()
    print(f"Searching across {chunk_count} chunks in the collection.\n")
    
    if chunk_count == 0:
        print("Collection is empty. Run ingestion first:")
        print("  python -m scripts.run_ingestion")
        return
    
    # Sample queries — each tests a different document
    queries = [
        "What is Python used for?",
        "How does retrieval-augmented generation work?",
        "What did we discuss about Q4 priorities?",
        "Tell me about embeddings",  # not directly in any doc — interesting test
    ]
    
    for query in queries:
        print(f"=== Query: '{query}' ===")
        
        results = search(collection, query, n_results=3)
        
        for i, result in enumerate(results, start=1):
            distance = result["distance"]
            similarity = 1 - distance
            source = result["metadata"]["source"]
            chunk_idx = result["metadata"]["chunk_index"]
            doc_preview = result["document"][:120].replace("\n", " ")
            
            print(f"  {i}. [{source} #{chunk_idx}] sim={similarity:.3f}")
            print(f"     {doc_preview}...")
        
        print()


if __name__ == "__main__":
    main()