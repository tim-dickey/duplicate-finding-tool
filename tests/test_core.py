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
