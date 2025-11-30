# JSON Output Schema Documentation

## Overview
The Duplicate Finding Tool provides JSON output via the `--json` flag. This document describes the schema, versioning policy, and evolution strategy.

## Schema Version
All JSON output includes a `schema_version` field (integer) to enable downstream consumers to handle format changes.

**Current Version:** 1

## Output Modes

### Pair Mode (default)
Returns a JSON array of duplicate pair objects.

**Structure:**
```json
[
  {
    "schema_version": 1,
    "similarity": 0.9234,
    "file_a": "/path/to/file1.py",
    "file_b": "/path/to/file2.py",
    "tokens_a": 150,
    "tokens_b": 155
  },
  ...
]
```

**Fields:**
- `schema_version` (int): Schema version number.
- `similarity` (float): Jaccard similarity score, range [0.0, 1.0], rounded to 4 decimals.
- `file_a` (string): Absolute path to first file.
- `file_b` (string): Absolute path to second file.
- `tokens_a` (int): Token count in file_a.
- `tokens_b` (int): Token count in file_b.

**Ordering:** Pairs sorted by similarity descending, then lexicographically by file paths.

### Cluster Mode (`--clusters`)
Returns a JSON object with cluster array.

**Structure:**
```json
{
  "schema_version": 1,
  "mode": "clusters",
  "threshold": 0.85,
  "clusters": [
    {
      "representative": "/path/to/file1.py",
      "members": ["/path/to/file1.py", "/path/to/file2.py", "/path/to/file3.py"],
      "size": 3,
      "max_similarity": 0.95
    },
    ...
  ]
}
```

**Top-level Fields:**
- `schema_version` (int): Schema version.
- `mode` (string): Always `"clusters"` for cluster mode.
- `threshold` (float): Similarity threshold used.
- `clusters` (array): List of cluster objects.

**Cluster Object Fields:**
- `representative` (string): Lexicographically first file path in cluster.
- `members` (array of strings): All file paths in cluster, sorted.
- `size` (int): Number of files in cluster.
- `max_similarity` (float): Highest pairwise similarity within cluster.

**Ordering:** Clusters sorted by representative path.

## Versioning Policy

### Version 1 (Current)
- Initial stable schema.
- Pair mode: array of objects with similarity + file paths + token counts.
- Cluster mode: object with clusters array.

### Future Changes
Backward-compatible additions (new optional fields) will not increment version. Breaking changes (field removal, type change, structure change) will increment `schema_version`.

**Planned Additions (v1 extensions):**
- `shingle_count_a`, `shingle_count_b`: Number of unique shingles per file.
- `prefilter_used`: Boolean indicating if LSH prefilter was applied.
- `cluster.avg_similarity`: Average pairwise similarity within cluster.

**Breaking Changes (future v2):**
- Cluster mode may switch to nested pair details.
- Path normalization strategy may change.

## Consumption Guidelines

1. **Always check `schema_version`** before parsing.
2. **Ignore unknown fields** for forward compatibility.
3. **Validate required fields** exist (similarity, file_a, file_b for pairs; representative, members for clusters).
4. **Handle empty results:** Pair mode returns `[]`, cluster mode returns `{"clusters": []}`.

## Examples

### Example: Pair Mode
```bash
duplicate-finder scan ./repo --json --threshold 0.8 > output.json
```
Output:
```json
[
  {
    "schema_version": 1,
    "similarity": 0.8765,
    "file_a": "/repo/utils.py",
    "file_b": "/repo/helpers.py",
    "tokens_a": 200,
    "tokens_b": 195
  }
]
```

### Example: Cluster Mode
```bash
duplicate-finder scan ./repo --clusters --json --threshold 0.7 > clusters.json
```
Output:
```json
{
  "schema_version": 1,
  "mode": "clusters",
  "threshold": 0.7,
  "clusters": [
    {
      "representative": "/repo/module_a.py",
      "members": ["/repo/module_a.py", "/repo/module_a_copy.py"],
      "size": 2,
      "max_similarity": 0.98
    }
  ]
}
```

## Validation

For automated validation, refer to `schema/duplicates.schema.json` (JSON Schema draft-07 format).

## Change Log

- **v1 (2025-11-30):** Initial release with pair and cluster modes.
