"""Interface de linha de comando do Cantai Builder."""

import json
import re
import shutil
from pathlib import Path

import typer
from rich.console import Console

from cantai.database import count_hymns, create_database, load_hymns, save_hymns
from cantai.exporters.json import export_json
from cantai.importers.cantor_cristao import import_cantor_cristao
from cantai.importers.cantor_cristao_index import import_cc_index
from cantai.importers.ctp import import_ctp
from cantai.importers.hcc import import_hcc
from cantai.importers.ctp_index import import_ctp_index
from cantai.importers.harpa import import_harpa
from cantai.importers.harpa_index import import_harpa_index
from cantai.importers.novo_cantico import import_novo_cantico
from cantai.importers.salmos_hinos import import_salmos_hinos
from cantai.importers.salmos_hinos_index import import_sh_index

app = typer.Typer(
    name="Cantai Builder",
    help="CLI para importação, exportação, validação e estatísticas.",
    no_args_is_help=True,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_INPUT = PROJECT_ROOT / "data" / "input"
JSON_OUTPUT = PROJECT_ROOT / "data" / "output" / "cantai.json"
WEB_OUTPUT = PROJECT_ROOT / "web" / "cantai.json"

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

    try:
        hinos, report = import_ctp(pasta)
    except ValueError as e:
        console.print(f"[red]Erro:[/red] {e}")
        raise typer.Exit(code=1)
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
def importar_indice() -> None:
    """Importar índice temático do CTP."""
    resultado = import_ctp_index()

    if "erro" in resultado:
        console.print(f"[red]Erro:[/red] {resultado['erro']}")
        raise typer.Exit(code=1)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Índice Temático do CTP[/bold]")
    console.print("─" * 50)
    console.print(f"Categorias encontradas:           {resultado['categorias_encontradas']}")
    console.print(f"Categorias importadas:            {resultado['categorias_importadas']}")
    console.print(f"Hinos atualizados:                {resultado['hinos_atualizados']}")
    console.print(f"Hinos não encontrados:            {resultado['hinos_nao_encontrados']}")
    console.print(f"Hinos pertencentes a mais de 1:   {resultado['hinos_multipla_categoria']}")
    console.print("─" * 50)

    if resultado["multi_topics"]:
        console.print()
        console.print("[bold]Hinos com múltiplas categorias:[/bold]")
        for num, topics in sorted(resultado["multi_topics"].items()):
            console.print(f"  CTP {num}: {', '.join(topics)}")


@app.command()
def auditar_indice() -> None:
    """Auditar e normalizar o índice temático do CTP."""
    from cantai.importers.ctp_index_data import CTP_INDEX

    console.print()
    console.print("═" * 60)
    console.print("[bold]Categorias do Índice Temático[/bold]")
    console.print("═" * 60)

    for cat_name in sorted(CTP_INDEX.keys()):
        nums = CTP_INDEX[cat_name]
        nums_sorted = sorted(nums, key=_sort_key)
        console.print()
        console.print(f"[bold]{cat_name}[/bold] ({len(nums)} hinos)")
        console.print(f"  {', '.join(nums_sorted)}")

    console.print()
    console.print("═" * 60)
    console.print("[bold]Validações[/bold]")
    console.print("═" * 60)

    duplicados_cat = len(CTP_INDEX) - len(set(CTP_INDEX.keys()))
    vazias = [cat for cat, nums in CTP_INDEX.items() if not nums]

    duplicados_interno = 0
    for cat, nums in CTP_INDEX.items():
        vistos = set()
        for n in nums:
            if n in vistos:
                duplicados_interno += 1
            vistos.add(n)

    invalidos = []
    for cat, nums in CTP_INDEX.items():
        for n in nums:
            motivo = _check_invalid_number(n)
            if motivo:
                invalidos.append((cat, n, motivo))

    console.print(f"Categorias:             {len(CTP_INDEX)}")
    console.print(f"Categorias duplicadas:  {duplicados_cat}")
    console.print(f"Categorias vazias:      {len(vazias)}")
    console.print(f"Duplicados removíveis:  {duplicados_interno}")
    console.print(f"Números inválidos:      {len(invalidos)}")
    console.print("═" * 60)

    if duplicados_interno > 0:
        console.print()
        console.print("[yellow]Duplicados encontrados e removidos:[/yellow]")
        for cat in sorted(CTP_INDEX.keys()):
            vistos = []
            duplicados = []
            for n in CTP_INDEX[cat]:
                if n in vistos:
                    duplicados.append(n)
                else:
                    vistos.append(n)
            if duplicados:
                console.print(f"  {cat}: {', '.join(duplicados)}")

    if invalidos:
        console.print()
        console.print("[bold]Números inválidos[/bold]")
        console.print()
        for cat, num, motivo in invalidos:
            console.print(f"[bold]Categoria:[/bold] {cat}")
            console.print(f"[bold]Valor:[/bold]     {num}")
            console.print(f"[bold]Motivo:[/bold]    {motivo}")
            console.print()

    normalized = {}
    for cat in sorted(CTP_INDEX.keys()):
        nums = list(dict.fromkeys(CTP_INDEX[cat]))
        normalized[cat] = sorted(nums, key=_sort_key)

    _save_normalized_index(normalized)
    console.print("[green]Arquivo normalizado salvo.[/green]")


def _check_invalid_number(num_str: str) -> str | None:
    """Verifica se um número é inválido e retorna o motivo."""
    match = re.match(r"^(\d+)(.*)", num_str)
    if not match:
        return "formato inválido"

    val = int(match.group(1))
    suffix = match.group(2)

    if val < 1 or val > 500:
        return f"fora do intervalo (1-500): {val}"

    if suffix:
        if re.match(r"^[A-Z]$", suffix):
            return "harmonização alternativa"
        if re.match(r"^\(\d+[a-z]?\)$", suffix):
            return "versão alternativa"
        return f"sufixo inválido: {suffix}"

    return None


def _sort_key(num_str: str):
    match = re.match(r"^(\d+)", num_str)
    return int(match.group(1)) if match else 0


def _save_normalized_index(data: dict) -> None:
    """Salva o índice normalizado em ctp_index_data.py."""

    lines = [
        '"""Índice temático do CTP - dados extraídos manualmente do PDF."""',
        "",
        "CTP_INDEX: dict[str, list[str]] = {",
    ]

    for cat_name in sorted(data.keys()):
        nums = data[cat_name]
        nums_repr = ", ".join(f'"{n}"' for n in nums)
        if len(nums_repr) + 8 <= 88:
            lines.append(f'    "{cat_name}": [{nums_repr}],')
        else:
            lines.append(f'    "{cat_name}": [')
            chunks = []
            chunk = "        "
            for n in nums:
                entry = f'"{n}", '
                if len(chunk) + len(entry) > 80:
                    chunks.append(chunk.rstrip())
                    chunk = "        " + entry
                else:
                    chunk += entry
            if chunk.strip():
                chunks.append(chunk.rstrip())
            lines.extend(chunks)
            lines.append("    ],")

    lines.append("}")
    lines.append("")

    target = Path(__file__).resolve().parent / "importers" / "ctp_index_data.py"
    target.write_text("\n".join(lines), encoding="utf-8")


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


@app.command()
def importar_harpa(
    pdf: Path = typer.Argument(..., help="PDF da Harpa Crista"),
) -> None:
    """Importar hinário Harpa Cristã de PDF."""
    if not pdf.is_file():
        console.print(f"[red]Erro:[/red] '{pdf}' não é um arquivo válido.")
        raise typer.Exit(code=1)

    create_database()

    hinos, report = import_harpa(pdf)
    novos, atualizados = save_hymns(hinos)
    total = count_hymns()

    _imprimir_relatorio(report)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Relatório da Harpa[/bold]")
    console.print("─" * 50)
    console.print(f"Hinos importados:  {report.hinos_criados}")
    console.print(f"Novos:             {novos}")
    console.print(f"Atualizados:       {atualizados}")
    console.print(f"Total no banco:    {total}")
    console.print("─" * 50)


@app.command()
def importar_indice_harpa() -> None:
    """Importar índice temático da Harpa Cristã."""
    resultado = import_harpa_index()

    if "erro" in resultado:
        console.print(f"[red]Erro:[/red] {resultado['erro']}")
        raise typer.Exit(code=1)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Índice Temático da Harpa Cristã[/bold]")
    console.print("─" * 50)
    console.print(f"Categorias encontradas:           {resultado['categorias_encontradas']}")
    console.print(f"Categorias importadas:            {resultado['categorias_importadas']}")
    console.print(f"Hinos atualizados:                {resultado['hinos_atualizados']}")
    console.print(f"Hinos não encontrados:            {resultado['hinos_nao_encontrados']}")
    console.print(f"Hinos pertencentes a mais de 1:   {resultado['hinos_multipla_categoria']}")
    console.print("─" * 50)

    if resultado["multi_topics"]:
        console.print()
        console.print("[bold]Hinos com múltiplas categorias:[/bold]")
        for num, topics in sorted(resultado["multi_topics"].items()):
            console.print(f"  HARPA {num}: {', '.join(topics)}")


@app.command()
def importar_cc(
    pdf: Path = typer.Argument(..., help="PDF do Cantor Cristao"),
) -> None:
    """Importar hinário Cantor Cristão de PDF."""
    if not pdf.is_file():
        console.print(f"[red]Erro:[/red] '{pdf}' não é um arquivo válido.")
        raise typer.Exit(code=1)

    create_database()

    hinos, report = import_cantor_cristao(pdf)
    novos, atualizados = save_hymns(hinos)
    total = count_hymns()

    _imprimir_relatorio(report)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Relatório do Cantor Cristão[/bold]")
    console.print("─" * 50)
    console.print(f"Hinos importados:  {report.hinos_criados}")
    console.print(f"Novos:             {novos}")
    console.print(f"Atualizados:       {atualizados}")
    console.print(f"Total no banco:    {total}")
    console.print("─" * 50)


@app.command()
def importar_indice_cc() -> None:
    """Importar índice temático do Cantor Cristão."""
    resultado = import_cc_index()

    if "erro" in resultado:
        console.print(f"[red]Erro:[/red] {resultado['erro']}")
        raise typer.Exit(code=1)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Índice Temático do Cantor Cristão[/bold]")
    console.print("─" * 50)
    console.print(f"Categorias encontradas:           {resultado['categorias_encontradas']}")
    console.print(f"Categorias importadas:            {resultado['categorias_importadas']}")
    console.print(f"Hinos atualizados:                {resultado['hinos_atualizados']}")
    console.print(f"Hinos não encontrados:            {resultado['hinos_nao_encontrados']}")
    console.print(f"Hinos pertencentes a mais de 1:   {resultado['hinos_multipla_categoria']}")
    console.print("─" * 50)

    if resultado["multi_topics"]:
        console.print()
        console.print("[bold]Hinos com múltiplas categorias:[/bold]")
        for num, topics in sorted(resultado["multi_topics"].items()):
            console.print(f"  CC {num}: {', '.join(topics)}")


@app.command()
def importar_hcc(
    pdf: Path = typer.Argument(..., help="PDF do HCC"),
) -> None:
    """Importar hinário HCC de PDF."""
    if not pdf.is_file():
        console.print(f"[red]Erro:[/red] '{pdf}' não é um arquivo válido.")
        raise typer.Exit(code=1)

    create_database()

    hinos, report = import_hcc(pdf)
    novos, atualizados = save_hymns(hinos)
    total = count_hymns()

    _imprimir_relatorio(report)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Relatório do HCC[/bold]")
    console.print("─" * 50)
    console.print(f"Hinos importados:  {report.hinos_criados}")
    console.print(f"Novos:             {novos}")
    console.print(f"Atualizados:       {atualizados}")
    console.print(f"Total no banco:    {total}")
    console.print("─" * 50)


@app.command()
def importar_sh(
    pdf: Path = typer.Argument(..., help="PDF de Salmos e Hinos"),
) -> None:
    """Importar hinário Salmos e Hinos de PDF."""
    if not pdf.is_file():
        console.print(f"[red]Erro:[/red] '{pdf}' não é um arquivo válido.")
        raise typer.Exit(code=1)

    create_database()

    hinos, report = import_salmos_hinos(pdf)
    novos, atualizados = save_hymns(hinos)
    total = count_hymns()

    _imprimir_relatorio(report)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Relatório de Salmos e Hinos[/bold]")
    console.print("─" * 50)
    console.print(f"Hinos importados:  {report.hinos_criados}")
    console.print(f"Novos:             {novos}")
    console.print(f"Atualizados:       {atualizados}")
    console.print(f"Total no banco:    {total}")
    console.print("─" * 50)


@app.command()
def importar_indice_sh() -> None:
    """Importar índice temático de Salmos e Hinos."""
    resultado = import_sh_index()

    if "erro" in resultado:
        console.print(f"[red]Erro:[/red] {resultado['erro']}")
        raise typer.Exit(code=1)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Índice Temático de Salmos e Hinos[/bold]")
    console.print("─" * 50)
    console.print(f"Categorias encontradas:           {resultado['categorias_encontradas']}")
    console.print(f"Categorias importadas:            {resultado['categorias_importadas']}")
    console.print(f"Hinos atualizados:                {resultado['hinos_atualizados']}")
    console.print(f"Hinos não encontrados:            {resultado['hinos_nao_encontrados']}")
    console.print(f"Hinos pertencentes a mais de 1:   {resultado['hinos_multipla_categoria']}")
    console.print("─" * 50)

    if resultado["multi_topics"]:
        console.print()
        console.print("[bold]Hinos com múltiplas categorias:[/bold]")
        for num, topics in sorted(resultado["multi_topics"].items()):
            console.print(f"  SH {num}: {', '.join(topics)}")


@app.command()
def importar_nc(
    pdf: Path = typer.Argument(..., help="PDF do Novo Cantico"),
) -> None:
    """Importar hinário Novo Cântico de PDF."""
    if not pdf.is_file():
        console.print(f"[red]Erro:[/red] '{pdf}' não é um arquivo válido.")
        raise typer.Exit(code=1)

    create_database()

    hinos, report = import_novo_cantico(pdf)
    novos, atualizados = save_hymns(hinos)
    total = count_hymns()

    _imprimir_relatorio(report)

    console.print()
    console.print("─" * 50)
    console.print("[bold]Relatório do Novo Cântico[/bold]")
    console.print("─" * 50)
    console.print(f"Hinos importados:  {report.hinos_criados}")
    console.print(f"Novos:             {novos}")
    console.print(f"Atualizados:       {atualizados}")
    console.print(f"Total no banco:    {total}")
    console.print("─" * 50)


@app.command()
def reclassificar() -> None:
    """Reclassificar todos os hinos para o catálogo único do Cantai."""
    from cantai.topics.reclassifier import reclassify_all

    create_database()

    console.print()
    console.print("═" * 50)
    console.print("[bold]Reclassificação — Catálogo Único Cantai[/bold]")
    console.print("═" * 50)

    stats = reclassify_all()

    console.print(f"Total de hinos:              {stats['total']}")
    console.print(f"Com temas originais:         {stats['com_temas_originais']}")
    console.print(f"Reclassificados:             {stats['reclassificados']}")
    console.print(f"Já canônicos:                {stats['ja_canonicos']}")
    console.print(f"Classificados por letra:     {stats['classificados_por_letra']}")
    console.print(f"Sem temas antes:             {stats['sem_temas_antes']}")
    console.print(f"Sem temas depois:            {stats['sem_temas_depois']}")
    console.print("─" * 50)

    console.print()
    console.print("[bold]Por hinário:[/bold]")
    for hymnal, data in sorted(stats["por_hinario"].items()):
        console.print(f"  {hymnal:10s} total={data['total']:4d}  "
                      f"reclass={data['reclassificados']:4d}  "
                      f"letra={data['classificados_por_letra']:4d}")

    console.print("═" * 50)


@app.command()
def relatorio_qualidade() -> None:
    """Exibir relatório de qualidade do acervo."""
    create_database()

    console.print()
    console.print("═" * 60)
    console.print("[bold]Relatório de Qualidade — Cantai[/bold]")
    console.print("═" * 60)

    all_hymns = load_hymns()
    total = len(all_hymns)

    por_hinario: dict[str, int] = {}
    sem_letra = 0
    sem_primeira_linha = 0
    sem_topics = 0
    topic_counter: dict[str, int] = {}

    for h in all_hymns:
        por_hinario[h.hymnal] = por_hinario.get(h.hymnal, 0) + 1
        if not h.lyrics.strip():
            sem_letra += 1
        if not h.first_line.strip():
            sem_primeira_linha += 1
        if not h.topics:
            sem_topics += 1
        for t in h.topics:
            topic_counter[t] = topic_counter.get(t, 0) + 1

    console.print(f"Quantidade total de hinos:       {total}")
    console.print()
    console.print("[bold]Por hinário:[/bold]")
    for hymnal in ["CTP", "HARPA", "CC", "SH", "NC"]:
        console.print(f"  {hymnal:10s} {por_hinario.get(hymnal, 0):5d}")

    console.print()
    console.print(f"Quantidade de temas:             {len(topic_counter)}")

    top_topics = sorted(topic_counter.items(), key=lambda x: -x[1])[:10]
    console.print()
    console.print("[bold]Temas mais utilizados:[/bold]")
    for topic, count in top_topics:
        console.print(f"  {topic:30s} {count:5d}")

    console.print()
    console.print(f"Hinos sem letra:                 {sem_letra}")
    console.print(f"Hinos sem primeira linha:        {sem_primeira_linha}")
    console.print(f"Hinos sem topics:                {sem_topics}")

    if sem_topics == 0:
        console.print()
        console.print("[green]✓ Todos os hinos possuem topics![/green]")
    else:
        console.print()
        console.print(f"[red]✗ {sem_topics} hinos ainda sem topics[/red]")

    console.print("═" * 60)


@app.command()
def validar_topicos() -> None:
    """Validar catálogo de temas e consistência com o banco."""
    from cantai.topics.validator import validate_all

    create_database()

    console.print()
    console.print("═" * 60)
    console.print("[bold]Validação de Temas — Cantai[/bold]")
    console.print("═" * 60)

    report = validate_all()

    console.print()
    console.print("[bold]YAML (canonical_topics.yaml)[/bold]")
    yaml_data = report["yaml"]
    console.print(f"  Temas:          {yaml_data.get('topics_count', 0)}")
    console.print(f"  Válido:         {'Sim' if yaml_data['valid'] else 'Não'}")

    for issue in yaml_data.get("issues", []):
        console.print(f"  [red]✗[/red] {issue}")

    console.print()
    console.print("[bold]Banco de dados[/bold]")
    db_data = report["database"]
    console.print(f"  Total hinos:    {db_data['total_hymns']}")
    console.print(f"  Sem topics:     {db_data['sem_topics']}")

    nao_canonicos = db_data.get("topicos_nao_canonicos", {})
    if nao_canonicos:
        console.print()
        console.print("[yellow]Temas não canônicos no banco:[/yellow]")
        for topic, count in sorted(nao_canonicos.items(), key=lambda x: -x[1]):
            console.print(f"  {topic:30s} {count:5d} hinos")

    for issue in db_data.get("issues", []):
        if "sem topics" in issue or "não canônico" in issue:
            continue
        console.print(f"  [red]✗[/red] {issue}")

    console.print()
    console.print("═" * 60)
    if report["valid"]:
        console.print("[green]✓ Validação concluída sem inconsistências.[/green]")
    else:
        console.print(f"[red]✗ {report['issues_count']} inconsistência(s) encontrada(s).[/red]")
    console.print("═" * 60)


@app.command()
def auditoria_topicos() -> None:
    """Auditoria de integridade: Índice CTP × Banco × JSON."""
    import json

    from sqlmodel import Session, select

    from cantai.database import engine, load_hymns
    from cantai.models import HymnModel

    create_database()

    console.print()
    console.print("═" * 70)
    console.print("[bold]Auditoria de Temas — Índice × Banco × JSON[/bold]")
    console.print("═" * 70)

    # 1. Load CTP index
    from cantai.importers.ctp_index_data import CTP_INDEX
    from cantai.importers.ctp_index import _normalize_number

    # Build index: normalized_number -> list of topics
    index_topics: dict[str, list[str]] = {}
    for cat_name, numbers in CTP_INDEX.items():
        for num in numbers:
            normalized = _normalize_number(num)
            if not normalized:
                continue
            if normalized not in index_topics:
                index_topics[normalized] = []
            if cat_name not in index_topics[normalized]:
                index_topics[normalized].append(cat_name)

    # 2. Load database
    with Session(engine) as session:
        db_models = session.exec(
            select(HymnModel).where(HymnModel.hymnal == "CTP")
        ).all()

    # Build DB lookup: normalized_number -> topics
    db_topics: dict[str, list[str]] = {}
    db_numbers: dict[str, str] = {}  # normalized -> actual
    for m in db_models:
        # Normalize the DB number
        num = m.number
        if num.isdigit():
            normalized = str(int(num))
        else:
            normalized = num
        topics = json.loads(m.topics) if m.topics else []
        db_topics[normalized] = topics
        db_numbers[normalized] = num

    # 3. Load JSON
    all_hymns = load_hymns()
    json_topics: dict[str, list[str]] = {}
    for h in all_hymns:
        if h.hymnal == "CTP":
            num = h.number
            if num.isdigit():
                normalized = str(int(num))
            else:
                normalized = num
            json_topics[normalized] = h.topics

    # 4. Compare
    console.print()
    console.print("[bold]Comparação por tema:[/bold]")
    console.print()

    total_index = 0
    total_db = 0
    total_json = 0
    divergencias = 0
    hinos_divergentes: list[str] = []

    for cat_name in sorted(CTP_INDEX.keys()):
        index_nums = set()
        for num in CTP_INDEX[cat_name]:
            normalized = _normalize_number(num)
            if normalized:
                index_nums.add(normalized)

        db_nums = set()
        for norm, topics in db_topics.items():
            if cat_name in topics:
                db_nums.add(norm)

        json_nums = set()
        for norm, topics in json_topics.items():
            if cat_name in topics:
                json_nums.add(norm)

        total_index += len(index_nums)
        total_db += len(db_nums)
        total_json += len(json_nums)

        # Check for missing
        missing_db = index_nums - db_nums
        missing_json = index_nums - json_nums

        if missing_db or missing_json:
            divergencias += 1
            console.print(f"[red]✗ {cat_name}[/red]")
            console.print(f"  Índice: {len(index_nums)} hinos")
            console.print(f"  Banco:  {len(db_nums)} hinos")
            console.print(f"  JSON:   {len(json_nums)} hinos")

            if missing_db:
                display_nums = [db_numbers.get(n, n) for n in sorted(missing_db)]
                console.print(f"  [red]Faltando no banco: {', '.join(display_nums)}[/red]")
                for n in missing_db:
                    hinos_divergentes.append(f"CTP {db_numbers.get(n, n)} - {cat_name} (falta no banco)")

            if missing_json and not missing_db:
                display_nums = sorted(missing_json)
                console.print(f"  [yellow]Faltando no JSON: {', '.join(display_nums)}[/yellow]")
                for n in missing_json:
                    hinos_divergentes.append(f"CTP {db_numbers.get(n, n)} - {cat_name} (falta no JSON)")
        else:
            console.print(f"[green]✓ {cat_name}[/green] ({len(index_nums)} hinos)")

    # 5. Summary
    console.print()
    console.print("═" * 70)
    console.print("[bold]Resumo da Auditoria[/bold]")
    console.print("─" * 70)
    console.print(f"  Temas no índice:           {len(CTP_INDEX)}")
    console.print(f"  Total referências (índice): {total_index}")
    console.print(f"  Total referências (banco):  {total_db}")
    console.print(f"  Total referências (JSON):   {total_json}")
    console.print("─" * 70)

    if divergencias == 0:
        console.print()
        console.print("[green]✓ Índice, Banco e JSON 100% sincronizados![/green]")
    else:
        console.print()
        console.print(f"[red]✗ {divergencias} tema(s) com divergência(s)[/red]")
        console.print()
        console.print("[bold]Hinos divergentes:[/bold]")
        for h in hinos_divergentes:
            console.print(f"  {h}")

    console.print("═" * 70)


@app.command()
def build(
    ctp_dir: Path = typer.Option(
        None, "--ctp-dir", help="Pasta original do CTP (PPT/PPTX)"
    ),
) -> None:
    """Build completo: importa todos os hinários e exporta JSON."""
    create_database()

    console.print()
    console.print("═" * 50)
    console.print("[bold]Cantai Builder — Build V1.6[/bold]")
    console.print("═" * 50)

    counts: dict[str, int] = {}

    # 1. Importar CTP
    if ctp_dir and ctp_dir.is_dir():
        console.print()
        console.print("[bold]1/14[/bold] Importando CTP...")
        try:
            hinos, report = import_ctp(ctp_dir)
            save_hymns(hinos)
            counts["CTP"] = report.hinos_criados
            console.print(f"  CTP: {report.hinos_criados} hinos")
        except (ValueError, Exception) as e:
            console.print(f"  [red]CTP: Erro — {e}[/red]")
            counts["CTP"] = 0
    else:
        console.print()
        console.print("[bold]1/14[/bold] CTP ignorado (sem --ctp-dir)")

    # 2. Importar índice CTP
    console.print("[bold]2/14[/bold] Importando índice CTP...")
    try:
        import_ctp_index()
        console.print("  Índice CTP: OK")
    except Exception as e:
        console.print(f"  [yellow]Índice CTP: {e}[/yellow]")

    # 3. Importar Harpa
    harpa_pdf = DATA_INPUT / "HARPA CRISTÃ.pdf"
    console.print("[bold]3/14[/bold] Importando Harpa Cristã...")
    if harpa_pdf.is_file():
        hinos, report = import_harpa(harpa_pdf)
        save_hymns(hinos)
        counts["HARPA"] = report.hinos_criados
        console.print(f"  HARPA: {report.hinos_criados} hinos")
    else:
        console.print("  [yellow]HARPA: PDF não encontrado[/yellow]")
        counts["HARPA"] = 0

    # 4. Importar índice Harpa
    console.print("[bold]4/14[/bold] Importando índice Harpa...")
    try:
        import_harpa_index()
        console.print("  Índice Harpa: OK")
    except Exception as e:
        console.print(f"  [yellow]Índice Harpa: {e}[/yellow]")

    # 5. Importar Cantor Cristão
    cc_pdf = DATA_INPUT / "Cantor Cristão em formato pdf.pdf"
    console.print("[bold]5/14[/bold] Importando Cantor Cristão...")
    if cc_pdf.is_file():
        hinos, report = import_cantor_cristao(cc_pdf)
        save_hymns(hinos)
        counts["CC"] = report.hinos_criados
        console.print(f"  CC: {report.hinos_criados} hinos")
    else:
        console.print("  [yellow]CC: PDF não encontrado[/yellow]")
        counts["CC"] = 0

    # 6. Importar índice CC
    console.print("[bold]6/14[/bold] Importando índice CC...")
    try:
        import_cc_index()
        console.print("  Índice CC: OK")
    except Exception as e:
        console.print(f"  [yellow]Índice CC: {e}[/yellow]")

    # 7. Importar HCC
    hcc_pdf = DATA_INPUT / "hcc-completo_compress.pdf"
    console.print("[bold]7/14[/bold] Importando HCC...")
    if hcc_pdf.is_file():
        hinos, report = import_hcc(hcc_pdf)
        save_hymns(hinos)
        counts["HCC"] = report.hinos_criados
        console.print(f"  HCC: {report.hinos_criados} hinos")
    else:
        console.print("  [yellow]HCC: PDF não encontrado[/yellow]")
        counts["HCC"] = 0

    # 8. Importar Salmos e Hinos (novo PDF completo)
    sh_pdf = DATA_INPUT / "SALMOS-HINOS completo.pdf"
    if not sh_pdf.is_file():
        sh_pdf = DATA_INPUT / "Coletania de Salmos & Hinos.pdf"
    console.print("[bold]8/14[/bold] Importando Salmos e Hinos...")
    if sh_pdf.is_file():
        hinos, report = import_salmos_hinos(sh_pdf)
        save_hymns(hinos)
        counts["SH"] = report.hinos_criados
        console.print(f"  SH: {report.hinos_criados} hinos")
    else:
        console.print("  [yellow]SH: PDF não encontrado[/yellow]")
        counts["SH"] = 0

    # 9. Importar Novo Cântico
    nc_pdf = DATA_INPUT / "novo_cantico.pdf"
    console.print("[bold]9/14[/bold] Importando Novo Cântico...")
    if nc_pdf.is_file():
        hinos, report = import_novo_cantico(nc_pdf)
        save_hymns(hinos)
        counts["NC"] = report.hinos_criados
        console.print(f"  NC: {report.hinos_criados} hinos")
    else:
        console.print("  [yellow]NC: PDF não encontrado[/yellow]")
        counts["NC"] = 0

    # 10. Reclassificar para catálogo único
    console.print("[bold]10/14[/bold] Reclassificando para catálogo único...")
    from cantai.topics.reclassifier import reclassify_all
    reclassify_stats = reclassify_all()
    console.print(f"  Reclassificados: {reclassify_stats['reclassificados']}")
    console.print(f"  Classificados por letra: {reclassify_stats['classificados_por_letra']}")
    console.print(f"  Sem temas depois: {reclassify_stats['sem_temas_depois']}")

    # 11. Exportar JSON
    console.print("[bold]11/14[/bold] Exportando JSON...")
    all_hymns = load_hymns()
    export_json(all_hymns, JSON_OUTPUT)
    console.print(f"  {JSON_OUTPUT.relative_to(PROJECT_ROOT)}: {len(all_hymns)} hinos")

    # 12. Sincronizar web
    console.print("[bold]12/14[/bold] Sincronizando web...")
    shutil.copy2(JSON_OUTPUT, WEB_OUTPUT)
    console.print(f"  {WEB_OUTPUT.relative_to(PROJECT_ROOT)}: copiado")

    # 13. Relatório de qualidade
    console.print("[bold]13/14[/bold] Relatório de qualidade...")
    sem_topics_final = sum(1 for h in all_hymns if not h.topics)
    console.print(f"  Hinos sem topics: {sem_topics_final}")

    # 14. Validar temas
    console.print("[bold]14/14[/bold] Validando catálogo de temas...")
    from cantai.topics.validator import validate_all
    val_report = validate_all()
    if val_report["valid"]:
        console.print("  [green]✓ Temas válidos[/green]")
    else:
        console.print(f"  [yellow]✗ {val_report['issues_count']} inconsistência(s)[/yellow]")
        for issue in val_report["issues"][:5]:
            console.print(f"    {issue}")
        if val_report["issues_count"] > 5:
            console.print(f"    ... e mais {val_report['issues_count'] - 5}")

    # 15. Auditoria de integridade CTP
    console.print()
    console.print("[bold]Auditoria de integridade CTP...[/bold]")
    from cantai.importers.ctp_index_data import CTP_INDEX
    from cantai.importers.ctp_index import _normalize_number

    index_topics_map: dict[str, list[str]] = {}
    for cat_name, numbers in CTP_INDEX.items():
        for num in numbers:
            normalized = _normalize_number(num)
            if not normalized:
                continue
            if normalized not in index_topics_map:
                index_topics_map[normalized] = []
            if cat_name not in index_topics_map[normalized]:
                index_topics_map[normalized].append(cat_name)

    # Check DB
    from sqlmodel import Session as AuditSession, select as audit_select
    from cantai.models import HymnModel as AuditHymnModel
    with AuditSession(engine) as session:
        db_models = session.exec(
            audit_select(AuditHymnModel).where(AuditHymnModel.hymnal == "CTP")
        ).all()

    db_topics_map: dict[str, list[str]] = {}
    for m in db_models:
        num = m.number
        if num.isdigit():
            normalized = str(int(num))
        else:
            normalized = num
        topics = json.loads(m.topics) if m.topics else []
        db_topics_map[normalized] = topics

    audit_divergencias = 0
    for cat_name in sorted(CTP_INDEX.keys()):
        index_nums = set()
        for num in CTP_INDEX[cat_name]:
            normalized = _normalize_number(num)
            if normalized:
                index_nums.add(normalized)

        db_nums = set()
        for norm, topics in db_topics_map.items():
            if cat_name in topics:
                db_nums.add(norm)

        missing = index_nums - db_nums
        if missing:
            audit_divergencias += 1
            console.print(f"  [red]✗ {cat_name}: faltando {len(missing)} hinos no banco[/red]")

    if audit_divergencias == 0:
        console.print("  [green]✓ Índice CTP 100% sincronizado com o banco[/green]")
    else:
        console.print()
        console.print(f"[red]✗ AUDITORIA FALHOU: {audit_divergencias} tema(s) com divergência(s)[/red]")
        console.print("[red]Execute 'cantai auditoria-topicos' para detalhes.[/red]")
        raise typer.Exit(code=1)

    # Resumo
    total = sum(counts.values())
    console.print()
    console.print("═" * 50)
    console.print("[bold]Builder concluído[/bold]")
    console.print("─" * 50)
    for hymnal in ["CTP", "HARPA", "CC", "HCC", "SH", "NC"]:
        console.print(f"  {hymnal:15s} {counts.get(hymnal, 0):4d}")
    console.print("─" * 50)
    console.print(f"  {'TOTAL':15s} {total:4d}")
    console.print("═" * 50)
    console.print("  SQLite atualizado")
    console.print("  JSON atualizado")
    console.print("  Web sincronizada")
    console.print("  Catálogo único aplicado")
    console.print("═" * 50)


@app.command()
def preview(
    port: int = typer.Option(8000, "--port", "-p", help="Porta do servidor"),
) -> None:
    """Preview local: exporta JSON e inicia servidor HTTP."""
    import http.server
    import threading

    create_database()

    console.print()
    console.print("═" * 50)
    console.print("[bold]Cantai Preview[/bold]")
    console.print("═" * 50)

    # 1. Exportar JSON do banco existente
    console.print()
    console.print("[bold]1/3[/bold] Exportando JSON...")
    all_hymns = load_hymns()
    if not all_hymns:
        console.print("  [yellow]Banco vazio. Execute 'cantai build' primeiro.[/yellow]")
        raise typer.Exit(code=1)
    export_json(all_hymns, JSON_OUTPUT)
    console.print(f"  [green]{len(all_hymns)} hinos exportados[/green]")

    # 2. Sincronizar web
    console.print("[bold]2/3[/bold] Sincronizando web...")
    shutil.copy2(JSON_OUTPUT, WEB_OUTPUT)
    console.print(f"  [green]web/cantai.json atualizado[/green]")

    # 3. Servidor HTTP
    console.print("[bold]3/3[/bold] Iniciando servidor...")

    web_dir = str(WEB_OUTPUT.parent)

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=web_dir, **kwargs)

        def log_message(self, format, *args):
            pass

    server = http.server.HTTPServer(("localhost", port), QuietHandler)

    def start_server():
        server.serve_forever()

    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()

    url = f"http://localhost:{port}"
    console.print()
    console.print("═" * 50)
    console.print("[bold green]Cantai Preview pronto![/bold green]")
    console.print("─" * 50)
    console.print(f"  Banco atualizado")
    console.print(f"  JSON atualizado")
    console.print(f"  Servidor iniciado")
    console.print()
    console.print(f"  [bold]{url}[/bold]")
    console.print()
    console.print("  Pressione Ctrl+C para parar.")
    console.print("═" * 50)
    console.print()

    try:
        import webbrowser
        webbrowser.open(url)
    except Exception:
        pass

    try:
        thread.join()
    except KeyboardInterrupt:
        console.print()
        console.print("[yellow]Servidor encerrado.[/yellow]")
        server.shutdown()
