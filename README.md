# Duplicate Finding Tool

Identify exact and near-duplicate files (text / source) within a directory tree.

## Features
- Shingling (k-token) with configurable size
- Lightweight hashed shingles + Jaccard similarity
- Parallel scan option (`--workers`) for larger corpora
- CLI for scanning directories and reporting duplicate pairs above a threshold
- Extensible: plug in alternative tokenizers, filters, similarity strategies

## Installation
```
pip install -e .
```
Requires Python >=3.9.

## CLI Usage
```
duplicate-finder scan ./repo --threshold 0.85 --ext .py,.md,.txt --k 5
```
JSON output:
```
duplicate-finder scan ./repo --json
```
Parallel scan (4 processes):
```
duplicate-finder scan ./repo --workers 4
```
Lower shingle size for short files:
```
duplicate-finder scan ./small --k 3 --threshold 0.9
```

## Similarity Approach
1. Read and normalize text (newline + basic whitespace collapse)
2. Tokenize on word boundaries (alphanumeric + underscore)
3. Form k-token shingles (default k=5)
4. Hash shingles (MD5) to stable integers
5. Jaccard similarity on hashed shingle sets for scoring

## Parallelism
The `--workers` flag distributes file signature computation across processes. Use number of CPU cores or slightly fewer. Overhead may outweigh benefit for <300 files.

## Output
Table with similarity, file paths, token counts. Optional JSON list of objects.

## Benchmarks
Run synthetic benchmarks:
```
python benchmarks/run_benchmarks.py --files 500 --dup-groups 40 --group-size 5 --workers 4
```
Metrics shown: files scanned, time seconds, files/sec, duplicate pairs found.

## Repository Structure
```
src/duplicate_finder/
  __init__.py
  core.py          # Shingling + similarity + parallel scan
  index.py         # Future acceleration abstraction
  cli.py           # Click-based command interface
benchmarks/
  run_benchmarks.py
  README.md
tests/
  test_core.py
```

## Roadmap (Excerpt)
- Signature-based prefilter for large corpora
- Multiprocessing improvements (chunking, memory mapping)
- Ignore patterns / block filtering
- Pluggable tokenizers
- Semantic duplicate detection (embeddings)

## Contributing
Open issues for enhancements, performance, or false positive/negative cases. Submit focused PRs.

## License
(Select a license and add a LICENSE file; none included yet.)
