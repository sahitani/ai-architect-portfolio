"""Ingest all sample documents into the RAG vector store.

Usage:
    python scripts/run_ingestion.py
"""

from rag.ingest import ingest_documents
from rag.vector_store import get_collection


def main():
    # Documents to ingest
    documents = [
        "data/python_intro.txt",
        "data/rag_basics.txt",
        "data/short_note.txt",
    ]
    
    print("Starting ingestion...")
    print(f"Documents to process: {len(documents)}\n")
    
    # Get or create the collection
    collection = get_collection(name="rag_collection")
    
    # Show current state before ingesting
    initial_count = collection.count()
    print(f"Collection currently contains: {initial_count} chunks\n")
    
    # Skip ingestion if already done (idempotent)
    if initial_count > 0:
        print("Collection already populated — skipping ingestion.")
        print("To re-ingest from scratch: delete the chroma_db/ folder and re-run.\n")
    else:
        # Run the ingestion pipeline
        results, _ = ingest_documents(documents, collection=collection)
        
        # Summary
        successes = [r for r in results if "error" not in r]
        failures = [r for r in results if "error" in r]
        
        print(f"\n=== Ingestion summary ===")
        print(f"Successful: {len(successes)} / {len(documents)} documents")
        if failures:
            print(f"Failed: {len(failures)}")
            for f in failures:
                print(f"  - {f['file_path']}: {f['error']}")
        
        total_chunks = sum(r.get("num_chunks", 0) for r in successes)
        total_chars = sum(r.get("total_chars", 0) for r in successes)
        print(f"\nTotal chunks ingested: {total_chunks}")
        print(f"Total characters processed: {total_chars}")
    
    # Final state
    final_count = collection.count()
    print(f"\nCollection now contains: {final_count} chunks total")


if __name__ == "__main__":
    main()