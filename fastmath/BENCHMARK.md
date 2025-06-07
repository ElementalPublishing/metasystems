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
- **mat_pow**: PASS
- **integrate**: PASS
- **set_union**: PASS
- **set_intersection**: PASS
- **set_difference**: PASS
- **set_symmetric_difference**: PASS

**Summary:** 82 passed, 3 failed.
> :warning: Some functions failed correctness checks. Review your Cython implementations for logic or type errors.

## Performance Benchmark

The table below shows the time taken (in seconds) by each function in Python and in your Cython `fastmath` module, as well as the speedup factor. The table is sorted by speedup (highest to lowest).

| Function | Python (s) | fastmath (s) | Speedup | Note |
|---|---|---|---|---|
| clamp_array | 15.544413 | 0.262749 | 59.16x |  |
| is_prime | 0.893547 | 0.023595 | 37.87x |  |
| smoothstep | 0.033632 | 0.003467 | 9.70x |  |
| array_max | 0.881233 | 0.103838 | 8.49x |  |
| array_min | 0.853999 | 0.106215 | 8.04x |  |
| sum_array | 0.507272 | 0.067389 | 7.53x |  |
| variance_array | 9.363794 | 1.322073 | 7.08x |  |
| mean_array | 0.510046 | 0.072776 | 7.01x |  |
| saturate | 0.015298 | 0.002925 | 5.23x |  |
| safe_log | 0.015336 | 0.003693 | 4.15x |  |
| harmonic_mean | 0.058839 | 0.015286 | 3.85x |  |
| geometric_mean | 0.058602 | 0.016347 | 3.58x |  |
| wrap_angle_rad | 0.009258 | 0.002903 | 3.19x |  |
| lcm | 0.031522 | 0.010426 | 3.02x |  |
| dfactorial | 0.008697 | 0.003225 | 2.70x |  |
| gcd | 0.025465 | 0.009778 | 2.60x |  |
| percent_change | 0.007559 | 0.002918 | 2.59x |  |
| distance3d | 0.022083 | 0.008646 | 2.55x |  |
| fract | 0.007300 | 0.002956 | 2.47x |  |
| nth_root | 0.010018 | 0.004390 | 2.28x |  |
| wrap_angle_deg | 0.006105 | 0.002719 | 2.25x |  |
| safe_pow | 0.009428 | 0.004224 | 2.23x |  |
| sign | 0.006675 | 0.003169 | 2.11x |  |
| reciprocal | 0.005621 | 0.002850 | 1.97x |  |
| safe_div | 0.005910 | 0.003066 | 1.93x |  |
| fmin | 0.005854 | 0.003082 | 1.90x |  |
| fmax | 0.005709 | 0.003018 | 1.89x |  |
| imax | 0.006076 | 0.003445 | 1.76x |  |
| cdiv | 0.006997 | 0.004005 | 1.75x |  |
| hypot | 0.005142 | 0.002968 | 1.73x |  |
| square | 0.004794 | 0.002865 | 1.67x |  |
| modinv | 0.025426 | 0.015266 | 1.67x |  |
| imin | 0.006178 | 0.003716 | 1.66x |  |
| round_nearest | 0.005158 | 0.003180 | 1.62x |  |
| bit_shr | 0.005311 | 0.003438 | 1.54x |  |
| cube | 0.004658 | 0.003023 | 1.54x |  |
| bit_not | 0.004701 | 0.003056 | 1.54x |  |
| mat_pow | 0.202423 | 0.132544 | 1.53x |  |
| clamp | 0.015226 | 0.010154 | 1.50x |  |
| myasinh | 0.005330 | 0.003556 | 1.50x |  |
| step | 0.004583 | 0.003072 | 1.49x |  |
| add | 0.004968 | 0.003339 | 1.49x |  |
| csub | 0.005344 | 0.003725 | 1.43x |  |
| mysinh | 0.004414 | 0.003130 | 1.41x |  |
| cabs | 0.004087 | 0.002918 | 1.40x |  |
| power | 0.005937 | 0.004302 | 1.38x |  |
| bit_or | 0.005202 | 0.003785 | 1.37x |  |
| myatanh | 0.004455 | 0.003259 | 1.37x |  |
| cconj | 0.004652 | 0.003439 | 1.35x |  |
| bit_shl | 0.005173 | 0.003846 | 1.35x |  |
| bit_and | 0.004773 | 0.003605 | 1.32x |  |
| integrate | 12.062830 | 9.249572 | 1.30x |  |
| mycosh | 0.004498 | 0.003539 | 1.27x |  |
| cmul | 0.005003 | 0.003956 | 1.26x |  |
| cadd | 0.005014 | 0.004010 | 1.25x |  |
| sub | 0.004735 | 0.003802 | 1.25x |  |
| bit_xor | 0.004926 | 0.003996 | 1.23x |  |
| mytanh | 0.004552 | 0.003715 | 1.23x |  |
| fmodulus | 0.007539 | 0.006167 | 1.22x |  |
| myacosh | 0.005084 | 0.004414 | 1.15x |  |
| set_difference | 0.022108 | 0.019283 | 1.15x |  |
| set_intersection | 0.022439 | 0.019608 | 1.14x |  |
| mylog | 0.006807 | 0.006063 | 1.12x |  |
| set_symmetric_difference | 0.026565 | 0.024037 | 1.11x |  |
| set_union | 0.025299 | 0.023171 | 1.09x |  |
| mysin | 0.006244 | 0.005775 | 1.08x |  |
| mytan | 0.006783 | 0.006359 | 1.07x |  |
| myexp | 0.006085 | 0.005774 | 1.05x |  |
| mycos | 0.006250 | 0.006004 | 1.04x |  |
| factorial | 0.003559 | 0.003452 | 1.03x |  |
| distance2d | 0.009411 | 0.009479 | 0.99x | WARNING: Cython overhead outweighs gain |
| fdiv | 0.005766 | 0.005837 | 0.99x | WARNING: Cython overhead outweighs gain |
| mysqrt | 0.005889 | 0.005992 | 0.98x | WARNING: Cython overhead outweighs gain |
| myceil | 0.002819 | 0.002975 | 0.95x | WARNING: Cython overhead outweighs gain |
| distance2d | 0.008863 | 0.009408 | 0.94x | WARNING: Cython overhead outweighs gain |
| myfloor | 0.002630 | 0.002831 | 0.93x | WARNING: Cython overhead outweighs gain |
| deg2rad | 0.002648 | 0.003006 | 0.88x | WARNING: Cython overhead outweighs gain |
| rad2deg | 0.002603 | 0.002995 | 0.87x | WARNING: Cython overhead outweighs gain |
| myabs | 0.002592 | 0.002991 | 0.87x | WARNING: Cython overhead outweighs gain |
| imod | 0.005238 | 0.006416 | 0.82x | WARNING: Cython overhead outweighs gain |
| median | 5.881594 | 7.207711 | 0.82x | WARNING: Cython overhead outweighs gain |
| fadd | 0.004820 | 0.006238 | 0.77x | WARNING: Cython overhead outweighs gain |
| fmul | 0.004139 | 0.006014 | 0.69x | WARNING: Cython overhead outweighs gain |
| mul | 0.004597 | 0.006696 | 0.69x | WARNING: Cython overhead outweighs gain |
| fsub | 0.004173 | 0.006549 | 0.64x | WARNING: Cython overhead outweighs gain |

## Analysis & Recommendations

- **70 functions** ran faster with Cython (`fastmath`) than with pure Python.
- **15 functions** ran slower with Cython. For these, the overhead of calling a Cython function outweighs any speed gain. This is typical for very simple operations (like single multiplications or additions).

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
