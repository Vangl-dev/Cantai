"""Recupera o fim das letras do CTP cortadas na quebra de página.

O parser original do CTP parava no rodapé do PDF ("Hinário 1 - 136.pmd",
data, número da página): em 193 hinos o rodapé entrou na letra e o texto da
página seguinte se perdeu. Aqui, para cada hino afetado, a última linha boa
é localizada no PDF e as linhas depois do rodapé são recuperadas, até o
aviso de copyright ou o próximo hino.

O resultado (número do hino -> linhas recuperadas) fica em
data/base/ctp_continuacoes.json; o build remove o rodapé e acrescenta as
linhas, sem alterar data/base/ctp.json.
"""

import re
import unicodedata
from pathlib import Path

FOOTER = re.compile(
    r"^(Hinário \d+ ?- ?\d+\.pmd.*|\d{1,2}/\d{1,2}/\d{4},? \d{1,2}:\d{2}|\d{1,3})$"
)
_HEADER = re.compile(r"^\s*(\d{1,3})\s*[AB]?\s*-\s*(\S.*)$")
_MAX_LINES = 40


def _header_number(line: str) -> int | None:
    """Número do hino se a linha for um cabeçalho ("13- DEUS DOS ANTIGOS")."""
    match = _HEADER.match(line)
    if not match:
        return None
    letters = [c for c in match.group(2) if c.isalpha()]
    if len(letters) < 3 or sum(c.isupper() for c in letters) < 0.8 * len(letters):
        return None  # estrofe ("1- Deus dos antigos")
    return int(match.group(1))


def _key(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode()
    return re.sub(r"\W+", "", text.lower())


def has_footer(lyrics: str) -> bool:
    return any(FOOTER.match(line.strip()) for line in lyrics.split("\n"))


def strip_footer(lyrics: str) -> str:
    return "\n".join(ln for ln in lyrics.split("\n") if not FOOTER.match(ln.strip())).strip()


def import_ctp_continuations(pdf_path: str | Path, hymns: list[dict]) -> dict[str, list[str]]:
    """Linhas perdidas de cada hino com rodapé na letra.

    Args:
        pdf_path: PDF do hinário CTP.
        hymns: hinos de data/base/ctp.json.
    """
    import pymupdf

    with pymupdf.open(str(pdf_path)) as doc:
        lines = [ln.strip() for page in doc for ln in page.get_text().split("\n")]

    headers = [(i, n) for i, ln in enumerate(lines) if (n := _header_number(ln)) is not None]

    def region(number: int) -> tuple[int, int]:
        """Trecho do PDF entre o cabeçalho do hino e o do próximo."""
        starts = [i for i, n in headers if n == number]
        if not starts:
            return 0, len(lines)
        start = starts[0]
        end = next((i for i, n in headers if i > start and n != number), len(lines))
        return start, end

    def next_text(i: int) -> str:
        while i < len(lines) and not lines[i]:
            i += 1
        return lines[i] if i < len(lines) else ""

    result: dict[str, list[str]] = {}
    for hymn in hymns:
        if not has_footer(hymn["lyrics"]):
            continue
        clean = strip_footer(hymn["lyrics"]).split("\n")
        target = _key(clean[-1])
        start, end = region(hymn["number"])
        positions = [i for i in range(start, end) if _key(lines[i]) == target]
        positions = [i for i in positions if FOOTER.match(next_text(i + 1))] or positions
        if not positions:
            continue
        i = positions[-1] + 1
        recovered: list[str] = []
        while i < len(lines):
            line = lines[i]
            i += 1
            if not line or FOOTER.match(line):
                continue
            if line.startswith("©") or _header_number(line) is not None:
                break
            recovered.append(line)
        if len(recovered) > _MAX_LINES:
            continue  # passou do fim do hino; melhor não recuperar
        if recovered:
            result[str(hymn["number"]) + (hymn.get("variant") or "")] = recovered
    return result
