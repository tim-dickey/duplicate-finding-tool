from typing import List, Dict, Set
from .core import FileSignature, compute_jaccard

class SignatureIndex:
    """In-memory index for potential future acceleration.
    Currently stores raw shingles; can be extended to LSH buckets.
    """
    def __init__(self):
        self._map: Dict[str, Set[int]] = {}

    def add(self, sig: FileSignature) -> None:
        self._map[sig.path] = sig.shingles

    def candidates(self, shingles: Set[int], min_overlap: int = 1) -> List[str]:
        out: List[str] = []
        for path, other in self._map.items():
            if len(shingles & other) >= min_overlap:
                out.append(path)
        return out

    def similarity(self, a: str, b: str) -> float:
        return compute_jaccard(self._map.get(a, set()), self._map.get(b, set()))
