"""Importa a Harpa Cristã (HC) do PDF e os temas do índice de assuntos.

Formato do PDF ("HARPA CRISTÃ.pdf"):

    1. CHUVAS DE GRAÇA
    1 Deus prometeu com certeza,
    Chuvas de graça mandar;
    CHUVAS DE GRAÇA,            <- coro em maiúsculas
    ...
    Do santo Preceptor.    J.R. <- iniciais do autor no fim

O parser é sequencial: espera sempre o hino seguinte (n+1). Isso contorna
os defeitos do PDF: cabeçalhos sem ponto ("117 O SENHOR..."), número trocado
pelo OCR ("442." no lugar de "542.") e blocos repetidos (200 e 201 aparecem
duas vezes).
"""

import re
from pathlib import Path

from cantai.textnorm import fix_ocr, strip_verse_number

HYMNAL = "HC"
TOTAL = 640

_HEADER = re.compile(r"^\s*(\d{1,3})\s*(?:[.\-–]\s*|\s+)(\S.*)$")
# Iniciais de autor no fim da última linha ("    J.R.", " H.M.W.", "F.L.C./S.E.M’N")
_INITIALS = r"(?:[A-ZÀ-Ü][a-z]?\.\s?){2,}[A-ZÀ-Üa-z.’'/ ]*"
_AUTHOR = re.compile(r"\s+" + _INITIALS + r"$")
_AUTHOR_LINE = re.compile(r"^\s*" + _INITIALS + r"$")
_STANZA = re.compile(r"^\s*(\d{1,2})\s*\.?\s+\S")


def _is_upper(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and sum(c.isupper() for c in letters) >= 0.8 * len(letters)


def _looks_like_header(line: str) -> bool:
    match = _HEADER.match(line)
    return bool(match) and _is_upper(match.group(2)) and len(match.group(2)) > 2


def _is_ocr_typo(number: int, expected: int) -> bool:
    """Número com um só dígito trocado pelo OCR (442 no lugar de 542)."""
    a, b = str(number), str(expected)
    return expected >= 100 and len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1


def split_hymns(text: str) -> list[tuple[int, str, list[str]]]:
    """Divide o texto do PDF em (número, título, linhas)."""
    # Cabeçalho quebrado em duas linhas: "61." / "DEUS TOMARÁ CONTA DE TI"
    text = re.sub(r"(?m)^(\s*\d{1,3}\.)\s*\n\s*(?=[A-ZÀ-Ü\"“])", r"\1 ", text)
    lines = text.split("\n")

    candidates: list[tuple[int, int, str]] = []
    for idx, line in enumerate(lines):
        match = _HEADER.match(line)
        if match and _looks_like_header(line):
            candidates.append((idx, int(match.group(1)), match.group(2)))

    def next_index(number: int, after: int) -> int | None:
        return next((i for i, n, _ in candidates if n == number and i > after), None)

    # Escolhe a sequência 1, 2, 3... em ordem. O cabeçalho de n só vale se
    # vier antes do de n+1; um número com erro de OCR só é aceito quando o
    # cabeçalho certo não existe nesse trecho.
    accepted: list[tuple[int, int, str]] = []
    position = -1
    for number in range(1, TOTAL + 1):
        limit = next_index(number + 1, position)
        found = next(
            (c for c in candidates if c[1] == number and position < c[0] < (limit or len(lines))),
            None,
        )
        if found is None and limit is not None:
            found = next(
                (
                    c
                    for c in candidates
                    if position < c[0] < limit
                    and _is_ocr_typo(c[1], number)
                    and re.match(r"^\s*\d{3}\.", lines[c[0]])
                ),
                None,
            )
        if found is None:
            continue  # hino ausente no PDF
        accepted.append((found[0], number, found[2]))
        position = found[0]

    hymns: list[tuple[int, str, list[str]]] = []
    titles: set[str] = set()
    for k, (idx, number, raw_title) in enumerate(accepted):
        end = accepted[k + 1][0] if k + 1 < len(accepted) else len(lines)
        body = lines[idx + 1 : end]
        # Bloco repetido no PDF: corta no cabeçalho de um hino já visto
        for j, line in enumerate(body):
            match = _HEADER.match(line)
            if match and _looks_like_header(line) and fix_ocr(match.group(2)).strip() in titles:
                body = body[:j]
                break
        title = fix_ocr(raw_title).strip().strip('"“”').strip()
        titles.add(title)
        hymns.append((number, title, body))
    return hymns


def format_lyrics(lines: list[str]) -> str:
    """Organiza as linhas em estrofes e coro, sem iniciais de autor."""
    paragraphs: list[list[str]] = []
    previous_upper: bool | None = None
    for raw in lines:
        if _AUTHOR_LINE.match(raw):
            continue
        line = _AUTHOR.sub("", raw).rstrip()
        line = fix_ocr(line).strip()
        line = re.sub(r"^((?:\d{1,2}\.?\s*)?)0(?=\s+[A-Za-zÀ-ÿ])", r"\1O", line)  # "0 Senhor"
        line = re.sub(r"^(\d{1,2})\.?\s*(?=[^\d\s])", r"\1 ", line)  # "1Já" -> "1 Já"
        if not line or re.fullmatch(r"[\d\s]+", line):
            continue
        if line.lower() in ("coro", "coro:"):
            paragraphs.append([])
            previous_upper = True
            continue
        upper = _is_upper(line)
        new_stanza = bool(_STANZA.match(line))
        if not paragraphs or new_stanza or (previous_upper is not None and upper != previous_upper):
            paragraphs.append([])
        paragraphs[-1].append(line)
        previous_upper = upper
    return "\n\n".join("\n".join(p) for p in paragraphs if p)


def parse_harpa_text(text: str) -> list[dict]:
    """Converte o texto do PDF em hinos no formato de base."""
    hymns = []
    for number, title, lines in split_hymns(text):
        lyrics = format_lyrics(lines)
        first = next((ln for ln in lyrics.split("\n") if ln.strip()), "")
        hymns.append(
            {
                "number": number,
                "title": title,
                "first_line": strip_verse_number(first),
                "lyrics": lyrics,
                "topics": [],
            }
        )
    return hymns


def import_harpa(pdf_path: str | Path, themes_path: str | Path | None = None) -> list[dict]:
    """Importa a Harpa Cristã do PDF (e os temas, se o índice for informado)."""
    import pymupdf

    with pymupdf.open(str(pdf_path)) as doc:
        text = "\n".join(page.get_text() for page in doc)
    hymns = parse_harpa_text(text)
    if themes_path:
        themes = import_harpa_themes(themes_path)
        for hymn in hymns:
            hymn["topics"] = themes.get(hymn["number"], [])
    return hymns


def import_harpa_themes(md_path: str | Path) -> dict[int, list[str]]:
    """Lê o índice de assuntos da Harpa (temas_harpa_crista.md).

    Os temas seguem o padrão do canonical_topics.yaml: subtemas de "DEUS, O
    FILHO" viram "DEUS, O FILHO: Louvores"; os demais usam o próprio nome.
    """
    text = Path(md_path).read_text(encoding="utf-8")
    text = re.sub(r"</td><td>", " ", text)
    text = re.sub(r"</tr>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)

    result: dict[int, list[str]] = {}
    section: str | None = None
    topic: str | None = None
    for raw in text.split("\n"):
        line = re.sub(r"^#+\s*", "", raw.strip())
        if not line or line.upper().startswith("ÍNDICE"):
            continue
        entry = re.match(r"^(.+?)\s+(\d{1,3})\s*$", line)
        if entry:
            if topic:
                result.setdefault(int(entry.group(2)), [])
                if topic not in result[int(entry.group(2))]:
                    result[int(entry.group(2))].append(topic)
            continue
        name = line.rstrip(":").strip()
        if not _is_upper(name) and not line.endswith(":"):
            continue  # entrada do índice que perdeu o número no OCR
        if _is_upper(name):
            section, topic = name, name
        elif section == "DEUS, O FILHO" and name == "Louvores":
            topic = f"{section}: {name}"
        else:
            topic = name
    return result
