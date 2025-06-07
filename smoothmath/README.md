# smoothmath

**Professional-grade smoothstep and interpolation math for Blender, animation, and scientific computing.**

---

## Features

- 🚀 **High-precision, robust** smoothstep, smootherstep, and generalized smoothstep
- 🏎️ **Extremely fast**: Cython-accelerated, outperforms NumPy for most use cases
- 🧮 **Vectorized**: Efficient batch processing with Cython memoryviews
- 🧑‍💻 **Derivative and inverse** functions for animation/easing
- 🧪 **Fully tested**: Includes correctness and performance benchmarks
- 📝 **MIT License** — free for any use

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/smoothmath.git
   cd smoothmath
   ```

2. **Build the Cython extension:**
   ```sh
   python setup.py build_ext --inplace
   ```

3. *(Optional)* Install dependencies for testing/benchmarking:
   ```sh
   pip install numpy pytest
   ```

---

## Usage

```python
import smoothmath

# Scalar usage
y = smoothmath.smoothstep(0.0, 1.0, 0.5)
y2 = smoothmath.smootherstep(0.0, 1.0, 0.5)
y3 = smoothmath.generalized_smoothstep(0.0, 1.0, 0.5, 5)

# Vectorized usage (with array.array or memoryview)
import array
arr = array.array('d', [0.0, 0.25, 0.5, 0.75, 1.0])
out = array.array('d', [0.0]*len(arr))
smoothmath.smoothstep_array(arr, 0.0, 1.0, out)
print(list(out))
```

---

## Performance

See [`COMPARE.md`](./COMPARE.md) for detailed benchmarks vs NumPy.

- **smoothmath** is significantly faster than NumPy for small and large arrays, and for all advanced interpolation functions.
- For medium-sized arrays and classic smoothstep, NumPy may be slightly faster, but `smoothmath` is still highly competitive and more flexible.

---

## Testing

Run the test suite:
```sh
pytest test_smoothmath.py
```

Run the benchmark and generate a Markdown comparison:
```sh
python benchmark_smoothmath_vs_numpy.py
```

---

## For Blender Add-on Developers

`smoothmath` is ideal for procedural animation, geometry nodes, and custom Blender add-ons.  
Just build the extension and import as usual in Blender’s scripting workspace.

---

## License

MIT License — see [LICENSE](./LICENSE)

---

## Author

Wesley Alexander Houser

---

## Contributing

Pull requests and issues are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) if you want to help improve smoothmath.
