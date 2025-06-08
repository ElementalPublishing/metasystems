# cython: language_level=3

import numpy as np
cimport numpy as np

cdef inline int min3(int a, int b, int c):
    """Return the minimum of three integers."""
    if a < b:
        if a < c:
            return a
        else:
            return c
    else:
        if b < c:
            return b
        else:
            return c

cpdef int levenshtein(str s1, str s2):
    """
    Compute the Levenshtein distance between two Unicode strings.
    Handles all edge cases, including empty strings.
    """
    cdef int len1 = len(s1)
    cdef int len2 = len(s2)
    cdef int i, j

    # Edge cases
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    if s1 == s2:
        return 0

    # Allocate two rows for dynamic programming using NumPy arrays
    cdef np.ndarray[np.int32_t, ndim=1] prev_row = np.arange(len2 + 1, dtype=np.int32)
    cdef np.ndarray[np.int32_t, ndim=1] curr_row = np.zeros(len2 + 1, dtype=np.int32)
    cdef np.int32_t[:] prev_row_mv = prev_row
    cdef np.int32_t[:] curr_row_mv = curr_row

    for i in range(1, len1 + 1):
        curr_row_mv[0] = i
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            curr_row_mv[j] = min3(
                curr_row_mv[j - 1] + 1,      # insertion
                prev_row_mv[j] + 1,          # deletion
                prev_row_mv[j - 1] + cost    # substitution
            )
        # Swap rows for next iteration
        prev_row_mv, curr_row_mv = curr_row_mv, prev_row_mv

    return prev_row_mv[len2]

cpdef double similarity_ratio(str s1, str s2):
    """
    Return a similarity ratio between 0.0 and 1.0 based on Levenshtein distance.
    Handles all edge cases.
    """
    cdef int max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    cdef int dist = levenshtein(s1, s2)
    return 1.0 - dist / max_len

cpdef list fuzzy_search(str pattern, list lines, double threshold=0.7, int context=0, int max_results=1000):
    """
    Fuzzy search for pattern in a list of lines.
    Returns a list of (line_number, line, context_before, context_after) for matches above threshold.
    """
    cdef int n_lines = len(lines)
    cdef int results_found = 0
    results = []
    for i in range(n_lines):
        line = lines[i]
        score = similarity_ratio(pattern, line)
        if score >= threshold:
            before = [lines[j].strip() for j in range(max(0, i-context), i)] if context else []
            after = [lines[j].strip() for j in range(i+1, min(n_lines, i+1+context))] if context else []
            results.append((i+1, line.strip(), before, after, score))
            results_found += 1
            if results_found >= max_results:
                break
    return results