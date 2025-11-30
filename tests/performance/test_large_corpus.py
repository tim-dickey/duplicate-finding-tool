import pytest
import tempfile
import os
from duplicate_finder.core import DuplicateFinder
import time


def write(fp: str, content: str):
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)


@pytest.mark.slow
def test_large_corpus_serial_vs_parallel():
    """Performance test: serial vs parallel on 300 files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate 300 files with controlled duplicates
        base_content = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"] * 10
        for i in range(300):
            content = " ".join(base_content + [f"unique_{i % 20}"])  # 20 dup groups
            write(os.path.join(tmpdir, f"file_{i}.txt"), content)
        
        finder = DuplicateFinder(k=5, threshold=0.7)
        
        # Serial
        start = time.perf_counter()
        sigs_serial = finder.scan(tmpdir, [".txt"], workers=0)
        pairs_serial = finder.find_duplicates(sigs_serial, prefilter=False)
        serial_time = time.perf_counter() - start
        
        # Parallel
        start = time.perf_counter()
        sigs_parallel = finder.scan(tmpdir, [".txt"], workers=4)
        pairs_parallel = finder.find_duplicates(sigs_parallel, prefilter=False)
        parallel_time = time.perf_counter() - start
        
        # Verify equivalence
        assert len(sigs_serial) == len(sigs_parallel) == 300
        serial_set = {(a.path, b.path) for _, a, b in pairs_serial}
        parallel_set = {(a.path, b.path) for _, a, b in pairs_parallel}
        assert serial_set == parallel_set
        
        # Log performance
        print(f"\nSerial: {serial_time:.2f}s, Parallel: {parallel_time:.2f}s, Speedup: {serial_time/parallel_time:.2f}x")
        # No hard assertion on speedup due to variability, but log for visibility


@pytest.mark.slow
def test_prefilter_performance():
    """Performance test: prefilter reduces comparison time on 500 files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = ["word" + str(i % 50) for i in range(100)]
        for i in range(500):
            content = " ".join(base + [f"file_{i}"])
            write(os.path.join(tmpdir, f"f{i}.txt"), content)
        
        finder = DuplicateFinder(k=5, threshold=0.6)
        sigs = finder.scan(tmpdir, [".txt"], workers=4)
        
        # Full pairwise
        start = time.perf_counter()
        pairs_full = finder.find_duplicates(sigs, prefilter=False)
        full_time = time.perf_counter() - start
        
        # Prefilter
        start = time.perf_counter()
        pairs_prefilter = finder.find_duplicates(sigs, prefilter=True, minhash_perms=64, lsh_bands=16)
        prefilter_time = time.perf_counter() - start
        
        print(f"\nFull: {full_time:.2f}s, Prefilter: {prefilter_time:.2f}s")
        # Prefilter should be faster or comparable; at minimum it shouldn't crash
        assert len(pairs_prefilter) > 0  # Expect some duplicates


@pytest.mark.slow
def test_memory_footprint():
    """Performance test: memory usage stays reasonable for 1000 small files."""
    try:
        import psutil
        process = psutil.Process()
    except ImportError:
        pytest.skip("psutil not available")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(1000):
            content = f"sample content number {i} " * 20
            write(os.path.join(tmpdir, f"f{i}.txt"), content)
        
        rss_start = process.memory_info().rss / (1024 * 1024)  # MB
        finder = DuplicateFinder(k=5, threshold=0.8)
        sigs = finder.scan(tmpdir, [".txt"], workers=4)
        pairs = finder.find_duplicates(sigs, prefilter=True)
        rss_end = process.memory_info().rss / (1024 * 1024)
        
        rss_delta = rss_end - rss_start
        print(f"\nMemory delta: {rss_delta:.2f} MB for {len(sigs)} files")
        # Sanity check: should not exceed 500MB for this dataset
        assert rss_delta < 500
