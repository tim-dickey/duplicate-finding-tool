from duplicate_finder.core import DuplicateFinder
from duplicate_finder.cluster import build_clusters


def write(fp: str, content: str):
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)


def test_cluster_build(tmp_path):
    # Create a chain A-B-C where all are similar forming one cluster
    write(str(tmp_path / "a.txt"), "alpha beta gamma delta epsilon")
    write(str(tmp_path / "b.txt"), "alpha beta gamma delta epsilon zeta")
    write(str(tmp_path / "c.txt"), "alpha beta gamma delta epsilon zeta eta")
    finder = DuplicateFinder(k=2, threshold=0.5)
    sigs = finder.scan(str(tmp_path), [".txt"], workers=0)
    pairs = finder.find_duplicates(sigs)
    clusters = build_clusters(pairs)
    # Expect single cluster of size 3
    assert len(clusters) == 1
    assert clusters[0]['size'] == 3
    assert set(clusters[0]['members']) == {str(tmp_path / 'a.txt'), str(tmp_path / 'b.txt'), str(tmp_path / 'c.txt')}
