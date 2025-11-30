import hashlib
import os
import re
from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple
from concurrent.futures import ProcessPoolExecutor

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def normalize(text: str) -> str:
    return " ".join(text.split())

def tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(text)

def make_shingles(tokens: List[str], k: int = 5) -> List[Tuple[str, ...]]:
    if k <= 0 or len(tokens) < k:
        return []
    return [tuple(tokens[i:i+k]) for i in range(len(tokens) - k + 1)]

def shingle_hash(shingle: Tuple[str, ...]) -> int:
    h = hashlib.md5("::".join(shingle).encode("utf-8")).hexdigest()
    return int(h, 16)

def hashed_shingles(tokens: List[str], k: int = 5) -> Set[int]:
    return {shingle_hash(s) for s in make_shingles(tokens, k)}

def compute_jaccard(a: Set[int], b: Set[int]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0

@dataclass
class FileSignature:
    path: str
    shingles: Set[int]
    size: int

def _compute_file_signature(args):
    path, k = args
    try:
        text = normalize(read_file(path))
        tokens = tokenize(text)
        sh = hashed_shingles(tokens, k)
        return FileSignature(path=path, shingles=sh, size=len(tokens))
    except Exception:
        return None

class DuplicateFinder:
    def __init__(self, k: int = 5, threshold: float = 0.85):
        self.k = k
        self.threshold = threshold

    def _gather_files(self, root: str, extensions: Iterable[str]) -> List[str]:
        ext_set = {e.lower() for e in extensions}
        out: List[str] = []
        for dirpath, _, filenames in os.walk(root):
            for name in filenames:
                fp = os.path.join(dirpath, name)
                _, ext = os.path.splitext(name)
                if not ext_set or ext.lower() in ext_set:
                    out.append(fp)
        return out

    def scan(self, root: str, extensions: Iterable[str], min_tokens: int = 0, workers: int = 0) -> List[FileSignature]:
        files = self._gather_files(root, extensions)
        sigs: List[FileSignature] = []
        if workers and workers > 1:
            with ProcessPoolExecutor(max_workers=workers) as ex:
                for sig in ex.map(_compute_file_signature, [(f, self.k) for f in files]):
                    if sig and sig.size >= min_tokens:
                        sigs.append(sig)
        else:
            for f in files:
                sig = _compute_file_signature((f, self.k))
                if sig and sig.size >= min_tokens:
                    sigs.append(sig)
        return sigs

    def find_duplicates(self, signatures: List[FileSignature]) -> List[Tuple[float, FileSignature, FileSignature]]:
        results: List[Tuple[float, FileSignature, FileSignature]] = []
        for i in range(len(signatures)):
            for j in range(i + 1, len(signatures)):
                a = signatures[i]
                b = signatures[j]
                sim = compute_jaccard(a.shingles, b.shingles)
                if sim >= self.threshold:
                    results.append((sim, a, b))
        results.sort(key=lambda x: (-x[0], x[1].path, x[2].path))
        return results
