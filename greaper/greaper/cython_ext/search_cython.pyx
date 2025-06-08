# cython: language_level=3

import re
from cython_ext.fuzzy_cython import similarity_ratio

# --- Syntax-aware helpers ---

def is_comment_line(line):
    """
    Heuristic: treat lines starting with '#' or '//' as comments.
    Extend for more languages as needed.
    """
    stripped = line.strip()
    return stripped.startswith("#") or stripped.startswith("//")

def is_string_line(line):
    """
    Heuristic: treat lines that start and end with quotes as strings.
    Extend for more languages as needed.
    """
    stripped = line.strip()
    return (stripped.startswith('"') and stripped.endswith('"')) or \
           (stripped.startswith("'") and stripped.endswith("'"))

def is_code_line(line):
    """
    Heuristic: treat lines that are not comments or strings as code.
    """
    return not is_comment_line(line) and not is_string_line(line)

def is_syntax_match(line, syntax_mode):
    """
    Returns True if the line matches the desired syntax mode.
    """
    if syntax_mode == "comment":
        return is_comment_line(line)
    elif syntax_mode == "string":
        return is_string_line(line)
    elif syntax_mode == "code":
        return is_code_line(line)
    else:
        # Default: match all lines
        return True

# --- Main search loop ---

def search_lines_cython(
    lines,
    pattern,
    fuzzy,
    pat_flags,
    word,
    context,
    max_results,
    regex,
    syntax_aware=False,
    syntax_mode="comment",  # "comment", "string", "code", or "all"
):
    """
    Cython-accelerated search loop with advanced syntax-aware filtering.
    Returns a list of (line_number, match, context_before, context_after)
    """
    results = []
    n_lines = len(lines)

    # Compile pattern for regex/word/plain
    if regex:
        try:
            pat = re.compile(pattern, pat_flags)
        except Exception:
            return []
    elif word:
        pat = re.compile(r"\b%s\b" % re.escape(pattern), pat_flags)
    else:
        pat = re.compile(re.escape(pattern), pat_flags)

    for i in range(n_lines):
        line = lines[i]
        found = False

        # Syntax-aware filtering
        if syntax_aware and not is_syntax_match(line, syntax_mode):
            continue

        if fuzzy:
            if similarity_ratio(pattern, line) > 0.7:
                found = True
        else:
            if pat.search(line):
                found = True
        if found:
            before = [lines[j].strip() for j in range(max(0, i-context), i)] if context else []
            after = [lines[j].strip() for j in range(i+1, min(n_lines, i+1+context))] if context else []
            results.append((i+1, line.strip(), before, after))
            if len(results) >= max_results:
                return results
    return results