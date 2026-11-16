# Aland Arif

Work completed:
- Matrix-matrix benchmark (`benchmark_matmat.py`): C = AB with NumPy, A full of 1.0
  and B full of 2.0, so every entry of C should be 2N. The code comes from the group's
  sample; I read it, ran it and checked the results.
- Ran both benchmarks and the plotting script on my laptop (Intel i7-8565U, 16 GB,
  Windows 11), N = 128 to 4096, float32 and float64, 1 BLAS thread.
- Filled in results/aland/observations.md.

Checks completed:
- All 24 correctness checks passed (12 matrix-vector, 12 matrix-matrix).
- Matrix-matrix time grows about 8x per size doubling (expected from 2N^3 FLOPs).
- Plots checked against the summary CSV values.

Laptop results folder: results/aland

PR links:
- Matrix-matrix benchmark: https://github.com/norouzi-UPC/roofline/pull/4
- Laptop results: https://github.com/norouzi-UPC/roofline/pull/5

Reviews completed:
- PR #1 (matrix-vector benchmark): https://github.com/norouzi-UPC/roofline/pull/1
- PR #3 (plotting script): https://github.com/norouzi-UPC/roofline/pull/3