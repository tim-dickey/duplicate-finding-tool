import os
import shutil
import tempfile
import pytest

@pytest.fixture
def sample_dir(tmp_path):
    # Create a small directory with some duplicates and near-duplicates
    texts = {
        "a.txt": "alpha beta gamma delta epsilon",
        "b.txt": "alpha beta gamma delta epsilon zeta",
        "c.txt": "alpha beta gamma delta EPSILON zeta",  # case variation
        "d.md": "alpha beta gamma delta epsilon",  # duplicate of a.txt different ext
        "unique.py": "def func():\n    return 'unique content here'\n",
    }
    for name, content in texts.items():
        (tmp_path / name).write_text(content, encoding="utf-8")
    return tmp_path
