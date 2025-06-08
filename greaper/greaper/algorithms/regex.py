import re

def regex_search(pattern, lines, ignore_case=False, regex=False, word=False):
    flags = re.IGNORECASE if ignore_case else 0
    if regex:
        compiled = re.compile(pattern, flags)
    elif word:
        compiled = re.compile(rf"\b{re.escape(pattern)}\b", flags)
    else:
        compiled = re.compile(re.escape(pattern), flags)
    results = []
    for i, line in enumerate(lines):
        if compiled.search(line):
            results.append((i, line))
    return results