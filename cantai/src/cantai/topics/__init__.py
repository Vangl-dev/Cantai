"""Módulo de classificação temática unificada do Cantai."""

from cantai.topics.catalog import (
    CANONICAL_TOPICS,
    CC_TO_CANONICAL,
    CTP_TO_CANONICAL,
    HARPAS_TO_CANONICAL,
    NC_TO_CANONICAL,
    SH_TO_CANONICAL,
    SYNONYMS,
    resolve_topic,
    resolve_topics,
)
from cantai.topics.classifier import classify_by_lyrics
from cantai.topics.reclassifier import reclassify_all

__all__ = [
    "CANONICAL_TOPICS",
    "CC_TO_CANONICAL",
    "CTP_TO_CANONICAL",
    "HARPAS_TO_CANONICAL",
    "NC_TO_CANONICAL",
    "SH_TO_CANONICAL",
    "SYNONYMS",
    "classify_by_lyrics",
    "reclassify_all",
    "resolve_topic",
    "resolve_topics",
]
