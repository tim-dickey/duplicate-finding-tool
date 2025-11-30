import json
import click
from .core import DuplicateFinder

@click.group()
def main():
    """Duplicate Finding Tool CLI."""

@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False))
@click.option("--threshold", type=float, default=0.85, show_default=True, help="Similarity threshold (0-1)")
@click.option("--ext", type=str, default=".py,.md,.txt", show_default=True, help="Comma-separated list of file extensions")
@click.option("--k", type=int, default=5, show_default=True, help="Shingle size (tokens per shingle)")
@click.option("--json", "--json-output", is_flag=True, help="Emit JSON instead of table")
def scan(path, threshold, ext, k, json_output):
    """Scan PATH recursively for duplicate / near-duplicate files."""
    extensions = [e.strip() for e in ext.split(",") if e.strip()]
    finder = DuplicateFinder(k=k, threshold=threshold)
    sigs = finder.scan(path, extensions)
    results = finder.find_duplicates(sigs)

    if json_output:
        out = [
            {
                "similarity": round(sim, 4),
                "file_a": a.path,
                "file_b": b.path,
                "tokens_a": a.size,
                "tokens_b": b.size,
            }
            for sim, a, b in results
        ]
        click.echo(json.dumps(out, indent=2))
    else:
        if not results:
            click.echo("No duplicates above threshold.")
            return
        width = 8
        click.echo(f"{'SIM':<{width}} FILE_A | FILE_B")
        click.echo("-" * 80)
        for sim, a, b in results:
            click.echo(f"{sim:<{width}.4f} {a.path} | {b.path}")

if __name__ == "__main__":
    main()
