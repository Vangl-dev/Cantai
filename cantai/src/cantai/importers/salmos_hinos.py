"""Importador do hinário Salmos e Hinos (SH)."""

import re
from pathlib import Path

from cantai.schemas import AuditIssue, AuditReport, Hymn

_HYMNAL = "SH"
_SH_PATTERN = re.compile(r"^(.+?)\s+S\.?\s*H\.?\s+(\d+[A-Z]?)\s*$")
_VERSE_PATTERN = re.compile(r"^\d+[\.\s]")


def _extract_hymns_from_pdf(pdf_path: Path) -> list[tuple[int, str, str]]:
    """Extrai hinos do PDF da Coletânea de Salmos e Hinos.

    O PDF tem sumário (páginas 1-4) seguido dos hinos.
    O sumário contém o padrão S.H. mas sem letras abaixo.
    Identificamos hinos reais verificando se a próxima linha é verso.
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

    hymn_starts: list[tuple[int, int, str]] = []
    for idx, line in enumerate(lines):
        m = _SH_PATTERN.match(line.strip())
        if m:
            title = m.group(1).strip()
            num_str = m.group(2)
            try:
                num = int(re.sub(r"[A-Z]", "", num_str))
            except ValueError:
                continue
            if 1 <= num <= 700:
                is_real = False
                for j in range(idx + 1, min(idx + 5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line:
                        if _VERSE_PATTERN.match(next_line):
                            is_real = True
                        break
                if is_real:
                    hymn_starts.append((num, idx, title))

    seen: set[int] = set()
    unique: list[tuple[int, int, str]] = []
    for num, idx, title in hymn_starts:
        if num not in seen:
            seen.add(num)
            unique.append((num, idx, title))

    results: list[tuple[int, str, str]] = []
    for i, (num, start_idx, title) in enumerate(unique):
        end_idx = unique[i + 1][1] if i + 1 < len(unique) else len(lines)
        hymn_text = "\n".join(lines[start_idx:end_idx])
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
            if _SH_PATTERN.match(stripped):
                found_header = True
            continue
        if stripped:
            cleaned = re.sub(r"^\d+[\.\s]+", "", stripped)
            lyrics_lines.append(cleaned)

    if not lyrics_lines:
        return "", ""

    first_line = lyrics_lines[0]
    lyrics = "\n".join(lyrics_lines)
    return lyrics, first_line


def import_salmos_hinos(pdf_path: Path) -> tuple[list[Hymn], AuditReport]:
    """Importa hinário Salmos e Hinos de um arquivo PDF.

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
                    arquivo=f"Hino SH {num}",
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
                arquivo=f"Hino SH {num}",
                motivo=f"Erro ao processar: {e}",
            ))

    report.hinos_criados = len(hinos)
    return hinos, report
