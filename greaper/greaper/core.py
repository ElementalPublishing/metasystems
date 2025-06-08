import re
from pathlib import Path
from algorithms.fuzzy import similarity_ratio

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
            # Heuristic: if >30% non-printable, likely binary
            nontext = sum(1 for b in chunk if b < 9 or (b > 13 and b < 32) or b > 126)
            if chunk and nontext / len(chunk) > 0.3:
                return False
        return True
    except Exception:
        return False

def file_matches_globs(filename, include_globs, exclude_globs):
    """Advanced glob matching: supports full path, negation, and multiple patterns."""
    from fnmatch import fnmatch
    filename = str(filename)
    included = any(fnmatch(filename, pat) for pat in include_globs)
    excluded = any(fnmatch(filename, pat) for pat in exclude_globs)
    return included and not excluded

def detect_language(filepath):
    """Guess language from file extension."""
    ext = Path(filepath).suffix.lower()
    mapping = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
        ".java": "java",
        ".sh": "bash",
        ".md": "markdown",
        ".json": "json",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".toml": "toml",
        ".ini": "ini",
    }
    return mapping.get(ext, "plain")

def is_comment_or_string(line, language="python", in_multiline_string=[False]):
    """
    Advanced syntax-aware check for comments and strings.
    Supports Python, JavaScript, C/C++, Java, Bash, Markdown, and can be expanded.
    Tracks multi-line strings for Python and JS.
    """
    line_strip = line.strip()

    # --- Python ---
    if language == "python":
        triple_quotes = ("'''", '"""')
        # Multi-line string start/end
        if not in_multiline_string[0]:
            for tq in triple_quotes:
                if line_strip.startswith(tq):
                    if line_strip.count(tq) == 1:
                        in_multiline_string[0] = tq
                        return True
        else:
            if in_multiline_string[0] in line_strip:
                in_multiline_string[0] = False
            return True
        # Single-line comment
        if line_strip.startswith("#"):
            return True
        # Inline comment
        if "#" in line_strip and not line_strip.startswith("#"):
            return True
        # String literal
        if (line_strip.startswith("'") and line_strip.endswith("'") and len(line_strip) > 1) or \
           (line_strip.startswith('"') and line_strip.endswith('"') and len(line_strip) > 1):
            return True
        # Assignment to string
        if "=" in line_strip:
            parts = line_strip.split("=")
            if len(parts) == 2:
                val = parts[1].strip()
                if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
                    return True
        return False

    # --- JavaScript/TypeScript ---
    if language in ("js", "javascript", "ts", "typescript"):
        # Multi-line comment
        if not in_multiline_string[0]:
            if line_strip.startswith("/*"):
                in_multiline_string[0] = "/*"
                return True
        else:
            if "*/" in line_strip:
                in_multiline_string[0] = False
            return True
        # Single-line comment
        if line_strip.startswith("//"):
            return True
        # String literals
        if (line_strip.startswith("'") and line_strip.endswith("'")) or \
           (line_strip.startswith('"') and line_strip.endswith('"')) or \
           (line_strip.startswith("`") and line_strip.endswith("`")):
            return True
        return False

    # --- C/C++/Java ---
    if language in ("c", "cpp", "java"):
        # Multi-line comment
        if not in_multiline_string[0]:
            if line_strip.startswith("/*"):
                in_multiline_string[0] = "/*"
                return True
        else:
            if "*/" in line_strip:
                in_multiline_string[0] = False
            return True
        # Single-line comment
        if line_strip.startswith("//"):
            return True
        # String literals
        if (line_strip.startswith('"') and line_strip.endswith('"')):
            return True
        return False

    # --- Bash/Shell ---
    if language in ("sh", "bash"):
        if line_strip.startswith("#"):
            return True
        if (line_strip.startswith("'") and line_strip.endswith("'")) or \
           (line_strip.startswith('"') and line_strip.endswith('"')):
            return True
        return False

    # --- Markdown ---
    if language == "markdown":
        if line_strip.startswith("```") or line_strip.startswith(">"):
            return True
        return False

    # --- JSON/YAML/TOML/INI ---
    if language in ("json", "yaml", "toml", "ini"):
        # No comments or strings in JSON, but YAML/TOML/INI may have comments
        if line_strip.startswith("#") or line_strip.startswith(";"):
            return True
        return False

    # --- Default: not syntax aware ---
    return False

def search_files(
    pattern,
    path=".",
    fuzzy=False,
    ignore_case=False,
    word=False,
    context=0,
    include=None,
    exclude=None,
    max_results=1000,
    fuzzy_threshold=0.75,
    syntax_aware=False,
    language=None,
):
    """
    Search files for pattern. Yields (file, line_number, match_line, [context_before], [context_after]).
    """
    if include is None:
        include = ["*"]
    if exclude is None:
        exclude = []

    flags = re.IGNORECASE if ignore_case else 0
    regex = None
    if not fuzzy:
        regex_pattern = r"\b{}\b".format(re.escape(pattern)) if word else pattern
        regex = re.compile(regex_pattern, flags)

    results = []
    for filepath in Path(path).rglob("*"):
        if not filepath.is_file():
            continue
        if not file_matches_globs(filepath.name, include, exclude):
            continue
        if not is_text_file(filepath):
            continue
        lang = language or detect_language(filepath)
        in_multiline_string = [False]
        try:
            with open(filepath, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            continue

        for idx, line in enumerate(lines, 1):
            match = False
            if syntax_aware and not is_comment_or_string(line, language=lang, in_multiline_string=in_multiline_string):
                continue
            if fuzzy:
                score = similarity_ratio(pattern, line.strip())
                if score >= fuzzy_threshold:
                    match = True
            else:
                if regex.search(line):
                    match = True
            if match:
                before = [lines[i].rstrip() for i in range(max(0, idx - context - 1), idx - 1)] if context > 0 else []
                after = [lines[i].rstrip() for i in range(idx, min(len(lines), idx + context))] if context > 0 else []
                results.append((str(filepath), idx, line.rstrip(), before, after))
                if len(results) >= max_results:
                    return results
    return results