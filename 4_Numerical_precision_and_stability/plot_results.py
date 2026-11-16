import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import (
    FixedLocator, FuncFormatter, LogFormatterMathtext, LogLocator,
    MaxNLocator, NullFormatter, NullLocator,
)
import numpy as np


# Independent hardware limits (optional).
BANDWIDTH_GB_S = None
PEAK32_GFLOPS = None
PEAK64_GFLOPS = None

COLORS = {"matvec": "#205a83", "matmat": "#ad4166"}
LABELS = {"matvec": "Matrix-vector", "matmat": "Matrix-matrix"}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.axisbelow": True,
    "savefig.facecolor": "white",
    "pdf.fonttype": 42,
})


def size_axis(ax, sizes):
    ticks = sizes
    if len(sizes) > 7:
        indices = np.linspace(0, len(sizes) - 1, 7, dtype=int)
        ticks = [sizes[index] for index in indices]
    ax.set_xscale("log", base=2)
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, pos: str(int(value))))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xlim(min(sizes) / 1.16, max(sizes) * 1.16)
    ax.set_xlabel("Matrix size N")
    ax.tick_params(axis="x", pad=7)


def log_axis(ax, axis, values, number_labels=False):
    low, high = min(values) / 1.18, max(values) * 1.18
    powers = range(int(np.floor(np.log10(low))) - 1, int(np.ceil(np.log10(high))) + 1)
    candidates = [step * 10.0 ** power for power in powers for step in (1, 2, 5)]
    limit = (max(value for value in candidates if value <= low),
             min(value for value in candidates if value >= high))
    target = ax.xaxis if axis == "x" else ax.yaxis
    if axis == "x":
        ax.set_xscale("log")
        ax.set_xlim(10.0 ** np.floor(np.log10(low)), 10.0 ** np.ceil(np.log10(high)))
    else:
        ax.set_yscale("log")
        ax.set_ylim(limit)
    if number_labels:
        target.set_major_locator(LogLocator(base=10, subs=(1, 2, 5), numticks=12))
        target.set_major_formatter(FuncFormatter(lambda value, pos: f"{value:g}"))
    else:
        target.set_major_locator(LogLocator(base=10, numticks=10))
        target.set_major_formatter(LogFormatterMathtext(base=10, labelOnlyBase=True))
    target.set_minor_locator(LogLocator(base=10, subs=(2, 5), numticks=30))
    target.set_minor_formatter(NullFormatter())


def grid(ax):
    ax.grid(True, which="major", color="#dce2e7", linewidth=0.8)
    ax.tick_params(length=4)


def save_figure(fig, stem):
    fig.savefig(plot_folder / (stem + ".png"), dpi=240)
    fig.savefig(plot_folder / (stem + ".pdf"))
    plt.close(fig)


name = input("Result folder (e.g. mohammadjavad): ").strip().lower()
if not name or not name.replace("_", "").isalnum():
    raise SystemExit("Use letters, numbers and underscores only.")
folder = Path(__file__).resolve().parent / "results" / name
plot_folder = folder / "plots"

data = []
machines = []
for operation in ["matvec", "matmat"]:
    with open(folder / (operation + "_machine.json"), encoding="utf-8") as file:
        machine = json.load(file)
    if not machine["completed"]:
        raise SystemExit("A benchmark did not finish. Check its results first.")
    machines.append(machine)
    with open(folder / (operation + "_summary.csv"), newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            row["operation"] = operation
            data.append(row)

for setting in ["sizes_requested", "repeats", "requested_blas_threads", "numpy"]:
    if machines[0][setting] != machines[1][setting]:
        raise SystemExit("The benchmarks used different settings: " + setting)
for row in data:
    if row["correct"] != "True":
        raise SystemExit("A correctness check failed. Do not plot these results.")
    for key in ["N", "median_seconds", "min_seconds", "max_seconds",
                "gflops", "estimated_gb_s", "arithmetic_intensity"]:
        value = float(row[key])
        if not np.isfinite(value) or value <= 0:
            raise SystemExit("Invalid or non-positive value in " + key)
    if not float(row["min_seconds"]) <= float(row["median_seconds"]) <= float(row["max_seconds"]):
        raise SystemExit("The median time is outside the recorded timing range.")

groups = []
sizes = sorted(int(N) for N in machines[0]["sizes_requested"])
for operation in ["matvec", "matmat"]:
    for dtype in ["float32", "float64"]:
        rows = [row for row in data if row["operation"] == operation and row["dtype"] == dtype]
        rows.sort(key=lambda row: int(row["N"]))
        if [int(row["N"]) for row in rows] != sizes:
            raise SystemExit("Missing or duplicate sizes for " + operation + " " + dtype)
        groups.append((operation, dtype, rows))

limits = [BANDWIDTH_GB_S, PEAK32_GFLOPS, PEAK64_GFLOPS]
if any(value is not None for value in limits):
    if any(value is None for value in limits) or any(not np.isfinite(value) or value <= 0 for value in limits):
        raise SystemExit("Supply all three positive hardware limits, or leave all as None.")

plot_folder.mkdir(exist_ok=True)
fig_overview, axes = plt.subplots(2, 2, figsize=(14, 10.5))
fig_overview.subplots_adjust(left=0.085, right=0.975, bottom=0.085, top=0.83,
                             hspace=0.42, wspace=0.29)
panels = [
    (axes[0, 0], "N", "median_seconds", "Time per call (s)", "(a) Execution time"),
    (axes[0, 1], "N", "gflops", "Performance (GFLOP/s)", "(b) Computational performance"),
    (axes[1, 0], "N", "estimated_gb_s", "Estimated effective bandwidth (GB/s)", "(c) Estimated bytes / time"),
    (axes[1, 1], "arithmetic_intensity", "gflops", "Performance (GFLOP/s)", "(d) Roofline coordinates"),
]

for ax, x_key, y_key, y_label, title in panels:
    all_x, all_y = [], []
    for operation, dtype, rows in groups:
        xs = [float(row[x_key]) for row in rows]
        ys = [float(row[y_key]) for row in rows]
        all_x.extend(xs)
        all_y.extend(ys)
        style = "o-" if dtype == "float32" else "s--"
        ax.plot(xs, ys, style, color=COLORS[operation], linewidth=1.9,
                markersize=5.5, label=LABELS[operation] + " | " + dtype)
        if y_key == "median_seconds":
            lower = [float(row["min_seconds"]) for row in rows]
            upper = [float(row["max_seconds"]) for row in rows]
            ax.fill_between(xs, lower, upper, color=COLORS[operation], alpha=0.13, linewidth=0)
            all_y.extend(lower + upper)
    if x_key == "N":
        size_axis(ax, sizes)
    else:
        log_axis(ax, "x", all_x)
        ax.set_xlabel("Estimated arithmetic intensity (FLOP/byte)")
    if x_key == "N" and y_key == "gflops":
        ax.set_ylim(0, max(all_y) * 1.16)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=5, min_n_ticks=4))
    else:
        log_axis(ax, "y", all_y, number_labels=(x_key == "arithmetic_intensity"))
    ax.set_ylabel(y_label)
    ax.set_title(title, loc="left", pad=11)
    grid(ax)

if all(value is not None for value in limits):
    ax = axes[1, 1]
    intensities = np.geomspace(*ax.get_xlim(), 300)
    roof_values = [float(row["gflops"]) for row in data]
    for peak, label, color in [
        (PEAK32_GFLOPS, "FP32 supplied ceiling", "#737373"),
        (PEAK64_GFLOPS, "FP64 supplied ceiling", "#a6a6a6"),
    ]:
        roof = np.minimum(peak, BANDWIDTH_GB_S * intensities)
        roof_values.extend(roof)
        ax.plot(intensities, roof, ":", color=color, linewidth=1.5, label=label)
    log_axis(ax, "y", roof_values, number_labels=True)
    ax.legend(handles=ax.lines[-2:], loc="lower right", fontsize=9, frameon=False)

handles, labels = axes[0, 0].get_legend_handles_labels()
fig_overview.suptitle("NumPy benchmark results", y=0.976, fontsize=19)
fig_overview.text(0.5, 0.936, name + "  |  BLAS threads: " + str(machines[0]["requested_blas_threads"]),
                  ha="center", color="#4b5563", fontsize=12)
fig_overview.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.906),
                    ncol=4, frameon=False, fontsize=10.5, columnspacing=1.6)
save_figure(fig_overview, "overview")

fig_speedup, ax_speedup = plt.subplots(figsize=(9.5, 6.0))
fig_speedup.subplots_adjust(left=0.105, right=0.97, bottom=0.13, top=0.75)
all_ratios = []
with open(folder / "discussion_numbers.txt", "w", encoding="utf-8") as notes:
    notes.write("Values calculated from this folder only. Speedup = time64 / time32.\n")
    notes.write("Time scaling = time(N) / time(previous N); not always a doubling.\n\n")
    for operation in ["matvec", "matmat"]:
        times32 = {int(row["N"]): float(row["median_seconds"]) for row in data
                   if row["operation"] == operation and row["dtype"] == "float32"}
        times64 = {int(row["N"]): float(row["median_seconds"]) for row in data
                   if row["operation"] == operation and row["dtype"] == "float64"}
        ratios = [times64[N] / times32[N] for N in sizes]
        all_ratios.extend(ratios)
        notes.write(operation + "\n")
        for N, ratio in zip(sizes, ratios):
            notes.write("N=" + str(N) + ": float32 speedup=" + str(round(ratio, 3)) + "\n")
        marker = "o" if operation == "matvec" else "s"
        ax_speedup.plot(sizes, ratios, marker + "-", color=COLORS[operation],
                        linewidth=2.1, markersize=6, label=LABELS[operation])
    notes.write("\nAdjacent-size time ratios\n")
    for operation, dtype, rows in groups:
        for index in range(1, len(rows)):
            previous, current = rows[index - 1], rows[index]
            ratio = float(current["median_seconds"]) / float(previous["median_seconds"])
            notes.write(operation + " " + dtype + " " + previous["N"] + " -> " + current["N"]
                        + ": " + str(round(ratio, 3)) + "\n")

ax_speedup.axhline(1.0, color="#707780", linestyle="--", linewidth=1.3, label="Equal time (1x)")
size_axis(ax_speedup, sizes)
speedup_locator = MaxNLocator(nbins=6, steps=[1, 2, 2.5, 5, 10])
speedup_ticks = speedup_locator.tick_values(0, max(1.0, max(all_ratios)) * 1.15)
ax_speedup.set_ylim(0, speedup_ticks[-1])
ax_speedup.yaxis.set_major_locator(FixedLocator(speedup_ticks))
ax_speedup.set_ylabel("Float32 speedup (time64 / time32)")
grid(ax_speedup)
fig_speedup.suptitle("Float32 speedup", y=0.97, fontsize=19)
fig_speedup.text(0.5, 0.897, name,
                 ha="center", fontsize=11, color="#4b5563")
fig_speedup.legend(*ax_speedup.get_legend_handles_labels(), loc="upper center",
                   bbox_to_anchor=(0.5, 0.85), ncol=3, frameon=False, fontsize=10.5)
save_figure(fig_speedup, "precision_speedup")

print("Saved figures in", plot_folder)
print("Saved discussion_numbers.txt in", folder)
