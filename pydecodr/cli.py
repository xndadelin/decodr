"""
pydecodr.cli - command-line interface for decodr.

Provides the commands:
- encode
- decode
- detect
- encrypt
- decrypt
"""

from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from pydecodr import encode as api_encode, decode as api_decode, detect as api_detect

app = typer.Typer(
    help="decodr - decodr - a modular CTF/crypto CLI toolkit for encodings, classic ciphers, and autodetection."
)
console = Console()

@app.command()
def encode(
    scheme: str = typer.Argument(..., help="Encoding or cipher scheme (e.g., base64, caesar, rot13)"),
    text: str = typer.Argument(..., help="Text to encode"),
):
    try:
        result = api_encode(scheme, text)
        console.print(f"[bold green]Result:[/bold green] {result}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@app.command()
def decode(
    scheme: str = typer.Argument(..., help="Decoding or cipher scheme (e.g., base64, caesar, rot13)"),
    text: str = typer.Argument(..., help="Text to decode"),
):
    try:
        result = api_decode(scheme, text)
        console.print(f"[bold green]Result:[/bold green] {result}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@app.command()
def detect(
    text: str = typer.Argument(..., help="Text to automatically analyze and decode"),
    limit: int = typer.Option(5, help="Number of best results to show"),
): 
    try:
        results = api_detect(text, limit=limit)
        if not results:
            console.print("[yello]No likely encoding found.[/yellow]")
            raise typer.Exit()
        
        table = Table(title="Detection results")
        table.add_column("Rank", justify="right", style="cyan", no_wrap=True)
        table.add_column("Scheme", style="magenta")
        table.add_column("Score", justify="right", style="yellow")
        table.add_column("Result", style="white")

        for i, r in enumerate(results, 1):
            table.add_row(str(i), r["scheme"], r["score"], r["result"][:80])
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error: [/bold red] {e}")

@app.callback()
def main():
    pass

if __name__ == "__main__":
    app()
