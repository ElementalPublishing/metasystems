import array
import math
import pytest

import smoothmath

def test_smoothstep_array_basic():
    arr = array.array('d', [0.0, 0.25, 0.5, 0.75, 1.0])
    out = array.array('d', [0.0] * len(arr))
    smoothmath.smoothstep_array(arr, 0.0, 1.0, out)
    expected = [smoothmath.smoothstep(0.0, 1.0, x) for x in arr]
    for o, e in zip(out, expected):
        assert math.isclose(o, e, rel_tol=1e-12)

def test_smootherstep_array_basic():
    arr = array.array('d', [0.0, 0.25, 0.5, 0.75, 1.0])
    out = array.array('d', [0.0] * len(arr))
    smoothmath.smootherstep_array(arr, 0.0, 1.0, out)
    expected = [smoothmath.smootherstep(0.0, 1.0, x) for x in arr]
    for o, e in zip(out, expected):
        assert math.isclose(o, e, rel_tol=1e-12)

def test_generalized_smoothstep_array_cubic():
    arr = array.array('d', [0.0, 0.25, 0.5, 0.75, 1.0])
    out = array.array('d', [0.0] * len(arr))
    smoothmath.generalized_smoothstep_array(arr, 0.0, 1.0, 3, out)
    expected = [smoothmath.generalized_smoothstep(0.0, 1.0, x, 3) for x in arr]
    for o, e in zip(out, expected):
        assert math.isclose(o, e, rel_tol=1e-12)

def test_array_nan_inf_handling():
    arr = array.array('d', [float('nan'), float('inf'), -float('inf'), 0.5])
    out = array.array('d', [0.0] * len(arr))
    smoothmath.smoothstep_array(arr, 0.0, 1.0, out)
    assert math.isnan(out[0])
    assert math.isnan(out[1])
    assert math.isnan(out[2])
    assert math.isclose(out[3], smoothmath.smoothstep(0.0, 1.0, 0.5), rel_tol=1e-12)

def test_array_length_mismatch():
    arr = array.array('d', [0.0, 0.5, 1.0])
    out = array.array('d', [0.0, 0.0])  # Wrong length
    try:
        smoothmath.smoothstep_array(arr, 0.0, 1.0, out)
        assert False, "Expected ValueError due to length mismatch"
    except ValueError:
        pass

def test_large_array_performance():
    arr = array.array('d', [i / 10000.0 for i in range(10000)])
    out = array.array('d', [0.0] * len(arr))
    smoothmath.smoothstep_array(arr, 0.0, 1.0, out)
    # Spot check a few values
    for idx in (0, 5000, 9999):
        assert math.isclose(out[idx], smoothmath.smoothstep(0.0, 1.0, arr[idx]), rel_tol=1e-12)

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])