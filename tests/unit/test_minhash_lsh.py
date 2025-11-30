from src.duplicate_finder.minhash import minhash_signature, lsh_candidates
import pytest
from hypothesis import given, strategies as st

@given(st.sets(st.integers(min_value=0, max_value=10_000), max_size=30))
def test_minhash_deterministic(shingles):
    sig1 = minhash_signature(shingles, perms=32)
    sig2 = minhash_signature(shingles, perms=32)
    assert sig1 == sig2
    assert len(sig1) == 32


def test_lsh_candidates_basic():
    # Two identical signatures should produce a candidate pair in at least one band
    sigs = [list(range(32)), list(range(32)), list(range(32, 64))]
    pairs = lsh_candidates(sigs, bands=8)
    assert (0, 1) in pairs


def test_lsh_invalid_band_count():
    sigs = [list(range(16)), list(range(16))]
    with pytest.raises(ValueError):
        lsh_candidates(sigs, bands=0)
