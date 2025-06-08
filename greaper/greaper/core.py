import os
import sys
import re
from pathlib import Path
from greaper.algorithms.fuzzy import similarity_ratio
from greaper.algorithms import regex as regex_alg

# --- John Wick Import Resolver ---
# Get the absolute path to this file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the root of the project (assuming greaper/greaper/core.py, so root is two levels up)
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Ensure current_dir and project_root are in sys.path for imports
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now you can import from anywhere in your project, regardless of where you run the script
# --- End John Wick Import Resolver ---

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

def search_files(
    pattern,
    path=".",
    fuzzy=False,
    ignore_case=False,
    word=False,
    context=0,
    syntax_aware=False,
    include=None,
    exclude=None,
    max_results=1000,
    regex=False,
):
    """
    Search files for a pattern.
    Returns a list of (file, line_number, match, context_before, context_after)
    """
    include = include or ["*"]
    exclude = exclude or []
    root = Path(path)
    files_to_search = set()
    for inc in include:
        files_to_search.update(root.rglob(inc))
    # Remove excluded files
    files_to_search = [
        f for f in files_to_search
        if all(not f.match(ex) for ex in exclude) and f.is_file() and is_text_file(f)
    ]

    results = []
    pat_flags = re.IGNORECASE if ignore_case else 0

    # Prepare regex pattern if needed
    if regex:
        try:
            pat = re.compile(pattern, pat_flags)
        except Exception as e:
            raise ValueError(f"Invalid regex: {e}")
    elif word:
        pat = re.compile(rf"\b{re.escape(pattern)}\b", pat_flags)
    else:
        pat = re.compile(re.escape(pattern), pat_flags)

    for file in files_to_search:
        try:
            with open(file, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            continue
        for i, line in enumerate(lines):
            found = False
            if fuzzy:
                # Use fuzzy match (very basic, can be improved)
                if similarity_ratio(pattern, line) > 0.7:
                    found = True
            else:
                if pat.search(line):
                    found = True
            if found:
                before = lines[max(0, i-context):i] if context else []
                after = lines[i+1:i+1+context] if context else []
                results.append((str(file), i+1, line.strip(), [b.strip() for b in before], [a.strip() for a in after]))
                if len(results) >= max_results:
                    return results
    return results