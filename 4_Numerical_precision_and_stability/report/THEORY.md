# Theory: a sample answer in simple words

These estimates do not depend on which laptop we use. The times and measured
GFLOP/s do depend on the laptop and its software.

## 1. Count the work

For y = Ax, one output entry needs N multiplications and N-1 additions.
There are N output entries, so the exact count is N(2N-1). For large N,
this is about 2N^2 FLOPs.

For C = AB, the same dot product is calculated for each of N^2 output
entries. The exact count is N^2(2N-1), or about 2N^3 FLOPs.
We count a fused multiply-add as two FLOPs. Our code consistently uses the
large-N counts. This convention is for performance accounting, not a claim
that each machine executes that exact instruction sequence.

## 2. Estimate the bytes

Let s be the bytes in one number: 4 for float32, 8 for float64.

For matrix-vector multiplication we read A (N^2 numbers), read x (N numbers)
and write y (N numbers). With ideal reuse of x:

Q_mv = s(N^2 + 2N).

For matrix-matrix multiplication we read A and B (2N^2 numbers in total)
and write C (N^2 numbers). With ideal input reuse:

Q_mm = 3sN^2.

We do not need the old C or y because the operation overwrites the output.
The model ignores hardware write-allocate reads and any packing/workspace.

These are idealized per-call traffic estimates at a chosen memory level.
They are also the total sizes of the input and output arrays here, but that
does not make them a physical RAM traffic measurement. Finite cache can force
extra reloads; repeated warm calls can serve inputs from cache. Our warmed
benchmark deliberately does not flush caches. Explain these assumptions
whenever using the reported estimated GB/s or arithmetic intensity.

If x were read again for every output entry, a simple alternative estimate
would be s(2N^2+N) for matrix-vector multiplication. If neither matrix were
reused across dot products, a simple estimate for matrix-matrix would be
s(2N^3+N^2), assuming partial sums stay in a register. Its intensity would
approach 1/s rather than grow with N. Optimized matrix multiplication uses
blocking to improve reuse, so that pessimistic model is not our main model.

## 3. Divide work by bytes

| Operation | float32 | float64 |
|---|---|---|
| Matrix-vector | 2N^2 / [4(N^2+2N)], approaching 0.5 | 2N^2 / [8(N^2+2N)], approaching 0.25 |
| Matrix-matrix | N/6 | N/12 |

All entries are FLOP/byte. For example, at N=1024, ideal matrix-matrix
intensity is about 170.67 in float32 and 85.33 in float64. Matrix-vector
intensity is about 0.499 and 0.250 respectively.

## 4. Use the Roofline model

P <= min(P_peak, B_memory * I).

P is performance in GFLOP/s. P_peak is the matching compute ceiling.
B_memory is bandwidth in GB/s and I is FLOP/byte at that same memory level.
The bend is at I = P_peak / B_memory. Below this intensity, the bandwidth
ceiling is lower. Above it, the compute ceiling is lower. Actual performance
can be below both because of overhead, cache behavior and other limitations.

We have no independent hardware ceilings in the basic experiment, so we use
the equation and measured coordinates qualitatively. We cannot prove the
bottleneck just from these derived numbers. Never use estimated_bytes/time
as an independent measured bandwidth ceiling: it is calculated from the same
timing as GFLOP/s. Do not assume the CPU's full multicore peak applies to
our one-BLAS-thread experiment.

## 5. Expectations before measuring

1. Doubling N multiplies the work by about 4 for matrix-vector and 8 for
   matrix-matrix. Time can behave differently while performance is changing.
2. Matrix-vector has almost constant, low estimated intensity. Large cases
   are expected to depend strongly on memory supply.
3. Matrix-matrix can reuse its inputs much more and can reach higher GFLOP/s.
   It still performs more total work, so higher GFLOP/s does not mean less
   execution time than matrix-vector at the same N.
4. Float32 halves each array's bytes and doubles our estimated intensity.
   It can also use more SIMD lanes. Neither effect guarantees a twofold
   speedup for every size or machine.
5. With these small integer constants and sizes, output values are exactly
   representable. This is a performance comparison, not a useful accuracy
   study of round-off errors for general matrix data.

## 6. Sample wording to finish after the real runs

Replace every bracket with a measured value. If the observation is different,
write what actually happened instead.

"On [person]'s laptop, doubling N from [N1] to [N2] changed matrix-vector
time by [ratio]. The work increased by about four. The difference could be
related to [evidence-based explanation]."

"At N=[N], matrix-matrix achieved [value] GFLOP/s and matrix-vector achieved
[value]. This agrees/does not agree with the expected effect of data reuse.
Matrix-matrix still took [time] seconds because it did more work."

"For [operation] at N=[N], time64/time32 was [value]. Float32 was
[faster/slower/about the same]. A factor of two was [observed/not observed]."

"The largest timing spread was [value]. [Background work, power setting,
thermal behavior or another explanation] is a possible explanation, but we
did not directly measure that cause."

Sources: the class assignment, NumPy matmul documentation, threadpoolctl
documentation and https://docs.nersc.gov/tools/performance/roofline/.
