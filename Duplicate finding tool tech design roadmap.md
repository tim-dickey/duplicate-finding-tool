# Tech Design Roadmap (Placeholder)

Replace with your original roadmap content.

## Phases
1. MVP: Single-thread scan, Jaccard on shingles.
2. Scale: Signature prefilter + multiprocessing.
3. UX: Progress indicators, JSON output, ignore patterns.
4. Advanced: Pluggable analyzers, semantic similarity.
5. Integration: Pre-commit hook, CI drift detector.

## Metrics
- Throughput (files/sec)
- Memory usage
- False positive / false negative rates (later with benchmarks)

## Open Questions
- Shingle size adaptation?
- Language-specific filters?
