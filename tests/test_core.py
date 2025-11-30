from src.duplicate_finder.core import DuplicateFinder
import tempfile
import os


def write(fp: str, content: str):
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)


def test_exact_duplicate(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    write(str(a), "alpha beta gamma delta epsilon")
    write(str(b), "alpha beta gamma delta epsilon")
    finder = DuplicateFinder(k=2, threshold=0.99)
    sigs = finder.scan(str(tmp_path), [".txt"])
    pairs = finder.find_duplicates(sigs)
    assert len(pairs) == 1
    assert pairs[0][0] >= 0.99


def test_near_duplicate(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    write(str(a), "alpha beta gamma delta epsilon")
    write(str(b), "alpha beta gamma delta epsilonn")  # slight change
    finder = DuplicateFinder(k=2, threshold=0.6)
    sigs = finder.scan(str(tmp_path), [".txt"])
    pairs = finder.find_duplicates(sigs)
    assert pairs
    assert pairs[0][0] >= 0.6


def test_parallel_matches_serial(tmp_path):
    files = []
    for i in range(10):
        fp = tmp_path / f"f{i}.txt"
        write(str(fp), "alpha beta gamma delta epsilon " + str(i))
        files.append(fp)
    finder = DuplicateFinder(k=3, threshold=0.5)
    serial = finder.scan(str(tmp_path), [".txt"], workers=0)
    parallel = finder.scan(str(tmp_path), [".txt"], workers=2)
    serial_paths = {s.path for s in serial}
    parallel_paths = {s.path for s in parallel}
    assert serial_paths == parallel_paths
    # Compare shingles sizes for consistency
    size_map_serial = {s.path: len(s.shingles) for s in serial}
    size_map_parallel = {s.path: len(s.shingles) for s in parallel}
    assert size_map_serial == size_map_parallel
