# MohammadJavad Norouzi: my laptop observations

Status: Both benchmarks completed. These notes use the second run, saved as `mohammadjavad_run2`.

## Laptop and run conditions

- Selected result-folder name: `mohammadjavad_run2`.
- Date and approximate local start time: 14 November 2026, 13:00 in Europe/Madrid (12:00 UTC). Matrix-vector ran from about 13:00:08 to 13:00:20. Matrix-matrix ran from about 13:00:38 to 13:01:14.
- Laptop model (optional): Not recorded.
- CPU model: 13th Gen Intel Core i7-13800H. Task Manager shows 14 cores and 20 logical processors.
- Installed RAM: 64.0 GB LPDDR5, shown at 5200 MT/s in the earlier Task Manager screenshot.
- Operating system: Windows 11, build 26200.
- Charger connected: Yes, plugged in during the run.
- Power mode: The exact power mode and Energy saver setting for this second run were not recorded.
- Other heavy applications running: I had no other programs running.
- Python, NumPy and BLAS versions: Python 3.14.2 (64-bit), NumPy 2.5.4 and OpenBLAS 0.3.34.106.0, as recorded in both JSON files.
- Detected BLAS threads: One, verified in both JSON files.
- Sizes, repeats and changes from the defaults: N = 128, 256, 512, 1024, 2048 and 4096, using float32 and float64. Five repeated timing blocks per case, with a minimum target block time of 0.10 s. The recorded settings match the package defaults.
- Did both JSON files say completed: true? Yes.
- Were all correctness values True? Yes. There are 12 cases for each operation, so 24 in total, with 120 recorded timing blocks.
- Full package list: `packages.txt` was not included in the uploaded second-run folder. It still needs to be saved from the environment used for this run.

## What I noticed

1. For matrix-vector with float64, increasing N from 2048 to 4096 changed the median time from 0.000843 s to 0.004595 s. It took about 5.45 times longer. The amount of work increased by about 4 times.

2. For matrix-matrix with float64, the same size change increased the median time from 0.236591 s to 1.866665 s. It took about 7.89 times longer, which is close to the 8-fold increase in the amount of work.

3. At N = 4096, matrix-vector took 0.001904 s with float32 and 0.004595 s with float64. Float32 was about 2.41 times faster. Matrix-matrix took 0.899876 s with float32 and 1.866665 s with float64, so float32 was about 2.07 times faster.

4. At N = 4096, matrix-vector reached 17.619 GFLOP/s with float32 and 7.302 GFLOP/s with float64. Matrix-matrix reached 152.731 and 73.628 GFLOP/s respectively. Matrix-matrix took longer overall, but it did many more calculations per second.

5. The largest relative spread was 0.68549, or 68.55%, for matrix-vector with float32 at N = 256. The shortest time was 3.136 microseconds, the median was 3.412 microseconds and the longest time was 5.475 microseconds. Here, relative spread means (maximum - minimum) / median. For matrix-matrix, the largest spread was much smaller: 4.19%, with float32 at N = 128.

6. Matrix-matrix was much more consistent than in the first run. Its largest spread fell from 167.97% to 4.19%. The unusual float32 slowdown at N = 1024 did not appear again: in this run, float32 was faster than float64 at every tested size for both operations. Matrix-vector still had noticeable variation, including spreads of 40.39% at N = 512 and 22.98% at N = 4096 with float32. Both scripts finished, and no interruption or memory error is recorded in the result files.

7. I do not know the exact reason for the timing changes between runs. I had the charger plugged in and kept other programs closed. CPU speed, operating-system activity and cache behaviour could still affect the timings, but these were not measured. The files do not show which power mode was used for the second run, so I cannot say that changing it caused the improvement.

## Comparison with my first run

These are median times at N = 4096. The speedup in the last column is the first-run time divided by the second-run time.

| Operation | Precision | First run (s) | Second run (s) | Second-run speedup |
|---|---|---:|---:|---:|
| Matrix-vector | float32 | 0.005515 | 0.001904 | 2.896 |
| Matrix-vector | float64 | 0.011319 | 0.004595 | 2.463 |
| Matrix-matrix | float32 | 3.260607 | 0.899876 | 3.623 |
| Matrix-matrix | float64 | 6.646548 | 1.866665 | 3.561 |

I will use the whole second run for the report and keep the first run as an initial check. The matrix-matrix repeats were much more consistent, and the unusual slowdown at N = 1024 did not appear again. I am keeping the variable matrix-vector results too, rather than choosing individual points from different runs.

The report should use the plots in `results/mohammadjavad_run2/plots/`.

## Remaining details

- Add the actual power mode and Energy saver setting used for this second run, if known.
- Save a fresh `packages.txt` in this result folder.
