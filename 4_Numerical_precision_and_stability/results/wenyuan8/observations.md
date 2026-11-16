# Wenyuan Huang: my laptop observations

Status: Both benchmarks completed in one run, saved as `results/wenyuan8`.

## Laptop and run conditions

- Selected result-folder name: `wenyuan8`.
- Date and approximate local start time: 16 November 2026. Matrix-matrix ran from about 19:03:58 to 19:04:46 (Europe/Madrid, UTC+1). Matrix-vector ran from about 19:04:55 to 19:05:08.
- Laptop model (optional): MECHREVO XINGYAO Series.
- CPU model: AMD Ryzen AI 9 H 365 w/ Radeon 880M, 10 cores and 20 logical processors.
- CPU cache: 24 MB L3 and 10 MB L2 in total, as reported by Windows.
- Installed RAM: 32 GB (33,597,804,544 bytes reported by Windows).
- Operating system: Windows 11 Home (Chinese), version 10.0.26200.
- Charger connected: Yes; the battery reported AC status. The exact charge level at the time of the run was not recorded.
- Power mode: Balanced. Best Performance was not selected for this run.
- Other heavy applications running: Not recorded; the two benchmarks were run one after the other.
- Python, NumPy and BLAS versions: Python 3.14.9, NumPy 2.5.4, Matplotlib 3.11.2, threadpoolctl 3.8.0 and OpenBLAS 0.3.34.106.0. The full package list is in `packages.txt`.
- Detected BLAS threads: One, verified in both JSON files.
- Sizes, repeats and any changes from the defaults: N = 128, 256, 512, 1024, 2048 and 4096, using float32 and float64. Five repeated timing blocks per case, with a minimum target block time of 0.10 s. The recorded settings match the defaults.
- Did both JSON files say completed: true? Yes.
- Were all correctness values True? Yes. There are 12 matrix-vector cases and 12 matrix-matrix cases, 24 in total, with 120 recorded timing blocks. No interruption or memory error was recorded.
- Interpreter note: the run used the Python 3.14.9 environment configured in PyCharm; the JSON records the OpenBLAS library path from that environment.

## What I noticed

1. For matrix-vector with float32, increasing N from 512 to 1024 changed the median time from 0.00001088 s to 0.00004508 s. It took about 4.14 times longer, close to the 4-fold increase in work. With float64, increasing N from 512 to 1024 changed the median time from 0.00002126 s to 0.00008201 s, a ratio of 3.86. The step from N = 1024 to 2048 took 6.36 times longer in float32 and 8.60 times longer in float64, above 4. This is the cache transition described below.

2. For matrix-matrix with float32, the adjacent-size time ratios were 7.12, 7.79, 8.01, 8.01 and 7.92, close to the expected 8-fold work increase. With float64 the ratios were 4.31, 7.56, 7.99, 7.95 and 7.86. The first ratio is affected by the very small N = 128 timing; from N = 256 onward the float64 ratios are also close to 8.

3. At N = 4096, time64/time32 was 2.379 for matrix-vector and 2.227 for matrix-matrix. At N = 2048, the same ratios were 2.458 and 2.242. Float32 is faster, but the speedup is not exactly 2.

4. At N = 4096, matrix-vector reached 21.112 GFLOP/s with float32 and 8.875 GFLOP/s with float64. Matrix-matrix reached 127.916 and 57.450 GFLOP/s respectively. Matrix-matrix achieved much higher GFLOP/s, but it still took much longer overall because it did far more work: 2.392334 s in float64, compared with 0.003781 s for matrix-vector.

5. The largest relative spread was 0.615, or 61.5%, for matrix-matrix with float64 at N = 128. The shortest block was 0.000106354 s, the median was 0.000146982 s and the longest block was 0.000196695 s. Here, relative spread means (maximum - minimum) / median. The next largest were 21.3% for matrix-vector float64 at N = 512 and 12.8% for matrix-matrix float64 at N = 256.

6. Matrix-vector performance peaked at N = 512 in this run: 48.181 GFLOP/s for float32 and 24.662 GFLOP/s for float64. It then fell to 21.112 and 8.875 GFLOP/s at N = 4096. Matrix-matrix float32 stayed around 124–128 GFLOP/s from N = 256 onward. Matrix-matrix float64 rose from 28.5 GFLOP/s at N = 128 to about 56–57.5 GFLOP/s from N = 512 onward. The N = 128 float64 point has large spread because each call is very short.

7. I do not know the exact cause of every fluctuation, but the main pattern is consistent with the memory hierarchy and with small timing noise. The CPU has 24 MB of L3 cache. A float64 matrix of size N = 1024 occupies 8 MB and fits in L3; at N = 2048 it occupies 32 MB and no longer fits. The float32 matrix grows from 4 MB to 16 MB over the same step, which is close to the effective cache boundary. Because the benchmark calls the same operation repeatedly, small matrices stay cache-resident and their estimated bytes overstate the real DRAM traffic. The large spread at matrix-matrix float64 N = 128 is a small-size timing effect; the median reduces its influence.

## Summary at N = 4096

| Operation | Precision | Median time (s) | GFLOP/s | Estimated GB/s | Estimated intensity (FLOP/byte) |
|---|---|---:|---:|---:|---:|
| Matrix-vector | float32 | 0.001589 | 21.112 | 42.245 | 0.500 |
| Matrix-vector | float64 | 0.003781 | 8.875 | 35.519 | 0.250 |
| Matrix-matrix | float32 | 1.074448 | 127.916 | 0.187 | 682.667 |
| Matrix-matrix | float64 | 2.392334 | 57.450 | 0.168 | 341.333 |

The estimated GB/s values are derived from ideal byte estimates and the same measured time. They are not measurements of physical RAM traffic. At small and medium N, cache reuse makes the real DRAM traffic much smaller than the estimate; at large N the estimate is closer to reality.

## Run used in the report

I selected this run, saved as `results/wenyuan8`. There was no rerun. All reported matrix-vector and matrix-matrix values and the figures in `results/wenyuan8/plots/` refer to this run.

## Notes for the discussion

- Matrix-vector has low, almost constant ideal intensity: about 0.5 FLOP/byte in float32 and 0.25 in float64 for large N. Its lower GFLOP/s and its drop after N = 512 are consistent with a memory-supply limitation, but the drop is a cache effect rather than a failure of the benchmark.
- Matrix-matrix has ideal intensity N/6 in float32 and N/12 in float64, reaching about 682.7 and 341.3 FLOP/byte at N = 4096. Its much higher GFLOP/s is consistent with greater data reuse. It still takes longer than matrix-vector because its total work grows as 2N^3.
- Float32 was faster than float64 at N = 4096 for both operations, but the speedup was about 2.23 to 2.38, not exactly 2. The result therefore does not support a universal twofold speedup.
- The simple Roofline expression P <= min(P_peak, B_memory * I) uses one memory bandwidth. The measurements show different effective bandwidths at different sizes because of L3 caching, so the points do not all lie on one straight memory roof.
- The matrix-matrix float64 point at N = 128 has large spread, so the 8-fold scaling is clearest from N = 256 onward. The experiment does not independently measure hardware ceilings, and the largest measured GFLOP/s should not be called a hardware peak.
