# smoothmath vs NumPy Speed Benchmark Results

| Size/Type                  | Function                | NumPy avg (ms) | smoothmath avg (ms) | Faster         | Speedup |
|----------------------------|-------------------------|---------------:|--------------------:|:--------------:|--------:|
| edge case 1                | smoothstep              |         0.004 |              0.000 |   smoothmath   |   12.07x |
| edge case 1                | smootherstep            |         0.010 |              0.000 |   smoothmath   |   35.03x |
| edge case 1                | generalized_smoothstep  |         0.005 |              0.000 |   smoothmath   |   14.29x |
| edge case 2                | smoothstep              |         0.004 |              0.000 |   smoothmath   |   16.56x |
| edge case 2                | smootherstep            |         0.006 |              0.000 |   smoothmath   |   21.28x |
| edge case 2                | generalized_smoothstep  |         0.005 |              0.000 |   smoothmath   |   10.86x |
| edge case 8                | smoothstep              |         0.005 |              0.000 |   smoothmath   |    9.43x |
| edge case 8                | smootherstep            |         0.006 |              0.000 |   smoothmath   |   16.72x |
| edge case 8                | generalized_smoothstep  |         0.006 |              0.001 |   smoothmath   |    3.98x |
| animation curve            | smoothstep              |         0.006 |              0.001 |   smoothmath   |    6.05x |
| animation curve            | smootherstep            |         0.007 |              0.001 |   smoothmath   |    5.95x |
| animation curve            | generalized_smoothstep  |         0.005 |              0.001 |   smoothmath   |    4.20x |
| color ramp/LUT             | smoothstep              |         0.005 |              0.002 |   smoothmath   |    2.68x |
| color ramp/LUT             | smootherstep            |         0.008 |              0.003 |   smoothmath   |    2.66x |
| color ramp/LUT             | generalized_smoothstep  |         0.009 |              0.003 |   smoothmath   |    2.93x |
| procedural texture         | smoothstep              |         0.007 |              0.013 |     NumPy      |    1.82x |
| procedural texture         | smootherstep            |         0.028 |              0.013 |   smoothmath   |    2.20x |
| procedural texture         | generalized_smoothstep  |         0.007 |              0.013 |     NumPy      |    1.74x |
| simulation grid 32x32x32   | smoothstep              |         0.277 |              0.381 |     NumPy      |    1.38x |
| simulation grid 32x32x32   | smootherstep            |         0.639 |              0.419 |   smoothmath   |    1.53x |
| simulation grid 32x32x32   | generalized_smoothstep  |         0.261 |              0.408 |     NumPy      |    1.56x |
| image 256x256              | smoothstep              |         0.619 |              0.795 |     NumPy      |    1.28x |
| image 256x256              | smootherstep            |         1.313 |              0.827 |   smoothmath   |    1.59x |
| image 256x256              | generalized_smoothstep  |         0.604 |              0.811 |     NumPy      |    1.34x |
| mesh vertex attributes     | smoothstep              |         0.021 |              0.123 |     NumPy      |    5.82x |
| mesh vertex attributes     | smootherstep            |         0.150 |              0.132 |   smoothmath   |    1.14x |
| mesh vertex attributes     | generalized_smoothstep  |         0.022 |              0.144 |     NumPy      |    6.63x |
| high-poly mesh             | smoothstep              |         1.065 |              1.216 |     NumPy      |    1.14x |
| high-poly mesh             | smootherstep            |         2.198 |              1.288 |   smoothmath   |    1.71x |
| high-poly mesh             | generalized_smoothstep  |         0.907 |              1.227 |     NumPy      |    1.35x |
| particle system            | smoothstep              |        13.426 |             12.110 |   smoothmath   |    1.11x |
| particle system            | smootherstep            |        27.603 |             13.333 |   smoothmath   |    2.07x |
| particle system            | generalized_smoothstep  |        13.486 |             12.218 |   smoothmath   |    1.10x |
| image 1024x1024            | smoothstep              |        13.948 |             12.682 |   smoothmath   |    1.10x |
| image 1024x1024            | smootherstep            |        28.870 |             13.466 |   smoothmath   |    2.14x |
| image 1024x1024            | generalized_smoothstep  |        14.006 |             12.729 |   smoothmath   |    1.10x |
| simulation grid 128x128x128 | smoothstep              |        27.351 |             25.360 |   smoothmath   |    1.08x |
| simulation grid 128x128x128 | smootherstep            |        56.630 |             27.027 |   smoothmath   |    2.10x |
| simulation grid 128x128x128 | generalized_smoothstep  |        27.344 |             25.579 |   smoothmath   |    1.07x |

*Lower time is better. Speedup >1 means smoothmath is faster.*
