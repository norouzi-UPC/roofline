# Exploring the Roofline Model

**Status: DRAFT. Laptop results and the final discussion are TO COMPLETE.**

Team: MohammadJavad Norouzi, Aland Arif, Hamed Zahraei Ramazani, Wenyuan Huang.

Course: Scientific Programming and High Performance Computing, UPC.

Repository: TO COMPLETE.

## 1. Aim

We compare matrix-vector multiplication, y = Ax, and matrix-matrix
multiplication, C = AB. We use NumPy with float32 and float64. We want to
understand how the amount of work and data reuse affect performance. Each
member runs the same experiment on their own laptop.

## 2. Method

We create A with ones, B with twos and x with threes. We allocate the output
before timing and use np.matmul with its out argument. The arrays use the
selected precision throughout. For these inputs, each y entry should equal
3N and each C entry should equal 2N. We check the complete output before and
after the measurements.

The default sizes are 128, 256, 512, 1024, 2048 and 4096. Each case has
three warm-up calls. We double the calls per block until a block lasts at
least 0.10 seconds, unless the 1,048,576-call cap is reached. We then measure
five blocks, divide each duration by its call count and use the median time
per call. We retain all five times and their minimum and maximum. The Python
loop adds some overhead, which matters most for the smallest sizes.

Allocation, initialization, correctness checks and file output are outside
the measured region. NumPy/BLAS internal workspace may still be used. We
reuse the same arrays between warm-up and timed calls; we do not flush the
CPU caches. We request one BLAS thread and record detected thread counts.
This experiment does not measure the full multicore peak of each laptop.

TO COMPLETE: confirm that these settings describe the final selected runs.
List any reductions, interruptions, unverified threads or reruns.

| Member | CPU and RAM | OS | Python / NumPy / BLAS | Power conditions | Selected run folder |
|---|---|---|---|---|---|
| MohammadJavad | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE | mohammadjavad |
| Aland | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE | aland |
| Hamed | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE | hamed |
| Wenyuan | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE | wenyuan |

## 3. Theoretical estimates

A dot product of length N uses N multiplications and N-1 additions. Therefore
matrix-vector multiplication uses N(2N-1) FLOPs and matrix-matrix multiplication
uses N^2(2N-1). We use the common large-N approximations 2N^2 and 2N^3 in
the performance calculations. A multiply and an add count as two FLOPs,
including when implemented as a fused instruction.

Let s be 4 bytes for float32 and 8 bytes for float64. With ideal reuse,
matrix-vector multiplication reads A and x once and writes y once. This gives
Q_mv = s(N^2+2N). Matrix-matrix multiplication reads A and B once and writes C
once, giving Q_mm = 3sN^2. We do not read the old output in this model.

| Operation | Estimated intensity, float32 | Estimated intensity, float64 |
|---|---|---|
| Matrix-vector | 2N^2/[4(N^2+2N)], approaching 0.5 | 2N^2/[8(N^2+2N)], approaching 0.25 |
| Matrix-matrix | N/6 | N/12 |

The units are FLOP/byte. These ideal estimates omit write-allocate traffic,
packing and other transfers. Finite caches can force extra input reloads,
especially for large matrix-matrix multiplication. Small warmed cases may
reuse data already in cache. Estimated bytes are not measured RAM traffic.

For median time t, performance is F/(t*10^9) GFLOP/s and estimated effective
bandwidth is Q/(t*10^9) GB/s. GB uses 10^9 bytes. Because both use the same
time, estimated bandwidth is also performance divided by estimated intensity;
it is not an independent bandwidth measurement.

## 4. Roofline model

We use P <= min(P_peak, B_memory * I), with matching memory-level bytes and
bandwidth. The ridge is at I = P_peak/B_memory. Low intensity makes memory
supply a likely limit. Higher intensity can make compute throughput the
lower ceiling, provided the implementation reuses data well.

We do not independently measure the hardware ceilings in this experiment.
Our default Roofline-coordinate plots show measured GFLOP/s versus estimated
intensity. They have no claimed hardware-limit lines. The interpretation is
qualitative, and neither bottleneck is proven just from these points.

TO COMPLETE only if independently sourced ceilings were added: identify their
sources, memory level, precision and matching thread configuration. Otherwise
keep the preceding explanation and remove this instruction.

## 5. Experimental results

Insert each person's overview and speedup plots from their selected result
folder. The overview includes time, GFLOP/s, estimated GB/s and Roofline
coordinates. The time shading is the range across the five blocks.

TO COMPLETE: choose the largest common N across the four selected runs and
provide numeric examples. Use the original CSV precision when calculating
ratios; round only when writing the final text.

| Member | Common N | MV time64/time32 | MM time64/time32 | MV FP64 GFLOP/s | MM FP64 GFLOP/s |
|---|---:|---:|---:|---:|---:|
| MohammadJavad | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE |
| Aland | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE |
| Hamed | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE |
| Wenyuan | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE |

A value above 1 in either time64/time32 column means float32 was faster.

## 6. Discussion questions

### 6.1 How does execution time scale with N?

The work scales as N^2 for matrix-vector and N^3 for matrix-matrix, so
doubling N increases work by about 4 and 8 respectively. This is the expected
time scaling only when the achieved performance stays approximately constant.

TO COMPLETE: give actual time ratios for both operations and both precisions.
Discuss small sizes, cache transitions and any change in achieved GFLOP/s.

### 6.2 How do the two operations compare?

Matrix-vector has a low, almost constant ideal intensity. Matrix-matrix has
an ideal intensity that grows with N because inputs can contribute to many
output entries. Optimized BLAS uses blocking to improve this reuse.

TO COMPLETE: compare measured GFLOP/s at the same N, and explain the
difference. Also compare execution times: higher GFLOP/s does not imply the
operation takes less time when its total work is much larger.

### 6.3 What changes with float32?

Float32 halves the array bytes and doubles our ideal intensity. It may also
allow greater vector arithmetic throughput. A twofold speedup is a possible
expectation in some regimes, not a guaranteed result.

TO COMPLETE: use time64/time32 for both operations at matching N. Report any
case where float32 was not faster. Mention library, overhead or cache effects
as possible explanations when the measurements support them.

### 6.4 Were there unexpected results?

TO COMPLETE: identify unusual points and timing spreads, or say that no
substantial irregularity was found. Possible explanations include background
tasks, clock or power behavior, cache capacity, BLAS choices and timing
overhead. Distinguish observed evidence from untested explanations. Do not
claim to have measured thermal throttling without evidence.

Keep each laptop's results separate. Hardware and software vary together,
so the comparison does not isolate one hardware feature by itself.

## 7. Conclusion

TO COMPLETE: write a short conclusion based on the real results. State the
main operation difference, the observed effect of float32 and the limitations
of our estimated-byte Roofline interpretation. Do not copy expectations as
if they were measurements.

## 8. Contributions

TO COMPLETE from the four personal contribution files, with PR links. Include
source review/changes, the four runs, plot checking and report work accurately.

## References

- Course handout: *Homework: Exploring the Roofline Model*.
- NumPy matmul: https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
- threadpoolctl: https://github.com/joblib/threadpoolctl
- NERSC Roofline model: https://docs.nersc.gov/tools/performance/roofline/
