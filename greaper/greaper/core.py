import os
import sys
from pathlib import Path
from greaper.filewalker import get_files_to_search

# --- John Wick Import Resolver ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- End John Wick Import Resolver ---

# Import algorithms (Python fallback)
from greaper.algorithms.regex import regex_search
from greaper.algorithms.fuzzy import similarity_ratio, fuzzy_search
from greaper.algorithms.tokenization import is_syntax_match

# Try to import Cython-accelerated search loop if available
try:
    from cython_ext.search_cython import search_lines_cython as search_lines
    CYTHON_SEARCH = True
except ImportError:
    CYTHON_SEARCH = False

def search_files(
    pattern,
    path=".",
    fuzzy=False,
    ignore_case=False,
    word=False,
    context=0,
    syntax_aware=False,
    syntax_mode="all",  # "comment", "string", "code", "all", etc.
    include=None,
    exclude=None,
    max_results=1000,
    regex=False,
    fuzzy_threshold=0.7,
):
    """
    Search files for a pattern.
    Returns a list of (file, line_number, match, context_before, context_after)
    """
    files_to_search = get_files_to_search(path=path, include=include, exclude=exclude)
    results = []
    pat_flags = 0
    if ignore_case:
        pat_flags |= 2  # re.IGNORECASE

    for file in files_to_search:
        try:
            with open(file, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            continue

        # Use Cython-accelerated search if available
        if CYTHON_SEARCH:
            file_results = search_lines(
                lines, pattern, fuzzy, pat_flags, word, context, max_results, regex,
                syntax_aware, syntax_mode
            )
            results.extend([(str(file), *r) for r in file_results])
            if len(results) >= max_results:
                return results[:max_results]
            continue

        # Pure Python fallback using algorithms
        if fuzzy:
            for i, line in enumerate(lines):
                if syntax_aware and not is_syntax_match(line, syntax_mode):
                    continue
                if similarity_ratio(pattern, line) > fuzzy_threshold:
                    before = [lines[j].strip() for j in range(max(0, i-context), i)] if context else []
                    after = [lines[j].strip() for j in range(i+1, min(len(lines), i+1+context))] if context else []
                    results.append(
                        (str(file), i+1, line.strip(), before, after)
                    )
                    if len(results) >= max_results:
                        return results
        else:
            matches = regex_search(
                pattern, lines, ignore_case=ignore_case, regex=regex, word=word
            )
            for i, line in matches:
                if syntax_aware and not is_syntax_match(line, syntax_mode):
                    continue
                before = [lines[j].strip() for j in range(max(0, i-context), i)] if context else []
                after = [lines[j].strip() for j in range(i+1, min(len(lines), i+1+context))] if context else []
                results.append(
                    (str(file), i+1, line.strip(), before, after)
                )
                if len(results) >= max_results:
                    return results
    return results