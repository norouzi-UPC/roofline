# Wenyuan Huang

## Work actually completed

- Source files I reviewed or changed: `report/THEORY.md`,
  `report/REPORT_TEMPLATE.md`, `report/report_template.tex`.
- My laptop result-folder name: `wenyuan8`
- I ran `benchmark_matvec.py`, `benchmark_matmat.py` and `plot_results.py`
  on my laptop with one BLAS thread, checked the summary CSV values and
  checked the generated plots.
- My observations or analysis: I selected `results/wenyuan8` from my runs.
  All 24 correctness checks passed, and both machine JSON files report
  `completed: true`. At N = 4096, matrix-vector reached 21.112 GFLOP/s in
  float32 and 8.875 GFLOP/s in float64; matrix-matrix reached 127.916 and
  57.450 GFLOP/s. I wrote `results/wenyuan8/observations.md`,
  `results/wenyuan8/packages.txt`, and the plots from that run.
- Source PR link: https://github.com/norouzi-UPC/roofline/pull/9
- Results PR link: https://github.com/norouzi-UPC/roofline/pull/8
- PR(s) I reviewed and what I checked: No formal PR review submitted yet.
- Report work: Updated the selected run folders in `REPORT_TEMPLATE.md` and
  the two `\runplots` entries in `report_template.tex`: `mohammadjavad_run2`
  for MohammadJavad and `wenyuan8` for me. Added the theory and report
  structure that the final report will use.
