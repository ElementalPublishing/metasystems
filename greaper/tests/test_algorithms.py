from greaper.algorithms import fuzzy

def test_levenshtein_basic():
    assert fuzzy.levenshtein("kitten", "sitting") == 3
    assert fuzzy.levenshtein("flaw", "lawn") == 2
    assert fuzzy.levenshtein("", "") == 0
    assert fuzzy.levenshtein("a", "") == 1
    assert fuzzy.levenshtein("", "a") == 1
    assert fuzzy.levenshtein("abc", "abc") == 0

def test_similarity_ratio_basic():
    assert fuzzy.similarity_ratio("kitten", "kitten") == 1.0
    assert fuzzy.similarity_ratio("kitten", "sitting") < 1.0
    assert fuzzy.similarity_ratio("", "") == 1.0
    assert fuzzy.similarity_ratio("a", "") == 0.0
    assert fuzzy.similarity_ratio("", "a") == 0.0