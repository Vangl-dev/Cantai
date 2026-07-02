"""Importador do índice temático de Salmos e Hinos."""

import re

from cantai.database import create_database, update_hymn_categories
from cantai.importers.salmos_hinos_index_data import SH_INDEX


def _normalize_number(num_str: str) -> str:
    """Normaliza número do hino."""
    num_str = num_str.strip()
    num_str = re.sub(r"\(.*\)", "", num_str)
    return num_str.strip()


def import_sh_index() -> dict:
    """Importa o índice temático de Salmos e Hinos e atualiza o banco.

    Retorna dict com estatísticas.
    """
    hymn_topics: dict[str, list[str]] = {}
    hymn_first_category: dict[str, str] = {}

    for cat_name, numbers in SH_INDEX.items():
        for num in numbers:
            normalized = _normalize_number(num)
            if not normalized:
                continue

            if normalized not in hymn_topics:
                hymn_topics[normalized] = []
            hymn_topics[normalized].append(cat_name)

            if normalized not in hymn_first_category:
                hymn_first_category[normalized] = cat_name

    updates = {}
    for num, topics in hymn_topics.items():
        updates[num] = {
            "category": hymn_first_category.get(num),
            "topics": topics,
        }

    create_database()
    atualizados, nao_encontrados = update_hymn_categories(updates, hymnal="SH")

    multi_topics = {
        num: topics for num, topics in hymn_topics.items() if len(topics) > 1
    }

    return {
        "categorias_encontradas": len(SH_INDEX),
        "categorias_importadas": len(SH_INDEX),
        "hinos_atualizados": atualizados,
        "hinos_nao_encontrados": nao_encontrados,
        "hinos_multipla_categoria": len(multi_topics),
        "multi_topics": multi_topics,
    }
