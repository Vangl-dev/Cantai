"""CLI interface for Cantai2."""

import json
from pathlib import Path

import typer

app = typer.Typer(
    name="cantai",
    help="Cantai2 - Selecionador de hinos (CTP, HCC, SH, Harpa Cristã, Novo Cântico)",
    no_args_is_help=True,
)

PROJECT_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = PROJECT_DIR / "data" / "input"
BASE_DIR = PROJECT_DIR / "data" / "base"


def _save(name: str, data: object) -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    path = BASE_DIR / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    typer.echo(f"Salvo: {path.relative_to(PROJECT_DIR)}")


@app.command()
def version() -> None:
    """Show version information."""
    from cantai import __version__

    typer.echo(f"cantai2 version {__version__}")


@app.command("importar-harpa")
def importar_harpa(
    pdf: Path = INPUT_DIR / "HARPA CRISTÃ.pdf",
    temas: Path = INPUT_DIR / "temas_harpa_crista.md",
) -> None:
    """Importa a Harpa Cristã do PDF para data/base/harpa.json."""
    from cantai.importers.harpa import TOTAL, import_harpa

    hymns = import_harpa(pdf, temas if temas.exists() else None)
    if len(hymns) < TOTAL - 10:
        typer.echo(f"ERRO: só {len(hymns)} hinos encontrados; nada foi salvo.", err=True)
        raise typer.Exit(1)
    _save("harpa.json", hymns)
    typer.echo(f"{len(hymns)} hinos; {sum(1 for h in hymns if h['topics'])} com tema.")


@app.command("importar-nc")
def importar_nc(pdf: Path = INPUT_DIR / "novo_cantico.pdf") -> None:
    """Importa o Novo Cântico do PDF para data/base/nc.json."""
    from cantai.importers.novo_cantico import import_novo_cantico

    hymns = import_novo_cantico(pdf)
    if len(hymns) < 390:
        typer.echo(f"ERRO: só {len(hymns)} hinos encontrados; nada foi salvo.", err=True)
        raise typer.Exit(1)
    _save("nc.json", hymns)
    typer.echo(f"{len(hymns)} hinos.")


@app.command("importar-metricas")
def importar_metricas(
    ctp: Path = INPUT_DIR / "HinarioCTP_metricas.md",
    hcc: Path = INPUT_DIR / "metricas_HCC.pdf",
) -> None:
    """Importa os índices de métricas do CTP e do HCC para data/base."""
    from cantai.importers.hcc_metrics import import_hcc_metrics
    from cantai.importers.metrics import import_metrics

    ctp_data = import_metrics(ctp)
    hcc_data = {str(k): v for k, v in sorted(import_hcc_metrics(hcc).items())}
    _save("ctp_metricas.json", ctp_data)
    _save("hcc_metricas.json", hcc_data)
    typer.echo(f"CTP: {len(ctp_data)} hinos; HCC: {len(hcc_data)} hinos.")


@app.command("importar-continuacoes-ctp")
def importar_continuacoes_ctp(pdf: Path = INPUT_DIR / "Hinário Cantai Todos os Povos.pdf") -> None:
    """Recupera do PDF o fim das letras do CTP cortadas na quebra de página."""
    from cantai.build import assign_ctp_variants
    from cantai.importers.ctp_continuations import import_ctp_continuations

    base = json.loads((BASE_DIR / "ctp.json").read_text(encoding="utf-8"))
    data = import_ctp_continuations(pdf, assign_ctp_variants(base["hymns"]))
    _save("ctp_continuacoes.json", data)
    typer.echo(f"{len(data)} hinos com linhas recuperadas.")


@app.command()
def build() -> None:
    """Gera web/data a partir de data/base (pode rodar quantas vezes quiser)."""
    from cantai.build import build as run_build

    stats = run_build(PROJECT_DIR)
    for code, values in stats.items():
        typer.echo(f"{code:4} " + "  ".join(f"{k}={v}" for k, v in values.items()))


@app.command()
def preview(port: int = 8000) -> None:
    """Abre o site localmente em http://localhost:<port>."""
    import functools
    import http.server

    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(PROJECT_DIR / "web")
    )
    typer.echo(f"http://localhost:{port}  (Ctrl+C para sair)")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


if __name__ == "__main__":
    app()
