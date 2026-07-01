"""Importador do hinário Cantor Cristão."""

import re
from pathlib import Path

from cantai.schemas import AuditIssue, AuditReport, Hymn

_HYMNAL = "CC"
_HYMN_PATTERN = re.compile(r"^(\d{3})\s*-\s*(.+)$")


def _extract_hymns_from_pdf(pdf_path: Path) -> list[tuple[int, str, str]]:
    """Extrai hinos do PDF do Cantor Cristão.

    Retorna lista de (numero, titulo, texto_completo_por_pagina).
    """
    import pdfplumber

    pdf = pdfplumber.open(str(pdf_path))
    pages_text: list[str] = []
    for page in pdf.pages:
        text = page.extract_text()
        pages_text.append(text or "")
    pdf.close()

    full_text = "\n".join(pages_text)
    lines = full_text.split("\n")

    hymn_boundaries: list[tuple[int, int, str]] = []
    for idx, line in enumerate(lines):
        m = _HYMN_PATTERN.match(line.strip())
        if m:
            num = int(m.group(1))
            title = m.group(2).strip()
            if 1 <= num <= 600 and len(title) > 1:
                hymn_boundaries.append((num, idx, title))

    seen: set[int] = set()
    unique_boundaries: list[tuple[int, int, str]] = []
    for num, idx, title in hymn_boundaries:
        if num not in seen:
            seen.add(num)
            unique_boundaries.append((num, idx, title))

    results: list[tuple[int, str, str]] = []
    for i, (num, start_idx, title) in enumerate(unique_boundaries):
        end_idx = unique_boundaries[i + 1][1] if i + 1 < len(unique_boundaries) else len(lines)
        hymn_lines = lines[start_idx:end_idx]
        hymn_text = "\n".join(hymn_lines)
        results.append((num, title, hymn_text))

    return results


def _parse_lyrics(hymn_text: str) -> tuple[str, str]:
    """Extrai letra e primeira linha do texto do hino."""
    lines = hymn_text.split("\n")

    lyrics_lines: list[str] = []
    found_header = False
    for line in lines:
        stripped = line.strip()
        if not found_header:
            if _HYMN_PATTERN.match(stripped):
                found_header = True
            continue
        if stripped:
            cleaned = re.sub(r"^\[\d+\]\s*", "", stripped)
            if cleaned:
                lyrics_lines.append(cleaned)

    if not lyrics_lines:
        return "", ""

    first_line = lyrics_lines[0] if lyrics_lines else ""
    lyrics = "\n".join(lyrics_lines)
    return lyrics, first_line


def import_cantor_cristao(pdf_path: Path) -> tuple[list[Hymn], AuditReport]:
    """Importa hinário Cantor Cristão de um arquivo PDF.

    Retorna uma tupla (hinos, relatorio).
    """
    report = AuditReport()

    if not pdf_path.is_file():
        report.erros.append(AuditIssue(
            arquivo=str(pdf_path),
            motivo="Arquivo não encontrado",
        ))
        return [], report

    raw_hymns = _extract_hymns_from_pdf(pdf_path)
    report.pptx_encontrados = len(raw_hymns)

    hinos: list[Hymn] = []
    for num, title, hymn_text in raw_hymns:
        report.processados += 1
        try:
            lyrics, first_line = _parse_lyrics(hymn_text)
            if not lyrics:
                report.ignorados.append(AuditIssue(
                    arquivo=f"Hino {num:03d}",
                    motivo="Sem letra extraída",
                ))
                continue

            hinos.append(Hymn(
                hymnal=_HYMNAL,
                number=str(num),
                title=title,
                category=None,
                first_line=first_line,
                lyrics=lyrics,
                slide_count=0,
                source_file=pdf_path,
            ))
        except Exception as e:
            report.erros.append(AuditIssue(
                arquivo=f"Hino {num:03d}",
                motivo=f"Erro ao processar: {e}",
            ))

    report.hinos_criados = len(hinos)
    return hinos, report
