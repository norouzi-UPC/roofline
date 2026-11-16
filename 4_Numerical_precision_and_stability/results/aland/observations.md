# Aland Arif: laptop observations

Status: Completed.

## Laptop and conditions

- Result folder: aland
- Date and start time: 16 Nov 2026, about 17:40 (matrix-vector, then matrix-matrix, then plots)
- CPU: Intel Core i7-8565U @ 1.80 GHz, 4 cores / 8 logical processors; caches L1 256 KB, L2 1 MB, L3 8 MB
- RAM: 16 GB DDR4
- Operating system: Windows 11 Pro
- Charger connected: Yes
- Power mode and Energy saver setting: Best performance; Energy saver off
- Other heavy programs running: None (only VS Code and a browser open, not in use)
- Python, NumPy and BLAS versions: Python 3.14.7, NumPy 2.5.5, OpenBLAS 0.3.34
- BLAS threads: 1 (verified by threadpoolctl)
- Sizes and repeats: N = 128, 256, 512, 1024, 2048, 4096; 5 timing blocks per case
- Both benchmarks completed: Yes
- All 24 correctness checks passed: Yes

## Results

1. Matrix-vector time ratio when N changes from 2048 to 4096, using float64 precision: 4.55
   (close to the expected 4, since the work grows as N^2). From 1024 to 2048 in float32
   the ratio is 7.90, much larger than 4: this is where the matrix stops fitting in cache.
2. Matrix-matrix time ratio for a size doubling, using float64 precision (2048 to 4096): 7.97
   (expected 8, since the work grows as N^3).
3. At the largest N, time64/time32: matrix-vector 2.26, matrix-matrix 2.39.
4. At the largest N, GFLOP/s: matrix-vector float32 11.68, float64 5.18;
   matrix-matrix float32 98.96, float64 41.47.
5. Largest relative_spread: 0.231 (23 %), matrix-vector float32, N = 256.
6. Matrix-vector performance rises and then drops: float32 peaks at N = 1024 (29.4 GFLOP/s)
   and falls to 14.9 at N = 2048; float64 peaks at N = 512 (15.2) and falls to 9.2 at N = 1024.
   The matrix-vector float32 speedup at N = 1024 is 3.19, above the expected 2.
   Matrix-matrix performance stays nearly flat (about 41 GFLOP/s float64, about 100 float32).
7. The drops match the 8 MB L3 cache: the float32 matrix is 4 MB at N = 1024 (fits) and 16 MB
   at N = 2048 (does not fit); the float64 matrix is 2 MB at N = 512 and 8 MB at N = 1024.
   At N = 1024 the float32 matrix still fits in cache but the float64 one does not, which
   explains the speedup above 2. The large spread at N = 256 is likely timer and OS noise,
   since each call takes only about 6 microseconds. Not measured: actual cache misses or
   memory traffic, CPU clock speed and temperature during the runs, and the laptop's
   hardware peak bandwidth and FLOP/s.

## Run selected

- Folder used for the report: aland
- Reason, if there was more than one run: Only one run.