# smoothmath vs NumPy Benchmark Results

| Size         | Function                | NumPy avg (ms) | smoothmath avg (ms) | Faster     |
|--------------|-------------------------|---------------:|--------------------:|:----------:|
| very small   | smoothstep              |         0.005 |              0.000 | smoothmath |
| very small   | smootherstep            |         0.006 |              0.000 | smoothmath |
| very small   | generalized_smoothstep  |         0.005 |              0.000 | smoothmath |
| small        | smoothstep              |         0.005 |              0.001 | smoothmath |
| small        | smootherstep            |         0.007 |              0.002 | smoothmath |
| small        | generalized_smoothstep  |         0.005 |              0.002 | smoothmath |
| medium       | smoothstep              |         0.997 |              1.220 |   NumPy    |
| medium       | smootherstep            |         2.157 |              1.270 | smoothmath |
| medium       | generalized_smoothstep  |         1.191 |              1.227 |   NumPy    |
| large        | smoothstep              |        13.281 |             12.323 | smoothmath |
| large        | smootherstep            |        27.580 |             12.679 | smoothmath |
| large        | generalized_smoothstep  |        13.427 |             12.126 | smoothmath |
| very large   | smoothstep              |       127.757 |            121.323 | smoothmath |
| very large   | smootherstep            |       267.177 |            128.571 | smoothmath |
| very large   | generalized_smoothstep  |       128.219 |            129.096 |   NumPy    |

*Lower time is better. Speedup >1 means smoothmath is faster.*
