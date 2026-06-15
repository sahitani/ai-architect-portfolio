"""Ask questions of the RAG knowledge base and get grounded answers.

Usage:
    python -m scripts.run_qa
"""

from rag.qa import answer_question
from rag.vector_store import get_collection


def display_result(question, result):
    """Pretty-print a QA result with answer, sources, and chunk previews."""
    print(f"\n{'=' * 70}")
    print(f"Q: {question}")
    print(f"{'=' * 70}")
    
    print(f"\nA: {result['answer']}")
    
    if result['sources']:
        print(f"\nSources used: {', '.join(result['sources'])}")
    else:
        print(f"\nSources used: (none — no chunks passed the similarity threshold)")
    
    print(f"\nRetrieval details: {result['num_relevant']} relevant chunks out of "
          f"{len(result['retrieved_chunks'])} retrieved")
    
    # Show the actual chunks that were used (for transparency / debugging)
    if result['retrieved_chunks']:
        print(f"\nTop chunks considered:")
        for i, chunk in enumerate(result['retrieved_chunks'], start=1):
            sim = 1 - chunk['distance']
            source = chunk['metadata'].get('source', 'unknown')
            preview = chunk['document'][:100].replace('\n', ' ')
            marker = "✓" if sim >= 0.3 else "✗"
            print(f"  {marker} #{i} [{source}] sim={sim:.3f}: {preview}...")


def main():
    collection = get_collection(name="rag_collection")
    
    if collection.count() == 0:
        print("⚠ Collection is empty. Run ingestion first:")
        print("  python -m scripts.run_ingestion")
        return
    
    print(f"RAG knowledge base: {collection.count()} chunks indexed.\n")
    
    # A range of test questions — covering each document, plus edge cases
    questions = [
        "What is Python used for in data science?",          # python_intro
        "How does retrieval-augmented generation work?",     # rag_basics
        "What did we discuss about Q4 priorities?",          # short_note
        "When was Python first released?",                   # python_intro (specific fact)
        "What's the capital of France?",                     # outside knowledge — should say "I don't know"
    ]
    
    for question in questions:
        result = answer_question(question, collection=collection)
        display_result(question, result)


if __name__ == "__main__":
    main()