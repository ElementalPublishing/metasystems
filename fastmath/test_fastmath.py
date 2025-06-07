import fastmath
import math
import array
import traceback
import inspect

# Helper for isnan
def isnan(x):
    try:
        return math.isnan(x)
    except Exception:
        return False

# Map function names to safe test arguments
TEST_ARGS = {
    # Arithmetic
    'add': (2, 3),
    'sub': (5, 2),
    'mul': (2, 4),
    'fadd': (1.5, 2.5),
    'fsub': (2.5, 1.5),
    'fmul': (2.0, 4.0),
    'fdiv': (10.0, 2.0),
    'imod': (10, 3),
    'fmodulus': (10.5, 3.0),
    'imin': (1, 2),
    'imax': (1, 2),
    'fmin': (1.0, 2.0),
    'fmax': (1.0, 2.0),
    # Array math
    'sum_array': (array.array('d', [1.0, 2.0, 3.0]),),
    'mean_array': (array.array('d', [1.0, 2.0, 3.0]),),
    'variance_array': (array.array('d', [1.0, 2.0, 3.0]),),
    'stddev_array': (array.array('d', [1.0, 2.0, 3.0]),),
    'array_min': (array.array('d', [1.0, 2.0, 3.0]),),
    'array_max': (array.array('d', [1.0, 2.0, 3.0]),),
    'clamp_array': (array.array('d', [5.0, -2.0, 7.0]), 0.0, 6.0),
    # Logic
    'logic_and': (1, 0),
    'logic_or': (1, 0),
    'logic_xor': (1, 1),
    'logic_nand': (1, 1),
    'logic_nor': (0, 0),
    'logic_not': (1,),
    'logic_implication': (1, 0),
    'logic_equivalence': (1, 1),
    'majority': (1, 1, 0),
    'parity3': (1, 1, 1),
    # Geometry
    'distance2d': (0, 0, 3, 4),
    'polygon_area': (array.array('d', [0, 1, 0]), array.array('d', [0, 0, 1])),
    'point_in_circle': (0, 0, 0, 0, 1),
    # Probability & statistics
    'median': (array.array('d', [1, 2, 3, 4]),),
    'quantile': (array.array('d', [1, 2, 3, 4]), 0.5),
    'harmonic_mean': (array.array('d', [1, 2, 3, 4]),),
    'geometric_mean': (array.array('d', [1, 2, 3, 4]),),
    # Number theory
    'gcd': (12, 8),
    'lcm': (12, 8),
    'is_prime': (13,),
    'modinv': (3, 11),
    # Misc
    'clamp': (5, 1, 10),
    'sign': (10,),
    'bit_and': (6, 3),
    'bit_or': (6, 3),
    'bit_xor': (6, 3),
    'bit_not': (6,),
    'bit_shl': (3, 2),
    'bit_shr': (12, 2),
    # Financial
    'percent_change': (100, 110),
    # Scientific
    'mysin': (math.pi/2,),
    'mycos': (0,),
    'mytan': (0,),
    'myexp': (1,),
    'mylog': (math.e,),
    'mylog10': (100,),
    'mysqrt': (9,),
    # Add more as you add functions!
    # Edge cases for arrays
    'mean_array_empty': (array.array('d', []),),
    'variance_array_empty': (array.array('d', []),),
    'median_single': (array.array('d', [42]),),
    'median_even': (array.array('d', [1, 2, 3, 4]),),
    'median_odd': (array.array('d', [1, 2, 3]),),

    # Edge cases for numbers
    'is_prime_zero': (0,),
    'is_prime_one': (1,),
    'is_prime_negative': (-7,),
    'gcd_zero': (0, 10),
    'gcd_both_zero': (0, 0),
    'modinv_no_inverse': (2, 4),

    # New test cases
    'aabb_overlap': (0.0, 0.0, 1.0, 1.0, 0.5, 0.5, 1.5, 1.5),
    'acceleration': (0.0, 10.0, 0.0, 2.0),
    'angular_acceleration': (0.0, 10.0, 0.0, 2.0),
    'angular_velocity': (90.0, 2.0),
    'apply_gate': (((1, 0), (0, 1)), (1, 0)),
    'apply_sine_wave': (array.array('d', [1.0, 2.0, 3.0]), 1.0, 44100.0),
    'atan2d': (1.0, 1.0),
    'barycentric2d': (0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.3, 0.3),
    'blend': (0.0, 1.0, 0.5),
    'cabs': (3.0 + 4.0j,),
    'cadd': (1.0 + 2.0j, 3.0 + 4.0j),
    'cartesian_to_polar': (1.0, 1.0),
    'cconj': (1.0 + 2.0j,),
    'cdiv': (1.0 + 2.0j, 3.0 + 4.0j),
    'clamp01': (1.5,),
    'cmul': (1.0 + 2.0j, 3.0 + 4.0j),
    'count_nucleotide': (bytearray(b"ACGTACGT"), ord("A")),
    'cross3d': (
        array.array('d', [1.0, 0.0, 0.0]),
        array.array('d', [0.0, 1.0, 0.0]),
        array.array('d', [0.0, 0.0, 0.0])
    ),
    'csub': (1.0 + 2.0j, 3.0 + 4.0j),
    'cube': (3.0,),
    'cubic_interp': (0.0, 1.0, 2.0, 3.0, 0.5),
    'deg2rad': (180.0,),
    'dfactorial': (5,),
    'displacement': (10.0, 2.0),
    'displacement_acc': (10.0, 2.0, 1.0),
    'distance3d': (0.0, 0.0, 0.0, 1.0, 1.0, 1.0),
    'dot2d': (1.0, 2.0, 3.0, 4.0),
    'dot3d': (1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
    'factorial': (5,),
    'fade': (0.5,),
    'force': (2.0, 3.0),
    'fract': (2.7,),
    'fractal_brownian_motion': (0.5, 0.5, 3),
    'grad': (1.0, 2.0, 3.0, 4.0),
    'hadamard': (),
    'hash01': (12345,),
    'hash_int': (12345,),
    'hypot': (3.0, 4.0),
    'identity2': (),
    'impulse': (1.0, 0.5),
    'inv_lerp': (0.0, 10.0, 5.0),
    'is_identity_permutation': (array.array('i', [0, 1, 2, 3]),),
    'isclose': (1.0, 1.0 + 1e-10, 1e-9),
    'kinetic_energy': (2.0, 3.0),
    'kron2': (((1, 0), (0, 1)), ((0, 1), (1, 0))),
    'lerp': (0.0, 10.0, 0.5),
    'lerp_noise': (0.0, 1.0, 0.5),
    'line_intersect': (0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0),
    'logic_xnor': (1, 1),
    'mat2_det': (((1.0, 2.0), (3.0, 4.0)),),
    'mat2_mul': (((1.0, 2.0), (3.0, 4.0)), ((5.0, 6.0), (7.0, 8.0))),
    'mat3_det': (((1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)),),
    'mat3_mul': (
        ((1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)),
        ((9.0, 8.0, 7.0), (6.0, 5.0, 4.0), (3.0, 2.0, 1.0))
    ),
    'measure_prob': ((1.0, 0.0), 0),
    'moment_of_inertia_disk': (2.0, 1.0),
    'moment_of_inertia_sphere': (2.0, 1.0),
    'momentum': (2.0, 3.0),
    'myabs': (-7.5,),
    'myacos': (0.5,),
    'myacosh': (2.0,),
    'myasin': (0.5,),
    'myasinh': (1.0,),
    'myatan': (1.0,),
    'myatanh': (0.5,),
    'myceil': (1.2,),
    'mycosh': (1.0,),
    'myfloor': (1.8,),
    'mysinh': (1.0,),
    'mytanh': (1.0,),
    'norm2d': (3.0, 4.0),
    'norm3d': (1.0, 2.0, 2.0),
    'normalize2d': (array.array('d', [3.0, 4.0]),),
    'normalize3d': (array.array('d', [1.0, 2.0, 2.0]),),
    'nth_root': (27.0, 3.0),
    'numerical_derivative': (lambda x: x**2, 1.0),
    'numerical_integral': (lambda x: x, 0.0, 1.0, 100),
    'pauli_x': (),
    'pauli_y': (),
    'pauli_z': (),
    'perlin1d': (0.5,),
    'permutation_sign': (array.array('i', [0, 1, 2, 3]),),
    'permute': (2,),
    'polar_to_cartesian': (1.0, math.pi/4),
    'potential_energy': (2.0, 10.0, 1.0),
    'power': (2.0, 8.0),
    'proj2d': (1.0, 2.0, 3.0, 4.0),
    'pulse': (0.5, 0.2, 0.8),
    'quadratic_roots': (1.0, -3.0, 2.0),
    'quantum_example': (),
    'quat_conj': (
        array.array('d', [1.0, 0.0, 0.0, 0.0]),
        array.array('d', [0.0, 0.0, 0.0, 0.0])
    ),
    'quat_mul': (
        array.array('d', [1.0, 0.0, 0.0, 0.0]),
        array.array('d', [0.0, 1.0, 0.0, 0.0]),
        array.array('d', [0.0, 0.0, 0.0, 0.0])
    ),
    'quat_normalize': (array.array('d', [1.0, 1.0, 1.0, 1.0]),),
    'rad2deg': (math.pi,),
    'rand01': (),
    'randint': (1, 10),
    'reciprocal': (2.0,),
    'reflect2d': (
        array.array('d', [1.0, -1.0]),
        array.array('d', [0.0, 1.0]),
        array.array('d', [0.0, 0.0])
    ),
    'remap': (5.0, 0.0, 10.0, 0.0, 1.0),
    'round_nearest': (1.7,),
    'safe_div': (1.0, 0.0),
    'safe_log': (-1.0,),
    'safe_pow': (-2.0, 0.5),
    'saturate': (1.5,),
    'sawtooth_wave': (0.5, 1.0),
    'sdf_box': (0.5, 0.5, 0.0, 0.0, 1.0, 1.0),
    'sdf_circle': (0.5, 0.5, 0.0, 0.0, 1.0),
    'seed_random': (42,),
    'slerp_angle': (0.0, math.pi, 0.5),
    'smooth_max': (1.0, 2.0, 0.5),
    'smooth_min': (1.0, 2.0, 0.5),
    'smoothstep': (0.5, 0.0, 1.0),
    'solve_linear2': (
        array.array('d', [1.0, 2.0, 3.0, 4.0]),  # Flat 2x2 matrix
        array.array('d', [5.0, 6.0]),
        array.array('d', [0.0, 0.0])
    ),
    'spiral': (1.0, 1.0),
    'square': (3.0,),
    'step': (0.5, 1.0),
    'step_particles': (array.array('d', [1.0, 2.0]), array.array('d', [0.5, 0.5]), 0.1),
    'swap_double': (array.array('d', [1.0, 2.0]), 0, 1),
    'torque': (2.0, 3.0),
    'triangle_wave': (0.5, 1.0),
    'velocity': (0.0, 10.0, 0.0, 2.0),
    'work': (2.0, 10.0),
    'wrap_angle_deg': (370.0,),
    'wrap_angle_rad': (7.0,),
}

# Optionally, map functions to reference implementations for correctness checks
REFERENCE_IMPL = {
    'add': lambda a, b: a + b,
    'mul': lambda a, b: a * b,
    'mysin': math.sin,
    'mycos': math.cos,
    'mylog': math.log,
    # Add more as needed
}

def test_all_functions():
    passed = []
    failed = []
    skipped = []
    mismatched = []
    for name, func in inspect.getmembers(fastmath, inspect.isroutine):
        if name.startswith('_'):
            continue  # Skip private/internal functions
        args = TEST_ARGS.get(name, None)
        if args is None:
            print(f"{name}: SKIPPED (no test args)")
            skipped.append(name)
            continue
        try:
            result = func(*args)
            # Optional: check against reference implementation
            if name in REFERENCE_IMPL:
                ref_result = REFERENCE_IMPL[name](*args)
                if isinstance(result, float):
                    if not math.isclose(result, ref_result, rel_tol=1e-9, abs_tol=1e-9):
                        print(f"{name}: MISMATCH (fastmath={result}, python={ref_result})")
                        mismatched.append(name)
                        continue
                else:
                    if result != ref_result:
                        print(f"{name}: MISMATCH (fastmath={result}, python={ref_result})")
                        mismatched.append(name)
                        continue
            print(f"{name}: PASS")
            passed.append(name)
        except Exception as e:
            print(f"{name}: FAIL ({e})")
            print(f"  To find the signature for '{name}', open your Cython .pyx file and search for a line like:")
            print(f"    def {name}(")
            print(f"  or")
            print(f"    cpdef {name}(")
            print(f"  or")
            print(f"    cdef {name}(")
            print(f"  This will show you the argument names and types expected by the function.")
            failed.append(name)
    print("\nSummary:")
    print(f"  {len(passed)} functions passed.")
    print(f"  {len(failed)} functions failed.")
    print(f"  {len(mismatched)} functions mismatched reference.")
    print(f"  {len(skipped)} functions skipped (no test args).")
    if failed:
        print("  Failed functions:", failed)
    if mismatched:
        print("  Mismatched functions:", mismatched)
    if skipped:
        print("  Skipped functions:", skipped)

def test_exceptions():
    try:
        fastmath.mean_array(array.array('d', []))
        print("mean_array([]): No exception (expected nan or error) [PASS]")
    except Exception as e:
        print(f"mean_array([]): Exception caught as expected: {e} [PASS]")

def test_type_errors():
    try:
        fastmath.add("a", "b")
        print("add('a', 'b'): No exception [FAIL]")
    except Exception:
        print("add('a', 'b'): Exception caught as expected [PASS]")

def test_large_inputs():
    arr = array.array('d', [i for i in range(100000)])
    result = fastmath.sum_array(arr)
    print(f"sum_array(large): {result} [PASS]" if result == sum(arr) else "[FAIL]")

def test_math_consistency():
    x = 1.2345
    assert abs(fastmath.mysin(x) - math.sin(x)) < 1e-9
    assert abs(fastmath.mycos(x) - math.cos(x)) < 1e-9
    assert abs(fastmath.mylog(math.e) - math.log(math.e)) < 1e-9
    print("Trigonometric and log consistency: [PASS]")

if __name__ == "__main__":
    test_all_functions()
    test_exceptions()
    test_type_errors()
    test_large_inputs()
    test_math_consistency()