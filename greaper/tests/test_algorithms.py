from ..algorithms.fuzzy import levenshtein, similarity_ratio

def test_levenshtein_basic():
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("flaw", "lawn") == 2
    assert levenshtein("", "") == 0
    assert levenshtein("a", "") == 1
    assert levenshtein("", "a") == 1
    assert levenshtein("abc", "abc") == 0

def test_similarity_ratio_basic():
    assert similarity_ratio("kitten", "kitten") == 1.0
    assert similarity_ratio("kitten", "sitting") < 1.0
    assert similarity_ratio("", "") == 1.0
    assert similarity_ratio("a", "") == 0.0
    assert similarity_ratio("", "a") == 0.0