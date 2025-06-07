# cython: language_level=3

from libc.math cimport (
    sin, cos, tan, exp, log, log10, sqrt, pow, fabs, floor, ceil, atan2,
    sinh, cosh, tanh, asinh, acosh, atanh, asin, acos, atan, fmod
)
from libc.stdlib cimport rand, srand, RAND_MAX

# --- Arithmetic ---
cpdef int add(int a, int b):
    """
    Add two 32-bit integers.
    Inputs must be in the range -2**31 to 2**31-1.
    """
    return a + b

cpdef int sub(int a, int b):
    """
    Subtract two 32-bit integers.
    Inputs must be in the range -2**31 to 2**31-1.
    """
    return a - b

cpdef int mul(int a, int b):
    """
    Multiply two 32-bit integers.
    Inputs must be in the range -2**31 to 2**31-1.
    """
    return a * b

cpdef double fadd(double a, double b):
    """
    Add two floating-point numbers.
    """
    return a + b

cpdef double fsub(double a, double b):
    """
    Subtract two floating-point numbers.
    """
    return a - b

cpdef double fmul(double a, double b):
    """
    Multiply two floating-point numbers.
    """
    return a * b

cpdef double fdiv(double a, double b):
    """
    Divide two floating-point numbers.
    Returns nan if b == 0.
    """
    if b == 0:
        return float('nan')
    return a / b

cpdef int imod(int a, int b):
    """
    Integer modulus (remainder).
    Inputs must be in the range -2**31 to 2**31-1.
    Returns 0 if b == 0.
    """
    if b == 0:
        return 0
    return a % b

cpdef double fmodulus(double a, double b):
    """
    Floating-point modulus (remainder).
    Returns nan if b == 0.
    """
    if b == 0:
        return float('nan')
    return fmod(a, b)

cpdef int imin(int a, int b):
    """
    Minimum of two 32-bit integers.
    """
    return a if a < b else b

cpdef int imax(int a, int b):
    """
    Maximum of two 32-bit integers.
    """
    return a if a > b else b

cpdef double fmin(double a, double b):
    """
    Minimum of two floating-point numbers.
    """
    return a if a < b else b

cpdef double fmax(double a, double b):
    """
    Maximum of two floating-point numbers.
    """
    return a if a > b else b

# --- Powers and Roots ---
cpdef double square(double x): return x * x
cpdef double cube(double x): return x * x * x
cpdef double hypot(double a, double b): return sqrt(a*a + b*b)
cpdef double power(double base, double exp_): return pow(base, exp_)

cpdef double mysqrt(double x):
    if x < 0:
        return float('nan')
    return sqrt(x)

# --- Trigonometric ---
cpdef double mysin(double x): return sin(x)
cpdef double mycos(double x): return cos(x)
cpdef double mytan(double x): return tan(x)
cpdef double myasin(double x):
    if x < -1 or x > 1:
        return float('nan')
    return asin(x)
cpdef double myacos(double x):
    if x < -1 or x > 1:
        return float('nan')
    return acos(x)
cpdef double myatan(double x): return atan(x)
cpdef double atan2d(double y, double x): return atan2(y, x)

# --- Hyperbolic ---
cpdef double mysinh(double x): return sinh(x)
cpdef double mycosh(double x): return cosh(x)
cpdef double mytanh(double x): return tanh(x)
cpdef double myasinh(double x): return asinh(x)
cpdef double myacosh(double x):
    if x < 1:
        return float('nan')
    return acosh(x)
cpdef double myatanh(double x):
    if x <= -1 or x >= 1:
        return float('nan')
    return atanh(x)

# --- Exponential and Logarithmic ---
cpdef double myexp(double x): return exp(x)
cpdef double mylog(double x):
    if x <= 0:
        return float('nan')
    return log(x)
cpdef double mylog10(double x):
    if x <= 0:
        return float('nan')
    return log10(x)

# --- Rounding and Absolute Value ---
cpdef double myabs(double x): return fabs(x)
cpdef double myfloor(double x): return floor(x)
cpdef double myceil(double x): return ceil(x)
cpdef double round_nearest(double x):
    return floor(x + 0.5) if x > 0 else ceil(x - 0.5)

# --- Combinatorics ---
cpdef int factorial(int n):
    if n < 0:
        return 0
    cdef int i, result = 1
    for i in range(2, n+1):
        result *= i
    return result

cpdef double dfactorial(int n):
    if n < 0:
        return 0.0
    cdef int i
    cdef double result = 1
    for i in range(2, n+1):
        result *= i
    return result

cpdef int gcd(int a, int b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

cpdef int lcm(int a, int b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)

# --- Array Math ---
cpdef double sum_array(double[:] arr):
    if arr.shape[0] == 0:
        return 0.0
    cdef double total = 0
    cdef Py_ssize_t i
    for i in range(arr.shape[0]):
        total += arr[i]
    return total

cpdef double mean_array(double[:] arr):
    n = arr.shape[0]
    if n == 0:
        return float('nan')
    return sum_array(arr) / n

cpdef double variance_array(double[:] arr):
    n = arr.shape[0]
    if n == 0:
        return float('nan')
    cdef double mean = mean_array(arr)
    cdef double var = 0
    cdef Py_ssize_t i
    for i in range(n):
        var += (arr[i] - mean) ** 2
    return var / n

cpdef double stddev_array(double[:] arr):
    return mysqrt(variance_array(arr))

# --- Utility / Examples ---
cpdef void apply_sine_wave(double[:] signal, double freq, double rate):
    cdef Py_ssize_t i, n = signal.shape[0]
    for i in range(n):
        signal[i] *= sin(2 * 3.141592653589793 * freq * i / rate)

cpdef int count_nucleotide(char[:] seq, char nucleotide):
    cdef Py_ssize_t i, n = seq.shape[0]
    cdef int count = 0
    for i in range(n):
        if seq[i] == nucleotide:
            count += 1
    return count

cpdef void step_particles(double[:, :] positions, double[:, :] velocities, double dt):
    cdef Py_ssize_t i, n = positions.shape[0]
    for i in range(n):
        positions[i, 0] += velocities[i, 0] * dt
        positions[i, 1] += velocities[i, 1] * dt

# --- Vector Math (2D/3D) ---
cpdef double dot2d(double x1, double y1, double x2, double y2):
    return x1 * x2 + y1 * y2

cpdef double dot3d(double x1, double y1, double z1, double x2, double y2, double z2):
    return x1 * x2 + y1 * y2 + z1 * z2

cpdef void cross3d(double[:] a, double[:] b, double[:] out):
    if a.shape[0] != 3 or b.shape[0] != 3 or out.shape[0] != 3:
        raise ValueError("All arrays must be 3-element for cross3d")
    out[0] = a[1]*b[2] - a[2]*b[1]
    out[1] = a[2]*b[0] - a[0]*b[2]
    out[2] = a[0]*b[1] - a[1]*b[0]

cpdef double norm2d(double x, double y):
    return sqrt(x*x + y*y)

cpdef double norm3d(double x, double y, double z):
    return sqrt(x*x + y*y + z*z)

# --- Kinematics ---
cpdef double velocity(double x0, double x1, double t0, double t1):
    if t1 == t0:
        return float('nan')
    return (x1 - x0) / (t1 - t0)

cpdef double acceleration(double v0, double v1, double t0, double t1):
    if t1 == t0:
        return float('nan')
    return (v1 - v0) / (t1 - t0)

cpdef double displacement(double v, double t):
    return v * t

cpdef double displacement_acc(double v0, double a, double t):
    return v0 * t + 0.5 * a * t * t

# --- Energy, Force, Work ---
cpdef double kinetic_energy(double m, double v):
    return 0.5 * m * v * v

cpdef double potential_energy(double m, double g, double h):
    return m * g * h

cpdef double work(double force, double distance):
    return force * distance

cpdef double force(double mass, double acceleration):
    return mass * acceleration

cpdef double momentum(double mass, double velocity):
    return mass * velocity

cpdef double impulse(double force, double time):
    return force * time

# --- Rotational Motion ---
cpdef double angular_velocity(double theta, double t):
    if t == 0:
        return float('nan')
    return theta / t

cpdef double angular_acceleration(double w0, double w1, double t0, double t1):
    if t1 == t0:
        return float('nan')
    return (w1 - w0) / (t1 - t0)

cpdef double moment_of_inertia_disk(double m, double r):
    return 0.5 * m * r * r

cpdef double moment_of_inertia_sphere(double m, double r):
    return (2.0/5.0) * m * r * r

cpdef double torque(double force, double radius):
    return force * radius

# --- Floating Point Utilities ---
cpdef bint isclose(double a, double b, double rel_tol=1e-9, double abs_tol=0.0):
    return fabs(a - b) <= max(rel_tol * max(fabs(a), fabs(b)), abs_tol)

cpdef double clamp(double x, double minval, double maxval):
    if minval > maxval:
        minval, maxval = maxval, minval
    if x < minval:
        return minval
    elif x > maxval:
        return maxval
    else:
        return x

# --- Quadratic Equation Solver ---
cpdef tuple quadratic_roots(double a, double b, double c):
    if a == 0:
        if b == 0:
            return ()
        return (-c / b,)
    disc = b*b - 4*a*c
    if disc < 0:
        return ()
    elif disc == 0:
        root = -b / (2*a)
        return (root,)
    else:
        sqrt_disc = sqrt(disc)
        root1 = (-b + sqrt_disc) / (2*a)
        root2 = (-b - sqrt_disc) / (2*a)
        return (root1, root2)

# --- Game Math Utilities ---
cpdef double lerp(double a, double b, double t):
    return a + (b - a) * t

cpdef double inv_lerp(double a, double b, double v):
    if a == b:
        return float('nan')
    return (v - a) / (b - a)

cpdef double remap(double in_min, double in_max, double out_min, double out_max, double v):
    if in_max == in_min:
        return float('nan')
    return out_min + (out_max - out_min) * (v - in_min) / (in_max - in_min)

cpdef double clamp01(double x):
    if x < 0.0:
        return 0.0
    elif x > 1.0:
        return 1.0
    else:
        return x

cpdef double deg2rad(double deg):
    return deg * 0.017453292519943295  # pi / 180

cpdef double rad2deg(double rad):
    return rad * 57.29577951308232  # 180 / pi

cpdef double distance2d(double x1, double y1, double x2, double y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

cpdef double distance3d(double x1, double y1, double z1, double x2, double y2, double z2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

cpdef double smoothstep(double edge0, double edge1, double x):
    if edge1 == edge0:
        return float('nan')
    t = clamp01((x - edge0) / (edge1 - edge0))
    return t * t * (3 - 2 * t)

cpdef double sign(double x):
    if x > 0:
        return 1.0
    elif x < 0:
        return -1.0
    else:
        return 0.0

cpdef double step(double edge, double x):
    return 0.0 if x < edge else 1.0

cpdef double fract(double x):
    return x - floor(x)

cpdef double saturate(double x):
    return clamp01(x)

# --- Angle Utilities ---
cdef double M_PI = 3.141592653589793

cpdef double wrap_angle_rad(double angle):
    while angle <= -M_PI:
        angle += 2 * M_PI
    while angle > M_PI:
        angle -= 2 * M_PI
    return angle

cpdef double wrap_angle_deg(double angle):
    while angle <= -180.0:
        angle += 360.0
    while angle > 180.0:
        angle -= 360.0
    return angle

# --- Vector Normalization ---
cpdef void normalize2d(double[:] v):
    if v.shape[0] != 2:
        raise ValueError("Array must be 2-element for normalize2d")
    cdef double n = sqrt(v[0]*v[0] + v[1]*v[1])
    if n > 0:
        v[0] /= n
        v[1] /= n

cpdef void normalize3d(double[:] v):
    if v.shape[0] != 3:
        raise ValueError("Array must be 3-element for normalize3d")
    cdef double n = sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    if n > 0:
        v[0] /= n
        v[1] /= n
        v[2] /= n

# --- Vector Projection ---
cpdef double proj2d(double x1, double y1, double x2, double y2):
    denom = x2*x2 + y2*y2
    if denom == 0:
        return float('nan')
    return (x1*x2 + y1*y2) / sqrt(denom)

cpdef void reflect2d(double[:] v, double[:] n, double[:] out):
    if v.shape[0] != 2 or n.shape[0] != 2 or out.shape[0] != 2:
        raise ValueError("All arrays must be 2-element for reflect2d")
    dot = v[0]*n[0] + v[1]*n[1]
    out[0] = v[0] - 2 * dot * n[0]
    out[1] = v[1] - 2 * dot * n[1]

# --- Barycentric Coordinates (Triangle) ---
cpdef tuple barycentric2d(double px, double py, double x0, double y0, double x1, double y1, double x2, double y2):
    denom = ((y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2))
    if denom == 0:
        return (float('nan'), float('nan'), float('nan'))
    u = ((y1 - y2)*(px - x2) + (x2 - x1)*(py - y2)) / denom
    v = ((y2 - y0)*(px - x2) + (x0 - x2)*(py - y2)) / denom
    w = 1 - u - v
    return (u, v, w)

# --- Random Number Helpers ---
cpdef void seed_random(unsigned int seed):
    srand(seed)

cpdef double rand01():
    return rand() / <double>RAND_MAX

cpdef int randint(int a, int b):
    if b < a:
        a, b = b, a
    return a + <int>((b - a + 1) * rand01())

# --- Slerp (Spherical Linear Interpolation) for angles in radians ---
cpdef double slerp_angle(double a, double b, double t):
    diff = wrap_angle_rad(b - a)
    return a + diff * t

# --- Perlin Fade Function (used in noise) ---
cpdef double fade(double t):
    return t * t * t * (t * (t * 6 - 15) + 10)

# --- Hashing and Noise Helpers ---
cpdef unsigned int hash_int(unsigned int x):
    x = ((x >> 16) ^ x) * 0x45d9f3b
    x = ((x >> 16) ^ x) * 0x45d9f3b
    x = (x >> 16) ^ x
    return x

cpdef double hash01(unsigned int x):
    return (hash_int(x) & 0xFFFFFF) / 16777216.0

cpdef double lerp_noise(double a, double b, double t):
    return lerp(a, b, fade(t))

cpdef double grad(int hash, double x, double y=0, double z=0):
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else (x if h in (12, 14) else z)
    return ((u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v))

# --- Fractal and Blending ---
cpdef double fractal_brownian_motion(double x, int octaves=4, double lacunarity=2.0, double gain=0.5):
    cdef double amplitude = 1.0
    cdef double frequency = 1.0
    cdef double sum = 0.0
    cdef int i
    for i in range(octaves):
        sum += amplitude * hash01(<unsigned int>(x * frequency))
        amplitude *= gain
        frequency *= lacunarity
    return sum

cpdef double blend(double a, double b, double t):
    return a * (1 - t) + b * t

cpdef double cubic_interp(double a, double b, double c, double d, double t):
    t2 = t * t
    t3 = t2 * t
    return 0.5 * ((2 * b) +
                  (-a + c) * t +
                  (2*a - 5*b + 4*c - d) * t2 +
                  (-a + 3*b - 3*c + d) * t3)

# --- Step and Pulse Functions ---
cpdef double pulse(double a, double b, double x):
    return 1.0 if a <= x < b else 0.0

cpdef double triangle_wave(double x, double period=1.0):
    if period == 0:
        return float('nan')
    return 2.0 * abs(fract(x / period) - 0.5)

cpdef double sawtooth_wave(double x, double period=1.0):
    if period == 0:
        return float('nan')
    return fract(x / period)

cpdef double smooth_min(double a, double b, double k):
    if k == 0:
        return min(a, b)
    h = clamp01(0.5 + 0.5 * (b - a) / k)
    return a * h + b * (1 - h) - k * h * (1 - h)

cpdef double smooth_max(double a, double b, double k):
    if k == 0:
        return max(a, b)
    h = clamp01(0.5 + 0.5 * (a - b) / k)
    return a * h + b * (1 - h) + k * h * (1 - h)

# --- Permutation (for noise) ---
cpdef int permute(int x):
    return ((34 * x + 1) * x) % 289

# --- Spiral and Polar Coordinates ---
cpdef tuple polar_to_cartesian(double r, double theta):
    return (r * cos(theta), r * sin(theta))

cpdef tuple cartesian_to_polar(double x, double y):
    return (sqrt(x*x + y*y), atan2(y, x))

cpdef tuple spiral(double t, double a=1.0, double b=0.2):
    r = a + b * t
    return polar_to_cartesian(r, t)

# --- Matrix Math (2x2, 3x3, 4x4) ---
cpdef void mat2_mul(double[:, :] a, double[:, :] b, double[:, :] out):
    if a.shape[0] != 2 or a.shape[1] != 2 or b.shape[0] != 2 or b.shape[1] != 2 or out.shape[0] != 2 or out.shape[1] != 2:
        raise ValueError("All matrices must be 2x2")
    out[0,0] = a[0,0]*b[0,0] + a[0,1]*b[1,0]
    out[0,1] = a[0,0]*b[0,1] + a[0,1]*b[1,1]
    out[1,0] = a[1,0]*b[0,0] + a[1,1]*b[1,0]
    out[1,1] = a[1,0]*b[0,1] + a[1,1]*b[1,1]

cpdef void mat3_mul(double[:, :] a, double[:, :] b, double[:, :] out):
    if a.shape[0] != 3 or a.shape[1] != 3 or b.shape[0] != 3 or b.shape[1] != 3 or out.shape[0] != 3 or out.shape[1] != 3:
        raise ValueError("All matrices must be 3x3")
    cdef int i, j, k
    for i in range(3):
        for j in range(3):
            out[i, j] = 0
            for k in range(3):
                out[i, j] += a[i, k] * b[k, j]

cpdef double mat2_det(double[:, :] m):
    if m.shape[0] != 2 or m.shape[1] != 2:
        return float('nan')
    return m[0,0]*m[1,1] - m[0,1]*m[1,0]

cpdef double mat3_det(double[:, :] m):
    if m.shape[0] != 3 or m.shape[1] != 3:
        return float('nan')
    return (m[0,0]*(m[1,1]*m[2,2] - m[1,2]*m[2,1])
          - m[0,1]*(m[1,0]*m[2,2] - m[1,2]*m[2,0])
          + m[0,2]*(m[1,0]*m[2,1] - m[1,1]*m[2,0]))

# --- Quaternion Math ---
cpdef void quat_mul(double[:] q1, double[:] q2, double[:] out):
    if q1.shape[0] != 4 or q2.shape[0] != 4 or out.shape[0] != 4:
        raise ValueError("All arrays must be 4-element for quat_mul")
    a, b, c, d = q1[0], q1[1], q1[2], q1[3]
    e, f, g, h = q2[0], q2[1], q2[2], q2[3]
    out[0] = a*e - b*f - c*g - d*h
    out[1] = a*f + b*e + c*h - d*g
    out[2] = a*g - b*h + c*e + d*f
    out[3] = a*h + b*g - c*f + d*e

cpdef void quat_conj(double[:] q, double[:] out):
    if q.shape[0] != 4 or out.shape[0] != 4:
        raise ValueError("All arrays must be 4-element for quat_conj")
    out[0] = q[0]
    out[1] = -q[1]
    out[2] = -q[2]
    out[3] = -q[3]

cpdef void quat_normalize(double[:] q):
    if q.shape[0] != 4:
        raise ValueError("Array must be 4-element for quat_normalize")
    cdef double n = sqrt(q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3])
    if n > 0:
        q[0] /= n
        q[1] /= n
        q[2] /= n
        q[3] /= n

# --- Collision/Intersection Functions ---
cpdef bint point_in_circle(double px, double py, double cx, double cy, double r):
    return (px-cx)**2 + (py-cy)**2 <= r*r

cpdef bint aabb_overlap(double x1, double y1, double w1, double h1, double x2, double y2, double w2, double h2):
    return not (x1+w1 < x2 or x2+w2 < x1 or y1+h1 < y2 or y2+h2 < y1)

cdef bint ccw(double ax, double ay, double bx, double by, double cx, double cy):
    return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)

cpdef bint line_intersect(double x1, double y1, double x2, double y2,
                         double x3, double y3, double x4, double y4):
    return (ccw(x1, y1, x3, y3, x4, y4) != ccw(x2, y2, x3, y3, x4, y4) and
            ccw(x1, y1, x2, y2, x3, y3) != ccw(x1, y1, x2, y2, x4, y4))

# --- SDF (Signed Distance Functions) Primitives ---
cpdef double sdf_circle(double x, double y, double cx, double cy, double r):
    return sqrt((x-cx)**2 + (y-cy)**2) - r

cpdef double sdf_box(double x, double y, double cx, double cy, double hx, double hy):
    dx = fabs(x-cx) - hx
    dy = fabs(y-cy) - hy
    return min(max(dx, dy), 0.0) + sqrt(max(dx, 0.0)**2 + max(dy, 0.0)**2)

# --- More Advanced Noise (Simple 1D Perlin) ---
cpdef double perlin1d(double x):
    xi = int(floor(x))
    xf = x - xi
    h0 = hash01(xi)
    h1 = hash01(xi + 1)
    return lerp(h0, h1, fade(xf))

# --- Utility Functions ---
cpdef void swap_double(double[:] arr, int i, int j):
    n = arr.shape[0]
    if i < 0 or j < 0 or i >= n or j >= n:
        raise IndexError("swap_double: index out of bounds")
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp

cpdef double array_min(double[:] arr):
    n = arr.shape[0]
    if n == 0:
        return float('nan')
    cdef double m = arr[0]
    cdef Py_ssize_t i
    for i in range(1, n):
        if arr[i] < m:
            m = arr[i]
    return m

cpdef double array_max(double[:] arr):
    n = arr.shape[0]
    if n == 0:
        return float('nan')
    cdef double m = arr[0]
    cdef Py_ssize_t i
    for i in range(1, n):
        if arr[i] > m:
            m = arr[i]
    return m

cpdef void clamp_array(double[:] arr, double minval, double maxval):
    cdef Py_ssize_t i, n = arr.shape[0]
    for i in range(n):
        arr[i] = clamp(arr[i], minval, maxval)

# --- Bitwise Operations ---
cpdef int bit_and(int a, int b): return a & b
cpdef int bit_or(int a, int b): return a | b
cpdef int bit_xor(int a, int b): return a ^ b
cpdef int bit_not(int a): return ~a
cpdef int bit_shl(int a, int n): return a << n
cpdef int bit_shr(int a, int n): return a >> n

# --- Quantum Math: Complex Numbers ---
cpdef complex cadd(complex a, complex b): return a + b
cpdef complex csub(complex a, complex b): return a - b
cpdef complex cmul(complex a, complex b): return a * b
cpdef complex cdiv(complex a, complex b):
    if b == 0:
        return 0
    return a / b
cpdef double cabs(complex a): return abs(a)
cpdef complex cconj(complex a): return a.conjugate()

# --- Quantum Gates (2x2 matrices as tuples of tuples) ---
cpdef tuple pauli_x(): return ((0, 1), (1, 0))
cpdef tuple pauli_y(): return ((0, -1j), (1j, 0))
cpdef tuple pauli_z(): return ((1, 0), (0, -1))
cpdef tuple hadamard():
    from math import sqrt
    s = 1 / sqrt(2)
    return ((s, s), (s, -s))
cpdef tuple identity2(): return ((1, 0), (0, 1))

# --- Quantum Gate Application ---
cpdef tuple apply_gate(tuple gate, tuple state):
    a, b = gate[0]
    c, d = gate[1]
    x, y = state
    return (a*x + b*y, c*x + d*y)

# --- Tensor (Kronecker) Product ---
cpdef tuple kron2(tuple a, tuple b):
    if isinstance(a[0], (int, float, complex)) and isinstance(b[0], (int, float, complex)):
        return (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1])
    out = []
    for row_a in a:
        for row_b in b:
            row = []
            for x in row_a:
                for y in row_b:
                    row.append(x * y)
            out.append(tuple(row))
    return tuple(out)

# --- Quantum Measurement Probability ---
cpdef double measure_prob(tuple state, int idx):
    norm = 0.0
    for x in state:
        norm += abs(x)**2
    if norm == 0 or idx < 0 or idx >= len(state):
        return 0.0
    return abs(state[idx])**2 / norm

# --- Example: Apply Hadamard to |0> and measure probabilities ---
cpdef tuple quantum_example():
    h = hadamard()
    state0 = (1, 0)
    state1 = apply_gate(h, state0)
    p0 = measure_prob(state1, 0)
    p1 = measure_prob(state1, 1)
    return (p0, p1)

# --- Logic Gates and Boolean Algebra ---
cpdef int logic_and(int a, int b): return int(bool(a) and bool(b))
cpdef int logic_or(int a, int b): return int(bool(a) or bool(b))
cpdef int logic_not(int a): return int(not bool(a))
cpdef int logic_nand(int a, int b): return int(not (bool(a) and bool(b)))
cpdef int logic_nor(int a, int b): return int(not (bool(a) or bool(b)))
cpdef int logic_xor(int a, int b): return int(bool(a) != bool(b))
cpdef int logic_xnor(int a, int b): return int(bool(a) == bool(b))
cpdef int logic_implication(int a, int b): return int((not bool(a)) or bool(b))
cpdef int logic_equivalence(int a, int b): return int(bool(a) == bool(b))
cpdef int majority(int a, int b, int c): return int((bool(a) + bool(b) + bool(c)) >= 2)
cpdef int parity3(int a, int b, int c): return int((bool(a) + bool(b) + bool(c)) % 2)

# --- Additional Math Utilities ---

cpdef double reciprocal(double x):
    if x == 0:
        return float('nan')
    return 1.0 / x

cpdef double safe_log(double x, double base=10.0):
    if x <= 0 or base <= 0 or base == 1:
        return float('nan')
    return log(x) / log(base)

cpdef double nth_root(double x, double n):
    if n == 0:
        return float('nan')
    if x < 0 and int(n) % 2 == 0:
        return float('nan')
    return pow(x, 1.0 / n)

cpdef double safe_div(double a, double b):
    if b == 0:
        return float('nan')
    return a / b

cpdef double percent_change(double old, double new):
    if old == 0:
        return float('nan')
    return ((new - old) / old) * 100.0

cpdef double harmonic_mean(double[:] arr):
    n = arr.shape[0]
    if n == 0:
        return float('nan')
    cdef double denom = 0
    cdef Py_ssize_t i
    for i in range(n):
        if arr[i] == 0:
            return float('nan')
        denom += 1.0 / arr[i]
    return n / denom

cpdef double geometric_mean(double[:] arr):
    n = arr.shape[0]
    if n == 0:
        return float('nan')
    cdef double prod = 1.0
    cdef Py_ssize_t i
    for i in range(n):
        if arr[i] <= 0:
            return float('nan')
        prod *= arr[i]
    return pow(prod, 1.0 / n)

cpdef double safe_pow(double base, double exp_):
    if base == 0 and exp_ <= 0:
        return float('nan')
    return pow(base, exp_)

# --- Symmetry and Group Theory ---
cpdef int permutation_sign(int[:] perm):
    """Return +1 for even, -1 for odd permutation."""
    n = perm.shape[0]
    cdef int i, j, sign = 1
    for i in range(n):
        for j in range(i+1, n):
            if perm[i] > perm[j]:
                sign *= -1
    return sign

cpdef bint is_identity_permutation(int[:] perm):
    """Check if permutation is the identity."""
    cdef Py_ssize_t i, n = perm.shape[0]
    for i in range(n):
        if perm[i] != i:
            return False
    return True

# --- Calculus and Differential Equations ---
cpdef double numerical_derivative(object f, double x, double h=1e-6):
    """
    Numerical derivative using central difference.
    f must be a Python callable: f(x)
    """
    return (f(x + h) - f(x - h)) / (2 * h)

cpdef double numerical_integral(object f, double a, double b, int n=1000):
    """
    Numerical integration using the trapezoidal rule.
    f must be a Python callable: f(x)
    """
    if n <= 0 or a == b:
        return 0.0
    cdef double h = (b - a) / n
    cdef double s = 0.5 * (f(a) + f(b))
    cdef int i
    for i in range(1, n):
        s += f(a + i * h)
    return s * h

# --- Linear Algebra ---
cpdef int solve_linear2(double[:, :] A, double[:] b, double[:] x):
    """
    Solve 2x2 linear system Ax = b. Returns 1 if solved, 0 if singular.
    """
    if A.shape[0] != 2 or A.shape[1] != 2 or b.shape[0] != 2 or x.shape[0] != 2:
        raise ValueError("All arrays must be 2-element for solve_linear2")
    det = A[0,0]*A[1,1] - A[0,1]*A[1,0]
    if det == 0:
        return 0
    x[0] = (b[0]*A[1,1] - b[1]*A[0,1]) / det
    x[1] = (A[0,0]*b[1] - A[1,0]*b[0]) / det
    return 1

# --- Probability & Statistics ---
cpdef double median(double[:] arr):
    """Median of array."""
    n = arr.shape[0]
    if n == 0:
        return float('nan')
    # Convert to Python list and sort
    sorted_arr = sorted([arr[i] for i in range(n)])
    if n % 2 == 1:
        return sorted_arr[n // 2]
    else:
        return 0.5 * (sorted_arr[n // 2 - 1] + sorted_arr[n // 2])

cpdef double quantile(double[:] arr, double q):
    """q-quantile (0 <= q <= 1) of array."""
    n = arr.shape[0]
    if n == 0 or q < 0 or q > 1:
        return float('nan')
    sorted_arr = sorted([arr[i] for i in range(n)])
    idx = int(q * (n - 1))
    return sorted_arr[idx]

# --- Geometry & Topology ---
cpdef double polygon_area(double[:] x, double[:] y):
    """
    Area of a simple polygon given by vertices (x, y).
    """
    n = x.shape[0]
    if n < 3 or y.shape[0] != n:
        return 0.0
    cdef double area = 0.0
    cdef int i
    for i in range(n):
        area += x[i] * y[(i+1)%n] - x[(i+1)%n] * y[i]
    return fabs(area) / 2.0

# --- Number Theory & Logic ---
cpdef bint is_prime(int n):
    """Check if n is a prime number."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    cdef int i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

cpdef int modinv(int a, int m):
    """Modular inverse of a mod m, or 0 if none exists."""
    cdef int m0 = m
    cdef int y = 0
    cdef int x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x += m0
    return x

# --- Complex Math Benchmarks ---

# 1. Sieve of Eratosthenes (returns Python list of primes up to n)
cpdef list sieve(int n):
    """
    Return a list of all primes <= n using the Sieve of Eratosthenes.
    """
    if n < 2:
        return []
    cdef int i, j
    sieve = [True] * (n + 1)
    sieve[0] = False
    sieve[1] = False
    for i in range(2, int(sqrt(n)) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]

# 2. 2x2 Matrix Exponentiation (returns Python list of lists)
cpdef list mat_pow(list mat, int power):
    """
    Raise a 2x2 matrix (as list of lists) to an integer power.
    Example: mat_pow([[1,1],[1,0]], 10)
    """
    cdef int i, j
    cdef list result = [[1, 0], [0, 1]]
    cdef list base = [[mat[0][0], mat[0][1]], [mat[1][0], mat[1][1]]]
    while power:
        if power % 2:
            result = [
                [result[0][0]*base[0][0] + result[0][1]*base[1][0], result[0][0]*base[0][1] + result[0][1]*base[1][1]],
                [result[1][0]*base[0][0] + result[1][1]*base[1][0], result[1][0]*base[0][1] + result[1][1]*base[1][1]]
            ]
        base = [
            [base[0][0]*base[0][0] + base[0][1]*base[1][0], base[0][0]*base[0][1] + base[0][1]*base[1][1]],
            [base[1][0]*base[0][0] + base[1][1]*base[1][0], base[1][0]*base[0][1] + base[1][1]*base[1][1]]
        ]
        power //= 2
    return result

# 3. Numerical Integration (Simpson's Rule)
cpdef double integrate(object f, double a, double b, int n):
    """
    Numerically integrate f(x) from a to b using Simpson's rule with n intervals.
    f must be a Python callable.
    """
    if n % 2 == 1:
        n += 1  # Simpson's rule requires even n
    cdef double h = (b - a) / n
    cdef double s = f(a) + f(b)
    cdef int i
    for i in range(1, n, 2):
        s += 4 * f(a + i * h)
    for i in range(2, n, 2):
        s += 2 * f(a + i * h)
    return s * h / 3

# --- Set Operations ---
cpdef set set_union(object a, object b):
    """Return the union of two sets or iterables."""
    return set(a) | set(b)

cpdef set set_intersection(object a, object b):
    """Return the intersection of two sets or iterables."""
    return set(a) & set(b)

cpdef set set_difference(object a, object b):
    """Return the difference of two sets or iterables."""
    return set(a) - set(b)

cpdef set set_symmetric_difference(object a, object b):
    """Return the symmetric difference of two sets or iterables."""
    return set(a) ^ set(b)