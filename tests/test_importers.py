"""Importadores: casos que já quebraram antes."""

from pathlib import Path

from cantai.importers.celebration import (
    choose_meter,
    looks_like_first_line,
    normalize_meter,
    parse_topical_index,
    parse_tune_index,
    split_key,
)
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


def test_celebration_meters() -> None:
    assert normalize_meter("C.M. with Refrain") == "8.6.8.6. (C.M.) com estribilho"
    assert normalize_meter("Long Meter L.M. (8.8.8.8.)") == "8.8.8.8. (L.M.)"
    assert normalize_meter("(C.M.D.)") == "8.6.8.6.8.6.8.6. (C.M.D.)"
    assert normalize_meter("8.7.8.7.1D.") == "8.7.8.7.D."  # OCR
    assert normalize_meter("8.7.87.") == "8.7.8.7."  # OCR perdeu um ponto
    assert normalize_meter("7.7.7.7.D. w/Ret.") == "7.7.7.7.D. com estribilho"
    assert normalize_meter("lrreg.") == "Irregular"
    assert choose_meter("8.8.85.", "8.8.8.5") == "8.8.8.5"
    assert choose_meter("Irreg.", None) == "Irreg."
    assert choose_meter("C.M.", "GOLDEN CHAIN (REFRAIN") == "C.M."


def test_celebration_tune_index_lines() -> None:
    lines = [
        "AZMON (CM.), 21, 221, 650",
        "HYMN TO JOY (8.7.8.7.D.), 90, 271, 365 1 AM THINE (10.7.10.7. w/Ref.), 552",
        "LONDONDERRY AIR",
        "(11.10.11.10.11.10.11.12.), 354",
        "ADESTE FIDELES (Ref. only), (7.7.10.),",
        "196, 247",
        "CARMICHAEL (11.7.11.7. w/Ref.), 483 ©",
    ]
    tunes = parse_tune_index(lines)
    assert tunes[221] == ("AZMON", "CM.")
    assert tunes[365][0] == "HYMN TO JOY"
    assert tunes[552][0] == "I AM THINE"
    assert tunes[354][0] == "LONDONDERRY AIR"
    assert tunes[247] == ("ADESTE FIDELES", "7.7.10. (Ref. only)")
    assert tunes[483][0] == "CARMICHAEL"


def test_celebration_topical_index_headings() -> None:
    lines = [
        "When I Survey the Wondrous Cross,",
        "324",
        "CHRIST — Atonement, Crucifixion,",
        "Suffering and Death",
        "Amazing Grace, 343",
        "COMFORT AND",
        "ENCOURAGEMENT",
        "A Mighty Fortress Is Our God, 151",
    ]
    topics, titles = parse_topical_index(lines)
    assert topics[343] == ["CHRIST — Atonement, Crucifixion, Suffering and Death"]
    assert topics[151] == ["COMFORT AND ENCOURAGEMENT"]
    assert titles["amazinggrace"] == {343}


def test_celebration_song_entries() -> None:
    assert split_key("Amazing Grace (G/Ab)") == ("Amazing Grace", "G/Ab")
    assert split_key("Sing unto the Lord (FENDER) (d min.)") == ("Sing unto the Lord (FENDER)", "d min.")
    assert looks_like_first_line("A pilgrim was I, and a wand'ring")
    assert not looks_like_first_line("A Mighty Fortress Is Our God")
