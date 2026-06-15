"""Document loading utilities."""


def load_document(file_path):
    """Load a text document from disk and return its contents as a string.
    
    Args:
        file_path: Path to the text file (relative or absolute).
    
    Returns:
        The full text of the file as a single string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()