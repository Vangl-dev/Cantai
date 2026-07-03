"""Importador do hinário HCC (Hinário da Congregação Cristã)."""

import re
from pathlib import Path

from cantai.schemas import AuditIssue, AuditReport, Hymn

_HYMNAL = "HCC"

# Pattern 1: NUMBER. HCC TITLE (with period and HCC prefix)
_P1 = re.compile(r"^(\d+)\.\s+HCC\s+(.+)$")

# Pattern 1b: NUMBER HCC. TITLE (HCC with period after)
_P1b = re.compile(r"^(\d+)\s+HCC\.\s+(.+)$")

# Pattern 2: NUMBER HCC TITLE (without period, with HCC prefix)
_P2 = re.compile(r"^(\d{2,3})\s+HCC\s+([A-Z\u00C0-\u00D6\u00D8-\u00DE].+)$")

# Pattern 3: NUMBER. TITLE (with period, without HCC prefix)
_P3 = re.compile(r"^(\d{2,3})\.\s+([A-Z\u00C0-\u00D6\u00D8-\u00DE\u0022\u201C].{4,})$")

# Pattern 4: NUMBER TITLE (sem ponto, sem HCC) - para numeros altos (310+)
_P4 = re.compile(r"^(\d{3})\s+([A-Z\u00C0-\u00D6\u00D8-\u00DE\u0022\u201C].{5,})$")


def _is_likely_hymn_title(title: str, num: int) -> bool:
    """Heuristica para decidir se uma linha e titulo de hino (nao verso)."""
    if len(title) < 4:
        return False
    if num > 270:
        return True
    if title.isupper() or title.startswith(('\u201c', '"')):
        return True
    if len(title) > 15:
        return True
    return False


def _extract_hymns_from_pdf(pdf_path: Path) -> list[tuple[int, str, str]]:
    """Extrai hinos do PDF do HCC.

    Suporta tres padroes de cabecalho:
    - P1: NUMBER. HCC TITLE (hinos 1-269)
    - P2: NUMBER HCC TITLE (hinos 10-270)
    - P3: NUMBER. TITLE sem HCC (hinos 271-600+)

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
        stripped = line.strip()

        # Pattern 1: NUMBER. HCC TITLE
        m = _P1.match(stripped)
        if m:
            num = int(m.group(1))
            title = m.group(2).strip()
            if 1 <= num <= 610 and len(title) > 1:
                hymn_boundaries.append((num, idx, title))
                continue

        # Pattern 1b: NUMBER HCC. TITLE (HCC com ponto)
        m = _P1b.match(stripped)
        if m:
            num = int(m.group(1))
            title = m.group(2).strip()
            if 1 <= num <= 610 and len(title) > 1:
                hymn_boundaries.append((num, idx, title))
                continue

        # Pattern 2: NUMBER HCC TITLE (sem ponto)
        m = _P2.match(stripped)
        if m:
            num = int(m.group(1))
            title = m.group(2).strip()
            if 1 <= num <= 610 and len(title) > 1:
                hymn_boundaries.append((num, idx, title))
                continue

        # Pattern 3: NUMBER. TITLE (sem HCC)
        m = _P3.match(stripped)
        if m:
            num = int(m.group(1))
            title = m.group(2).strip()
            title = title.strip('"').strip('\u201c').strip('\u201d')
            if 1 <= num <= 610 and _is_likely_hymn_title(title, num):
                hymn_boundaries.append((num, idx, title))
                continue

        # Pattern 4: NUMBER TITLE (sem ponto, sem HCC, para numeros altos)
        m = _P4.match(stripped)
        if m:
            num = int(m.group(1))
            title = m.group(2).strip()
            title = title.strip('"').strip('\u201c').strip('\u201d')
            if 300 <= num <= 610 and _is_likely_hymn_title(title, num):
                hymn_boundaries.append((num, idx, title))

    # Deduplicar por numero, priorizando P1 > P2 > P3
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
            # Detectar cabecalho do hino
            if _P1.match(stripped) or _P1b.match(stripped) or _P2.match(stripped):
                found_header = True
                continue
            # P3: verificar se e numero seguido de titulo
            m = _P3.match(stripped)
            if m and 1 <= int(m.group(1)) <= 610:
                found_header = True
                continue
            # P4: verificar se e numero sem ponto seguido de titulo
            m = _P4.match(stripped)
            if m and 300 <= int(m.group(1)) <= 610:
                found_header = True
                continue
            continue
        if stripped:
            cleaned = re.sub(r"^\d+\.\s*", "", stripped)
            if cleaned:
                lyrics_lines.append(cleaned)

    if not lyrics_lines:
        return "", ""

    first_line = lyrics_lines[0] if lyrics_lines else ""
    lyrics = "\n".join(lyrics_lines)
    return lyrics, first_line


def import_hcc(pdf_path: Path) -> tuple[list[Hymn], AuditReport]:
    """Importa hinário HCC de um arquivo PDF.

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
                    arquivo=f"Hino {num}",
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
                arquivo=f"Hino {num}",
                motivo=f"Erro ao processar: {e}",
            ))

    report.hinos_criados = len(hinos)
    return hinos, report
