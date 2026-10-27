"""Importadores: casos que já quebraram antes."""

from pathlib import Path

from cantai.importers.harpa import format_lyrics, import_harpa_themes, split_hymns
from cantai.importers.metrics import import_metrics
from cantai.importers.novo_cantico import section_for


def test_ctp_metrics_plain_metric_lines(tmp_path: Path) -> None:
    """Métrica sem "## " não pode herdar a métrica anterior (bug dos 69 hinos)."""
    md = tmp_path / "m.md"
    md.write_text(
        "## 8.8.8.6 - 6.6.8.6\n\n"
        "TAKE ME AS I AM 205\n\n"
        "![image](x.jpg)\n\n"
        "8.8.8.7\n"
        "A LA RU ..... 341\n"
        "8.8.8.8\n"
        "OLD HUNDREDTH ..... 30, 488\n",
        encoding="utf-8",
    )
    data = import_metrics(md)
    assert data["205"] == [("8.8.8.6 - 6.6.8.6", "TAKE ME AS I AM")]
    assert data["341"] == [("8.8.8.7", "A LA RU")]
    assert data["30"] == [("8.8.8.8", "OLD HUNDREDTH")]
    assert data["488"] == [("8.8.8.8", "OLD HUNDREDTH")]


def test_ctp_metrics_tables_garbage_and_merged_lines(tmp_path: Path) -> None:
    md = tmp_path / "m.md"
    md.write_text(
        "## 6.6.6.6 - 4.4.4.4\n"
        "0.0.0.0 - 4.4.4.4\n"
        "<table><tr><td>MELODIA X</td><td>12</td></tr></table>\n"
        "8.7.8.7.8.7.[8.7] com estribilho PÃO E VINHO 258\n",
        encoding="utf-8",
    )
    data = import_metrics(md)
    assert data["12"] == [("6.6.6.6 - 4.4.4.4", "MELODIA X")]
    assert data["258"] == [("8.7.8.7.8.7.[8.7] com estribilho", "PÃO E VINHO")]


def test_harpa_split_handles_pdf_defects() -> None:
    text = "\n".join(
        [
            "1. PRIMEIRO",
            "1 Letra um",
            "2 TÍTULO SEM PONTO",  # cabeçalho sem ponto
            "1 Letra dois",
            "3.",  # cabeçalho quebrado em duas linhas
            "TERCEIRO",
            "1 Letra três",
            "2. TÍTULO SEM PONTO",  # bloco repetido no PDF
            "1 Letra dois",
            "4. QUARTO",
            "1 Letra quatro",
        ]
    )
    hymns = split_hymns(text)
    assert [(n, t) for n, t, _ in hymns[:4]] == [
        (1, "PRIMEIRO"),
        (2, "TÍTULO SEM PONTO"),
        (3, "TERCEIRO"),
        (4, "QUARTO"),
    ]
    assert hymns[2][2] == ["1 Letra três"]


def test_harpa_ocr_typo_number_accepted_only_when_missing() -> None:
    lines = []
    for n in range(538, 545):
        header = "442. HISTÓRIA" if n == 542 else f"{n}. HINO {n}"
        lines += [header, "1 Letra"]
    numbers = [n for n, _, _ in split_hymns("\n".join(["441. ANTERIOR", "1 x", "442. OUTRO", "1 y"] + lines))]
    assert 542 in numbers


def test_harpa_lyrics_without_author_initials() -> None:
    lyrics = format_lyrics(["1 Deus prometeu", "Do santo Preceptor.    J.R.", "F.L.C./S.E.M’N"])
    assert "J.R." not in lyrics and "F.L.C" not in lyrics
    assert lyrics.endswith("Do santo Preceptor.")


def test_harpa_themes_ignore_entries_without_number(tmp_path: Path) -> None:
    md = tmp_path / "t.md"
    md.write_text(
        "## DEUS, O FILHO:\n## Louvores:\nA Cristo coroai! 41\n"
        "Apelo:\nCristo já nos preparou\nCristo te chama 301\n",
        encoding="utf-8",
    )
    themes = import_harpa_themes(md)
    assert themes[41] == ["DEUS, O FILHO: Louvores"]
    assert themes[301] == ["Apelo"]


def test_nc_sections() -> None:
    assert section_for(1) == "Intróitos"
    assert section_for(155) == "Proteção"
    assert section_for(237, "A") == "Natal"
    assert section_for(400) == "Final de Culto"
    assert section_for(400, "A") == "Ofertório e Améns"
