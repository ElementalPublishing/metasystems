# cython: language_level=3

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

    # Allocate two rows for dynamic programming
    cdef int[:] prev_row = [i for i in range(len2 + 1)]
    cdef int[:] curr_row = [0] * (len2 + 1)

    for i in range(1, len1 + 1):
        curr_row[0] = i
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            curr_row[j] = min3(
                curr_row[j - 1] + 1,      # insertion
                prev_row[j] + 1,          # deletion
                prev_row[j - 1] + cost    # substitution
            )
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, prev_row

    return prev_row[len2]

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