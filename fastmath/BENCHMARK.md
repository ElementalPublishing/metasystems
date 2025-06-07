# fastmath Benchmark Report

This report summarizes the correctness and performance of your `fastmath` Cython module compared to pure Python implementations.

## Correctness Checks

- **sum_array**: PASS
- **mul**: PASS
- **mean_array**: PASS
- **variance_array**: PASS
- **gcd**: PASS
- **lcm**: PASS
- **is_prime**: PASS
- **mysin**: PASS
- **mycos**: PASS
- **mytan**: PASS
- **myexp**: PASS
- **mylog**: PASS
- **mysqrt**: PASS
- **clamp**: PASS
- **distance2d**: PASS
- **median**: PASS
- **modinv**: PASS
- **fadd**: PASS
- **fsub**: PASS
- **fmul**: PASS
- **fdiv**: PASS
- **imod**: PASS
- **fmodulus**: PASS
- **sub**: PASS
- **add**: PASS
- **imin**: PASS
- **imax**: PASS
- **fmin**: PASS
- **fmax**: PASS
- **square**: PASS
- **cube**: PASS
- **hypot**: PASS
- **power**: PASS
- **myabs**: PASS
- **myfloor**: PASS
- **myceil**: PASS
- **round_nearest**: PASS
- **factorial**: PASS
- **dfactorial**: PASS
- **mysinh**: PASS
- **mycosh**: PASS
- **mytanh**: PASS
- **myasinh**: PASS
- **myacosh**: PASS
- **myatanh**: PASS
- **safe_log**: PASS
- **nth_root**: PASS
- **safe_div**: PASS
- **percent_change**: PASS
- **safe_pow**: PASS
- **sign**: PASS
- **step**: PASS
- **fract**: PASS
- **saturate**: PASS
- **deg2rad**: PASS
- **rad2deg**: PASS
- **distance2d**: PASS
- **distance3d**: PASS
- **smoothstep**: PASS
- **wrap_angle_rad**: PASS
- **wrap_angle_deg**: PASS
- **reciprocal**: PASS
- **array_min**: PASS
- **array_max**: PASS
- **clamp_array**: FAIL ()
- **harmonic_mean**: FAIL ()
- **geometric_mean**: FAIL ()
- **bit_and**: PASS
- **bit_or**: PASS
- **bit_xor**: PASS
- **bit_not**: PASS
- **bit_shl**: PASS
- **bit_shr**: PASS
- **cadd**: PASS
- **csub**: PASS
- **cmul**: PASS
- **cdiv**: PASS
- **cabs**: PASS
- **cconj**: PASS

**Summary:** 76 passed, 3 failed.
> :warning: Some functions failed correctness checks. Review your Cython implementations for logic or type errors.

## Performance Benchmark

The table below shows the time taken (in seconds) by each function in Python and in your Cython `fastmath` module, as well as the speedup factor. The table is sorted by speedup (highest to lowest).

| Function | Python (s) | fastmath (s) | Speedup | Note |
|---|---|---|---|---|
| clamp_array | 14.957860 | 0.265150 | 56.41x |  |
| is_prime | 0.882364 | 0.022275 | 39.61x |  |
| smoothstep | 0.032356 | 0.003138 | 10.31x |  |
| array_max | 0.869554 | 0.104443 | 8.33x |  |
| array_min | 0.841121 | 0.104949 | 8.01x |  |
| sum_array | 0.508741 | 0.066150 | 7.69x |  |
| mean_array | 0.524799 | 0.071148 | 7.38x |  |
| variance_array | 9.266637 | 1.307181 | 7.09x |  |
| saturate | 0.015174 | 0.003057 | 4.96x |  |
| safe_log | 0.014960 | 0.003664 | 4.08x |  |
| geometric_mean | 0.058727 | 0.015984 | 3.67x |  |
| harmonic_mean | 0.056691 | 0.015592 | 3.64x |  |
| wrap_angle_rad | 0.009511 | 0.002781 | 3.42x |  |
| lcm | 0.032488 | 0.010410 | 3.12x |  |
| distance3d | 0.022316 | 0.007346 | 3.04x |  |
| gcd | 0.025768 | 0.009285 | 2.78x |  |
| nth_root | 0.010647 | 0.004419 | 2.41x |  |
| dfactorial | 0.007878 | 0.003324 | 2.37x |  |
| percent_change | 0.007403 | 0.003133 | 2.36x |  |
| reciprocal | 0.005890 | 0.002731 | 2.16x |  |
| sign | 0.006337 | 0.003043 | 2.08x |  |
| wrap_angle_deg | 0.006228 | 0.003022 | 2.06x |  |
| fmax | 0.005735 | 0.002878 | 1.99x |  |
| safe_pow | 0.009098 | 0.004570 | 1.99x |  |
| safe_div | 0.005739 | 0.003049 | 1.88x |  |
| fmin | 0.005766 | 0.003218 | 1.79x |  |
| round_nearest | 0.005307 | 0.003104 | 1.71x |  |
| modinv | 0.024535 | 0.014522 | 1.69x |  |
| cube | 0.004754 | 0.002819 | 1.69x |  |
| cdiv | 0.006938 | 0.004268 | 1.63x |  |
| square | 0.004357 | 0.002684 | 1.62x |  |
| mycosh | 0.004975 | 0.003190 | 1.56x |  |
| fract | 0.006232 | 0.004034 | 1.54x |  |
| imin | 0.005741 | 0.003749 | 1.53x |  |
| imax | 0.005593 | 0.003658 | 1.53x |  |
| clamp | 0.014904 | 0.009902 | 1.51x |  |
| hypot | 0.004799 | 0.003190 | 1.50x |  |
| bit_shl | 0.005170 | 0.003440 | 1.50x |  |
| cabs | 0.004279 | 0.002850 | 1.50x |  |
| cconj | 0.004917 | 0.003357 | 1.46x |  |
| bit_xor | 0.005046 | 0.003546 | 1.42x |  |
| bit_shr | 0.005263 | 0.003699 | 1.42x |  |
| power | 0.005909 | 0.004398 | 1.34x |  |
| add | 0.004674 | 0.003520 | 1.33x |  |
| sub | 0.004735 | 0.003590 | 1.32x |  |
| step | 0.004307 | 0.003298 | 1.31x |  |
| mysinh | 0.004390 | 0.003375 | 1.30x |  |
| bit_and | 0.004902 | 0.003774 | 1.30x |  |
| bit_not | 0.004528 | 0.003488 | 1.30x |  |
| mytanh | 0.004748 | 0.003685 | 1.29x |  |
| bit_or | 0.004796 | 0.003767 | 1.27x |  |
| cadd | 0.004717 | 0.003724 | 1.27x |  |
| fmodulus | 0.007736 | 0.006209 | 1.25x |  |
| myasinh | 0.004463 | 0.003711 | 1.20x |  |
| myatanh | 0.004326 | 0.003616 | 1.20x |  |
| csub | 0.005256 | 0.004442 | 1.18x |  |
| cmul | 0.004836 | 0.004138 | 1.17x |  |
| mycos | 0.006475 | 0.005674 | 1.14x |  |
| mylog | 0.006464 | 0.005710 | 1.13x |  |
| mysqrt | 0.006126 | 0.005576 | 1.10x |  |
| myexp | 0.006129 | 0.005804 | 1.06x |  |
| deg2rad | 0.002770 | 0.002676 | 1.04x |  |
| mysin | 0.006160 | 0.005962 | 1.03x |  |
| myabs | 0.002763 | 0.002708 | 1.02x |  |
| myceil | 0.002877 | 0.002840 | 1.01x |  |
| mytan | 0.006610 | 0.006566 | 1.01x |  |
| distance2d | 0.009287 | 0.009332 | 1.00x | WARNING: Cython overhead outweighs gain |
| rad2deg | 0.002828 | 0.002841 | 1.00x | WARNING: Cython overhead outweighs gain |
| distance2d | 0.009177 | 0.009286 | 0.99x | WARNING: Cython overhead outweighs gain |
| fdiv | 0.005778 | 0.005977 | 0.97x | WARNING: Cython overhead outweighs gain |
| myfloor | 0.002650 | 0.002745 | 0.97x | WARNING: Cython overhead outweighs gain |
| myacosh | 0.005221 | 0.005478 | 0.95x | WARNING: Cython overhead outweighs gain |
| imod | 0.005576 | 0.006206 | 0.90x | WARNING: Cython overhead outweighs gain |
| factorial | 0.003175 | 0.003559 | 0.89x | WARNING: Cython overhead outweighs gain |
| median | 5.765305 | 7.068398 | 0.82x | WARNING: Cython overhead outweighs gain |
| mul | 0.004701 | 0.006111 | 0.77x | WARNING: Cython overhead outweighs gain |
| fsub | 0.004278 | 0.005754 | 0.74x | WARNING: Cython overhead outweighs gain |
| fadd | 0.004371 | 0.005928 | 0.74x | WARNING: Cython overhead outweighs gain |
| fmul | 0.004416 | 0.006104 | 0.72x | WARNING: Cython overhead outweighs gain |

## Analysis & Recommendations

- **66 functions** ran faster with Cython (`fastmath`) than with pure Python.
- **13 functions** ran slower with Cython. For these, the overhead of calling a Cython function outweighs any speed gain. This is typical for very simple operations (like single multiplications or additions).

- :rocket: **Use Cython for functions with significant computation, loops, or array processing.**
- :bulb: **For trivial math (e.g., `a * b`), stick with plain Python.** Cython is best for heavy lifting, not for single operations.
- :warning: **Some functions failed correctness checks.** Investigate these for bugs or type mismatches.

### How to interpret 'Speedup'
- A speedup greater than 1.0 means `fastmath` is faster than Python.
- A speedup less than 1.0 (with a WARNING) means Python is faster for that function.

### Next Steps
- Focus on optimizing or fixing any functions that failed correctness.
- Consider removing or rewriting Cython wrappers for trivial math functions.
- For best results, use Cython for array operations, loops, and complex algorithms.

_This report was automatically generated by your benchmarking script._
