from click.testing import CliRunner
from duplicate_finder.cli import main


def test_cli_clusters_table(sample_dir):
    runner = CliRunner()
    result = runner.invoke(main, ["scan", str(sample_dir), "--clusters", "--ext", ".txt,.md", "--threshold", "0.5"])
    assert result.exit_code == 0
    # Expect header line
    assert "CLUSTER_ID" in result.output
