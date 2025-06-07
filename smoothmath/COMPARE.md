# smoothmath vs NumPy Benchmark Results

| Size    | Function                | NumPy avg (ms) | smoothmath avg (ms) | Faster     |
|---------|-------------------------|---------------:|--------------------:|:----------:|
| small   | smoothstep              |         0.023 |              0.002 | smoothmath |
| small   | smootherstep            |         0.009 |              0.002 | smoothmath |
| small   | generalized_smoothstep  |         0.005 |              0.002 | smoothmath |
| medium  | smoothstep              |         0.025 |              0.122 |   NumPy    |
| medium  | smootherstep            |         0.174 |              0.125 | smoothmath |
| medium  | generalized_smoothstep  |         0.022 |              0.125 |   NumPy    |
| large   | smoothstep              |        13.523 |             12.449 | smoothmath |
| large   | smootherstep            |        27.533 |             12.938 | smoothmath |
| large   | generalized_smoothstep  |        13.436 |             12.341 | smoothmath |

*Lower time is better. Speedup >1 means smoothmath is faster.*
