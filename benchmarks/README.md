# Benchmarks & Profiling

## Synthetic Benchmarks
Generate synthetic corpus with controlled duplicate groups.
```
python benchmarks/run_benchmarks.py --files 500 --dup-groups 50 --group-size 5 --workers 4 --verbose
```
Metrics: Files, Elapsed, Files/sec, Duplicate pairs.

## Profiling Real Directory
Profile serial vs parallel performance on an actual codebase directory.
```
python benchmarks/run_profile.py ./your_dir --ext .py,.md --parallel-workers 6 --repeat 3
```
Artifacts: `benchmarks/last_profile.md`, `benchmarks/last_profile.json`.

Example speedup line reports serial/parallel ratio.

## Tips
- Increase `--repeat` to smooth variance.
- Adjust `--parallel-workers` near CPU count minus 1.
- For small N (<300 files) serial may be faster due to overhead.

## Next Steps
Future profiling will include MinHash prefilter and pairwise parallel comparison metrics once implemented.
