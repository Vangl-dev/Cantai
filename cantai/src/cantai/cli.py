"""Interface de linha de comando do Cantai Builder."""

from pathlib import Path

import typer
from rich.console import Console

from cantai.database import create_database, count_hymns, load_hymns, save_hymns
from cantai.exporters.json import export_json
from cantai.importers.ctp import import_ctp

app = typer.Typer(
    name="Cantai Builder",
    help="CLI para importação, exportação, validação e estatísticas.",
    no_args_is_help=True,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
JSON_OUTPUT = PROJECT_ROOT / "data" / "output" / "cantai.json"

console = Console()


def _imprimir_relatorio(report):
    """Imprime o relatório de auditoria."""
    console.print()
    console.print("─" * 50)
    console.print("[bold]Relatório de Importação[/bold]")
    console.print("─" * 50)
    console.print(f"PPT encontrados:         {report.ppt_encontrados}")
    console.print(f"PPTX encontrados:        {report.pptx_encontrados}")
    console.print(f"Convertidos:             {report.convertidos}")
    console.print(f"Apresentações processadas: {report.processados}")
    console.print(f"Objetos Hymn criados:    {report.hinos_criados}")

    ignorados = len(report.ignorados)
    erros = len(report.erros)
    console.print(f"Apresentações ignoradas: {ignorados}")
    console.print(f"Apresentações com erro:  {erros}")
    console.print("─" * 50)

    if report.ignorados:
        console.print()
        console.print("[yellow]Apresentações Ignoradas:[/yellow]")
        for item in report.ignorados:
            console.print(f"  • {item.arquivo}")
            console.print(f"    Motivo: {item.motivo}")

    if report.erros:
        console.print()
        console.print("[red]Apresentações com Erro:[/red]")
        for item in report.erros:
            console.print(f"  • {item.arquivo}")
            console.print(f"    Motivo: {item.motivo}")


@app.command()
def importar(pasta: Path = typer.Argument(..., help="Pasta contendo arquivos .ppt/.pptx")) -> None:
    """Importar acervo de apresentações."""
    if not pasta.is_dir():
        console.print(f"[red]Erro:[/red] '{pasta}' não é uma pasta válida.")
        raise typer.Exit(code=1)

    create_database()

    hinos, report = import_ctp(pasta)
    novos, atualizados = save_hymns(hinos)
    total = count_hymns()

    _imprimir_relatorio(report)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Persistência[/bold]")
    console.print("─" * 50)
    console.print(f"Novos:             {novos}")
    console.print(f"Atualizados:       {atualizados}")
    console.print(f"Total no banco:    {total}")
    console.print("─" * 50)


@app.command()
def exportar() -> None:
    """Exportar hinos do banco para JSON."""
    create_database()

    hinos = load_hymns()
    if not hinos:
        console.print("[yellow]Nenhum hino encontrado no banco.[/yellow]")
        raise typer.Exit()

    export_json(hinos, JSON_OUTPUT)

    console.print(f"Hinos exportados: {len(hinos)}")
    console.print(f"Arquivo: {JSON_OUTPUT.relative_to(PROJECT_ROOT)}")


@app.command()
def validar() -> None:
    """Validar dados."""
    console.print("Não implementado", style="yellow")


@app.command()
def estatisticas() -> None:
    """Exibir estatísticas."""
    console.print("Não implementado", style="yellow")
