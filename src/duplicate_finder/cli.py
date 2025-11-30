import json
import click
from .core import DuplicateFinder
from .cluster import build_clusters

@click.group()
def main():
    """Duplicate Finding Tool CLI."""

@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False))
@click.option("--threshold", type=float, default=0.85, show_default=True, help="Similarity threshold (0-1)")
@click.option("--ext", type=str, default=".py,.md,.txt", show_default=True, help="Comma-separated list of file extensions")
@click.option("--k", type=int, default=5, show_default=True, help="Shingle size (tokens per shingle)")
@click.option("--workers", type=int, default=0, show_default=True, help="Parallel worker processes (0 = serial signature phase)")
@click.option("--prefilter", is_flag=True, help="Enable MinHash+LSH candidate prefiltering (improves scalability)")
@click.option("--minhash-perms", type=int, default=64, show_default=True, help="MinHash permutations when prefilter enabled")
@click.option("--lsh-bands", type=int, default=16, show_default=True, help="Number of LSH bands (must divide perms roughly)")
@click.option("--clusters", is_flag=True, help="Output duplicate clusters instead of raw pairs")
@click.option("--json", "--json-output", is_flag=True, help="Emit JSON instead of table")
def scan(path, threshold, ext, k, workers, prefilter, minhash_perms, lsh_bands, clusters, json_output):
    """Scan PATH recursively for duplicate / near-duplicate files."""
    extensions = [e.strip() for e in ext.split(",") if e.strip()]
    finder = DuplicateFinder(k=k, threshold=threshold)
    sigs = finder.scan(path, extensions, workers=workers)
    results = finder.find_duplicates(sigs, prefilter=prefilter, minhash_perms=minhash_perms, lsh_bands=lsh_bands)

    if clusters:
        cluster_list = build_clusters(results)
        if json_output:
            out = {
                "schema_version": 1,
                "mode": "clusters",
                "threshold": threshold,
                "clusters": cluster_list,
            }
            click.echo(json.dumps(out, indent=2))
            return
        if not cluster_list:
            click.echo("No duplicate clusters above threshold.")
            return
        click.echo("CLUSTER_ID SIZE MAX_SIM REPRESENTATIVE")
        click.echo("-" * 72)
        for idx, c in enumerate(cluster_list, start=1):
            click.echo(f"{idx:<10} {c['size']:<4} {c['max_similarity']:.4f} {c['representative']}")
        return

    if json_output:
        out = [
            {
                "schema_version": 1,
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
