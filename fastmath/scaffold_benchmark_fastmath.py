import fastmath
import math
import time
import array
import random

def python_sum(arr):
    return sum(arr)

def fastmath_sum(arr):
    return fastmath.sum_array(arr)

def python_mul(a, b):
    return a * b

def fastmath_mul(a, b):
    return fastmath.mul(a, b)

def python_mean(arr):
    return sum(arr) / len(arr)

def fastmath_mean(arr):
    return fastmath.mean_array(arr)

def python_variance(arr):
    m = python_mean(arr)
    return sum((x - m) ** 2 for x in arr) / len(arr)

def fastmath_variance(arr):
    return fastmath.variance_array(arr)

def python_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def fastmath_gcd(a, b):
    return fastmath.gcd(a, b)

def python_is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def fastmath_is_prime(n):
    return fastmath.is_prime(n)

def python_sin(x):
    return math.sin(x)

def fastmath_sin(x):
    return fastmath.mysin(x)

def python_cos(x):
    return math.cos(x)

def fastmath_cos(x):
    return fastmath.mycos(x)

def python_tan(x):
    return math.tan(x)

def fastmath_tan(x):
    return fastmath.mytan(x)

def python_exp(x):
    return math.exp(x)

def fastmath_exp(x):
    return fastmath.myexp(x)

def python_log(x):
    return math.log(x)

def fastmath_log(x):
    return fastmath.mylog(x)

def python_sqrt(x):
    return math.sqrt(x)

def fastmath_sqrt(x):
    return fastmath.mysqrt(x)

def python_clamp(x, a, b):
    return max(a, min(x, b))

def fastmath_clamp(x, a, b):
    return fastmath.clamp(x, a, b)

def python_distance2d(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def fastmath_distance2d(x1, y1, x2, y2):
    return fastmath.distance2d(x1, y1, x2, y2)

def python_median(arr):
    arr = sorted(arr)
    n = len(arr)
    if n % 2 == 1:
        return arr[n // 2]
    else:
        return 0.5 * (arr[n // 2 - 1] + arr[n // 2])

def fastmath_median(arr):
    return fastmath.median(arr)

def python_lcm(a, b):
    return abs(a * b) // python_gcd(a, b)

def fastmath_lcm(a, b):
    return fastmath.lcm(a, b)

def python_modinv(a, m):
    # Extended Euclidean Algorithm
    t, newt = 0, 1
    r, newr = m, a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        return 0
    if t < 0:
        t += m
    return t

def fastmath_modinv(a, m):
    return fastmath.modinv(a, m)

def check_correctness(func1, func2, args, tol=1e-9):
    result1 = func1(*args)
    result2 = func2(*args)
    if isinstance(result1, float):
        return abs(result1 - result2) < tol
    return result1 == result2

def benchmark(func, args, repeat=100000):
    t0 = time.perf_counter()
    for _ in range(repeat):
        func(*args)
    t1 = time.perf_counter()
    return t1 - t0

def main():
    arr = array.array('d', [random.uniform(-100, 100) for _ in range(1000)])
    a, b = 12345, 6789
    x, y = 3.1415, 2.7182
    x1, y1, x2, y2 = 1.0, 2.0, 3.0, 4.0
    n = 104729  # a large prime

    tests = [
        ("sum_array", python_sum, fastmath_sum, (arr,)),
        ("mul", python_mul, fastmath_mul, (a, b)),
        ("mean_array", python_mean, fastmath_mean, (arr,)),
        ("variance_array", python_variance, fastmath_variance, (arr,)),
        ("gcd", python_gcd, fastmath_gcd, (a, b)),
        ("lcm", python_lcm, fastmath_lcm, (a, b)),
        ("is_prime", python_is_prime, fastmath_is_prime, (n,)),
        ("mysin", python_sin, fastmath_sin, (x,)),
        ("mycos", python_cos, fastmath_cos, (x,)),
        ("mytan", python_tan, fastmath_tan, (x,)),
        ("myexp", python_exp, fastmath_exp, (y,)),
        ("mylog", python_log, fastmath_log, (math.e,)),
        ("mysqrt", python_sqrt, fastmath_sqrt, (100.0,)),
        ("clamp", python_clamp, fastmath_clamp, (150, 0, 100)),
        ("distance2d", python_distance2d, fastmath_distance2d, (x1, y1, x2, y2)),
        ("median", python_median, fastmath_median, (arr,)),
        ("modinv", python_modinv, fastmath_modinv, (3, 11)),
        ("fadd", lambda a, b: a + b, lambda a, b: fastmath.fadd(a, b), (1.5, 2.5)),
        ("fsub", lambda a, b: a - b, lambda a, b: fastmath.fsub(a, b), (2.5, 1.5)),
        ("fmul", lambda a, b: a * b, lambda a, b: fastmath.fmul(a, b), (2.0, 4.0)),
        ("fdiv", lambda a, b: a / b if b != 0 else float('nan'), lambda a, b: fastmath.fdiv(a, b), (10.0, 2.0)),
        ("imod", lambda a, b: a % b if b != 0 else 0, lambda a, b: fastmath.imod(a, b), (10, 3)),
        ("fmodulus", lambda a, b: math.fmod(a, b) if b != 0 else float('nan'), lambda a, b: fastmath.fmodulus(a, b), (10.5, 3.0)),
        ("sub", lambda a, b: a - b, fastmath.sub, (a, b)),
        ("add", lambda a, b: a + b, fastmath.add, (a, b)),
        ("imin", min, fastmath.imin, (a, b)),
        ("imax", max, fastmath.imax, (a, b)),
        ("fmin", min, fastmath.fmin, (x, y)),
        ("fmax", max, fastmath.fmax, (x, y)),
        ("square", lambda x: x * x, fastmath.square, (x,)),
        ("cube", lambda x: x * x * x, fastmath.cube, (x,)),
        ("hypot", math.hypot, fastmath.hypot, (x, y)),
        ("power", pow, fastmath.power, (x, y)),
        ("myabs", abs, fastmath.myabs, (x,)),
        ("myfloor", math.floor, fastmath.myfloor, (x,)),
        ("myceil", math.ceil, fastmath.myceil, (x,)),
        ("round_nearest", round, fastmath.round_nearest, (x,)),
        ("factorial", math.factorial, fastmath.factorial, (10,)),
        ("dfactorial", lambda n: math.gamma(n+1), fastmath.dfactorial, (10,)),
        ("mysinh", math.sinh, fastmath.mysinh, (x,)),
        ("mycosh", math.cosh, fastmath.mycosh, (x,)),
        ("mytanh", math.tanh, fastmath.mytanh, (x,)),
        ("myasinh", math.asinh, fastmath.myasinh, (x,)),
        ("myacosh", math.acosh, fastmath.myacosh, (10,)),
        ("myatanh", math.atanh, fastmath.myatanh, (0.5,)),
        ("safe_log", lambda x, base=10.0: math.log(x, base) if x > 0 and base > 0 and base != 1 else float('nan'), fastmath.safe_log, (10.0, 10.0)),
        ("nth_root", lambda x, n: x ** (1.0 / n) if n != 0 else float('nan'), fastmath.nth_root, (16.0, 2.0)),
        ("safe_div", lambda a, b: a / b if b != 0 else float('nan'), fastmath.safe_div, (10.0, 2.0)),
        ("percent_change", lambda old, new: ((new - old) / old) * 100.0 if old != 0 else float('nan'), fastmath.percent_change, (100.0, 110.0)),
        ("safe_pow", lambda base, exp_: pow(base, exp_) if not (base == 0 and exp_ <= 0) else float('nan'), fastmath.safe_pow, (2.0, 8.0)),
        ("sign", lambda x: (x > 0) - (x < 0), fastmath.sign, (x,)),
        ("step", lambda edge, x: 0.0 if x < edge else 1.0, fastmath.step, (0.5, 1.0)),
        ("fract", lambda x: x - math.floor(x), fastmath.fract, (x,)),
        ("saturate", lambda x: max(0.0, min(x, 1.0)), fastmath.saturate, (x,)),
        ("deg2rad", math.radians, fastmath.deg2rad, (180.0,)),
        ("rad2deg", math.degrees, fastmath.rad2deg, (math.pi,)),
        ("distance2d", python_distance2d, fastmath_distance2d, (x1, y1, x2, y2)),
        ("distance3d", lambda x1, y1, z1, x2, y2, z2: math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2), fastmath.distance3d, (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)),
        ("smoothstep", lambda edge0, edge1, x: ((lambda t: t*t*(3-2*t))(max(0.0, min((x-edge0)/(edge1-edge0), 1.0))) if edge1 != edge0 else float('nan')), fastmath.smoothstep, (0.0, 1.0, 0.5)),
        ("wrap_angle_rad", lambda angle: ((angle + math.pi) % (2*math.pi)) - math.pi, fastmath.wrap_angle_rad, (4.0,)),
        ("wrap_angle_deg", lambda angle: ((angle + 180.0) % 360.0) - 180.0, fastmath.wrap_angle_deg, (370.0,)),
        ("reciprocal", lambda x: 1.0 / x if x != 0 else float('nan'), fastmath.reciprocal, (2.0,)),
        ("array_min", min, fastmath.array_min, (arr,)),
        ("array_max", max, fastmath.array_max, (arr,)),
        ("clamp_array", lambda arr, lo, hi: array.array('d', [max(lo, min(x, hi)) for x in arr]), fastmath.clamp_array, (arr, 0.0, 6.0)),
        ("harmonic_mean", lambda arr: len(arr) / sum(1.0/x for x in arr if x != 0) if len(arr) > 0 and all(x != 0 for x in arr) else float('nan'), fastmath.harmonic_mean, (arr,)),
        ("geometric_mean", lambda arr: math.exp(sum(math.log(x) for x in arr if x > 0) / len(arr)) if len(arr) > 0 and all(x > 0 for x in arr) else float('nan'), fastmath.geometric_mean, (arr,)),
        ("bit_and", lambda a, b: a & b, fastmath.bit_and, (a, b)),
        ("bit_or", lambda a, b: a | b, fastmath.bit_or, (a, b)),
        ("bit_xor", lambda a, b: a ^ b, fastmath.bit_xor, (a, b)),
        ("bit_not", lambda a: ~a, fastmath.bit_not, (a,)),
        ("bit_shl", lambda a, n: a << n, fastmath.bit_shl, (a, 2)),
        ("bit_shr", lambda a, n: a >> n, fastmath.bit_shr, (a, 2)),
        ("cadd", lambda a, b: a + b, fastmath.cadd, (1.0+2.0j, 3.0+4.0j)),
        ("csub", lambda a, b: a - b, fastmath.csub, (1.0+2.0j, 3.0+4.0j)),
        ("cmul", lambda a, b: a * b, fastmath.cmul, (1.0+2.0j, 3.0+4.0j)),
        ("cdiv", lambda a, b: a / b if b != 0 else 0, fastmath.cdiv, (1.0+2.0j, 3.0+4.0j)),
        ("cabs", abs, fastmath.cabs, (3.0+4.0j,)),
        ("cconj", lambda a: a.conjugate(), fastmath.cconj, (1.0+2.0j,)),
    ]

    # Run benchmarks and collect results
    results = []
    for name, pyf, cyf, args in tests:
        t_py = benchmark(pyf, args)
        t_cy = benchmark(cyf, args)
        speedup = t_py / t_cy if t_cy > 0 else float('inf')
        results.append((speedup, name, t_py, t_cy))

    # Sort results by speedup (highest to lowest)
    results.sort(reverse=True, key=lambda x: x[0])

    # Print and collect report lines
    report_lines = []
    report_lines.append("# fastmath Benchmark Report")
    report_lines.append("")
    report_lines.append("This report summarizes the correctness and performance of your `fastmath` Cython module compared to pure Python implementations.")
    report_lines.append("")
    report_lines.append("## Correctness Checks")
    report_lines.append("")
    num_pass = 0
    num_fail = 0
    for name, pyf, cyf, args in tests:
        try:
            assert check_correctness(pyf, cyf, args)
            line = f"- **{name}**: PASS"
            num_pass += 1
        except Exception as e:
            line = f"- **{name}**: FAIL ({e})"
            num_fail += 1
        print(line)
        report_lines.append(line)
    report_lines.append("")
    report_lines.append(f"**Summary:** {num_pass} passed, {num_fail} failed.")
    if num_fail > 0:
        report_lines.append("> :warning: Some functions failed correctness checks. Review your Cython implementations for logic or type errors.")
    else:
        report_lines.append("> :white_check_mark: All functions passed correctness checks.")

    report_lines.append("")
    report_lines.append("## Performance Benchmark")
    report_lines.append("")
    report_lines.append("The table below shows the time taken (in seconds) by each function in Python and in your Cython `fastmath` module, as well as the speedup factor. The table is sorted by speedup (highest to lowest).")
    report_lines.append("")
    header = "| Function | Python (s) | fastmath (s) | Speedup | Note |"
    sep = "|---|---|---|---|---|"
    print(header)
    print(sep)
    report_lines.append(header)
    report_lines.append(sep)
    num_faster = 0
    num_slower = 0
    for speedup, name, t_py, t_cy in results:
        if speedup < 1:
            note = "WARNING: Cython overhead outweighs gain"
            num_slower += 1
        else:
            note = ""
            num_faster += 1
        row = f"| {name} | {t_py:.6f} | {t_cy:.6f} | {speedup:.2f}x | {note} |"
        print(row)
        report_lines.append(row)
    report_lines.append("")

    # Inference and advice section
    report_lines.append("## Analysis & Recommendations")
    report_lines.append("")
    report_lines.append(f"- **{num_faster} functions** ran faster with Cython (`fastmath`) than with pure Python.")
    report_lines.append(f"- **{num_slower} functions** ran slower with Cython. For these, the overhead of calling a Cython function outweighs any speed gain. This is typical for very simple operations (like single multiplications or additions).")
    report_lines.append("")
    if num_faster > 0:
        report_lines.append("- :rocket: **Use Cython for functions with significant computation, loops, or array processing.**")
    if num_slower > 0:
        report_lines.append("- :bulb: **For trivial math (e.g., `a * b`), stick with plain Python.** Cython is best for heavy lifting, not for single operations.")
    if num_fail > 0:
        report_lines.append("- :warning: **Some functions failed correctness checks.** Investigate these for bugs or type mismatches.")
    report_lines.append("")
    report_lines.append("### How to interpret 'Speedup'")
    report_lines.append("- A speedup greater than 1.0 means `fastmath` is faster than Python.")
    report_lines.append("- A speedup less than 1.0 (with a WARNING) means Python is faster for that function.")
    report_lines.append("")
    report_lines.append("### Next Steps")
    report_lines.append("- Focus on optimizing or fixing any functions that failed correctness.")
    report_lines.append("- Consider removing or rewriting Cython wrappers for trivial math functions.")
    report_lines.append("- For best results, use Cython for array operations, loops, and complex algorithms.")
    report_lines.append("")
    report_lines.append("_This report was automatically generated by your benchmarking script._")

    # Write to BENCHMARK.md with UTF-8 encoding
    with open("BENCHMARK.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    main()