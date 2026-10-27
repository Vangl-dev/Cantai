"""Proteção contra regressão dos dados publicados em web/data.

Se algum destes testes falhar depois de uma mudança, algo que já estava
certo foi desfeito.
"""

import json
from pathlib import Path

import pytest

from cantai.build import HYMNALS, build

PROJECT = Path(__file__).resolve().parents[1]
WEB_DATA = PROJECT / "web" / "data"

MINIMUM = {"CTP": 504, "HCC": 609, "SH": 621, "HC": 640, "NC": 405, "CE": 690}


@pytest.fixture(scope="module")
def hymns() -> dict[str, dict]:
    result = {}
    for code, info in HYMNALS.items():
        data = json.loads((WEB_DATA / "output" / info["output"]).read_text(encoding="utf-8"))
        assert data["hymnal"] == code
        for hymn in data["hymns"]:
            assert hymn["id"] not in result, f"id repetido: {hymn['id']}"
            result[hymn["id"]] = hymn
    return result


@pytest.fixture(scope="module")
def equivalences() -> dict[str, list[dict]]:
    return json.loads((WEB_DATA / "equivalencias.json").read_text(encoding="utf-8"))


def test_web_data_is_up_to_date(tmp_path: Path) -> None:
    """web/data precisa ser exatamente o resultado do build atual."""
    build(PROJECT, tmp_path)
    for path in tmp_path.rglob("*.json"):
        published = WEB_DATA / path.relative_to(tmp_path)
        assert published.exists(), f"faltando {published}"
        assert published.read_text(encoding="utf-8") == path.read_text(encoding="utf-8"), (
            f"{published.relative_to(PROJECT)} desatualizado: rode `cantai build`"
        )


@pytest.mark.parametrize(("code", "minimum"), MINIMUM.items())
def test_hymn_counts(hymns: dict[str, dict], code: str, minimum: int) -> None:
    assert sum(1 for h in hymns.values() if h["hymnal"] == code) >= minimum


def test_hymn_fields(hymns: dict[str, dict]) -> None:
    for hymn in hymns.values():
        assert hymn["title"].strip(), hymn["id"]
        assert hymn["metric"] is None or isinstance(hymn["metric"], str), hymn["id"]
        assert hymn["melody"] is None or isinstance(hymn["melody"], str), hymn["id"]
        assert not hymn["first_line"][:1].isdigit(), hymn["id"]


def test_ctp_variants(hymns: dict[str, dict]) -> None:
    for number in (30, 36, 314):
        assert f"CTP-{number}A" in hymns and f"CTP-{number}B" in hymns
    assert hymns["CTP-314B"]["first_line"].startswith("Os meus olhos viram")


def test_known_metrics_and_melodies(hymns: dict[str, dict]) -> None:
    assert hymns["CTP-36A"]["melody"] == "HYMN TO JOY"
    assert hymns["CTP-36A"]["metric_key"] == "8.7.8.7.8.7.8.7"
    assert hymns["CTP-30A"]["melody"] == "OLD HUNDREDTH"
    assert hymns["CTP-12"]["melody"] == "DUKE STREET"
    assert hymns["HCC-38"]["melody"] == "ST. ANNE"
    assert hymns["HCC-38"]["metric_key"] == "8.6.8.6"
    assert hymns["HCC-60"]["melody"] == "HYMN TO JOY"
    assert hymns["HCC-6"]["metric"] == "6.6.4.6.6.6.4."


def test_no_wrongly_propagated_ctp_metric(hymns: dict[str, dict]) -> None:
    """O importador antigo deu "8.8.8.6 - 6.6.8.6" a 69 hinos; só o 205 tem."""
    wrong = [
        h["id"] for h in hymns.values()
        if h["hymnal"] == "CTP" and h["metric"] == "8.8.8.6 - 6.6.8.6"
    ]
    assert wrong == ["CTP-205"]


def test_ctp_lyrics_without_pdf_footer(hymns: dict[str, dict]) -> None:
    """Rodapé do PDF fora da letra e fim da letra recuperado (CTP-13)."""
    for hymn in hymns.values():
        if hymn["hymnal"] == "CTP":
            assert ".pmd" not in hymn["lyrics"], hymn["id"]
    assert hymns["CTP-13"]["lyrics"].endswith("Com gratidão o teu eterno amor!")
    assert hymns["CTP-421"]["lyrics"].endswith("Pátria amada, Brasil!")


def test_sh_lyrics_are_clean(hymns: dict[str, dict]) -> None:
    for hymn in hymns.values():
        if hymn["hymnal"] == "SH":
            assert "\n- " not in hymn["lyrics"] or not any(
                line.strip("- ").isdigit() for line in hymn["lyrics"].split("\n") if line.startswith("- ")
            ), hymn["id"]
            assert not hymn["title"].endswith(" i"), hymn["id"]


def test_equivalences_resolve_and_are_symmetric(
    hymns: dict[str, dict], equivalences: dict[str, list[dict]]
) -> None:
    for hid, items in equivalences.items():
        assert hid in hymns
        for item in items:
            assert item["id"] in hymns
            assert any(back["id"] == hid for back in equivalences[item["id"]]), (hid, item["id"])


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("CTP-13", "SH-64"),  # índice oficial
        ("CTP-13", "HCC-34"),  # conferida no HCC
        ("CTP-94", "HC-526"),  # Grandioso és tu
        ("CTP-109", "SH-95"),
        ("CTP-111", "SH-94"),
        ("NC-155", "SH-640"),  # Castelo forte
    ],
)
def test_known_equivalences(equivalences: dict[str, list[dict]], a: str, b: str) -> None:
    confirmed = {e["id"] for e in equivalences.get(a, []) if e["confianca"] == "confirmada"}
    assert b in confirmed


def test_crossed_official_pairs_not_used(equivalences: dict[str, list[dict]]) -> None:
    assert "SH-94" not in {e["id"] for e in equivalences["CTP-109"]}


def test_inherited_metric_is_marked(hymns: dict[str, dict]) -> None:
    inherited = [h for h in hymns.values() if h["via"]]
    assert inherited
    for hymn in inherited:
        assert hymn["via"] in hymns
        assert hymns[hymn["via"]]["metric"] == hymn["metric"]


def test_every_canonical_theme_has_hymns(hymns: dict[str, dict]) -> None:
    topics = json.loads((WEB_DATA / "canonical_topics.json").read_text(encoding="utf-8"))
    used = {t for h in hymns.values() for t in h["topics_canonical"]}
    assert set(topics) <= used, set(topics) - used


def test_celebration_from_indexes(hymns: dict[str, dict]) -> None:
    """Celebration: dados conferidos nas páginas impressas dos índices."""
    assert hymns["CE-343"]["melody"] == "AMAZING GRACE"
    assert hymns["CE-343"]["key"] == "G/Ab"
    assert hymns["CE-343"]["metric_key"] == "8.6.8.6"
    assert hymns["CE-16"]["melody"] == "DIADEM" and hymns["CE-43"]["melody"] == "CORONATION"
    assert hymns["CE-221"]["title"] == "All Praise to Our Redeeming Lord"  # OCR leu "21"
    assert hymns["CE-324"]["key"] == "F/g min./Ab"
    assert "Natal" in hymns["CE-253"]["topics_canonical"]
    # A Mighty Fortress: mesma melodia do "Castelo forte" em português
    assert "EINFESTEBURG" in hymns["CE-151"]["melody_keys"]
    assert "EINFESTEBURG" in hymns["CTP-409"]["melody_keys"]


def test_celebration_has_no_lyrics_or_text_equivalences(
    hymns: dict[str, dict], equivalences: dict[str, list[dict]]
) -> None:
    for hymn in hymns.values():
        if hymn["hymnal"] == "CE":
            assert hymn["lyrics"] == "" and hymn["via"] is None
            assert hymn["id"] not in equivalences
