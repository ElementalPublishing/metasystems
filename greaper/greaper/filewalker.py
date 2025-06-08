from pathlib import Path

def is_text_file(filepath, blocksize=2048):
    """Robust check to skip binary files using heuristics and file extension."""
    text_extensions = {'.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.hpp', '.sh', '.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.ini'}
    ext = Path(filepath).suffix.lower()
    if ext in text_extensions:
        return True
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(blocksize)
            if b"\0" in chunk:
                return False
            # Heuristic: if >95% printable, treat as text
            text_characters = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)))
            nontext = chunk.translate(None, text_characters)
            return float(len(nontext)) / float(len(chunk) or 1) < 0.05
    except Exception:
        return False

def get_files_to_search(
    path=".",
    include=None,
    exclude=None,
):
    """
    Returns a list of text files to search, applying include/exclude globs.
    """
    include = include or ["*"]
    exclude = exclude or []
    root = Path(path)
    files_to_search = set()
    for inc in include:
        files_to_search.update(root.rglob(inc))
    # Remove excluded files and non-text files
    files_to_search = [
        f for f in files_to_search
        if all(not f.match(ex) for ex in exclude) and f.is_file() and is_text_file(f)
    ]
    return files_to_search