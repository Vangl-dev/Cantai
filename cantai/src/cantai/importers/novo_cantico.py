"""Importador do hinário Novo Cântico (NC)."""

import re
from pathlib import Path

from cantai.schemas import AuditIssue, AuditReport, Hymn

_HYMNAL = "NC"
_NC_PATTERN = re.compile(r"^(\d+(?:-?[A-Z])?)\s+(.+)$")


def _extract_hymns_from_pdf(pdf_path: Path) -> list[tuple[str, str, str]]:
    """Extrai hinos do PDF do Novo Cântico.

    Formato: "NUMBER TITLE" seguido de letras.
    Página 1 é copyright e deve ser ignorada.
    """
    import pdfplumber

    pdf = pdfplumber.open(str(pdf_path))
    pages_text: list[str] = []
    for i, page in enumerate(pdf.pages):
        if i == 0:
            pages_text.append("")
            continue
        text = page.extract_text()
        pages_text.append(text or "")
    pdf.close()

    full_text = "\n".join(pages_text)
    lines = full_text.split("\n")

    hymn_starts: list[tuple[str, int, str]] = []
    for idx, line in enumerate(lines):
        m = _NC_PATTERN.match(line.strip())
        if m:
            num_str = m.group(1)
            title = m.group(2).strip()
            try:
                num = int(re.sub(r"[^0-9]", "", num_str))
            except ValueError:
                continue
            if 1 <= num <= 410 and 2 < len(title) < 100:
                is_real = False
                for j in range(idx + 1, min(idx + 3, len(lines))):
                    next_line = lines[j].strip()
                    if next_line:
                        if not re.match(r"^\d+(?:-?[A-Z])?$", next_line):
                            is_real = True
                        break
                if is_real:
                    hymn_starts.append((num_str, idx, title))

    seen: set[str] = set()
    unique: list[tuple[str, int, str]] = []
    for num_str, idx, title in hymn_starts:
        key = num_str.upper()
        if key not in seen:
            seen.add(key)
            unique.append((num_str, idx, title))

    results: list[tuple[str, str, str]] = []
    for i, (num_str, start_idx, title) in enumerate(unique):
        end_idx = unique[i + 1][1] if i + 1 < len(unique) else len(lines)
        hymn_text = "\n".join(lines[start_idx:end_idx])
        results.append((num_str, title, hymn_text))

    return results


def _parse_lyrics(hymn_text: str) -> tuple[str, str]:
    """Extrai letra e primeira linha do texto do hino."""
    lines = hymn_text.split("\n")

    lyrics_lines: list[str] = []
    found_header = False
    for line in lines:
        stripped = line.strip()
        if not found_header:
            if _NC_PATTERN.match(stripped):
                found_header = True
            continue
        if stripped:
            lyrics_lines.append(stripped)

    if not lyrics_lines:
        return "", ""

    first_line = lyrics_lines[0]
    lyrics = "\n".join(lyrics_lines)
    return lyrics, first_line


def import_novo_cantico(pdf_path: Path) -> tuple[list[Hymn], AuditReport]:
    """Importa hinário Novo Cântico de um arquivo PDF.

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
    for num_str, title, hymn_text in raw_hymns:
        report.processados += 1
        try:
            lyrics, first_line = _parse_lyrics(hymn_text)
            if not lyrics:
                report.ignorados.append(AuditIssue(
                    arquivo=f"Hino NC {num_str}",
                    motivo="Sem letra extraída",
                ))
                continue

            hinos.append(Hymn(
                hymnal=_HYMNAL,
                number=num_str,
                title=title,
                category=None,
                first_line=first_line,
                lyrics=lyrics,
                slide_count=0,
                source_file=pdf_path,
            ))
        except Exception as e:
            report.erros.append(AuditIssue(
                arquivo=f"Hino NC {num_str}",
                motivo=f"Erro ao processar: {e}",
            ))

    report.hinos_criados = len(hinos)
    return hinos, report
