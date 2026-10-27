"""Importa métricas e melodias do índice de métricas do HCC (PDF).

O PDF (metricas_HCC.pdf) tem duas colunas por página. Cada coluna alterna
linhas de métrica ("8.7.8.7.D.", "Irregular com estribilho") e linhas de
hino ("60 HYMN TO JOY"). As palavras são agrupadas por coluna e por linha a
partir das coordenadas, o que evita misturar as colunas.
"""

import re
from pathlib import Path

from cantai.textnorm import fix_ocr

_METRIC = re.compile(r"^\(?\d+\.|^Irregular")
_ENTRY = re.compile(r"^(\d{1,3})\s*([A-ZÀ-Ü'\"].*)$")
# Lixo de OCR em minúsculas antes da métrica ("hodan 8.6.9.6.", "a 373 ...")
_LEADING_JUNK = re.compile(r"^(?:[a-zш]+\s+)+(?=[\d(A-Z])")


def _column_lines(words: list[tuple], left: bool, middle: float) -> list[str]:
    column = sorted((w for w in words if (w[0] < middle) == left), key=lambda w: w[1])
    lines: list[list] = []
    for word in column:
        if lines and abs(lines[-1][0] - word[1]) < 5:
            lines[-1][1].append((word[0], word[4]))
        else:
            lines.append([word[1], [(word[0], word[4])]])
    return [" ".join(t for _, t in sorted(ts)).strip() for _, ts in lines]


def import_hcc_metrics(pdf_path: str | Path) -> dict[int, list[tuple[str, str]]]:
    """Lê o índice de métricas do HCC.

    Returns:
        Dicionário número do hino -> lista de (métrica, melodia).
    """
    import pymupdf

    result: dict[int, list[tuple[str, str]]] = {}
    current: str | None = None
    last_was_metric = False

    with pymupdf.open(str(pdf_path)) as doc:
        for page in doc:
            words = page.get_text("words")
            middle = page.rect.width / 2
            for left in (True, False):
                for raw in _column_lines(words, left, middle):
                    line = _LEADING_JUNK.sub("", fix_ocr(raw))
                    if not line or line.startswith("ÍNDICE"):
                        continue
                    if _METRIC.match(line):
                        current, last_was_metric = line, True
                        continue
                    entry = _ENTRY.match(line)
                    if entry and current:
                        melody = re.sub(r"(?<=[A-Z])\.[.\d]+$", "", entry.group(2)).strip()
                        result.setdefault(int(entry.group(1)), []).append(
                            (_clean_metric(current), melody)
                        )
                        last_was_metric = False
                        continue
                    if re.fullmatch(r"\d+", line):
                        continue  # número de página
                    if current and last_was_metric:
                        current = f"{current} {line}"  # métrica em duas linhas

    return result


def _clean_metric(metric: str) -> str:
    metric = re.sub(r"\s+", " ", metric).strip()
    # A leitura por colunas às vezes inverte "com repetição"
    return re.sub(r"repetição com$", "com repetição", metric)
