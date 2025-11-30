import argparse
import random
import string
import time
import tempfile
import os
from duplicate_finder.core import DuplicateFinder

WORDS = [
    "alpha","beta","gamma","delta","epsilon","zeta","eta","theta","iota","kappa","lambda","mu","nu","xi","omicron","pi","rho","sigma","tau","upsilon","phi","chi","psi","omega"
]

def random_tokens(count: int) -> list:
    return [random.choice(WORDS) + random.choice(["", random.choice(string.ascii_lowercase)]) for _ in range(count)]

def make_group(base_tokens, variations, out_dir, ext):
    paths = []
    for i in range(variations):
        tokens = base_tokens[:]
        # introduce slight variation
        if tokens and random.random() < 0.7:
            idx = random.randrange(len(tokens))
            tokens[idx] = random.choice(WORDS)
        if random.random() < 0.3:
            tokens.append(random.choice(WORDS))
        content = " ".join(tokens)
        fp = os.path.join(out_dir, f"group_{id(base_tokens)}_{i}{ext}")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        paths.append(fp)
    return paths

def synthesize(files: int, dup_groups: int, group_size: int, out_dir: str, ext: str):
    remaining = files
    for _ in range(dup_groups):
        if remaining <= 0:
            break
        size = min(group_size, remaining)
        base = random_tokens(random.randint(30, 60))
        make_group(base, size, out_dir, ext)
        remaining -= size
    # Fill remaining with unique random files
    for i in range(remaining):
        tokens = random_tokens(random.randint(40, 70))
        content = " ".join(tokens)
        fp = os.path.join(out_dir, f"unique_{i}{ext}")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)

def run_benchmark(args):
    with tempfile.TemporaryDirectory() as tmp:
        synthesize(args.files, args.dup_groups, args.group_size, tmp, args.ext)
        finder = DuplicateFinder(k=args.k, threshold=args.threshold)
        start = time.time()
        sigs = finder.scan(tmp, [args.ext], workers=args.workers)
        pairs = finder.find_duplicates(sigs)
        elapsed = time.time() - start
        rate = len(sigs) / elapsed if elapsed else 0
        print(f"Files: {len(sigs)}")
        print(f"Elapsed: {elapsed:.3f}s")
        print(f"Files/sec: {rate:.1f}")
        print(f"Duplicate pairs >= {args.threshold}: {len(pairs)}")
        if args.verbose:
            for sim, a, b in pairs[:10]:
                print(f"{sim:.4f} {os.path.basename(a.path)} | {os.path.basename(b.path)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic benchmark for Duplicate Finding Tool")
    parser.add_argument("--files", type=int, default=200, help="Total synthetic files")
    parser.add_argument("--dup-groups", type=int, default=20, help="Number of duplicate groups")
    parser.add_argument("--group-size", type=int, default=4, help="Files per duplicate group")
    parser.add_argument("--ext", type=str, default=".txt", help="File extension for synthetic files")
    parser.add_argument("--k", type=int, default=5, help="Shingle size")
    parser.add_argument("--threshold", type=float, default=0.85, help="Similarity threshold")
    parser.add_argument("--workers", type=int, default=0, help="Process workers (0=serial)")
    parser.add_argument("--verbose", action="store_true", help="Show sample duplicate pairs")
    args = parser.parse_args()
    run_benchmark(args)
