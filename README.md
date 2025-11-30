# Duplicate Finding Tool

Identify exact and near-duplicate files (text / source) within a directory tree.

## Features
- Shingling (k-token) with configurable size
- Hashed shingles + Jaccard similarity
- Parallel signature scan (`--workers`) for larger corpora
- MinHash + LSH prefilter (`--prefilter`) to prune candidate pairs (scales better)
- Cluster output mode (`--clusters`) groups interconnected duplicates
- CLI JSON or table output; schema versioned and documented
- Comprehensive test framework: unit, integration, property, performance tests
- CI via GitHub Actions (multi-version Python)
- Extensible: plug in tokenizers, ignore patterns (planned), semantic strategies

## Installation
```
pip install -e .[dev]
```
Requires Python >=3.9.

## CLI Usage
Basic scan:
```
duplicate-finder scan ./repo --threshold 0.85 --ext .py,.md,.txt --k 5
```
Parallel scan (6 workers):
```
duplicate-finder scan ./repo --workers 6
```
MinHash+LSH prefilter (recommended for >1k files):
```
duplicate-finder scan ./big --prefilter --minhash-perms 64 --lsh-bands 16
```
Cluster output (table):
```
duplicate-finder scan ./repo --clusters
```
Cluster JSON:
```
duplicate-finder scan ./repo --clusters --json
```

## Testing Framework
Run full suite:
```
pytest
```
Run only integration tests:
```
pytest tests/integration
```
Skip slow tests:
```
pytest -m "not slow"
```
Run slow performance tests:
```
pytest -m slow -v
```
Run property-based tests (Hypothesis):
```
pytest -m property
```

## CI/CD
GitHub Actions runs tests on Python 3.9-3.12 for every push/PR. Slow tests run only on main branch pushes.

## JSON Output Schema
See [`docs/json-schema.md`](docs/json-schema.md) for complete schema documentation and versioning policy.

Validate output with [`schema/duplicates.schema.json`](schema/duplicates.schema.json) (JSON Schema draft-07).

## Similarity Approach
1. Normalize whitespace.
2. Tokenize via regex `[A-Za-z0-9_]+`.
3. Build k-token shingles; hash with MD5.
4. Optional MinHash signature + LSH banding to pick candidate pairs.
5. Jaccard similarity on hashed shingle sets for scoring.

## Prefilter Notes
- `--prefilter` builds MinHash signatures (`--minhash-perms`) and buckets them into bands (`--lsh-bands`).
- Reduces pairwise comparison count; identical results retained for high probability settings.
- For small datasets (<50 files) prefilter automatically skipped internally.

## Clustering
Duplicate pairs are converted into connected components. Representative file chosen lexicographically; cluster size & max intra-pair similarity reported.

## Output
- Pair mode: similarity, file paths, token counts.
- Cluster mode: cluster id, size, representative, max similarity.
- JSON includes `schema_version` for downstream stability.

## Benchmarks & Profiling
Synthetic generation:
```
python benchmarks/run_benchmarks.py --files 800 --dup-groups 80 --group-size 5 --workers 6 --verbose
```
Profiling (serial vs parallel vs prefilter, with memory):
```
python benchmarks/run_profile.py ./repo --parallel-workers 6 --repeat 3
```
Artifacts written: `benchmarks/last_profile.md`, `benchmarks/last_profile.json`.

## Repository Structure
```
src/duplicate_finder/
  __init__.py
  core.py
  minhash.py
  cluster.py
  index.py
  cli.py
benchmarks/
  run_benchmarks.py
  run_profile.py
  README.md
tests/
  conftest.py
  unit/
  integration/
  performance/
  test_*.py
docs/
  json-schema.md
schema/
  duplicates.schema.json
.github/workflows/
  ci.yml
LICENSE
```

## Roadmap (Excerpt)
- Ignore patterns / region filtering
- Parallel pairwise comparison
- MinHash parameter tuning
- Semantic duplicate detection (embeddings)

## Contributing
Open issues focused on a single feature/performance improvement. Include benchmark deltas when relevant. PRs run full test suite via CI.

## License
MIT License - see [LICENSE](LICENSE) file for details.
