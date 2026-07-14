"""JSON exporter for hymns."""

import json
from pathlib import Path

from src.cantai.models import Hymn


def export_json(hymns: list[Hymn], output_path: str | Path) -> None:
    """Export a list of hymns to a JSON file.

    Args:
        hymns: List of Hymn objects to export
        output_path: Path to the output JSON file
    """
    data = {
        "version": 1,
        "hymnal": "CTP",
        "count": len(hymns),
        "hymns": [
            {
                "number": h.number,
                "title": h.title,
                "first_line": h.first_line,
                "lyrics": h.lyrics,
                "topics": h.topics,
                "metric": h.metric,
                "melody": h.melody,
                "variant": h.variant,
                "source": h.source,
            }
            for h in hymns
        ],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
