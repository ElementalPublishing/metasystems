import fastmath
from hypothesis import given, strategies as st
import math

# Property: Addition is commutative
@given(st.integers(min_value=-2**31, max_value=2**31-1), st.integers(min_value=-2**31, max_value=2**31-1))
def test_add_commutative(a, b):
    assert fastmath.add(a, b) == fastmath.add(b, a)

# Property: Multiplication is commutative
@given(st.integers(min_value=-2**31, max_value=2**31-1), st.integers(min_value=-2**31, max_value=2**31-1))
def test_mul_commutative(a, b):
    assert fastmath.mul(a, b) == fastmath.mul(b, a)

# Property: mysin should match math.sin (within floating point tolerance)
@given(st.floats(-1e6, 1e6, allow_nan=False, allow_infinity=False))
def test_mysin_matches_math_sin(x):
    assert math.isclose(fastmath.mysin(x), math.sin(x), rel_tol=1e-9, abs_tol=1e-9)

# Property: fadd should match Python addition for floats
@given(
    st.floats(allow_nan=False, allow_infinity=False),
    st.floats(allow_nan=False, allow_infinity=False)
)
def test_fadd_matches_python(a, b):
    assert fastmath.fadd(a, b) == a + b