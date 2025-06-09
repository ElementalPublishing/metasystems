from pathlib import Path
from greaper.archive import is_archive, list_archive_files

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
    Returns a list of text files and archive members to search, applying include/exclude globs.
    Archive members are returned as (archive_path, inner_path) tuples.
    """
    include = include or ["*"]
    exclude = exclude or []
    root = Path(path)
    files_to_search = set()
    for inc in include:
        files_to_search.update(root.rglob(inc))

    result = []
    for f in files_to_search:
        if any(f.match(ex) for ex in exclude) or not f.is_file():
            continue
        if is_archive(f):
            # Add each file inside the archive as a tuple
            for inner in list_archive_files(str(f)):
                # Optionally, filter archive members by extension or name here
                result.append((str(f), inner))
        elif is_text_file(f):
            result.append(str(f))
    return result