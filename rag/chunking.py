"""Text chunking strategies for splitting documents into retrievable pieces."""


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
    chunks = []
    start = 0
    
    while start < len(text):
        ideal_end = start + chunk_size
        
        if ideal_end >= len(text):
            chunks.append(text[start:])
            break
        
        chunk_text = text[start:ideal_end]
        
        # Priority 1: paragraph break
        last_paragraph = chunk_text.rfind("\n\n")
        if last_paragraph != -1 and last_paragraph > chunk_size // 2:
            end = start + last_paragraph
        else:
            # Priority 2: sentence end
            last_period = max(
                chunk_text.rfind(". "),
                chunk_text.rfind("! "),
                chunk_text.rfind("? "),
            )
            if last_period != -1 and last_period > chunk_size // 2:
                end = start + last_period + 1
            else:
                # Priority 3: word break
                last_space = chunk_text.rfind(" ")
                if last_space != -1 and last_space > chunk_size // 2:
                    end = start + last_space
                else:
                    end = ideal_end
        
        chunks.append(text[start:end].strip())
        start = end - overlap
    
    return chunks