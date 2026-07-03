"""Importador do índice temático do CTP."""

import re
from pathlib import Path

from cantai.database import create_database, update_hymn_categories
from cantai.importers.ctp_index_data import CTP_INDEX


def _normalize_number(num_str: str) -> str:
    """Normaliza número do hino para comparação.

    Remove parênteses, sufixos e leading zeros.
    Converte letras para minúsculas para comparação.
    Ex: '39(1)' -> '39', '069' -> '69', '30A' -> '30a'
    """
    num_str = num_str.strip()
    num_str = re.sub(r"\(.*\)", "", num_str)
    num_str = num_str.strip()
    # Convert letters to lowercase for comparison
    num_str = num_str.lower()
    # Remove leading zeros but keep the string for non-numeric suffixes
    if num_str.isdigit():
        num_str = str(int(num_str))
    return num_str


def _denormalize_number(num_str: str, existing_numbers: set[str]) -> str:
    """Encontra o número real no banco a partir do número normalizado.

    O CTP pode ter números com leading zeros ('069') ou sem ('69'),
    ou com letras maiúsculas ('30A') vs minúsculas ('030.a').
    Esta função encontra o formato correto.
    """
    # Try exact match first
    if num_str in existing_numbers:
        return num_str
    # Try with leading zeros (3 digits)
    padded = num_str.zfill(3)
    if padded in existing_numbers:
        return padded
    # Try without leading zeros
    stripped = num_str.lstrip("0") or "0"
    if stripped in existing_numbers:
        return stripped
    # Try matching by removing dots, leading zeros, and comparing lowercase
    num_normalized = num_str.replace(".", "").lower()
    for existing in existing_numbers:
        existing_normalized = existing.replace(".", "").lstrip("0").lower()
        if existing_normalized == num_normalized:
            return existing
    # Return original
    return num_str


def import_ctp_index() -> dict:
    """Importa o índice temático do CTP e atualiza o banco.

    Retorna dict com estatísticas.
    """
    # First, get all existing CTP numbers from the database
    from sqlmodel import Session, select
    from cantai.models import HymnModel
    from cantai.database import engine

    existing_numbers: set[str] = set()
    with Session(engine) as session:
        models = session.exec(
            select(HymnModel).where(HymnModel.hymnal == "CTP")
        ).all()
        for m in models:
            existing_numbers.add(m.number)

    hymn_topics: dict[str, list[str]] = {}
    hymn_first_category: dict[str, str] = {}
    nao_encontrados_list: list[str] = []

    for cat_name, numbers in CTP_INDEX.items():
        for num in numbers:
            normalized = _normalize_number(num)
            if not normalized:
                continue

            # Find the real number in the database
            real_number = _denormalize_number(normalized, existing_numbers)

            if real_number not in existing_numbers:
                nao_encontrados_list.append(f"{num} (normalizado: {normalized})")
                continue

            if real_number not in hymn_topics:
                hymn_topics[real_number] = []
            if cat_name not in hymn_topics[real_number]:
                hymn_topics[real_number].append(cat_name)

            if real_number not in hymn_first_category:
                hymn_first_category[real_number] = cat_name

    updates = {}
    for num, topics in hymn_topics.items():
        updates[num] = {
            "category": hymn_first_category.get(num),
            "topics": topics,
        }

    create_database()
    atualizados, _ = update_hymn_categories(updates)

    multi_topics = {
        num: topics for num, topics in hymn_topics.items() if len(topics) > 1
    }

    return {
        "categorias_encontradas": len(CTP_INDEX),
        "categorias_importadas": len(CTP_INDEX),
        "hinos_atualizados": atualizados,
        "hinos_nao_encontrados": len(nao_encontrados_list),
        "nao_encontrados_lista": nao_encontrados_list,
        "hinos_multipla_categoria": len(multi_topics),
        "multi_topics": multi_topics,
    }
