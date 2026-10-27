"""Normalização de texto, métricas e melodias.

Funções puras usadas pelos importadores, pelo build e pelo cálculo de
equivalências. Mantê-las num só lugar garante que todos os hinários sejam
comparados pelo mesmo critério.
"""

import re
import unicodedata

# Letras cirílicas que o OCR confunde com latinas.
_OCR_LOOKALIKES = str.maketrans("АВЕКМНОРСТХаеорсхуІіш", "ABEKMHOPCTXaeopcxyIim")

_NAMED_METERS = {"CM": "8.6.8.6", "LM": "8.8.8.8", "SM": "6.6.8.6"}


def fix_ocr(text: str) -> str:
    """Corrige confusões comuns de OCR (cirílico, l/I)."""
    text = text.translate(_OCR_LOOKALIKES)

    def fix_word(match: re.Match[str]) -> str:
        word = match.group(0)
        letters = [c for c in word if c.isalpha()]
        uppers = sum(1 for c in letters if c.isupper())
        if len(letters) > 2 and uppers >= len(letters) - 1:
            # Palavra em maiúsculas: "CRElO" -> "CREIO"
            return word.replace("l", "I")
        # Palavra em minúsculas: "Ihes" -> "lhes", "mIm" -> "mlm" não ocorre
        return re.sub(r"(?<=[a-zà-ü])I(?=[a-zà-ü])|^I(?=h[a-zà-ü])", "l", word)

    return re.sub(r"[A-Za-zÀ-ÿ]+", fix_word, text)


def strip_accents(text: str) -> str:
    """Remove acentos."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


def normalize_words(text: str) -> list[str]:
    """Palavras normalizadas (sem acento, minúsculas, sem números/pontuação)."""
    text = strip_accents(text).lower()
    text = re.sub(r"\(bis\)|\bbis\b", " ", text)
    return re.findall(r"[a-z]+", text)


def strip_verse_number(line: str) -> str:
    """Remove o número de estrofe do início da linha ("1- ", "2. ", "3 ")."""
    return re.sub(r"^\s*\d{1,2}\s*(?:[-.)–]\s*|\s+|(?=[^\d\s]))", "", line).strip()


def metric_key(metric: str | None) -> str | None:
    """Chave de comparação da métrica: só o padrão silábico da estrofe.

    "8.7.8.7.D" e "8.7.8.7.8.7.8.7." viram "8.7.8.7.8.7.8.7";
    "8.6.8.6. (C.M.)" vira "8.6.8.6"; o estribilho ("- 7.7.8.7",
    "com estribilho") e sílabas opcionais entre colchetes são ignorados.
    """
    if not metric:
        return None
    text = metric.strip()
    named = re.fullmatch(r"([CLS])\.?\s*M\.?\s*(D\.?)?", text, re.IGNORECASE)
    if named:
        base = _NAMED_METERS[named.group(1).upper() + "M"]
        return f"{base}.{base}" if named.group(2) else base
    text = re.split(r"\s+-\s+|\s+–\s+", text)[0]
    text = re.sub(r"\(.*?\)|\[.*?\]", "", text)
    text = re.split(r"\bcom\b|\brepeti|\birreg", text, flags=re.IGNORECASE)[0]
    parts: list[str] = []
    for token in re.findall(r"\d+|\bD\b", text.replace(".", " ")):
        if token == "D":
            parts = parts + parts
        elif token != "0":
            parts.append(token)
    return ".".join(parts) or None


def melody_key(melody: str | None) -> str | None:
    """Chave de comparação da melodia: maiúsculas, sem acento nem pontuação.

    O que vem entre parênteses é mantido, pois distingue melodias homônimas
    ("GENEVA (Lowden)" x "GENEVA (Day)"); o sufixo ", alt." é ignorado.
    """
    if not melody:
        return None
    text = re.sub(r",?\s*alt\.?$", "", melody.strip(), flags=re.IGNORECASE)
    key = re.sub(r"[^A-Z0-9]", "", strip_accents(text).upper())
    return key or None


def split_melodies(melody: str | None) -> list[str]:
    """Separa melodias alternativas ("EVENTIDE / MORECAMBE")."""
    if not melody:
        return []
    return [m.strip() for m in melody.split(" / ") if m.strip()]
