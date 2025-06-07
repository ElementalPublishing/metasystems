"""
Benchmark: smoothmath (Cython) vs NumPy for smoothstep and related functions

Tests very small, small, medium, large, and very large arrays.
Prints timings, speedups, and averages.
Also writes a Markdown summary to COMPARE.md.

Author: Wesley Alexander Houser
"""

import time
import numpy as np
import array
import smoothmath

# --- NumPy reference implementations ---

def numpy_smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def numpy_smootherstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t**3 * (t * (t * 6.0 - 15.0) + 10.0)

def numpy_generalized_smoothstep(edge0, edge1, x, order):
    if order != 3:
        raise NotImplementedError("NumPy reference only supports cubic (order=3)")
    return numpy_smoothstep(edge0, edge1, x)

# --- Benchmark utility ---

def benchmark(func, *args, repeat=10, inner_loops=1):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        for _ in range(inner_loops):
            func(*args)
        end = time.perf_counter()
        times.append((end - start) / inner_loops)
    return times

def check_correctness(arr_py, arr_np, out_py, numpy_func, cython_func, *args, name="function"):
    indices = [0, len(arr_py)//2, len(arr_py)-1]
    np_result = numpy_func(*args, arr_np) if name != "generalized_smoothstep" else numpy_func(*args, arr_np, 3)
    cython_func(arr_py, *args, out_py) if name != "generalized_smoothstep" else cython_func(arr_py, *args, 3, out_py)
    for idx in indices:
        np_val = np_result[idx]
        cy_val = out_py[idx]
        if not np.isclose(np_val, cy_val, rtol=1e-12, atol=1e-12):
            raise AssertionError(f"Correctness check failed for {name} at index {idx}: NumPy={np_val}, smoothmath={cy_val}")
    print(f"  [OK] Correctness check passed for {name}.")

def run_benchmarks(N, edge0, edge1, repeat=10, inner_loops=1):
    arr_np = np.linspace(0, 1, N, dtype=np.float64)
    arr_py = array.array('d', arr_np.tolist())
    out_py = array.array('d', [0.0] * N)

    results = {}

    # --- smoothstep ---
    numpy_smoothstep(edge0, edge1, arr_np)
    smoothmath.smoothstep_array(arr_py, edge0, edge1, out_py)
    check_correctness(arr_py, arr_np, out_py, numpy_smoothstep, smoothmath.smoothstep_array, edge0, edge1, name="smoothstep")
    t_numpy = benchmark(numpy_smoothstep, edge0, edge1, arr_np, repeat=repeat, inner_loops=inner_loops)
    t_cython = benchmark(smoothmath.smoothstep_array, arr_py, edge0, edge1, out_py, repeat=repeat, inner_loops=inner_loops)
    results['smoothstep'] = (t_numpy, t_cython)

    # --- smootherstep ---
    numpy_smootherstep(edge0, edge1, arr_np)
    smoothmath.smootherstep_array(arr_py, edge0, edge1, out_py)
    check_correctness(arr_py, arr_np, out_py, numpy_smootherstep, smoothmath.smootherstep_array, edge0, edge1, name="smootherstep")
    t_numpy = benchmark(numpy_smootherstep, edge0, edge1, arr_np, repeat=repeat, inner_loops=inner_loops)
    t_cython = benchmark(smoothmath.smootherstep_array, arr_py, edge0, edge1, out_py, repeat=repeat, inner_loops=inner_loops)
    results['smootherstep'] = (t_numpy, t_cython)

    # --- generalized_smoothstep (order=3) ---
    numpy_generalized_smoothstep(edge0, edge1, arr_np, 3)
    smoothmath.generalized_smoothstep_array(arr_py, edge0, edge1, 3, out_py)
    check_correctness(arr_py, arr_np, out_py, numpy_generalized_smoothstep, smoothmath.generalized_smoothstep_array, edge0, edge1, name="generalized_smoothstep")
    t_numpy = benchmark(lambda: numpy_generalized_smoothstep(edge0, edge1, arr_np, 3), repeat=repeat, inner_loops=inner_loops)
    t_cython = benchmark(lambda: smoothmath.generalized_smoothstep_array(arr_py, edge0, edge1, 3, out_py), repeat=repeat, inner_loops=inner_loops)
    results['generalized_smoothstep'] = (t_numpy, t_cython)

    return results

def print_results(size_label, N, results):
    print(f"\n{'='*70}")
    print(f"Array size: {N:,} ({size_label})")
    print(f"{'-'*70}")
    for func in ['smoothstep', 'smootherstep', 'generalized_smoothstep']:
        t_numpy = results[func][0]
        t_cython = results[func][1]
        avg_numpy = sum(t_numpy) / len(t_numpy)
        avg_cython = sum(t_cython) / len(t_cython)
        if avg_cython < avg_numpy:
            faster = "smoothmath"
            speedup = avg_numpy / avg_cython
        else:
            faster = "NumPy"
            speedup = avg_cython / avg_numpy
        print(f"{func}:")
        print(f"  NumPy avg:      {avg_numpy*1e3:10.3f} ms")
        print(f"  smoothmath avg: {avg_cython*1e3:10.3f} ms")
        print(f"  Speedup: {speedup:6.2f}x ({faster} faster)")
        print("-"*70)
    print()

def print_summary(all_results, sizes):
    lines = []
    lines.append("# smoothmath vs NumPy Benchmark Results\n")
    lines.append("| Size         | Function                | NumPy avg (ms) | smoothmath avg (ms) | Faster     |")
    lines.append("|--------------|-------------------------|---------------:|--------------------:|:----------:|")
    for (size_label, N, _), results in zip(sizes, all_results):
        for func in ['smoothstep', 'smootherstep', 'generalized_smoothstep']:
            t_numpy = results[func][0]
            t_cython = results[func][1]
            avg_numpy = sum(t_numpy) / len(t_numpy)
            avg_cython = sum(t_cython) / len(t_cython)
            faster = "smoothmath" if avg_cython < avg_numpy else "NumPy"
            lines.append(f"| {size_label:<12} | {func:<23} | {avg_numpy*1e3:13.3f} | {avg_cython*1e3:18.3f} | {faster:^10} |")
    lines.append("\n*Lower time is better. Speedup >1 means smoothmath is faster.*\n")
    with open("COMPARE.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n" + "="*70)
    print("Summary Table (average times in ms, best is lower):")
    print("="*70)
    print(f"{'Size':<14} {'Function':<25} {'NumPy avg (ms)':>15} {'smoothmath avg (ms)':>20} {'Faster':>10}")
    print("-"*80)
    for (size_label, N, _), results in zip(sizes, all_results):
        for func in ['smoothstep', 'smootherstep', 'generalized_smoothstep']:
            t_numpy = results[func][0]
            t_cython = results[func][1]
            avg_numpy = sum(t_numpy) / len(t_numpy)
            avg_cython = sum(t_cython) / len(t_cython)
            faster = "smoothmath" if avg_cython < avg_numpy else "NumPy"
            print(f"{size_label:<14} {func:<25} {avg_numpy*1e3:15.3f} {avg_cython*1e3:20.3f} {faster:>10}")
    print("="*80)
    print("Results also written to COMPARE.md (Markdown table).")

def main():
    print("="*80)
    print("Benchmark: smoothmath (Cython) vs NumPy")
    print("="*80)
    edge0, edge1 = 0.0, 1.0
    repeat = 10

    # Array sizes and inner_loops for timer resolution
    sizes = [
        ("very small", 10, 10000),
        ("small", 100, 1000),
        ("medium", 100_000, 10),
        ("large", 1_000_000, 1),
        ("very large", 10_000_000, 1),
    ]

    all_results = []
    for size_label, N, inner_loops in sizes:
        results = run_benchmarks(N, edge0, edge1, repeat=repeat, inner_loops=inner_loops)
        print_results(size_label, N, results)
        all_results.append(results)

    print_summary(all_results, sizes)
    print("Note: Lower time is better. Speedup >1 means smoothmath is faster.")
    print("All timings are best-of-10 runs. Results may vary by hardware and build.")
    print("="*80)

if __name__ == "__main__":
    main()