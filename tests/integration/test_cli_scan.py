from click.testing import CliRunner
from duplicate_finder.cli import main
import json


def test_cli_json_pairs(sample_dir):
    runner = CliRunner()
    result = runner.invoke(main, ["scan", str(sample_dir), "--json", "--ext", ".txt,.md", "--threshold", "0.5"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert all("schema_version" in rec for rec in data)
    assert data, "Expected some duplicate pairs"


def test_cli_prefilter_equivalence(sample_dir):
    runner = CliRunner()
    direct = runner.invoke(main, ["scan", str(sample_dir), "--json", "--ext", ".txt,.md", "--threshold", "0.5"])
    prefilter = runner.invoke(main, ["scan", str(sample_dir), "--json", "--ext", ".txt,.md", "--threshold", "0.5", "--prefilter"])
    assert direct.exit_code == 0 and prefilter.exit_code == 0
    d_pairs = {(rec['file_a'], rec['file_b']) for rec in json.loads(direct.output)}
    p_pairs = {(rec['file_a'], rec['file_b']) for rec in json.loads(prefilter.output)}
    assert d_pairs == p_pairs


def test_cli_clusters_json(sample_dir):
    runner = CliRunner()
    result = runner.invoke(main, ["scan", str(sample_dir), "--clusters", "--json", "--ext", ".txt,.md", "--threshold", "0.5"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["schema_version"] == 1
    assert data["mode"] == "clusters"
    assert isinstance(data["clusters"], list)
    if data["clusters"]:
        cluster = data["clusters"][0]
        assert "representative" in cluster and "members" in cluster and "size" in cluster
