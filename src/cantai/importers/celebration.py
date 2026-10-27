"""Importa o Celebration Hymnal a partir dos índices do fim do livro.

O livro só existe como PDF de imagens com partitura, então as letras não
entram. Dos índices (PDF com OCR, páginas 820-865 do livro) saem, para cada
hino: título, primeira linha, tom, melodia, métrica e temas. Isso basta para
ligar o Celebration aos outros hinários pela melodia e pela métrica.

Páginas usadas (contadas a partir de 0 no PDF do índice):
    15-17  Alphabetical Index by Tune Name   melodia + métrica + números
    18-21  Metrical Index of Tunes           métrica (mais confiável no OCR)
    27-37  Topical Index of Songs            temas
    38-45  Alphabetical Index of Songs       número, título/1ª linha, tom
"""

import re
from pathlib import Path

TUNE_PAGES = range(15, 18)
METRICAL_PAGES = range(18, 22)
TOPICAL_PAGES = range(27, 38)
SONG_PAGES = range(38, 46)

_NAMED = {"C.M.": "8.6.8.6.", "L.M.": "8.8.8.8.", "S.M.": "6.6.8.6."}
_SMALL_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into", "of",
    "on", "or", "the", "to", "upon", "with", "than", "like", "o",
}
# Nomes de melodia que o OCR leu errado (conferidos contra o índice impresso)
_TUNE_FIXES = {
    "MOOQDY": "MOODY",
    "MORECAMSBE": "MORECAMBE",
    "MCcAFEE": "McAFEE",
    "JESU, MEINE FREUDIE": "JESU, MEINE FREUDE",
    "JESUS, LORD TOME": "JESUS, LORD TO ME",
    "LASST UNS5 ERFREUEN": "LASST UNS ERFREUEN",
}
_KEY = r"\(((?:[A-G][b#]?|[a-g][b#]?\s*min\.?)(?:\s*/\s*(?:[A-G][b#]?|[a-g][b#]?\s*min\.?))*)\s*\)"


def _clean(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'")
    text = re.sub(r"\b(OQur|Qur|QOur)\b", "Our", text)
    text = text.replace("})", "b)").replace("“", "'").replace("”", "'")
    text = re.sub(r"^I(?=(lay|love|must)\b)|^I'(?=must\b)", "I ", text).replace("I  ", "I ")
    text = re.sub(r"\s+[|'!:.\-]+(\s*\d)?\s*$", "", text)
    text = re.sub(r"^'(?!T)", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _page_lines(doc, page: int) -> list[str]:
    return [ln for ln in doc[page].get_text().split("\n") if ln.strip()]


# --- Métrica -----------------------------------------------------------------


def normalize_meter(text: str | None) -> str | None:
    """Métrica do índice em inglês no formato usado pelo app.

    "C.M. with Refrain" -> "8.6.8.6. (C.M.) com estribilho";
    "8.7.8.7.D." -> "8.7.8.7.D."; "Irreg." -> "Irregular".
    """
    if not text:
        return None
    text = _clean(text).replace(",", ".")
    text = re.sub(r"^(Common|Long|Short) Meter( Double)?\s*", "", text)
    if re.match(r"^[IlT]rreg", text, re.IGNORECASE):
        return "Irregular"
    text = re.sub(r"^\((.*)\)$", r"\1", text)
    text = re.sub(r"\b5\.M\.", "S.M.", text).replace("1D.", "D.")
    text = re.sub(r"[^\w.)]+$", "", text)
    # nenhum verso tem mais de 15 sílabas: "8.7.87." é "8.7.8.7."
    text = re.sub(r"\d{2,}", lambda m: m.group(0) if int(m.group(0)) <= 15 else ".".join(m.group(0)), text)
    text = re.sub(r"(\d)\s+(\d)", r"\1.\2", text)
    extra = ""
    for pattern, label in (
        (r"\s*(with|w/)\s*Re[ft](rain|\.)?", " com estribilho"),
        (r"\s*(with|w/)\s*Alleluias", " com aleluias"),
        (r"\s*(with|w/)\s*Repeats", " com repetições"),
        (r"\s*(with|w/)\s*Coda", " com coda"),
        (r"\s*\(?Ref(rain|\.)? only\)?", " (só estribilho)"),
    ):
        if re.search(pattern, text, re.IGNORECASE):
            extra += label
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    text = re.sub(r"\(\s*\)", "", text).strip(" ,")
    named = re.match(r"^([CLS])\.?\s?M\.?\s*(D\.?)?\s*(\((.*?)\))?$", text)
    if named:
        name = f"{named.group(1)}.M."
        base = named.group(4) or (_NAMED[name] if not named.group(2) else "")
        if named.group(2):
            name += "D."
            base = named.group(4) or _NAMED[f"{named.group(1)}.M."] * 2
        text = f"{base.strip()} ({name})"
    return (text + extra).strip() or None


def _fix_index_line(line: str) -> str:
    """Erros de OCR recorrentes nos índices: "1 EXALT" = "I EXALT", "(lrreg))"."""
    line = _clean(line)
    line = re.sub(r"(^|\s)1(?=\s[A-Z]{2})", r"\1I", line)
    line = re.sub(r"\b[lT]rreg", "Irreg", line).replace("))", ")").replace("Irreg )", "Irreg.)")
    return re.sub(r"(\d)\s*[^\w\s()]+\s*$", r"\1", line).strip()


_METER_HEADING = re.compile(r"^(\d|(Common|Long|Short) Meter|[CLS]\.?M\.)")


def choose_meter(from_tunes: str | None, from_metrical: str | None) -> str | None:
    """Métrica do índice de melodias, com a pontuação do índice métrico.

    O índice de melodias tem uma entrada por linha e sai mais limpo do OCR,
    mas às vezes perde pontos ("8.8.85."); quando os dígitos batem com o
    índice métrico, vale a grafia deste.
    """
    if from_metrical and (
        not _METER_HEADING.match(from_metrical) or re.search(r"[A-Z]{3,}|Mc[A-Z]", from_metrical)
    ):
        from_metrical = None  # cabeçalho misturado com nome de melodia
    if from_tunes and from_metrical:
        same = re.sub(r"\D", "", from_tunes) == re.sub(r"\D", "", from_metrical)
        return from_metrical if same else from_tunes.replace(",", ".")
    return (from_tunes or from_metrical or "").replace(",", ".") or None


# --- Índice de melodias ------------------------------------------------------

_TUNE_START = re.compile(r"^(?:Mc)?[A-ZÀ-Ü'][A-ZÀ-Üa-z'.,?!\- ]*[A-ZÀ-Ü.'?!]\s*(?:\(|,\s*\(|\d)")
_TUNE_ENTRY = re.compile(
    r"^(?P<tune>[^()]+?)\s*,?\s*(?:\((?P<m1>[^)]*)\))?\s*,?\s*(?:\((?P<m2>[^)]*)\))?"
    r"\s*,?\s*(?P<nums>\d[\d,\s]*)$"
)


def parse_tune_index(lines: list[str]) -> dict[int, tuple[str, str | None]]:
    """número do hino -> (melodia, métrica do índice de melodias)."""
    entries: list[str] = []
    for line in lines:
        line = _fix_index_line(line)
        line = re.sub(r"\s*ALPHABETICAL INDEX BY TUNE NAME\s*", " ", line).strip()
        if not line or "INDEXES" in line.upper() or re.fullmatch(r"\d{3}", line):
            continue
        # o OCR às vezes junta na mesma linha entradas de colunas vizinhas
        for part in re.split(r"(?<=\d)\s+(?=(?:Mc)?[A-Z][A-Za-z'.,?!\- ]+\()", line):
            starts = _TUNE_START.match(part) or re.fullmatch(r"(?:Mc)?[A-Z][A-Z'.\- ]{3,},?", part)
            if starts and not part[0].isdigit():
                entries.append(part)
            elif entries:
                entries[-1] += " " + part
    result: dict[int, tuple[str, str | None]] = {}
    for entry in entries:
        match = _TUNE_ENTRY.match(entry)
        if not match:
            continue
        tune = match.group("tune").strip(" ,")
        meter = match.group("m1")
        if match.group("m2"):
            meter = f"{match.group('m2')} ({meter})" if meter else match.group("m2")
        for number in re.findall(r"\d+", match.group("nums")):
            result.setdefault(int(number), (tune, meter))
    return result


# --- Índice métrico ----------------------------------------------------------

_METRICAL_TUNE = re.compile(r"^(?P<tune>[A-ZÀ-Ü'][A-ZÀ-Ü'.,()\- ]+?),\s*(?P<nums>\d[\d,\s]*)$")


def parse_metrical_index(lines: list[str]) -> dict[int, tuple[str, str]]:
    """número do hino -> (melodia, métrica) do índice métrico."""
    result: dict[int, tuple[str, str]] = {}
    heading: list[str] = []
    current = ""
    pending = ""
    for line in lines:
        line = _fix_index_line(line)
        if re.match(r"^(METRICAL INDEX|Metrical Index|INDEXES FOR|\d{3}$|Complete listing|in the Worship)", line):
            continue
        if pending:
            line = pending + " " + line
            pending = ""
        match = _METRICAL_TUNE.match(line)
        if match:
            if heading:
                current = " ".join(heading)
                heading = []
            for number in re.findall(r"\d+", match.group("nums")):
                result.setdefault(int(number), (match.group("tune").strip(), current))
            continue
        if re.match(r"^[A-ZÀ-Ü'][A-ZÀ-Ü'.\- ]+,?$", line) and not re.search(r"\d", line):
            pending = line  # nome de melodia quebrado em duas linhas
            continue
        if re.match(r"^[\d,\s]+$", line):
            continue  # continuação de números já registrados
        heading.append(line)
    return result


def title_key(text: str) -> str:
    """Título sem tom, sem nome de melodia e sem pontuação, para comparar."""
    text = re.sub(_KEY, "", text)  # o nome da melodia entre parênteses distingue homônimos
    return re.sub(r"[^a-z0-9]", "", text.lower())


# --- Índice de temas ---------------------------------------------------------


def _is_heading(line: str) -> bool:
    head = line.split("—")[0]
    letters = [c for c in head if c.isalpha()]
    return len(letters) >= 3 and sum(c.isupper() for c in letters) >= 0.85 * len(letters)


def parse_topical_index(lines: list[str]) -> tuple[dict[int, list[str]], dict[str, set[int]]]:
    """(número do hino -> temas ("CHRIST — Birth"), título normalizado -> números)."""
    result: dict[int, list[str]] = {}
    titles: dict[str, set[int]] = {}
    topic = ""
    after_heading = False
    buffer = ""
    for line in lines:
        line = _clean(line).replace(" - ", " — ").replace("--", "—")
        if re.match(r"^(TOPICAL INDEX|INDEXES FOR)", line):
            continue
        if not buffer and re.fullmatch(r"8[4-5]\d", line):
            continue  # número da página
        if _is_heading(line) and not re.search(r",\s*\d+\s*$", line):
            if after_heading and not topic.endswith(("—", ",")) and "—" not in line:
                topic = f"{topic} {line}"  # "COMFORT AND" + "ENCOURAGEMENT"
            else:
                topic = line
            buffer = ""
            after_heading = True
            continue
        short = len(line.split()) <= 4 and not line.endswith(",") and not re.search(r"\d", line)
        if after_heading and not buffer and short:
            # subtítulo ("God Our Father") ou fim do cabeçalho quebrado ("Wisemen")
            joiner = " " if "—" in topic or line.startswith("(") else " — "
            topic = f"{topic}{joiner}{line}"
            after_heading = False
            continue
        after_heading = False
        text = f"{buffer} {line}".strip() if buffer else line
        match = re.match(r"^(.*?),\s*(\d{1,3})\s*$", text)
        if match:
            buffer = ""
            name = re.sub(r"\s*—\s*", " — ", topic).strip(" —")
            number = int(match.group(2))
            titles.setdefault(title_key(match.group(1)), set()).add(number)
            if name and name not in result.setdefault(number, []):
                result[number].append(name)
        else:
            buffer = text
    return result, titles


# --- Índice alfabético -------------------------------------------------------


def _rows(words: list[tuple], x_min: float, x_max: float) -> list[tuple[float, list[tuple]]]:
    """Agrupa palavras em linhas: (y do centro, palavras da esquerda para a direita)."""
    selected = sorted(
        (w for w in words if x_min <= w[0] < x_max), key=lambda w: (w[1] + w[3]) / 2
    )
    rows: list[list[tuple]] = []
    for word in selected:
        center = (word[1] + word[3]) / 2
        if rows and abs(center - sum((w[1] + w[3]) / 2 for w in rows[-1]) / len(rows[-1])) < 4.5:
            rows[-1].append(word)
        else:
            rows.append([word])
    return [
        (sum((w[1] + w[3]) / 2 for w in row) / len(row), sorted(row, key=lambda w: w[0]))
        for row in rows
    ]


def parse_song_index_page(words: list[tuple], width: float) -> list[tuple[int | None, str]]:
    """(número, texto) de uma página do índice alfabético (duas colunas).

    O número fica numa coluna à esquerda do texto; o OCR às vezes o junta à
    linha do texto e às vezes o deixa numa linha própria. Linhas sem número e
    mais recuadas continuam a entrada anterior.
    """
    entries: list[list] = []
    for x_min, x_max in ((0, width / 2), (width / 2, width)):
        numbers: list[tuple[float, int]] = []
        texts: list[tuple[float, float, int | None, str]] = []
        for y, row in _rows(words, x_min, x_max):
            number = None
            while row and re.fullmatch(r"[^A-Za-z]+", row[0][4]):
                if row[0][4] == "1" and len(row) > 1 and row[1][0] - row[0][2] < 8:
                    row = [(*row[0][:4], "I", *row[0][5:]), *row[1:]]  # "1 Sing" = "I Sing"
                    break
                digits = re.sub(r"\D", "", row[0][4])
                if digits and len(digits) <= 3:
                    number = int(digits)
                row = row[1:]
            if not row:
                if number is not None:
                    numbers.append((y, number))
                continue
            text = " ".join(w[4] for w in row)
            if re.search(r"(Index|INDEXES|Titles are|ALPHABETICAL)", text):
                continue
            texts.append((y, row[0][0], number, text))
        if not texts:
            continue
        starts = sorted(x for y, x, n, t in texts)
        start = starts[len(starts) // 4]
        current: list | None = None
        for y, x, number, text in sorted(texts):
            if number is None:
                near = [n for n in numbers if abs(n[0] - y) < 5]
                if near:
                    number = min(near, key=lambda n: abs(n[0] - y))[1]
            complete = current is not None and re.search(_KEY + r"\s*$", current[1])
            if x < start + 6 and (number is not None or complete or current is None):
                # sem número: o OCR perdeu o número (resolvido depois pelo título)
                current = [number, text]
                entries.append(current)
            elif current is not None:
                current[1] += " " + text
    return [(n, _clean(t)) for n, t in entries]


def split_key(text: str) -> tuple[str, str | None]:
    """"Amazing Grace (G/Ab)" -> ("Amazing Grace", "G/Ab")."""
    match = re.search(_KEY + r"\s*$", text)
    if not match:
        return text.strip(), None
    key = re.sub(r"\s+", "", match.group(1)).replace("min.", " min.").replace("min", " min").replace("  ", " ")
    return text[: match.start()].strip(" ,"), key.strip()


def looks_like_first_line(text: str) -> bool:
    """Primeira linha (frase) x título (Title Case)."""
    words = re.findall(r"[A-Za-z'][A-Za-z']*", re.sub(r"\(.*?\)", "", text))
    return any(w[0].islower() and w.lower() not in _SMALL_WORDS for w in words[1:])


# --- Importação --------------------------------------------------------------


def _fix_tune(name: str | None) -> str | None:
    if not name:
        return None
    name = name.strip(" ,.")
    return _TUNE_FIXES.get(name, name)


def import_celebration(pdf_path: str | Path) -> tuple[list[dict], list[str]]:
    """Hinos do Celebration Hymnal a partir do PDF dos índices (com OCR).

    Devolve os hinos e as entradas do índice alfabético cujo número não foi
    lido nem encontrado pelo título no índice de temas.
    """
    import pymupdf

    with pymupdf.open(str(pdf_path)) as doc:
        tunes = parse_tune_index([ln for p in TUNE_PAGES for ln in _page_lines(doc, p)])
        meters = parse_metrical_index([ln for p in METRICAL_PAGES for ln in _page_lines(doc, p)])
        topics, topical_titles = parse_topical_index(
            [ln for p in TOPICAL_PAGES for ln in _page_lines(doc, p)]
        )
        songs: list[tuple[int | None, str]] = []
        for page in SONG_PAGES:
            songs += parse_song_index_page(doc[page].get_text("words"), doc[page].rect.width)

    known = set(tunes) | set(meters) | set(topics)
    by_number: dict[int, list[tuple[str, str | None]]] = {}
    unresolved: list[str] = []
    split_songs: list[tuple[int | None, str]] = []
    for number, text in songs:
        # duas entradas que o OCR juntou numa linha: "Título A (Bb) Título B (F)"
        parts = re.split(r"(?<=\))\s*[^\w\s(]*\s+(?=[A-Z])", text)
        merged = [parts[0]]
        for part in parts[1:]:
            if re.search(_KEY + r"\s*$", merged[-1]):
                merged.append(part)
            else:
                merged[-1] += " " + part
        split_songs += [(number, merged[0])] + [(None, m) for m in merged[1:]]
    for number, text in split_songs:
        text, key = split_key(text)
        candidates = topical_titles.get(title_key(text), set())
        if len(candidates) == 1:
            # o número no texto corrido do índice de temas é lido com mais segurança
            number = next(iter(candidates))
        elif number is not None and number not in known and candidates:
            number = min(candidates)
        if number is None:
            unresolved.append(text)
            continue
        by_number.setdefault(number, []).append((text, key))

    hymns = []
    for number in sorted(by_number):
        items = by_number[number]
        in_topics = [it for it in items if title_key(it[0]) in topical_titles]
        titles = [it for it in in_topics if not looks_like_first_line(it[0])] + in_topics
        titles += [it for it in items if not looks_like_first_line(it[0])]
        titles = list(dict.fromkeys(titles))
        lines = [it for it in items if it not in titles]
        if not titles:
            titles, lines = lines[:1], lines[1:]
        title, key = titles[0]
        tune_name = re.search(r"\(([A-Z][A-Z .'\-]+)\)\s*$", title)
        title = re.sub(r"\s*\([A-Z][A-Z .'\-]+\)\s*$|\s*\(see .*?\)", "", title)
        tune, tune_meter = tunes.get(number, (None, None))
        metrical_tune, metrical_meter = meters.get(number, (None, None))
        hymns.append({
            "number": number,
            "title": title,
            "first_line": lines[0][0] if lines else "",
            "key": key or next((k for _, k in titles[1:] + lines if k), None),
            "melody": _fix_tune(tune or metrical_tune or (tune_name.group(1).strip() if tune_name else None)),
            "metric": normalize_meter(choose_meter(tune_meter, metrical_meter)),
            "topics": topics.get(number, []),
            "lyrics": "",
        })
    return hymns, unresolved
