"""Duplicate Finding Tool package."""
from .core import DuplicateFinder, compute_jaccard, FileSignature
from .minhash import minhash_signature, lsh_candidates
from .cluster import build_clusters

__all__ = [
    "DuplicateFinder",
    "compute_jaccard",
    "FileSignature",
    "minhash_signature",
    "lsh_candidates",
    "build_clusters",
]
__version__ = "0.2.0"  # bumped for new features
