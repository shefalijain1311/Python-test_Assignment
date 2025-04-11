import typer
import logging
from get_papers import pubmed_client, paper_filter, csv_writer

app = typer.Typer()

@app.command()
def main(
    query: str = typer.Argument(..., help="PubMed query string"),
    file: str = typer.Option("", "--file", "-f", help="Output CSV filename. If not provided, prints to console."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logs.")
):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    logging.info(f"Executing query: {query}")
    
    papers = pubmed_client.fetch_papers(query, debug)
    if not papers:
        logging.info("No papers found.")
        raise typer.Exit()
    
    for paper in papers:
        non_academic_authors, company_affiliations, corresponding_email = paper_filter.filter_paper_authors(paper)
        paper["non_academic_authors"] = non_academic_authors
        paper["company_affiliations"] = company_affiliations
        paper["corresponding_email"] = corresponding_email
    
    if file:
        csv_writer.write_csv(papers, file)
        logging.info(f"Output written to file: {file}")
    else:
        import pandas as pd
        rows = []
        for paper in papers:
            row = {
                "PubmedID": paper.get("pubmed_id", ""),
                "Title": paper.get("title", ""),
                "Publication Date": paper.get("pub_date", ""),
                "Non-academic Author(s)": "; ".join(paper.get("non_academic_authors", [])),
                "Company Affiliation(s)": "; ".join(paper.get("company_affiliations", [])),
                "Corresponding Author Email": paper.get("corresponding_email", ""),
            }
            rows.append(row)
        df = pd.DataFrame(rows)
        typer.echo(df.to_csv(index=False))

if __name__ == "__main__":
    main()
