import typer
from rich.prompt import Prompt
from kyb.console import console
from kyb.scrapers.crunchbase import search_companies

app = typer.Typer()


@app.command()
def main(company: str):
    console.log(f"Getting companies matching {company}")
    results = search_companies(company)
    choices = [f"{r.url_slug}: {r.description}" for r in results]
    console.log("got results", choices)
    Prompt.ask("which one to scrape?", choices=choices, show_choices=False)
