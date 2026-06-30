"""Exportador JSON do Cantai Builder."""

import json
from datetime import datetime, timezone
from pathlib import Path

from cantai.schemas import Hymn

_EXPORT_VERSION = 1


def export_json(hymns: list[Hymn], output: Path) -> None:
    """Exporta hinos para um arquivo JSON."""
    output.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "version": _EXPORT_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hymns": [
            {
                "hymnal": h.hymnal,
                "number": int(h.number) if h.number.isdigit() else h.number,
                "title": h.title,
                "category": h.category,
                "first_line": h.first_line,
                "lyrics": h.lyrics,
                "slide_count": h.slide_count,
            }
            for h in hymns
        ],
    }

    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
