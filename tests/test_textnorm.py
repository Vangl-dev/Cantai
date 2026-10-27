"""Normalização de métricas, melodias e correções de OCR."""

import pytest

from cantai.textnorm import fix_ocr, melody_key, metric_key, strip_verse_number


@pytest.mark.parametrize(
    ("metric", "key"),
    [
        ("8.7.8.7.D", "8.7.8.7.8.7.8.7"),
        ("8.7.8.7.8.7.8.7.", "8.7.8.7.8.7.8.7"),
        ("6.6.8.6.D. (S.M.D.)", "6.6.8.6.6.6.8.6"),
        ("8.6.8.6. (C.M.,Common Meter)", "8.6.8.6"),
        ("8.7.8.7 - 7.7.8.7", "8.7.8.7"),
        ("8.7.8.7. com estribilho", "8.7.8.7"),
        ("(5.)8.(5.)8.8.8", "8.8.8.8"),
        ("C.M.", "8.6.8.6"),
        ("L.M.D.", "8.8.8.8.8.8.8.8"),
        ("Irregular", None),
        (None, None),
    ],
)
def test_metric_key(metric: str | None, key: str | None) -> None:
    assert metric_key(metric) == key


def test_melody_key_ignores_case_accents_and_alt() -> None:
    assert melody_key("Old Hundredth, alt.") == melody_key("OLD HUNDREDTH")
    assert melody_key("TRANQÜILIDADE") == "TRANQUILIDADE"


def test_melody_key_keeps_parenthesis() -> None:
    # Melodias homônimas são distintas
    assert melody_key("GENEVA (Lowden)") != melody_key("GENEVA (Day)")


def test_fix_ocr() -> None:
    assert fix_ocr("ALELUIA! JA CRElO") == "ALELUIA! JA CREIO"
    assert fix_ocr("Dá-Ihes virtude") == "Dá-lhes virtude"
    assert fix_ocr("NUN DANKEТ") == "NUN DANKET"  # T cirílico


def test_strip_verse_number() -> None:
    assert strip_verse_number("1- Deus dos antigos") == "Deus dos antigos"
    assert strip_verse_number("2. Cristo nos tem") == "Cristo nos tem"
    assert strip_verse_number("Deus prometeu") == "Deus prometeu"
