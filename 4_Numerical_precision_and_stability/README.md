# Exploring the Roofline Model

Team: MohammadJavad Norouzi, Aland Arif, Hamed Zahraei Ramazani and Wenyuan Huang.

We compare NumPy matrix-vector and matrix-matrix multiplication using
float32 and float64, with matrix sizes from 128 to 4096.

## Setup

Install Python. Open a terminal in the repository's main folder and run:

```powershell
cd 4_Numerical_precision_and_stability
python -m pip install -r requirements.txt
```

## Run the experiments

Run these commands one at a time:

```powershell
python benchmark_matvec.py
python benchmark_matmat.py
python plot_results.py
```

Each script asks for a result-folder name. Use the same name for all
three scripts, for example `test_run1`.

For another benchmark run, choose a new folder name. The benchmark
scripts do not overwrite existing measurements.

Before benchmarking, connect the charger, turn off Energy saver and
close heavy applications.

The scripts request one BLAS thread, perform three warm-up calls and
measure five timing blocks per case. They report the median time per
call. Allocation and initialization are outside the timed region.

## Saved results

Each run folder contains raw timings, summary CSV files and machine
information in JSON files.

The plotting script creates `overview` and `precision_speedup` figures
in PNG and PDF formats under `results/<folder>/plots`. It also creates
`discussion_numbers.txt`.

The selected runs include observations and installed-package lists.

| Member | Selected result folder |
|---|---|
| MohammadJavad | `mohammadjavad_run2` |
| Aland | `aland` |
| Hamed | `hamed` |
| Wenyuan | `wenyuan8` |

## Recreate plots from saved measurements

Run:

```powershell
python plot_results.py
```

When prompted, enter one of the selected folder names above.
The benchmarks do not need to be repeated to regenerate the plots.

New timing measurements will vary between computers and runs.

## Report and contributions

Report files are in `report/`.
Individual contribution notes are in `docs/contributions/`.
