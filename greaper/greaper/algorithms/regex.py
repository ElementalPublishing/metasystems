import re

def simple_search(pattern, lines, ignore_case=False, regex=False):
    """Search lines for pattern, optionally using regex."""
    flags = re.IGNORECASE if ignore_case else 0
    if not regex:
        # Escape pattern for literal search
        pattern = re.escape(pattern)
    compiled = re.compile(pattern, flags)
    results = []
    for i, line in enumerate(lines):
        if compiled.search(line):
            results.append((i, line))
    return results