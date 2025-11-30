# Duplicate Finding Tool Design

## 1. Problem Statement
Large codebases and documentation repositories accumulate redundant or near-duplicate files (forked copies, outdated variants, copied utilities). Detecting and consolidating them reduces maintenance cost, improves search relevance, and lowers review overhead.

## 2. Scope (MVP)
- Target textual files (source code, Markdown, plain text).
- Detect exact and near-duplicate pairs above similarity threshold.
- Provide CLI with JSON and table output.
- Support parallel signature computation.

Out of scope initially: binary similarity, semantic similarity across refactors, language-aware AST transforms.

## 3. Data Model
- FileSignature: path, hashed shingle set, token count.
- DuplicatePair: (similarity, file_a, file_b) ephemeral, not stored.

## 4. Processing Pipeline
1. Enumerate files by extension filter.
2. Read & normalize (collapse whitespace, ignore encoding errors).
3. Tokenize (regex word tokens `[A-Za-z0-9_]+`).
4. Build k-token shingles; hash (MD5) for stable integer representation.
5. Compute Jaccard similarity on hashed sets for all pairings.
6. Emit pairs above threshold sorted by similarity desc.

## 5. Algorithmic Considerations
- Complexity: O(N^2) pairwise comparisons; acceptable for smaller N (<10k). Future: locality-sensitive hashing or banding to prune.
- Memory: hashed shingles set per file; typical size proportional to token_count - k.
- Parallelism: Only signature (I/O + tokenization + hashing) parallelized; pairwise similarity remains serial for deterministic ordering. Later improvement: block-wise parallel comparison with concurrency control.

## 6. Configuration
- `k`: affects granularity; smaller increases sensitivity but risk false positives.
- `threshold`: user tolerance for duplication.
- `--workers`: process count for signature stage.

## 7. Error Handling
- Unreadable files skipped silently (avoid noisy output). Potential improvement: verbose mode collecting skipped file list.

## 8. Extensions (Future)
- Ignore Regions: pattern-based removal (license headers, generated code banners).
- Tokenizers: language-aware (strip comments, normalize identifiers) to enhance semantic detection.
- Prefilter: MinHash signatures + LSH buckets to reduce comparisons.
- Semantic: embedding similarity (code embeddings, sentence transformers) for refactored duplicates.
- Incremental: maintain persistent signature index; update only changed files.

## 9. Performance Strategy
- Benchmark harness generates controlled duplicate groups for throughput tracking.
- Metrics: files/sec, pair computation time, memory footprint.
- Threshold for switching to parallel pairwise stage to be determined empirically.

## 10. Risks
- High false positives with very small `k` or low `threshold`.
- Large memory usage for huge shingles sets in long files.
- Multiprocessing overhead > benefit on small datasets.

## 11. Acceptance (MVP)
- CLI returns expected duplicates on synthetic dataset.
- Parallel mode produces identical results to serial.
- Benchmarks show >1.5x speedup on sufficiently large dataset with workers >1.

## 12. Open Questions
- When to introduce MinHash vs full set Jaccard? (size threshold)
- Should we stream file reading for huge files? (line-by-line shingling)
- Provide output grouping by duplicate clusters vs pair list?
