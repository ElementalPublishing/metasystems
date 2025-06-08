import sys
import os
# Add project root to sys.path so cython_ext can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_cython_extension():
    try:
        from cython_ext import fuzzy_cython
        print("[OK] Successfully imported cython_ext.fuzzy_cython")
    except ImportError as e:
        print("[FAIL] Could not import cython_ext.fuzzy_cython:", e)
        sys.exit(1)

    # Test levenshtein
    try:
        result = fuzzy_cython.levenshtein("kitten", "sitting")
        assert result == 3, f"Expected 3, got {result}"
        print("[OK] fuzzy_cython.levenshtein works as expected")
    except Exception as e:
        print("[FAIL] Error calling fuzzy_cython.levenshtein:", e)
        sys.exit(1)

    # Test similarity_ratio
    try:
        ratio = fuzzy_cython.similarity_ratio("kitten", "kitten")
        assert abs(ratio - 1.0) < 1e-9, f"Expected 1.0, got {ratio}"
        print("[OK] fuzzy_cython.similarity_ratio works as expected")
    except Exception as e:
        print("[FAIL] Error calling fuzzy_cython.similarity_ratio:", e)
        sys.exit(1)

if __name__ == "__main__":
    test_cython_extension()