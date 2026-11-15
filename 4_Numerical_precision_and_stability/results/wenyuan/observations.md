# Wenyuan Huang: my laptop observations

Status: Both benchmarks completed in one run, saved as `results/wenyuan`.

## Laptop and run conditions

- Selected result-folder name: `wenyuan`.
- Date and approximate local start time: 15 November 2026. Matrix-vector ran from about 04:13:53 to 04:14:05 (Europe/Madrid, UTC+1). Matrix-matrix ran from about 04:20:49 to 04:21:39.
- Laptop model (optional): MECHREVO XINGYAO Series.
- CPU model: AMD Ryzen AI 9 H 365 w/ Radeon 880M, 10 cores and 20 logical processors.
- Installed RAM: 32 GB (33,597,804,544 bytes reported by Windows).
- Operating system: Windows 11 Home (Chinese), version 10.0.26200.
- Charger connected: Yes; the battery reported 94% and AC status.
- Power mode: Balanced. 
- Other heavy applications running: Not recorded; the two benchmarks were run one after the other.
- Python, NumPy and BLAS versions: Python 3.14.9, NumPy 2.5.4, Matplotlib 3.11.2, threadpoolctl 3.8.0 and OpenBLAS 0.3.34.106.0.
- Detected BLAS threads: One, verified in both JSON files.
- Sizes, repeats and any changes from the defaults: N = 128, 256, 512, 1024, 2048 and 4096, using float32 and float64. Five repeated timing blocks per case, with a minimum target block time of 0.10 s. The recorded settings match the defaults.
- Did both JSON files say completed: true? Yes.
- Were all correctness values True? Yes. There are 12 matrix-vector cases and 12 matrix-matrix cases, 24 in total, with 120 recorded timing blocks. No interruption or memory error was recorded.
- Interpreter note: the run used the Python 3.14.9 environment configured in PyCharm; the JSON records the OpenBLAS library path from that environment.

## What I noticed

1. For matrix-vector with float32, increasing N from 512 to 1024 changed the median time from 0.00001152 s to 0.00004614 s. It took about 4.006 times longer, close to the 4-fold increase in work. At N = 2048 to 4096 the ratio was 6.443, above 4. With float64, the ratio from N = 1024 to 2048 was 7.907, almost twice the 4-fold work increase. Small sizes may be affected by timing overhead; the larger sizes show changing achieved performance.

2. For matrix-matrix with float64, increasing N from 2048 to 4096 changed the median time from 0.303932 s to 2.485376 s. It took about 8.177 times longer, close to the 8-fold increase in work. With float32, the ratio from N = 1024 to 2048 was 16.77, while the next step from 2048 to 4096 was 3.917. This pair is inconsistent with a constant-performance 8-fold scaling and coincides with a large timing spread.

3. At N = 4096, time64/time32 was 2.264 for matrix-vector and 2.126 for matrix-matrix. At N = 2048, the same ratios were 3.208 and 1.019; for matrix-matrix at N = 2048, float32 was not faster than float64.

4. At N = 4096, matrix-vector reached 19.402 GFLOP/s with float32 and 8.569 GFLOP/s with float64. Matrix-matrix reached 117.580 and 55.299 GFLOP/s respectively. Matrix-matrix achieved much higher GFLOP/s, but it still took much longer overall because it did far more work: 2.485376 s in float64, compared with 0.003916 s for matrix-vector.

5. The largest relative spread was 1.276, or 127.6%, for matrix-matrix with float32 at N = 4096. The shortest block was 1.104414 s, the median was 1.168901 s and the longest block was 2.595947 s. Here, relative spread means (maximum - minimum) / median. The next largest were 32.8% for matrix-matrix float32 at N = 2048 and 13.8% for matrix-vector float32 at N = 128.

6. Matrix-matrix float32 was unusually slow at N = 2048, reaching only 57.573 GFLOP/s, compared with about 118 GFLOP/s at N = 1024 and N = 4096. Matrix-vector performance peaked at N = 512: 45.519 GFLOP/s in float32 and 24.176 GFLOP/s in float64. Float32 stayed close to that value at N = 1024 (45.448 GFLOP/s), while float64 fell to 19.256 GFLOP/s. At N = 4096 the values were 19.402 and 8.569 GFLOP/s. I did not see an interruption or a memory error; both scripts finished and all correctness checks passed.

7. I do not know the exact cause of these variations. Background operating-system activity, CPU frequency or thermal behaviour, cache transitions and BLAS blocking are possible explanations, but I did not measure them. The 2.596 s maximum block for matrix-matrix at N = 4096 looks like a transient interruption; the median reduces its influence but does not remove it.

## Summary at N = 4096

| Operation | Precision | Median time (s) | GFLOP/s | Estimated GB/s | Estimated intensity (FLOP/byte) |
|---|---|---:|---:|---:|---:|
| Matrix-vector | float32 | 0.001729 | 19.402 | 38.822 | 0.500 |
| Matrix-vector | float64 | 0.003916 | 8.569 | 34.291 | 0.250 |
| Matrix-matrix | float32 | 1.168901 | 117.580 | 0.172 | 682.667 |
| Matrix-matrix | float64 | 2.485376 | 55.299 | 0.162 | 341.333 |

The estimated GB/s values are derived from ideal byte estimates and the same measured time. They are not measurements of physical RAM traffic.

## Run used in the report

I selected this run, saved as `results/wenyuan`. There was no rerun. All reported matrix-vector and matrix-matrix values and the figures in `results/wenyuan/plots/` refer to this run.

## Notes for the discussion

- Matrix-vector has low, almost constant ideal intensity: about 0.5 FLOP/byte in float32 and 0.25 in float64 for large N. Its lower GFLOP/s and its sensitivity at large N are consistent with a memory-supply limitation, but this experiment does not prove it.
- Matrix-matrix has ideal intensity N/6 in float32 and N/12 in float64, reaching about 682.7 and 341.3 FLOP/byte at N = 4096. Its much higher GFLOP/s is consistent with greater data reuse. It still takes longer than matrix-vector because its total work grows as 2N^3.
- Float32 was faster than float64 at N = 4096 for both operations, but the speedup was about 2.1 to 2.3, not exactly 2. At N = 2048, matrix-matrix showed almost no float32 benefit (1.019). The result therefore does not support a universal twofold speedup.
- The experiment does not independently measure hardware ceilings. The Roofline discussion should remain qualitative, and the largest measured GFLOP/s should not be called a hardware peak.
