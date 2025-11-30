from click.testing import CliRunner
from src.duplicate_finder.cli import main
import json


def test_cli_empty_directory(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["scan", str(tmp_path), "--json", "--ext", ".txt", "--threshold", "0.5"])
    # Expect either empty list JSON or message if no duplicates
    assert result.exit_code == 0
    # If JSON flag used, output should parse to a list
    data = json.loads(result.output)
    assert isinstance(data, list)
    assert data == []


def test_cli_invalid_threshold(sample_dir):
    runner = CliRunner()
    # Negative threshold should still run; validation not enforced yet, ensure no crash
    result = runner.invoke(main, ["scan", str(sample_dir), "--threshold", "-0.1", "--ext", ".txt,.md"])
    assert result.exit_code == 0
