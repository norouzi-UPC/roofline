import csv
import json
import os
import platform
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from threadpoolctl import threadpool_info, threadpool_limits


# Use the same settings in both benchmark files.
SIZES = [128, 256, 512, 1024, 2048, 4096]
REPEATS = 5
MIN_SECONDS = 0.10
MAX_CALLS = 1048576
THREADS = 1

name = input("Result folder (e.g. mohammadjavad): ").strip().lower()
if not name or not name.replace("_", "").isalnum():
    raise SystemExit("Use letters, numbers and underscores only.")

folder = Path(__file__).resolve().parent / "results" / name
folder.mkdir(parents=True, exist_ok=True)
summary_path = folder / "matvec_summary.csv"
raw_path = folder / "matvec_raw.csv"
machine_path = folder / "matvec_machine.json"
if summary_path.exists() or raw_path.exists() or machine_path.exists():
    raise SystemExit("Results already exist. Run again with a new folder name.")

# This limits NumPy numerical library to one thread.
thread_limit = threadpool_limits(limits=THREADS, user_api="blas")
libraries = threadpool_info()
print("Detected numerical libraries:", libraries)
blas_libraries = []
for library in libraries:
    if library.get("user_api") == "blas":
        blas_libraries.append(library)
if not blas_libraries:
    print("Thread count could not be verified. Mention this in your notes.")
for library in blas_libraries:
    if library.get("num_threads") != THREADS:
        raise SystemExit("Thread limit was not applied. Ask the group for help.")

machine = {
    "folder": name,
    "operation": "matvec",
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "system": platform.platform(),
    "cpu_reported_by_python": platform.processor(),
    "logical_cpus_reported_by_python": os.cpu_count(),
    "python": sys.version,
    "numpy": np.__version__,
    "requested_blas_threads": THREADS,
    "detected_libraries": libraries,
    "sizes_requested": SIZES,
    "repeats": REPEATS,
    "minimum_block_seconds": MIN_SECONDS,
    "maximum_calls_per_block": MAX_CALLS,
    "completed": False,
}
with open(machine_path, "w", encoding="utf-8") as file:
    json.dump(machine, file, indent=2)

with open(summary_path, "w", newline="", encoding="utf-8") as summary_file, open(
    raw_path, "w", newline="", encoding="utf-8"
) as raw_file:
    summary = csv.writer(summary_file)
    raw = csv.writer(raw_file)
    summary.writerow([
        "dtype", "N", "calls_per_repeat", "repeats", "median_seconds",
        "min_seconds", "max_seconds", "relative_spread", "flops",
        "estimated_bytes", "arithmetic_intensity", "gflops",
        "estimated_gb_s", "correct",
    ])
    raw.writerow(["dtype", "N", "repeat", "calls", "block_seconds", "seconds_per_call"])

    for dtype in [np.float32, np.float64]:
        for N in SIZES:
            # Allocation, initialization and checking are outside the timer.
            A = np.full((N, N), 1.0, dtype=dtype)
            x = np.full(N, 3.0, dtype=dtype)
            y = np.empty(N, dtype=dtype)
            for warmup in range(3):
                np.matmul(A, x, out=y)
            correct = bool(np.allclose(y, 3.0 * N))
            if not correct:
                raise SystemExit("Wrong result. Stop and check the code.")

            # Time enough calls together to avoid timing a very tiny interval.
            calls = 1
            while True:
                start = time.perf_counter()
                for call in range(calls):
                    np.matmul(A, x, out=y)
                elapsed = time.perf_counter() - start
                if elapsed >= MIN_SECONDS or calls >= MAX_CALLS:
                    break
                calls = calls * 2

            times = []
            for repeat in range(REPEATS):
                start = time.perf_counter()
                for call in range(calls):
                    np.matmul(A, x, out=y)
                elapsed = time.perf_counter() - start
                seconds = elapsed / calls
                times.append(seconds)
                raw.writerow([dtype.__name__, N, repeat + 1, calls, elapsed, seconds])

            seconds = statistics.median(times)
            flops = 2 * N * N
            estimated_bytes = np.dtype(dtype).itemsize * (N * N + 2 * N)
            intensity = flops / estimated_bytes
            gflops = flops / seconds / 1e9
            bandwidth = estimated_bytes / seconds / 1e9
            spread = (max(times) - min(times)) / seconds
            correct = bool(np.allclose(y, 3.0 * N))
            if not correct:
                raise SystemExit("Wrong result after timing. Stop and check the code.")

            summary.writerow([
                dtype.__name__, N, calls, REPEATS, seconds, min(times),
                max(times), spread, flops, estimated_bytes, intensity,
                gflops, bandwidth, correct,
            ])
            summary_file.flush()
            raw_file.flush()
            print(dtype.__name__, "N =", N, "seconds =", round(seconds, 7),
                  "GFLOP/s =", round(gflops, 3), "correct =", correct)
            del A, x, y

machine["completed"] = True
machine["finished_utc"] = datetime.now(timezone.utc).isoformat()
with open(machine_path, "w", encoding="utf-8") as file:
    json.dump(machine, file, indent=2)
print("Saved results in", folder)
