"""RAG question-answering: retrieve context + generate grounded answer."""

from rag.llm import ask_llm
from rag.vector_store import get_collection, search


# The system message that defines the assistant's behavior
QA_SYSTEM_MESSAGE = """You are a helpful AI assistant that answers questions using ONLY the context provided below.

Rules:
- Base your answer strictly on the provided context.
- If the context doesn't contain enough information to answer the question, respond with: "I don't have enough information in my knowledge base to answer this question."
- Do not fabricate, speculate, or use external knowledge beyond what's in the context.
- When possible, cite the source filename in your answer (e.g., "According to rag_basics.txt...").
- Keep answers concise and directly responsive to the question."""


def build_prompt(question, retrieved_chunks):
    """Build the augmented user prompt: context + question.
    
    Args:
        question: The user's natural-language question.
        retrieved_chunks: List of dicts from search() — each with document, metadata, distance.
    
    Returns:
        A formatted prompt string ready to pass to the LLM.
    """
    if not retrieved_chunks:
        # No chunks retrieved — let the LLM know
        return f"""CONTEXT:
(No relevant context was found in the knowledge base.)

QUESTION:
{question}"""
    
    # Build a context block with source markers between chunks
    context_blocks = []
    for chunk in retrieved_chunks:
        source = chunk["metadata"].get("source", "unknown")
        chunk_idx = chunk["metadata"].get("chunk_index", "?")
        document = chunk["document"]
        context_blocks.append(f"[Source: {source} (chunk {chunk_idx})]\n{document}")
    
    context = "\n\n".join(context_blocks)
    
    return f"""CONTEXT:
{context}

QUESTION:
{question}"""


def answer_question(question, collection=None, n_results=3, min_similarity=0.3):
    """Answer a question using RAG: retrieve relevant chunks, then ask the LLM.
    
    Args:
        question: The user's question in natural language.
        collection: Optional ChromaDB collection. If None, uses the default.
        n_results: How many chunks to retrieve as context.
        min_similarity: Filter out chunks below this similarity (cosine: 1-distance).
    
    Returns:
        A dict with:
            - answer: The LLM's text answer.
            - sources: List of source filenames used as context.
            - retrieved_chunks: The full list of retrieved chunks (for debugging).
            - num_relevant: How many chunks passed the similarity threshold.
    """
    if collection is None:
        collection = get_collection()
    
   # Step 1: Retrieve candidate chunks
    raw_results = search(collection, question, n_results=n_results)
    
    # Step 2: Filter by similarity threshold
    relevant_chunks = [
        r for r in raw_results
        if (1 - r["distance"]) >= min_similarity
    ]
    
    # Step 3: Build the prompt
    user_prompt = build_prompt(question, relevant_chunks)
    
    # Step 4: Call the LLM
    answer = ask_llm(
        prompt=user_prompt,
        system_message=QA_SYSTEM_MESSAGE,
    )
    
    # Step 5: Extract source list for transparency
    sources = sorted(set(c["metadata"].get("source", "unknown") for c in relevant_chunks))
    
    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": raw_results,  # all retrieved, for debugging
        "num_relevant": len(relevant_chunks),
    }