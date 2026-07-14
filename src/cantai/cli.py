"""CLI interface for Cantai2."""

import typer

app = typer.Typer(
    name="cantai",
    help="Cantai2 - Aplicação web para busca e consulta do Hinário Cantai Todos os Povos",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Show version information."""
    from cantai import __version__

    typer.echo(f"cantai2 version {__version__}")


if __name__ == "__main__":
    app()
