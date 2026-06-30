"""Schemas de dados do Cantai Builder."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Hymn:
    hymnal: str
    number: str
    title: str
    category: str | None
    first_line: str
    lyrics: str
    slide_count: int
    source_file: Path


@dataclass
class AuditIssue:
    arquivo: str
    motivo: str


@dataclass
class AuditReport:
    ppt_encontrados: int = 0
    pptx_encontrados: int = 0
    convertidos: int = 0
    processados: int = 0
    hinos_criados: int = 0
    ignorados: list[AuditIssue] = field(default_factory=list)
    erros: list[AuditIssue] = field(default_factory=list)
