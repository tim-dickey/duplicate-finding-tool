from duplicate_finder.core import DuplicateFinder
import os


def write(fp: str, content: str):
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)


def test_prefilter_equivalence(tmp_path):
    # Create a mix of similar and distinct files
    base = "alpha beta gamma delta epsilon theta lambda"
    for i in range(12):
        content = base + (" phi" if i % 3 == 0 else "") + (" psi" if i % 4 == 0 else "")
        write(str(tmp_path / f"f{i}.txt"), content)
    finder = DuplicateFinder(k=3, threshold=0.6)
    sigs = finder.scan(str(tmp_path), [".txt"], workers=0)
    full_pairs = finder.find_duplicates(sigs, prefilter=False)
    prefilter_pairs = finder.find_duplicates(sigs, prefilter=True, minhash_perms=32, lsh_bands=8)
    # Compare sets of path tuples
    full_set = {(a.path, b.path) for _, a, b in full_pairs}
    prefilter_set = {(a.path, b.path) for _, a, b in prefilter_pairs}
    assert full_set == prefilter_set


def test_prefilter_skip_small(tmp_path):
    write(str(tmp_path / "a.txt"), "alpha beta gamma")
    write(str(tmp_path / "b.txt"), "alpha beta gamma")
    finder = DuplicateFinder(k=2, threshold=0.9)
    sigs = finder.scan(str(tmp_path), [".txt"], workers=0)
    # Prefilter requested but small dataset (<50) should behave same
    direct_pairs = finder.find_duplicates(sigs, prefilter=False)
    prefilter_pairs = finder.find_duplicates(sigs, prefilter=True)
    assert {(a.path, b.path) for _, a, b in direct_pairs} == {(a.path, b.path) for _, a, b in prefilter_pairs}
