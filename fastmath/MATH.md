These functions are **basic arithmetic operations or simple math conversions** on floating-point or integer numbers. Here’s what each one does:

| Function      | Description                         | Example |
|---------------|-------------------------------------|---------|
| `fadd`        | Floating-point addition             | `fadd(a, b)` returns `a + b` |
| `fsub`        | Floating-point subtraction          | `fsub(a, b)` returns `a - b` |
| `fmul`        | Floating-point multiplication       | `fmul(a, b)` returns `a * b` |
| `fdiv`        | Floating-point division             | `fdiv(a, b)` returns `a / b` |
| `imod`        | Integer modulus (remainder)         | `imod(a, b)` returns `a % b` |
| `deg2rad`     | Degrees to radians conversion       | `deg2rad(180)` returns `math.pi` |
| `rad2deg`     | Radians to degrees conversion       | `rad2deg(math.pi)` returns `180` |
| `distance2d`  | 2D Euclidean distance               | `distance2d(x1, y1, x2, y2)` returns `sqrt((x2-x1)**2 + (y2-y1)**2)` |
| `myexp`       | Exponential function                | `myexp(x)` returns `math.exp(x)` |
| `median`      | Median of a list/array              | `median(arr)` returns the median value of `arr` |
| `factorial`   | Factorial of an integer             | `factorial(n)` returns `n!` |

**Associated with:**  
- **Elementary arithmetic and conversions** in programming, finance, science, engineering, geometry, and graphics.
- Used everywhere numbers are manipulated, e.g., calculators, spreadsheets, simulations, business logic, and coordinate calculations.

**Benchmark result meaning:**  
- These are so simple that Python’s built-in operations are already highly optimized.
- Calling them through Cython (`fastmath`) adds overhead, making them slower than plain Python for single operations or conversions.
- **Recommendation:** Use plain Python for these functions unless you are processing large arrays or need to optimize loops.
