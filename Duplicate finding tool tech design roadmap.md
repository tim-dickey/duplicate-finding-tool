# Tech Design Roadmap

## Phase 1: MVP (Complete)
- Shingling + Jaccard similarity.
- CLI with threshold, k, extensions, JSON output.
- Parallel signature computation.
- Synthetic benchmark harness.

## Phase 2: Scale-Up
- Add MinHash signature (e.g., 64 hash permutations) to reduce comparison candidates.
- LSH banding to prune pairs before full Jaccard.
- Parallel pairwise comparison (block partitioning).
- Memory optimization (shared immutable token arrays, optional disk spill for large corpora).

## Phase 3: Quality & UX
- Ignore pattern file (globs + regex + code region markers).
- Verbose mode: skipped files, stats summary.
- Cluster output grouping duplicates into sets.
- HTML/JSON report with summary metrics and cluster visualization.

## Phase 4: Language-Aware Layer
- Pluggable tokenizers: Python (strip comments, normalize literals), Markdown (strip code fences optionally), JSON (structural tokens).
- Identifier normalization (case-fold, shorten numeric literals).

## Phase 5: Semantic Expansion
- Embedding model integration for refactored code similarity.
- Hybrid scoring: lexical Jaccard + embedding cosine.
- Confidence calibration (precision / recall evaluation on labeled corpus).

## Phase 6: Operationalization
- Incremental index (track mtime, rescan changed files only).
- Pre-commit hook: reject new near-duplicate additions.
- CI drift detector: report newly introduced duplicates.

## Metrics & Targets
- Throughput: 5k medium files < 30s on 8 cores (post Phase 2).
- Memory: < 1GB for 5k files (shingle + MinHash sets).
- Precision: > 0.95 on labeled duplicate corpus (Phase 5).

## Risk Mitigation
- Start with feature flags for experimental tokenizers.
- Fallback to serial path if multiprocessing errors.
- Provide safeguards for extremely large files (size cap, stream mode).

## Decision Log Candidates
- Shingle size default (5) vs 7 tradeoff.
- Hash function (MD5 vs xxhash dependency).
- MinHash permutation count.

## Dependency Strategy
- Keep core zero-extra (stdlib + click + tqdm) for MVP.
- Optional extras for advanced features (fast hash libraries, embedding models).
