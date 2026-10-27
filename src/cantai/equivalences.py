"""Detecta o mesmo hino em hinários diferentes.

A comparação é feita pelo texto: sequências de 3 palavras normalizadas
(sem acento, pontuação nem números de estrofe). A similaridade é a fração
das sequências do hino mais curto que aparecem no outro, o que tolera
hinários que trazem só parte das estrofes.

Traduções diferentes do mesmo hino original não são detectadas por aqui,
pois o texto é outro; para isso servem a melodia e a métrica.
"""

import re
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from cantai.textnorm import normalize_words, strip_verse_number

CONFIRMED = 0.5
PROBABLE = 0.3
_MIN_SHARED = 4


def shingles(lyrics: str, size: int = 3) -> set[tuple[str, ...]]:
    """Sequências de `size` palavras do texto do hino."""
    words: list[str] = []
    for line in lyrics.split("\n"):
        words.extend(normalize_words(strip_verse_number(line)))
    return {tuple(words[i : i + size]) for i in range(len(words) - size + 1)}


def openings(hymn: dict, size: int = 4) -> set[tuple[str, ...]]:
    """Primeiras palavras do título, da primeira linha e das linhas iniciais.

    As linhas iniciais cobrem o HCC, que abre com uma citação bíblica antes
    da letra.
    """
    texts = [hymn.get("title") or "", hymn.get("first_line") or ""]
    texts += (hymn.get("lyrics") or "").split("\n")[:8]
    result = set()
    for text in texts:
        words = normalize_words(strip_verse_number(text))
        if len(words) >= size:
            result.add(tuple(words[:size]))
    return result


def similarity(a: set, b: set) -> float:
    """Fração das sequências do texto menor presentes no maior."""
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def find_pairs(hymns: Iterable[dict]) -> dict[tuple[str, str], float]:
    """Pares (id_a, id_b) de hinários diferentes com similaridade >= PROBABLE."""
    sets = {h["id"]: shingles(h.get("lyrics") or "") for h in hymns}
    hymnal = {hid: hid.split("-")[0] for hid in sets}

    # Sequências muito comuns ("aleluia aleluia aleluia") não identificam hino
    index: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for hid, items in sets.items():
        for item in items:
            index[item].append(hid)

    shared: dict[tuple[str, str], int] = defaultdict(int)
    for ids in index.values():
        if len(ids) > 40:
            continue
        for i, a in enumerate(ids):
            for b in ids[i + 1 :]:
                if hymnal[a] != hymnal[b]:
                    shared[(a, b) if a < b else (b, a)] += 1

    pairs: dict[tuple[str, str], float] = {}
    for (a, b), count in shared.items():
        if count < _MIN_SHARED:
            continue
        score = similarity(sets[a], sets[b])
        if score >= PROBABLE:
            pairs[(a, b)] = round(score, 3)
    return pairs


def parse_official_ctp_sh(md_path: str | Path) -> list[tuple[int, str, int]]:
    """Lê o índice oficial CTP x SH ("52 A Deus demos glória ....SH 233")."""
    result = []
    for line in Path(md_path).read_text(encoding="utf-8").split("\n"):
        match = re.match(r"^\s*(\d{1,3})\s+(.+?)\s*\.{2,}\s*SH\s*(\d{1,3})\s*$", line)
        if match:
            result.append((int(match.group(1)), match.group(2), int(match.group(3))))
    return result


class _Groups:
    """Grupos de hinos equivalentes, no máximo um hino por hinário."""

    def __init__(self) -> None:
        self.group: dict[str, set[str]] = {}

    def members(self, x: str) -> set[str]:
        return self.group.get(x, {x})

    def try_union(self, a: str, b: str) -> bool:
        ga, gb = self.members(a), self.members(b)
        if ga is gb:
            return True
        if {m.split("-")[0] for m in ga} & {m.split("-")[0] for m in gb}:
            return False  # juntaria dois hinos do mesmo hinário
        merged = ga | gb
        for m in merged:
            self.group[m] = merged
        return True


def build_equivalences(
    hymns: list[dict],
    manual: list[tuple[str, str, str]],
) -> dict[str, list[dict]]:
    """Monta o mapa id -> hinos equivalentes.

    Args:
        hymns: todos os hinos (formato unificado, com "id" e "lyrics").
        manual: pares já conhecidos (id_a, id_b, motivo), como o índice oficial
            CTP x SH e as equivalências conferidas do HCC.

    Returns:
        Para cada hino com equivalentes, a lista de
        {"id", "confianca": "confirmada"|"provável", "motivo", "similaridade"}.
        Hinos ligados por equivalências confirmadas formam um grupo (no máximo
        um hino por hinário, unindo primeiro as ligações mais fortes); todos os
        membros do grupo aparecem uns para os outros. Uma ligação confirmada
        que não coube no grupo continua valendo só entre os dois hinos.
    """
    by_id = {h["id"]: h for h in hymns}
    ids = set(by_id)
    pairs = find_pairs(hymns)

    direct: dict[tuple[str, str], tuple[str, str, float | None]] = {}
    for (a, b), score in pairs.items():
        reason = f"texto {round(score * 100)}% igual"
        if score >= CONFIRMED:
            level = "confirmada"
        elif openings(by_id[a]) & openings(by_id[b]):
            # Tradução revisada: texto parecido e mesmo início
            level, reason = "confirmada", reason + " e mesmo início"
        else:
            level = "provável"
        direct[(a, b)] = (level, reason, score)
    strong: dict[str, set[str]] = defaultdict(set)
    for (a, b), score in pairs.items():
        if score >= 0.8:
            strong[a].add(b)
            strong[b].add(a)

    def contradicted(a: str, b: str) -> bool:
        """Par manual desmentido por texto quase idêntico a outro hino."""
        for x, y in ((a, b), (b, a)):
            hymnal = y.split("-")[0]
            if any(o.split("-")[0] == hymnal and o != y for o in strong[x]):
                return True
        return False

    for a, b, reason in manual:
        if a in ids and b in ids and not contradicted(a, b):
            key = (a, b) if a < b else (b, a)
            direct[key] = ("confirmada", reason, pairs.get(key))

    def strength(item: tuple) -> tuple:
        (_, _), (_, reason, score) = item
        official = not reason.startswith("texto")
        return (-(score or 0) if (score or 0) >= 0.8 else 0, not official, -(score or 0))

    groups = _Groups()
    for (a, b), _ in sorted(
        ((k, v) for k, v in direct.items() if v[0] == "confirmada"), key=strength
    ):
        groups.try_union(a, b)

    result: dict[str, dict[str, dict]] = defaultdict(dict)
    seen_groups: list[set[str]] = []
    for group in groups.group.values():
        if any(group is g for g in seen_groups):
            continue
        seen_groups.append(group)
        for a in group:
            for b in group:
                if a == b:
                    continue
                info = direct.get((a, b) if a < b else (b, a))
                if info:
                    level, reason, score = info
                else:
                    level, reason, score = "confirmada", "mesmo grupo de hinos", None
                result[a][b] = {"id": b, "confianca": level, "motivo": reason,
                                "similaridade": score}
    for (a, b), (level, reason, score) in direct.items():
        for x, y in ((a, b), (b, a)):
            result[x].setdefault(y, {"id": y, "confianca": level, "motivo": reason,
                                     "similaridade": score})

    order = {"CTP": 0, "SH": 1, "HCC": 2, "HC": 3, "NC": 4}
    return {
        hid: sorted(
            items.values(),
            key=lambda e: (e["confianca"] != "confirmada", order.get(e["id"].split("-")[0], 9)),
        )
        for hid, items in sorted(result.items())
    }
