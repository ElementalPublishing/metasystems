try:
    from ..cython_ext.fuzzy_cython import levenshtein, similarity_ratio
except ImportError:
    # Optional: fallback to pure Python if Cython extension is not built
    def levenshtein(s1, s2):
        if len(s1) < len(s2):
            return levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def similarity_ratio(s1, s2):
        if not s1 and not s2:
            return 1.0
        distance = levenshtein(s1, s2)
        max_len = max(len(s1), len(s2))
        return 1.0 - distance / max_len if max_len else 1.0