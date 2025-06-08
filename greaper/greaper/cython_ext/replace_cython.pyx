# cython: language_level=3

import re

# --- Syntax-aware helpers (same as in search_cython.pyx) ---

def is_comment_line(line):
    stripped = line.strip()
    return stripped.startswith("#") or stripped.startswith("//")

def is_string_line(line):
    stripped = line.strip()
    return (stripped.startswith('"') and stripped.endswith('"')) or \
           (stripped.startswith("'") and stripped.endswith("'"))

def is_code_line(line):
    return not is_comment_line(line) and not is_string_line(line)

def is_syntax_match(line, syntax_mode):
    if syntax_mode == "comment":
        return is_comment_line(line)
    elif syntax_mode == "string":
        return is_string_line(line)
    elif syntax_mode == "code":
        return is_code_line(line)
    else:
        return True

# --- Main batch replace ---

def batch_replace(
    lines,
    pattern,
    replacement,
    regex=False,
    ignore_case=False,
    word=False,
    max_replacements=0,
    syntax_aware=False,
    syntax_mode="all",  # "comment", "string", "code", or "all"
):
    """
    Batch replace occurrences of pattern in lines.
    Supports plain, word, and regex replacement.
    Optionally restricts replacement to certain syntax contexts.
    Returns a list of replaced lines.
    """
    flags = re.IGNORECASE if ignore_case else 0
    if regex:
        pat = re.compile(pattern, flags)
    elif word:
        pat = re.compile(r"\b%s\b" % re.escape(pattern), flags)
    else:
        pat = re.compile(re.escape(pattern), flags)

    replaced_lines = []
    replacements_done = 0

    for line in lines:
        # Syntax-aware filtering
        if syntax_aware and not is_syntax_match(line, syntax_mode):
            replaced_lines.append(line)
            continue

        if max_replacements and replacements_done >= max_replacements:
            replaced_lines.append(line)
            continue

        # Only replace up to the remaining allowed replacements
        remaining = max_replacements - replacements_done if max_replacements else 0

        if regex or word:
            if max_replacements:
                new_line, n = pat.subn(replacement, line, count=remaining)
            else:
                new_line, n = pat.subn(replacement, line)
        else:
            if max_replacements:
                new_line, n = pat.subn(replacement, line, count=remaining)
            else:
                new_line, n = pat.subn(replacement, line)

        replaced_lines.append(new_line)
        replacements_done += n

        if max_replacements and replacements_done >= max_replacements:
            # If we've hit the limit, just append the rest of the lines unchanged
            replaced_lines.extend(lines[len(replaced_lines):])
            break

    return replaced_lines