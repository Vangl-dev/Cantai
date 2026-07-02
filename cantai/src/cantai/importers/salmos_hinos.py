"""Importador do hinário Salmos e Hinos (SH).

Suporta tanto o PDF da Coletânea original quanto o novo PDF completo.
Formato do novo PDF: "NUM TITLE" (ex: "1 O Servo do Senhor"),
seguido de "SALMO N", versículo bíblico, e depois a letra.
"""

import re
from pathlib import Path

from cantai.schemas import AuditIssue, AuditReport, Hymn

_HYMNAL = "SH"
_SH_PATTERN = re.compile(r"^(.+?)\s+S\.?\s*H\.?\s+(\d+[A-Z]?)\s*$")
_SH_PATTERN_ALT = re.compile(r"^(.+?)\s+SH\s+(\d+[A-Z]?)\s*$")
_SH_PATTERN_NUM = re.compile(r"^(\d+[A-Z]?)\s+(.+?)$")
_SH_SALMO_LINE = re.compile(r"^SALMO\s+\d+", re.IGNORECASE)
_VERSE_PATTERN = re.compile(r"^\d+[\.\s]")
_AUTHOR_PATTERN = re.compile(
    r"^\(?\d{4}\)?|^[A-Z][a-z]+\s+[A-Z]|^Sarah|^W\.\s*H\.|^F\.",
    re.IGNORECASE,
)
_CHORUS_PATTERN = re.compile(r"^\*|refr[ãa]o|chorus", re.IGNORECASE)


def _extract_hymns_from_pdf(pdf_path: Path) -> list[tuple[int, str, str]]:
    """Extrai hinos do PDF de Salmos e Hinos.

    Formato do novo PDF completo:
        NUM TITLE
        SALMO N
        "... versículo bíblico"
        1. Primeira linha do verso
        ...
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
        stripped = line.strip()
        num = None
        title = None

        m = _SH_PATTERN.match(stripped)
        if m:
            title = m.group(1).strip()
            num_str = m.group(2)
            try:
                num = int(re.sub(r"[A-Z]", "", num_str))
            except ValueError:
                continue
        else:
            m = _SH_PATTERN_ALT.match(stripped)
            if m:
                title = m.group(1).strip()
                num_str = m.group(2)
                try:
                    num = int(re.sub(r"[A-Z]", "", num_str))
                except ValueError:
                    continue
            else:
                m = _SH_PATTERN_NUM.match(stripped)
                if m:
                    num_str = m.group(1)
                    candidate_title = m.group(2).strip()
                    try:
                        num = int(re.sub(r"[A-Z]", "", num_str))
                    except ValueError:
                        continue
                    if candidate_title and not _SH_SALMO_LINE.match(candidate_title):
                        title = candidate_title

        if num is not None and title and 1 <= num <= 700:
            is_real = False
            for j in range(idx + 1, min(idx + 15, len(lines))):
                next_line = lines[j].strip()
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
            if _SH_PATTERN.match(stripped) or _SH_PATTERN_ALT.match(stripped):
                found_header = True
                continue
            m = _SH_PATTERN_NUM.match(stripped)
            if m:
                found_header = True
                continue
            if _VERSE_PATTERN.match(stripped):
                found_header = True
        if found_header and stripped:
            if _SH_SALMO_LINE.match(stripped):
                continue
            first_char = stripped[0] if stripped else ""
            if first_char in ('"', "\u201c", "\u201d", "\u2018", "\u2019"):
                continue
            if stripped.startswith("..."):
                continue
            if _AUTHOR_PATTERN.match(stripped):
                continue
            if stripped.upper() == "COROS":
                continue
            cleaned = re.sub(r"^\d+[\.\s]+", "", stripped)
            if not _CHORUS_PATTERN.match(cleaned):
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
