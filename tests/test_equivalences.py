"""Regras de equivalência entre hinários."""

from cantai.equivalences import build_equivalences, shingles, similarity

LYRICS_A = (
    "Conta-me a história de Cristo, grava-a no meu coração;\n"
    "conta-me a história preciosa, a mais divinal canção."
)
LYRICS_B = (
    "Conta-me a velha história do grande salvador\n"
    "que deixou o céu de glória por nos ter tanto amor."
)


def hymn(hid: str, lyrics: str) -> dict:
    return {"id": hid, "title": hid, "first_line": lyrics.split("\n")[0], "lyrics": lyrics}


def test_similarity_ignores_verse_numbers_and_accents() -> None:
    a = shingles("1- Grandioso és tu, Senhor do céu e da terra")
    b = shingles("Grandioso es Tu, senhor do ceu e da terra")
    assert similarity(a, b) == 1.0


def test_manual_pair_contradicted_by_identical_text_is_dropped() -> None:
    """Índice oficial com par cruzado não vence texto 100% igual."""
    hymns = [
        hymn("CTP-109", LYRICS_A),
        hymn("CTP-111", LYRICS_B),
        hymn("SH-95", LYRICS_A),
        hymn("SH-94", LYRICS_B),
    ]
    manual = [("CTP-109", "SH-94", "índice"), ("CTP-111", "SH-95", "índice")]
    result = build_equivalences(hymns, manual)
    assert [e["id"] for e in result["CTP-109"]] == ["SH-95"]
    assert [e["id"] for e in result["CTP-111"]] == ["SH-94"]


def test_group_has_at_most_one_hymn_per_hymnal() -> None:
    hymns = [hymn("CTP-1", LYRICS_A), hymn("SH-1", LYRICS_A), hymn("SH-2", LYRICS_A)]
    result = build_equivalences(hymns, [])
    # Os dois SH são equivalentes diretos do CTP, mas não entre si
    assert {e["id"] for e in result["CTP-1"]} == {"SH-1", "SH-2"}
    assert all(not e["id"].startswith("SH") for e in result["SH-1"])


def test_equivalences_are_symmetric() -> None:
    hymns = [hymn("CTP-1", LYRICS_A), hymn("NC-5", LYRICS_A)]
    result = build_equivalences(hymns, [])
    assert result["CTP-1"][0]["id"] == "NC-5"
    assert result["NC-5"][0]["id"] == "CTP-1"
