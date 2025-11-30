import argparse
import json
import os
import platform
import statistics
import time
from datetime import datetime
from typing import Dict, Any
import resource

try:
    import psutil  # optional
except ImportError:  # pragma: no cover
    psutil = None

from duplicate_finder.core import DuplicateFinder


def _rss_mb() -> float:
    if psutil:
        return psutil.Process().memory_info().rss / (1024 * 1024)
    # Fallback: ru_maxrss is kilobytes on Linux
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def profile_run(path: str, extensions, k: int, threshold: float, workers: int, prefilter: bool) -> Dict[str, Any]:
    finder = DuplicateFinder(k=k, threshold=threshold)
    rss_start = _rss_mb()
    start = time.perf_counter()
    sig_start = time.perf_counter()
    sigs = finder.scan(path, extensions, workers=workers)
    sig_elapsed = time.perf_counter() - sig_start
    pairs_start = time.perf_counter()
    pairs = finder.find_duplicates(sigs, prefilter=prefilter)
    pairs_elapsed = time.perf_counter() - pairs_start
    total_elapsed = time.perf_counter() - start
    rss_end = _rss_mb()
    return {
        "files": len(sigs),
        "duplicate_pairs": len(pairs),
        "signature_time": sig_elapsed,
        "comparison_time": pairs_elapsed,
        "total_time": total_elapsed,
        "files_per_sec": (len(sigs) / total_elapsed) if total_elapsed else 0.0,
        "workers": workers,
        "prefilter": prefilter,
        "rss_start_mb": rss_start,
        "rss_end_mb": rss_end,
        "rss_diff_mb": rss_end - rss_start,
    }


def write_artifacts(markdown: str, json_data: Dict[str, Any], out_dir: str):
    md_path = os.path.join(out_dir, "last_profile.md")
    json_path = os.path.join(out_dir, "last_profile.json")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    return md_path, json_path


def format_markdown(results_serial, results_parallel, meta, results_prefilter):
    def fmt(r):
        return (
            f"Files: {r['files']} | Pairs: {r['duplicate_pairs']} | Total: {r['total_time']:.3f}s | "
            f"Sig: {r['signature_time']:.3f}s | Comp: {r['comparison_time']:.3f}s | Files/sec: {r['files_per_sec']:.1f} | "
            f"Workers: {r['workers']} | Prefilter: {r['prefilter']} | RSSΔ: {r['rss_diff_mb']:.2f}MB"
        )
    lines = [
        f"# Profiling Report", "", f"Date: {meta['date']}", f"Python: {meta['python']}", f"Platform: {meta['platform']}", f"CPU Count: {meta['cpus']}", "",
        "## Parameters", f"Path: {meta['path']}", f"Extensions: {', '.join(meta['extensions'])}", f"k: {meta['k']}", f"Threshold: {meta['threshold']}", f"Parallel Workers Tested: {meta['parallel_workers']}", "",
        "## Results", "### Serial", fmt(results_serial), "", "### Parallel", fmt(results_parallel), "", "### Prefilter (Parallel Signature, MinHash+LSH)", fmt(results_prefilter), "",
    ]
    speedup = (results_serial['total_time'] / results_parallel['total_time']) if results_parallel['total_time'] else 0
    prefilter_speedup = (results_serial['total_time'] / results_prefilter['total_time']) if results_prefilter['total_time'] else 0
    lines.append(f"Speedup (serial/parallel): {speedup:.2f}x")
    lines.append(f"Speedup (serial/prefilter): {prefilter_speedup:.2f}x")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Profile duplicate finder performance")
    parser.add_argument("path", type=str, help="Directory path to scan")
    parser.add_argument("--ext", type=str, default=".py,.md,.txt", help="Comma-separated extensions")
    parser.add_argument("--k", type=int, default=5, help="Shingle size")
    parser.add_argument("--threshold", type=float, default=0.85, help="Similarity threshold")
    parser.add_argument("--parallel-workers", type=int, default=4, help="Workers for parallel test run")
    parser.add_argument("--serial-workers", type=int, default=0, help="Workers for serial test (0 or 1)")
    parser.add_argument("--repeat", type=int, default=1, help="Repeat runs to average timings")
    parser.add_argument("--out-dir", type=str, default="benchmarks", help="Output directory for artifacts")
    args = parser.parse_args()

    extensions = [e.strip() for e in args.ext.split(',') if e.strip()]

    serial_runs = []
    parallel_runs = []
    prefilter_runs = []
    for _ in range(args.repeat):
        serial_runs.append(profile_run(args.path, extensions, args.k, args.threshold, args.serial_workers, prefilter=False))
        parallel_runs.append(profile_run(args.path, extensions, args.k, args.threshold, args.parallel_workers, prefilter=False))
        prefilter_runs.append(profile_run(args.path, extensions, args.k, args.threshold, args.parallel_workers, prefilter=True))

    def aggregate(runs):
        agg = {}
        keys = runs[0].keys() if runs else []
        for k in keys:
            if isinstance(runs[0][k], (int, float)):
                values = [r[k] for r in runs]
                agg[k] = statistics.mean(values)
            else:
                agg[k] = runs[0][k]
        return agg

    results_serial = aggregate(serial_runs)
    results_parallel = aggregate(parallel_runs)
    results_prefilter = aggregate(prefilter_runs)

    meta = {
        "date": datetime.utcnow().isoformat(timespec='seconds') + 'Z',
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpus": os.cpu_count(),
        "path": args.path,
        "extensions": extensions,
        "k": args.k,
        "threshold": args.threshold,
        "parallel_workers": args.parallel_workers,
    }

    markdown = format_markdown(results_serial, results_parallel, meta, results_prefilter)
    combined = {"meta": meta, "serial": results_serial, "parallel": results_parallel, "prefilter": results_prefilter}

    os.makedirs(args.out_dir, exist_ok=True)
    md_path, json_path = write_artifacts(markdown, combined, args.out_dir)
    print(f"Profile written: {md_path}, {json_path}")
    print("\n" + markdown)

if __name__ == "__main__":
    main()
