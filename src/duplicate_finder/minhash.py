import hashlib
from typing import Iterable, List, Set, Tuple, Dict

# Pre-generated stable salts (hex of incremental numbers hashed once for diffusion)
_SALTS = [
    int(hashlib.md5(f"salt-{i}".encode()).hexdigest(), 16) & ((1<<64)-1) for i in range(128)
]

def minhash_signature(shingles: Set[int], perms: int = 64) -> List[int]:
    """Compute a MinHash signature list of length `perms`.
    Deterministic: uses stable salt list and MD5 hashing.
    """
    if perms > len(_SALTS):
        raise ValueError("perms exceeds available salts")
    if not shingles:
        # Represent empty set as maximal values (won't collide spuriously)
        return [(1<<64)-1] * perms
    sig: List[int] = []
    for salt in _SALTS[:perms]:
        m = (1<<64)-1
        # Iterate shingles, XOR salt then hash -> take min 64-bit prefix
        for s in shingles:
            h = hashlib.md5(f"{salt}:{s}".encode()).hexdigest()
            v = int(h[:16], 16)  # take first 64 bits
            if v < m:
                m = v
        sig.append(m)
    return sig

def lsh_candidates(signatures: List[List[int]], bands: int) -> Set[Tuple[int, int]]:
    """Generate candidate index pairs via LSH banding.
    Each band is a contiguous slice of the signature; items sharing identical band tuple are candidates.
    Returns set of (i,j) with i<j.
    """
    if not signatures:
        return set()
    perms = len(signatures[0])
    if any(len(sig) != perms for sig in signatures):
        raise ValueError("Inconsistent signature lengths")
    if bands <= 0 or bands > perms:
        raise ValueError("Invalid band count")
    band_size = perms // bands
    # Last band consumes remaining if not divisible
    buckets: Dict[Tuple[int, Tuple[int, ...]], List[int]] = {}
    for idx, sig in enumerate(signatures):
        for b in range(bands):
            start = b * band_size
            end = (b+1) * band_size if b < bands - 1 else perms
            key = (b, tuple(sig[start:end]))
            buckets.setdefault(key, []).append(idx)
    candidates: Set[Tuple[int, int]] = set()
    for item_list in buckets.values():
        if len(item_list) > 1:
            base = item_list
            for i in range(len(base)):
                for j in range(i+1, len(base)):
                    a, b = base[i], base[j]
                    if a > b:
                        a, b = b, a
                    candidates.add((a, b))
    return candidates
