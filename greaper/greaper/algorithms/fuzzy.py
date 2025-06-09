try:
    from greaper.cython_ext.fuzzy_cython import levenshtein, similarity_ratio, fuzzy_search
except ImportError:
    # Fallback to pure Python implementations
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

    def fuzzy_search(pattern, lines, threshold=0.7, context=0, max_results=1000):
        results = []
        for i, line in enumerate(lines):
            score = similarity_ratio(pattern, line)
            if score >= threshold:
                before = [lines[j].strip() for j in range(max(0, i-context), i)] if context else []
                after = [lines[j].strip() for j in range(i+1, min(len(lines), i+1+context))] if context else []
                results.append((i+1, line.strip(), before, after, score))
                if len(results) >= max_results:
                    break
        return results