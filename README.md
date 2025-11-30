# Duplicate Finding Tool

Identify exact and near-duplicate files (text / source) within a directory tree.

## Features
- Shingling (k-token) with configurable size
- Lightweight MinHash-style signatures for approximate similarity
- Jaccard similarity + optional content length filtering
- CLI for scanning directories and reporting duplicate pairs above a threshold
- Extensible: plug in alternative tokenizers, filters, similarity strategies

## Quick Start
```
pip install -e .
duplicate-finder scan /path/to/dir --threshold 0.85 --ext .py,.md,.txt
```

## Similarity Approach
1. Read and normalize text (newline + basic whitespace collapse)
2. Tokenize on word boundaries (alphanumeric + underscore)
3. Form k-token shingles (default k=5)
4. Hash shingles (MD5) to stable integers
5. Build MinHash-like signature across multiple hash salt rounds
6. Jaccard similarity on raw shingle sets for final scoring (signatures can accelerate later)

## Output
CLI prints a table with: similarity, file_a, file_b, token counts. Optionally JSON via `--json`.

## Roadmap (High-Level)
- Signature-based prefilter for large corpora
- Parallel scanning / multiprocessing
- Pluggable language-aware tokenizers
- Ignore blocks (license headers, boilerplate) via patterns
- Embedding-based semantic duplicate detection (future)

## Repository Structure
```
src/duplicate_finder/
  __init__.py
  core.py          # Shingling + similarity primitives
  index.py         # Signatures & indexing abstraction
  cli.py           # Click-based command interface
tests/
  test_core.py
```
Design docs placeholders added; replace with actual content if desired.

## Contributing
Open an issue for enhancements or performance concerns.

## License
(Select a license and add a LICENSE file; none included yet.)
