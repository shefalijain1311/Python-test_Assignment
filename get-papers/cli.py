# cli.py

import typer
from typing import Optional
from get_papers.pubmed_client import fetch_pubmed_ids, fetch_details
from get_papers.paper_filter import filter_papers
from get_papers.csv_writer import write_to_csv

app = typer.Typer(add_completion=False)


@app.command()
def main(
    query: str = typer.Argument(..., help="PubMed query string"),
    file: Optional[str] = typer.Option(None, "-f", "--file", help="Filename to save CSV output"),
    debug: bool = typer.Option(False, "-d", "--debug", help="Enable debug output"),
):
    """
    Fetch PubMed papers and filter for non-academic authors in pharmaceutical/biotech companies.
    """
    if debug:
        typer.echo(f"🔍 Searching PubMed for: {query}")

    try:
        ids = fetch_pubmed_ids(query)
        if debug:
            typer.echo(f"📄 Found {len(ids)} paper IDs")

        details = fetch_details(ids)
        if debug:
            typer.echo(f"📚 Fetched details for {len(details)} papers")

        filtered = filter_papers(details)
        if debug:
            typer.echo(f"🏢 Filtered to {len(filtered)} papers with non-academic authors")

        write_to_csv(filtered, filename=file)

    except Exception as e:
        typer.secho(f"❌ Error: {str(e)}", fg=typer.colors.RED)


if __name__ == "__main__":
    app()