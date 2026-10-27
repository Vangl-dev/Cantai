"""Importa métricas e melodias do índice de métricas do CTP (markdown).

O arquivo HinarioCTP_metricas.md veio de OCR e é irregular: algumas métricas
estão em cabeçalhos "## ", outras em linhas soltas; há tabelas HTML, linhas
com vários hinos ("OLD HUNDREDTH ..... 30, 488") e métricas coladas com a
melodia na mesma linha. A versão anterior deste importador só reconhecia
"## " e, ao pular as demais métricas, aplicava a métrica anterior a dezenas
de hinos (69 hinos ficaram com "8.8.8.6 - 6.6.8.6").
"""

import re
from pathlib import Path

_METRIC_START = re.compile(r"^[\(\[]?\d+[\.\]\)]")
_NUMBERS = r"(\d{1,3}\s*[A-Ba-b]?(?:\s*[,;e]\s*\d{1,3}\s*[A-Ba-b]?)*)\s*$"
_ENTRY = re.compile(r"^(.+?)\s*\.*\s*" + _NUMBERS)
_METRIC_WITH_ENTRY = re.compile(
    r"^(.*?(?:com [a-zçãé ]+?|irregular)?)\s+"
    r"([A-ZÀ-Ü][A-ZÀ-Ü'’ .,!-]+?)\s*\.*\s*" + _NUMBERS
)
_SKIP_HEADERS = ("indice", "índice", "métrica", "metrica")


def _is_garbage_metric(metric: str) -> bool:
    """Métricas com componente "0" são lixo de OCR ("0.0.0.0", "8.0.8.0")."""
    return any(part == "0" for part in re.findall(r"\d+", metric))


def import_metrics(metrics_path: str | Path) -> dict[str, list[tuple[str, str]]]:
    """Lê o índice de métricas do CTP.

    Args:
        metrics_path: Caminho do HinarioCTP_metricas.md

    Returns:
        Dicionário número do hino ("30", "314A") -> lista de (métrica, melodia).
        Um hino pode ter mais de uma melodia (melodias alternativas).
    """
    text = Path(metrics_path).read_text(encoding="utf-8")
    text = re.sub(r"</td><td>", " ", text)
    text = re.sub(r"</tr>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)

    result: dict[str, list[tuple[str, str]]] = {}
    current_metric: str | None = None

    for raw in text.split("\n"):
        line = raw.strip()
        if not line or line.startswith("!["):
            continue
        line = re.sub(r"^#+\s*", "", line)
        if line.lower().startswith(_SKIP_HEADERS):
            continue

        melody: str | None = None
        numbers: str | None = None
        if _METRIC_START.match(line):
            match = _METRIC_WITH_ENTRY.match(line)
            if match and re.search(r"[A-ZÀ-Ü]{3}", match.group(2)):
                metric, melody, numbers = (
                    match.group(1).strip(),
                    match.group(2).strip(),
                    match.group(3),
                )
            else:
                metric = line
            if not _is_garbage_metric(metric):
                current_metric = metric
            if not melody:
                continue
        else:
            match = _ENTRY.match(line)
            if not match:
                continue
            melody, numbers = match.group(1).strip(" ."), match.group(2)

        if current_metric is None or numbers is None:
            continue
        for number in re.findall(r"\d{1,3}\s*[A-Ba-b]?", numbers):
            key = re.sub(r"\s", "", number).upper()
            result.setdefault(key, []).append((current_metric, melody))

    return result
