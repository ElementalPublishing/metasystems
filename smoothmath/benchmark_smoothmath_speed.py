"""
Benchmark: smoothmath vs NumPy for all common Blender/game array sizes

Covers:
- Animation curves: 64
- Color ramps/LUTs: 128
- Procedural textures: 1,024
- Mesh vertex attributes: 10,000
- High-poly mesh: 100,000
- Particle system: 1,000,000
- Simulation grid (32x32x32): 32,768
- Simulation grid (128x128x128): 2,097,152
- Image/texture (256x256): 65,536
- Image/texture (1024x1024): 1,048,576
- Edge cases: 1, 2, 8

Author: Wesley Alexander Houser
"""

import time
import array
import numpy as np
import smoothmath

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

def benchmark(func, *args, repeat=10, inner_loops=10):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        for _ in range(inner_loops):
            func(*args)
        end = time.perf_counter()
        times.append((end - start) / inner_loops)
    return times

def check_correctness(arr_py, arr_np, out_py, numpy_func, cython_func, *args, name="function"):
    indices = [0, len(arr_py)//2, len(arr_py)-1] if len(arr_py) > 2 else range(len(arr_py))
    np_result = numpy_func(*args, arr_np) if name != "generalized_smoothstep" else numpy_func(*args, arr_np, 3)
    cython_func(arr_py, *args, out_py) if name != "generalized_smoothstep" else cython_func(arr_py, *args, 3, out_py)
    for idx in indices:
        np_val = np_result[idx]
        cy_val = out_py[idx]
        if not np.isclose(np_val, cy_val, rtol=1e-12, atol=1e-12):
            raise AssertionError(f"Correctness check failed for {name} at index {idx}: NumPy={np_val}, smoothmath={cy_val}")

def print_results(size_label, N, results):
    print(f"\n{'='*70}")
    print(f"Array size: {N:,} ({size_label})")
    print(f"{'-'*70}")
    for func in ['smoothstep', 'smootherstep', 'generalized_smoothstep']:
        t_numpy = results[func]['numpy']
        t_cython = results[func]['smoothmath']
        avg_numpy = sum(t_numpy) / len(t_numpy)
        avg_cython = sum(t_cython) / len(t_cython)
        std_numpy = np.std(t_numpy) * 1e3
        std_cython = np.std(t_cython) * 1e3
        if avg_cython < avg_numpy:
            faster = "smoothmath"
            speedup = avg_numpy / avg_cython
        else:
            faster = "NumPy"
            speedup = avg_cython / avg_numpy
        print(f"{func:<23}: NumPy {avg_numpy*1e3:8.3f}±{std_numpy:5.3f} ms | "
              f"smoothmath {avg_cython*1e3:8.3f}±{std_cython:5.3f} ms | "
              f"{faster} is {speedup:5.2f}x faster")
    print()

def run_benchmarks(N, edge0, edge1, repeat=10, inner_loops=10):
    arr_np = np.linspace(0, 1, N, dtype=np.float64)
    arr_py = array.array('d', arr_np.tolist())
    out_py = array.array('d', [0.0] * N)
    results = {}

    # Warm-up
    smoothmath.smoothstep_array(arr_py, edge0, edge1, out_py)
    numpy_smoothstep(edge0, edge1, arr_np)
    smoothmath.smootherstep_array(arr_py, edge0, edge1, out_py)
    numpy_smootherstep(edge0, edge1, arr_np)
    smoothmath.generalized_smoothstep_array(arr_py, edge0, edge1, 3, out_py)
    numpy_generalized_smoothstep(edge0, edge1, arr_np, 3)

    # Correctness check
    check_correctness(arr_py, arr_np, out_py, numpy_smoothstep, smoothmath.smoothstep_array, edge0, edge1, name="smoothstep")
    check_correctness(arr_py, arr_np, out_py, numpy_smootherstep, smoothmath.smootherstep_array, edge0, edge1, name="smootherstep")
    check_correctness(arr_py, arr_np, out_py, numpy_generalized_smoothstep, smoothmath.generalized_smoothstep_array, edge0, edge1, name="generalized_smoothstep")

    # Timings
    results['smoothstep'] = {
        'numpy': benchmark(numpy_smoothstep, edge0, edge1, arr_np, repeat=repeat, inner_loops=inner_loops),
        'smoothmath': benchmark(smoothmath.smoothstep_array, arr_py, edge0, edge1, out_py, repeat=repeat, inner_loops=inner_loops)
    }
    results['smootherstep'] = {
        'numpy': benchmark(numpy_smootherstep, edge0, edge1, arr_np, repeat=repeat, inner_loops=inner_loops),
        'smoothmath': benchmark(smoothmath.smootherstep_array, arr_py, edge0, edge1, out_py, repeat=repeat, inner_loops=inner_loops)
    }
    results['generalized_smoothstep'] = {
        'numpy': benchmark(lambda e0, e1, arr: numpy_generalized_smoothstep(e0, e1, arr, 3), edge0, edge1, arr_np, repeat=repeat, inner_loops=inner_loops),
        'smoothmath': benchmark(lambda arr, e0, e1, o, out: smoothmath.generalized_smoothstep_array(arr, e0, e1, o, out), arr_py, edge0, edge1, 3, out_py, repeat=repeat, inner_loops=inner_loops)
    }
    return results

def write_speed_md(all_results, sizes):
    lines = []
    lines.append("# smoothmath vs NumPy Speed Benchmark Results\n")
    lines.append("| Size/Type                  | Function                | NumPy avg (ms) | smoothmath avg (ms) | Faster         | Speedup |")
    lines.append("|----------------------------|-------------------------|---------------:|--------------------:|:--------------:|--------:|")
    for (size_label, N), results in zip(sizes, all_results):
        for func in ['smoothstep', 'smootherstep', 'generalized_smoothstep']:
            t_numpy = results[func]['numpy']
            t_cython = results[func]['smoothmath']
            avg_numpy = sum(t_numpy) / len(t_numpy)
            avg_cython = sum(t_cython) / len(t_cython)
            faster = "smoothmath" if avg_cython < avg_numpy else "NumPy"
            speedup = (avg_numpy / avg_cython) if avg_cython < avg_numpy else (avg_cython / avg_numpy)
            lines.append(f"| {size_label:<26} | {func:<23} | {avg_numpy*1e3:13.3f} | {avg_cython*1e3:18.3f} | {faster:^14} | {speedup:7.2f}x |")
    lines.append("\n*Lower time is better. Speedup >1 means smoothmath is faster.*\n")
    with open("SPEED.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Results also written to SPEED.md (Markdown table).")

def main():
    edge0, edge1 = 0.0, 1.0
    repeat = 10
    inner_loops = 10

    sizes = [
        ("edge case 1", 1),
        ("edge case 2", 2),
        ("edge case 8", 8),
        ("animation curve", 64),
        ("color ramp/LUT", 128),
        ("procedural texture", 1024),
        ("simulation grid 32x32x32", 32_768),
        ("image 256x256", 65_536),
        ("mesh vertex attributes", 10_000),
        ("high-poly mesh", 100_000),
        ("particle system", 1_000_000),
        ("image 1024x1024", 1_048_576),
        ("simulation grid 128x128x128", 2_097_152),
    ]

    all_results = []
    for size_label, N in sizes:
        results = run_benchmarks(N, edge0, edge1, repeat=repeat, inner_loops=inner_loops)
        print_results(size_label, N, results)
        all_results.append(results)

    write_speed_md(all_results, sizes)
    print("="*70)
    print("All timings are best-of-10 runs, averaged over 10 inner loops.")
    print("Lower time is better. Results may vary by hardware and build.")
    print("="*70)

if __name__ == "__main__":
    main()