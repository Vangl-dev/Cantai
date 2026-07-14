"""Domain model for Cantai2."""

from dataclasses import dataclass, field


@dataclass
class Hymn:
    """Represents a single hymn from the Cantai Todos os Povos hymnal."""

    number: int
    title: str
    first_line: str
    lyrics: str
    topics: list[str] = field(default_factory=list)
    metric: str | None = None
    melody: str | None = None
    variant: str | None = None
    source: str = "CTP"
