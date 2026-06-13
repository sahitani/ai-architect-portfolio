def load_document(file_path):
    """Load a text document from disk and return its contents as a string.
    
    Args:
        file_path: Path to the text file (relative or absolute).
    
    Returns:
        The full text of the file as a single string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_fixed(text, chunk_size=300):
    """Split text into chunks of a fixed character size.
    
    The naive strategy: ignores word and sentence boundaries entirely.
    Useful as a baseline; rarely the right choice in production.
    
    Args:
        text: The full document string.
        chunk_size: Number of characters per chunk.
    
    Returns:
        List of chunk strings.
    """
    chunks = []
    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
    return chunks

def chunk_with_overlap(text, chunk_size=300, overlap=50):
    """Split text into fixed-size chunks with overlap between consecutive chunks.
    
    Overlap helps preserve context across chunk boundaries. Words and sentences
    that would otherwise be split across two chunks will appear whole in at least
    one of them.
    
    Args:
        text: The full document string.
        chunk_size: Number of characters per chunk.
        overlap: Number of characters each chunk shares with the previous one.
    
    Returns:
        List of chunk strings.
    """
    chunks = []
    step = chunk_size - overlap  # how far to advance between chunks
    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
    return chunks

def chunk_smart(text, chunk_size=300, overlap=50):
    """Split text into chunks that respect natural boundaries.
    
    Tries to split on paragraph breaks first, then sentences, then words —
    falling back to mid-word only when no other option exists. Adds overlap
    between consecutive chunks for context continuity.
    
    Args:
        text: The full document string.
        chunk_size: Target number of characters per chunk (approximate).
        overlap: Number of characters of overlap between consecutive chunks.
    
    Returns:
        List of chunk strings, each ending on a clean boundary where possible.
    """
    # Boundary characters in priority order: paragraph > sentence > word
    # Try to split on the highest-priority boundary that fits within chunk_size
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Where would the chunk end if we took chunk_size characters?
        ideal_end = start + chunk_size
        
        if ideal_end >= len(text):
            # We're near the end of the document — take what's left
            chunks.append(text[start:])
            break
        
        # Look BACKWARDS from ideal_end for a clean boundary
        chunk_text = text[start:ideal_end]
        
        # Priority 1: split on paragraph break (double newline)
        last_paragraph = chunk_text.rfind("\n\n")
        if last_paragraph != -1 and last_paragraph > chunk_size // 2:
            end = start + last_paragraph
        else:
            # Priority 2: split on sentence end (. ! or ?)
            last_period = max(
                chunk_text.rfind(". "),
                chunk_text.rfind("! "),
                chunk_text.rfind("? "),
            )
            if last_period != -1 and last_period > chunk_size // 2:
                end = start + last_period + 1  # include the punctuation
            else:
                # Priority 3: split on word break (space)
                last_space = chunk_text.rfind(" ")
                if last_space != -1 and last_space > chunk_size // 2:
                    end = start + last_space
                else:
                    # No clean boundary found — fall back to hard cut
                    end = ideal_end
        
        chunks.append(text[start:end].strip())
        start = end - overlap  # advance, with overlap
    
    return chunks

# --- Test it ---
if __name__ == "__main__":
    documents = {
        "python_intro": load_document("data/python_intro.txt"),
        "rag_basics": load_document("data/rag_basics.txt"),
        "short_note": load_document("data/short_note.txt"),
        
    }
    # See the documents at scale
    print()
    print("=== Document sizes ===")
    for name, content in documents.items():
        word_count = len(content.split())
        approx_tokens = int(word_count * 1.3)  # rough estimate from Day 5
        print(f"  {name}: {len(content)} chars, ~{word_count} words, ~{approx_tokens} tokens")

    print("\n=== STRATEGY 1: FIXED-CHARACTER CHUNKS ===")
    chunks = chunk_fixed(documents["rag_basics"], chunk_size=300)
    print(f"Got {len(chunks)} chunks from rag_basics.txt")
    for i, chunk in enumerate(chunks[:3]):  # first 3 chunks
        print(f"\nChunk {i} ({len(chunk)} chars):")
        print(f"  '{chunk}'")

    print("\n=== STRATEGY 2: FIXED CHUNKS WITH OVERLAP ===")
    chunks = chunk_with_overlap(documents["rag_basics"], chunk_size=300, overlap=50)
    print(f"Got {len(chunks)} chunks (with 50-char overlap)")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i} ({len(chunk)} chars):")
        print(f"  '{chunk}'")

    print("\n=== STRATEGY 3: BOUNDARY-AWARE CHUNKS ===")
    chunks = chunk_smart(documents["rag_basics"], chunk_size=300, overlap=50)
    print(f"Got {len(chunks)} chunks (boundary-aware, with overlap)")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i} ({len(chunk)} chars):")
        print(f"  '{chunk}'")
        