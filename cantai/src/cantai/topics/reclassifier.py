"""Reclassificador de hinos para o catálogo único do Cantai.

Carrega todos os hinos do banco, converte temas originais para canônicos,
e classifica por letra os hinos que não possuem temas.
Garante que nenhum hino fique sem tags.
"""

import json

from sqlmodel import Session, select

from cantai.database import engine
from cantai.models import HymnModel
from cantai.topics.catalog import resolve_topics
from cantai.topics.classifier import classify_by_lyrics


def reclassify_all() -> dict:
    """Reclassifica todos os hinos do banco para o catálogo canônico.

    Retorna dict com estatísticas da reclassificação.
    """
    stats = {
        "total": 0,
        "com_temas_originais": 0,
        "reclassificados": 0,
        "classificados_por_letra": 0,
        "ja_canonicos": 0,
        "sem_temas_antes": 0,
        "sem_temas_depois": 0,
        "por_hinario": {},
    }

    with Session(engine) as session:
        models = session.exec(select(HymnModel)).all()
        stats["total"] = len(models)

        for model in models:
            hymnal = model.hymnal
            if hymnal not in stats["por_hinario"]:
                stats["por_hinario"][hymnal] = {
                    "total": 0,
                    "reclassificados": 0,
                    "classificados_por_letra": 0,
                }
            stats["por_hinario"][hymnal]["total"] += 1

            original_topics = json.loads(model.topics) if model.topics else []

            if original_topics:
                stats["com_temas_originais"] += 1
                resolved = resolve_topics(original_topics)
                if set(resolved) != set(original_topics):
                    stats["reclassificados"] += 1
                    stats["por_hinario"][hymnal]["reclassificados"] += 1
                else:
                    stats["ja_canonicos"] += 1
                model.topics = json.dumps(resolved, ensure_ascii=False)
            else:
                stats["sem_temas_antes"] += 1
                inferred = classify_by_lyrics(model.title, model.first_line, model.lyrics)
                if inferred:
                    stats["classificados_por_letra"] += 1
                    stats["por_hinario"][hymnal]["classificados_por_letra"] += 1
                    model.topics = json.dumps(inferred, ensure_ascii=False)
                else:
                    fallback = _generate_fallback_topics(
                        model.title, model.first_line, model.lyrics
                    )
                    model.topics = json.dumps(fallback, ensure_ascii=False)

            if not model.category and original_topics:
                model.category = original_topics[0] if original_topics else None

            final_topics = json.loads(model.topics) if model.topics else []
            if not final_topics:
                stats["sem_temas_depois"] += 1

            session.add(model)

        session.commit()

    return stats


def _generate_fallback_topics(title: str, first_line: str, lyrics: str) -> list[str]:
    """Gera temas a partir das palavras mais relevantes do hino.

    Usado quando a classificação por keywords não encontra correspondência.
    """
    text = f"{title} {first_line} {lyrics}".lower()

    word_scores: dict[str, int] = {}
    words = text.split()
    for w in words:
        w = w.strip(".,;:!?()[]{}\"'")
        if len(w) >= 4:
            word_scores[w] = word_scores.get(w, 0) + 1

    topic_keywords = {
        "esperança": "Esperança",
        "aleluia": "Louvor",
        "graça": "Graça",
        "jesus": "Adoração",
        "cristo": "Adoração",
        "reino": "Evangelização",
        "cordeiro": "Santa Ceia",
        "pai": "Trindade",
        "espírito": "Pentecostes",
        "amor": "Vida Cristã",
        "vida": "Vida Cristã",
        "luz": "Adoração",
        "paz": "Consolo",
        "força": "Confiança",
        "fiel": "Confiança",
        "bondade": "Graça",
        "misericórdia": "Graça",
        "glória": "Louvor",
        "vitória": "Louvor",
        "céu": "Esperança",
        "terra": "Missões",
        "mundo": "Missões",
        "nações": "Missões",
        "povo": "Comunhão",
        "igreja": "Comunhão",
        "senhor": "Adoração",
        "deus": "Adoração",
        "santo": "Santidade",
        "santa": "Santidade",
        "rei": "Soberania de Deus",
        "salvar": "Salvação",
        "perdão": "Graça",
        "orar": "Oração",
        "oração": "Oração",
        "cruz": "Cruz",
        "morte": "Redenção",
        "túmulo": "Ressurreição",
        "nascer": "Natal",
        "noite": "Consolo",
        "dia": "Louvor",
        "manhã": "Louvor",
    }

    matched: set[str] = set()
    for word, topic in topic_keywords.items():
        if word in text:
            matched.add(topic)
            if len(matched) >= 3:
                break

    if not matched:
        matched.add("Vida Cristã")

    return sorted(matched)
