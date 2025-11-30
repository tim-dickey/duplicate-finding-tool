from duplicate_finder.core import normalize, tokenize, hashed_shingles

def test_normalize_whitespace():
    text = "alpha   beta\n\t gamma"  # multiple spaces + newline + tab
    assert normalize(text) == "alpha beta gamma"


def test_tokenize_basic():
    tokens = tokenize("alpha beta gamma123 _delta_ ! ?")
    assert tokens == ["alpha", "beta", "gamma123", "_delta_"]


def test_hashed_shingles_empty():
    assert hashed_shingles([], k=3) == set()


def test_hashed_shingles_size():
    tokens = ["a", "b", "c", "d"]
    sh = hashed_shingles(tokens, k=2)
    # number of shingles = len(tokens) - k + 1
    assert len(sh) == 3
