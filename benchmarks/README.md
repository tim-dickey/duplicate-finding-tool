# Benchmarks

Synthetic workload generator to measure scan throughput and duplicate detection.

## Run
```
python benchmarks/run_benchmarks.py --files 500 --dup-groups 50 --group-size 5 --workers 4 --verbose
```

## Metrics
- Files: number processed
- Elapsed: wall-clock seconds
- Files/sec: throughput
- Duplicate pairs: matches above threshold

## Notes
- Parallel speedup depends on CPU cores and file count.
- For small datasets (<300 files) overhead may reduce benefit.
- Adjust shingle size `--k` for token granularity vs sensitivity.
