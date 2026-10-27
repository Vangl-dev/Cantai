"""Monta os dados publicados no site a partir de data/base.

Entradas (todas versionadas no git):
    data/base/ctp.json, hcc.json, sh.json  dados congelados dos hinários
    data/base/harpa.json, nc.json           gerados por `cantai importar-harpa`
                                            e `cantai importar-nc`
    data/base/ctp_metricas.json             gerado por `cantai importar-metricas`
    data/base/hcc_metricas.json             idem
    data/base/ctp_continuacoes.json         gerado por `cantai importar-continuacoes-ctp`
    data/canonical_topics.json              temas canônicos por hinário
    correspondencias ctp x sh.md            índice oficial CTP x SH

Saídas (web/data):
    output/<hinário>.json   hinos no formato unificado
    equivalencias.json      id -> hinos equivalentes
    canonical_topics.json   cópia dos temas canônicos

O build não altera data/base: rodá-lo de novo dá sempre o mesmo resultado.
"""

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from cantai.importers.ctp_continuations import has_footer, strip_footer
from cantai.equivalences import build_equivalences, parse_official_ctp_sh, shingles, similarity
from cantai.textnorm import melody_key, metric_key, split_melodies, strip_verse_number

HYMNALS: dict[str, dict[str, str]] = {
    "CTP": {"name": "Cantai Todos os Povos", "base": "ctp.json", "output": "cantai.json"},
    "HCC": {"name": "Hinário para o Culto Cristão", "base": "hcc.json", "output": "hcc.json"},
    "SH": {"name": "Salmos e Hinos", "base": "sh.json", "output": "sh.json"},
    "HC": {"name": "Harpa Cristã", "base": "harpa.json", "output": "harpa.json"},
    "NC": {"name": "Novo Cântico", "base": "nc.json", "output": "nc.json"},
}

# Ordem de preferência ao herdar métrica/melodia de um hino equivalente
_INHERIT_ORDER = ["CTP", "HCC", "SH", "HC", "NC"]


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def hymn_id(hymnal: str, number: int, variant: str | None) -> str:
    return f"{hymnal}-{number}{variant or ''}"


def _make(hymnal: str, raw: dict, **extra: Any) -> dict:
    hymn = {
        "id": hymn_id(hymnal, raw["number"], raw.get("variant")),
        "hymnal": hymnal,
        "number": raw["number"],
        "variant": raw.get("variant"),
        "title": raw["title"].strip(),
        "first_line": strip_verse_number(raw.get("first_line") or ""),
        "lyrics": raw.get("lyrics") or "",
        "topics": raw.get("topics") or [],
        "topics_canonical": [],
        "metric": None,
        "melody": None,
        "via": None,
    }
    hymn.update(extra)
    return hymn


def _metric_and_melody(entries: list) -> tuple[str | None, str | None]:
    if not entries:
        return None, None
    melodies: list[str] = []
    for _, melody in entries:
        if melody and melody not in melodies:
            melodies.append(melody)
    return entries[0][0], " / ".join(melodies) or None


# --- Normalização por hinário -------------------------------------------------


def assign_ctp_variants(raw_hymns: list[dict]) -> list[dict]:
    """Números repetidos no CTP (30, 36, 314) viram variantes A e B."""
    counts = Counter(h["number"] for h in raw_hymns)
    seen: Counter[int] = Counter()
    result = []
    for raw in raw_hymns:
        raw = dict(raw)
        if counts[raw["number"]] > 1:
            raw["variant"] = "AB"[seen[raw["number"]]]
            seen[raw["number"]] += 1
        result.append(raw)
    return result


def normalize_ctp(
    base: dict, metrics: dict[str, list], continuations: dict[str, list[str]]
) -> list[dict]:
    """CTP: variantes A/B, letras sem rodapé do PDF e métricas do índice corrigido."""
    hymns = []
    for raw in assign_ctp_variants(base["hymns"]):
        number = str(raw["number"])
        if has_footer(raw["lyrics"]):
            extra = continuations.get(number + (raw.get("variant") or ""), [])
            raw["lyrics"] = "\n".join([strip_footer(raw["lyrics"]), *extra]).strip()
        entries = metrics.get(number + (raw.get("variant") or "")) or metrics.get(number, [])
        metric, melody = _metric_and_melody(entries)
        hymns.append(_make("CTP", raw, metric=metric, melody=melody))
    return hymns


def normalize_hcc(base: dict, metrics: dict[str, list]) -> list[dict]:
    """HCC: métrica e melodia do índice de métricas (as antigas tinham erros)."""
    hymns = []
    for raw in base["hymns"]:
        entries = metrics.get(str(raw["number"]), [])
        old_melody = raw.get("melody") if isinstance(raw.get("melody"), str) else None
        if len(entries) > 1 and old_melody:
            # Mesmo número listado duas vezes no índice: fica a melodia já conhecida
            old_key = melody_key(old_melody) or ""
            entries = sorted(entries, key=lambda e: not (melody_key(e[1]) or "").startswith(old_key))[:1]
        metric, melody = _metric_and_melody(entries)
        hymns.append(
            _make(
                "HCC",
                {**raw, "topics": raw.get("topics_hcc") or []},
                metric=metric,
                melody=melody or old_melody,
            )
        )
    return hymns


_SH_PAGE = re.compile(r"^\s*-\s*\d+\s*-\s*$")
_SH_NOTE = re.compile(r"^i{1,3}\s+[A-ZÀ-Ü]")


def clean_sh_lyrics(lyrics: str) -> str:
    """Remove números de página ("- 33 -") e notas de rodapé do SH."""
    lines = lyrics.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if _SH_NOTE.match(line):
            # A nota vai até o número de página logo abaixo
            end = next((j for j in range(i, min(i + 8, len(lines))) if _SH_PAGE.match(lines[j])), None)
            if end is not None:
                i = end + 1
                continue
        if not _SH_PAGE.match(line):
            out.append(line)
        i += 1
    return "\n".join(out).strip()


_SH_MARK = re.compile(r"\s+i{1,3}$", re.MULTILINE)


def normalize_sh(base: dict) -> list[dict]:
    """SH: sem números de página, notas de rodapé e marcas de nota (" i")."""
    hymns = []
    for raw in base["hymns"]:
        lyrics = _SH_MARK.sub("", clean_sh_lyrics(raw["lyrics"]))
        hymns.append(
            _make(
                "SH",
                {
                    **raw,
                    "title": _SH_MARK.sub("", raw["title"]),
                    "first_line": _SH_MARK.sub("", raw.get("first_line") or ""),
                    "topics": raw.get("topics_sh") or [],
                    "lyrics": lyrics,
                },
            )
        )
    return hymns


def normalize_simple(hymnal: str, base: list[dict]) -> list[dict]:
    return [_make(hymnal, raw) for raw in base]


# --- Temas, equivalências e herança -----------------------------------------


# O SH usa o mesmo vocabulário de temas do CTP
_TOPIC_KEYS = {"CTP": "ctp", "HCC": "hcc", "SH": "ctp", "HC": "hc", "NC": "nc"}


def apply_canonical_topics(hymns: list[dict], canonical: dict[str, dict]) -> None:
    lookup: dict[tuple[str, str], list[str]] = {}
    for theme, data in canonical.items():
        for hymnal, key in _TOPIC_KEYS.items():
            for name in data.get(key, []):
                lookup.setdefault((hymnal, name), []).append(theme)
    for hymn in hymns:
        themes: list[str] = []
        for topic in hymn["topics"]:
            for theme in lookup.get((hymn["hymnal"], topic), []):
                if theme not in themes:
                    themes.append(theme)
        hymn["topics_canonical"] = themes


def official_pairs(hymns: list[dict], md_path: Path) -> list[tuple[str, str, str]]:
    """Pares do índice oficial CTP x SH, resolvendo variantes A/B pelo texto."""
    by_number: dict[tuple[str, int], list[dict]] = {}
    for hymn in hymns:
        by_number.setdefault((hymn["hymnal"], hymn["number"]), []).append(hymn)
    pairs = []
    for ctp_number, first_line, sh_number in parse_official_ctp_sh(md_path):
        ctp = by_number.get(("CTP", ctp_number), [])
        sh = by_number.get(("SH", sh_number), [])
        if not ctp or not sh:
            continue
        target = shingles(first_line, 2)
        best = max(ctp, key=lambda h: similarity(target, shingles(h["first_line"], 2)))
        pairs.append((best["id"], sh[0]["id"], "índice oficial do CTP"))
    return pairs


def hcc_manual_pairs(base: dict) -> list[tuple[str, str, str]]:
    """Equivalências de conteúdo já conferidas no HCC (relationships.same_hymn)."""
    pairs = []
    for raw in base["hymns"]:
        rel = (raw.get("relationships") or {}).get("content_equivalence")
        if rel and rel.get("type") == "same_hymn":
            pairs.append((f"HCC-{raw['number']}", f"{rel['hymnal']}-{rel['number']}",
                          "equivalência conferida no HCC"))
    return pairs


def inherit_from_equivalents(hymns: list[dict], equivalences: dict[str, list[dict]]) -> None:
    """Hinos sem métrica/melodia herdam do equivalente confirmado (CTP > HCC...)."""
    by_id = {h["id"]: h for h in hymns}
    for hymn in hymns:
        if hymn["metric"] or hymn["melody"]:
            continue
        candidates = [
            by_id[e["id"]]
            for e in equivalences.get(hymn["id"], [])
            if e["confianca"] == "confirmada" and e["id"] in by_id
        ]
        candidates = [c for c in candidates if not c["via"] and (c["metric"] or c["melody"])]
        if not candidates:
            continue
        source = min(candidates, key=lambda c: _INHERIT_ORDER.index(c["hymnal"]))
        hymn["metric"], hymn["melody"], hymn["via"] = source["metric"], source["melody"], source["id"]


def add_keys(hymns: list[dict]) -> None:
    for hymn in hymns:
        hymn["metric_key"] = metric_key(hymn["metric"])
        keys = [melody_key(m) for m in split_melodies(hymn["melody"])]
        hymn["melody_keys"] = [k for k in keys if k]


# --- Build -------------------------------------------------------------------


def build(project_dir: Path, web_dir: Path | None = None) -> dict[str, Any]:
    """Executa o build completo e devolve estatísticas.

    Args:
        project_dir: raiz do projeto.
        web_dir: onde gravar; o padrão é web/data (os testes usam uma pasta
            temporária para conferir se web/data está atualizado).
    """
    base_dir = project_dir / "data" / "base"
    web_dir = web_dir or project_dir / "web" / "data"

    hcc_base = _load(base_dir / "hcc.json")
    hymns_by_hymnal = {
        "CTP": normalize_ctp(
            _load(base_dir / "ctp.json"),
            _load(base_dir / "ctp_metricas.json"),
            _load(base_dir / "ctp_continuacoes.json"),
        ),
        "HCC": normalize_hcc(hcc_base, _load(base_dir / "hcc_metricas.json")),
        "SH": normalize_sh(_load(base_dir / "sh.json")),
        "HC": normalize_simple("HC", _load(base_dir / "harpa.json")),
        "NC": normalize_simple("NC", _load(base_dir / "nc.json")),
    }
    all_hymns = [h for hymns in hymns_by_hymnal.values() for h in hymns]

    canonical = _load(project_dir / "data" / "canonical_topics.json")
    apply_canonical_topics(all_hymns, canonical)

    manual = official_pairs(all_hymns, project_dir / "correspondencias ctp x sh.md")
    manual += hcc_manual_pairs(hcc_base)
    equivalences = build_equivalences(all_hymns, manual)
    inherit_from_equivalents(all_hymns, equivalences)
    add_keys(all_hymns)

    stats: dict[str, Any] = {}
    for code, hymns in hymns_by_hymnal.items():
        info = HYMNALS[code]
        _write(
            web_dir / "output" / info["output"],
            {"version": 2, "hymnal": code, "name": info["name"], "count": len(hymns), "hymns": hymns},
        )
        stats[code] = {
            "hinos": len(hymns),
            "com_metrica": sum(1 for h in hymns if h["metric"]),
            "metrica_herdada": sum(1 for h in hymns if h["via"]),
            "com_tema": sum(1 for h in hymns if h["topics_canonical"]),
            "com_equivalente": sum(1 for h in hymns if h["id"] in equivalences),
        }
    _write(web_dir / "equivalencias.json", equivalences)
    _write(web_dir / "canonical_topics.json", canonical)
    return stats
