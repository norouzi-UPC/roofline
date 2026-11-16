# Hamed Zahraei Ramazani: laptop observations

Both benchmarks completed successfully. The selected result folder is
results/hamed.

## Laptop and run conditions

- Date: 16 November 2026.
- CPU: Intel(R) Core(TM) i5-1035G4 CPU @ 1.10GHz.
- RAM: 8,0 GB LPDDR4.
- Operating system: Windows 11.
- Charger connected: Yes.
- Power mode and Energy saver: Not recorded.
- Other heavy programs running: Not recorded.
- Python: 3.14.8.
- NumPy: 2.5.5.
- BLAS: OpenBLAS 0.3.34.237.2.
- Detected BLAS threads: 1 in both benchmarks.
- Sizes: 128, 256, 512, 1024, 2048 and 4096.
- Precisions: float32 and float64.
- Repeats: five timing blocks per case.
- Both machine JSON files report completed: true.
- All 24 correctness checks passed.

## Results

1. For matrix-vector with float32, increasing N from 256 to 512 made
   the median time about 3.975 times longer, close to the fourfold
   increase in work.

2. For matrix-matrix with float32, increasing N from 2048 to 4096
   made the median time about 7.813 times longer, close to eight.

3. At N = 4096, time64/time32 was 2.262 for matrix-vector and 1.956
   for matrix-matrix. Float32 was faster for both operations.

4. At N = 4096, matrix-vector achieved 10.189 GFLOP/s with float32
   and 4.504 GFLOP/s with float64. Matrix-matrix achieved 96.875
   and 49.515 GFLOP/s respectively.

5. The largest relative timing spread was about 19.4%, for
   matrix-vector float32 at N = 4096.

6. Matrix-vector float64 took about 8.611 times longer when N
   increased from 512 to 1024. This was above the fourfold increase
   in work. Cache behaviour or changes in system activity are
   possible explanations, but I did not measure their causes.

Matrix-matrix achieved higher GFLOP/s, but took longer overall
because it performed much more work. The estimated bandwidth values
are calculated from estimated bytes and time, rather than measured
physical RAM traffic.

## Run selected

The report uses results/hamed. The measurements and plots discussed
here all come from that folder.