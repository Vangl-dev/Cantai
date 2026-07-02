"""Validador do catálogo de temas canônicos.

Valida o canonical_topics.yaml e verifica consistência com o banco de dados.
"""

import json
from pathlib import Path

import yaml
from sqlmodel import Session, select

from cantai.database import engine
from cantai.models import HymnModel
from cantai.topics.catalog import CANONICAL_TOPICS, SYNONYMS

YAML_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "canonical_topics.yaml"


def load_yaml() -> dict:
    """Carrega o canonical_topics.yaml."""
    if not YAML_PATH.exists():
        return {}
    with open(YAML_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate_yaml() -> dict:
    """Valida o YAML e retorna relatório de inconsistências."""
    data = load_yaml()
    issues: list[str] = []

    if not data:
        issues.append("Arquivo canonical_topics.yaml vazio ou não encontrado.")
        return {"valid": False, "issues": issues}

    topic_names = list(data.keys())

    dup_check: dict[str, list[str]] = {}
    for name in topic_names:
        lower = name.lower().strip()
        dup_check.setdefault(lower, []).append(name)
    for key, duplicates in dup_check.items():
        if len(duplicates) > 1:
            issues.append(f"Tema duplicado (case-insensitive): {duplicates}")

    all_aliases: dict[str, list[str]] = {}
    for topic_name, topic_data in data.items():
        if not isinstance(topic_data, dict):
            continue
        aliases = topic_data.get("aliases", [])
        for alias in aliases:
            lower = alias.lower().strip()
            all_aliases.setdefault(lower, []).append(f"{topic_name} → {alias}")

    for key, mappings in all_aliases.items():
        if len(mappings) > 1:
            issues.append(f"Alias duplicado '{key}': {mappings}")

    canonical_set = set(c.lower() for c in CANONICAL_TOPICS)
    yaml_set = set(n.lower() for n in topic_names)
    missing_in_yaml = canonical_set - yaml_set
    missing_in_catalog = yaml_set - canonical_set

    if missing_in_yaml:
        issues.append(f"Temas no catálogo Python mas não no YAML: {sorted(missing_in_yaml)}")
    if missing_in_catalog:
        issues.append(f"Temas no YAML mas não no catálogo Python: {sorted(missing_in_catalog)}")

    all_hymnal_aliases: dict[str, dict[str, str]] = {}
    for topic_name, topic_data in data.items():
        if not isinstance(topic_data, dict):
            continue
        for key in ["CTP", "HARPA", "CC", "SH", "NC"]:
            values = topic_data.get(key, [])
            if isinstance(values, str):
                values = [values]
            if not isinstance(values, list):
                continue
            for val in values:
                if not val:
                    continue
                lower = str(val).lower().strip()
                if lower in all_hymnal_aliases:
                    prev_topic = all_hymnal_aliases[lower]
                    if prev_topic != topic_name:
                        issues.append(
                            f"Alias de hinário conflitante '{lower}': "
                            f"'{prev_topic}' e '{topic_name}' ({key})"
                        )
                else:
                    all_hymnal_aliases[lower] = topic_name

    return {"valid": len(issues) == 0, "issues": issues, "topics_count": len(topic_names)}


def validate_database() -> dict:
    """Valida se todos os hinos possuem topics canônicos."""
    issues: list[str] = []
    canonical_set = set(CANONICAL_TOPICS)

    with Session(engine) as session:
        models = session.exec(select(HymnModel)).all()

    total = len(models)
    sem_topics = 0
    topicos_nao_canonicos: dict[str, int] = {}

    for model in models:
        topics = json.loads(model.topics) if model.topics else []
        if not topics:
            sem_topics += 1
            issues.append(f"{model.hymnal} {model.number} — sem topics")
            continue
        for t in topics:
            if t not in canonical_set:
                topicos_nao_canonicos[t] = topicos_nao_canonicos.get(t, 0) + 1

    if sem_topics > 0:
        issues.append(f"{sem_topics} hinos sem topics")

    for topic, count in sorted(topicos_nao_canonicos.items(), key=lambda x: -x[1]):
        issues.append(f"Tema não canônico '{topic}': {count} hinos")

    return {
        "valid": len(issues) == 0,
        "total_hymns": total,
        "sem_topics": sem_topics,
        "topicos_nao_canonicos": topicos_nao_canonicos,
        "issues": issues,
    }


def validate_all() -> dict:
    """Executa todas as validações e retorna relatório consolidado."""
    yaml_report = validate_yaml()
    db_report = validate_database()

    all_issues = []
    all_issues.extend(yaml_report.get("issues", []))
    all_issues.extend(db_report.get("issues", []))

    return {
        "valid": yaml_report["valid"] and db_report["valid"],
        "yaml": yaml_report,
        "database": db_report,
        "issues": all_issues,
        "issues_count": len(all_issues),
    }
