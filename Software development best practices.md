# Software Development Best Practices

## Coding Principles
- Consistency: follow established naming and file organization.
- Single Responsibility: keep functions narrowly focused.
- Determinism: tests and benchmarks produce repeatable outputs; control randomness with seeds when comparing runs.
- Progressive Enhancement: add complexity only after profiling bottlenecks.

## Project-Specific Guidelines
- Benchmark Before Optimizing: record baseline files/sec before major refactors.
- Configuration Over Forking: prefer flags (`--k`, `--threshold`, `--workers`) to code changes for tuning.
- Error Silence Policy: unreadable files skipped quietly; add verbose mode instead of raising.
- Input Size Awareness: document performance thresholds (e.g., when parallelism benefits > X files).

## Testing
- Unit tests for core similarity logic (exact + near duplicates).
- Equivalence tests: parallel vs serial produce identical signatures.
- Add regression test when fixing false positive/negative cases.

## Performance
- Avoid premature caching; profile first.
- Use multiprocessing only for CPU-bound phases (signature build) not for trivial I/O counts.
- Keep memory proportional; watch large token lists.

## Documentation
- README: quick start + performance notes.
- Design doc: rationale for algorithm choices and trade-offs.
- Roadmap: phased evolution with clear exit criteria.

## Versioning & Changes
- Increment minor version for new features (parallel scan).
- Patch version for bug fixes only.
- Document CLI changes clearly; avoid breaking defaults.

## Contribution Review Checklist
- Scope: single feature or fix.
- Tests: cover new logic, pass existing suite.
- Benchmarks (if perf-related): include delta metrics.
- Docs: updated when flags or behavior change.

## Quality Assurance
- Run `pytest -q` before commits.
- Optionally run benchmark for regression detection.
- Manual smoke test of CLI with small sample directory.

## Future Enhancements
- Add structured logging for debug mode.
- Provide reproducible benchmark dataset with fixed seed.
- Integrate static analysis (mypy) once types expanded.
