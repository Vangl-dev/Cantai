"""Apply metrics and melodies to the Cantai JSON file."""

import json
from pathlib import Path

from src.cantai.importers.metrics import import_metrics


def apply_metrics(
    json_path: str | Path,
    metrics_path: str | Path,
) -> dict:
    """Apply metrics and melodies to the Cantai JSON file.

    Args:
        json_path: Path to the cantai.json file
        metrics_path: Path to the HinarioCTP_metricas.md file

    Returns:
        dict: Statistics about the import
    """
    # Load JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Import metrics
    metrics_data = import_metrics(metrics_path)

    # Apply to hymns
    stats = {
        "total_hymns": len(data["hymns"]),
        "with_metric": 0,
        "with_melody": 0,
        "without_info": 0,
        "metrics_set": set(),
        "melodies_set": set(),
    }

    for hymn in data["hymns"]:
        hymn_number = hymn["number"]
        if hymn_number in metrics_data:
            info = metrics_data[hymn_number]

            if info["metric"]:
                hymn["metric"] = info["metric"]
                stats["with_metric"] += 1
                stats["metrics_set"].add(info["metric"])

            if info["melody"]:
                hymn["melody"] = info["melody"]
                stats["with_melody"] += 1
                stats["melodies_set"].add(info["melody"])

            if not info["metric"] and not info["melody"]:
                stats["without_info"] += 1
        else:
            stats["without_info"] += 1

    # Convert sets to counts for JSON serialization
    stats["unique_metrics"] = len(stats["metrics_set"])
    stats["unique_melodies"] = len(stats["melodies_set"])
    del stats["metrics_set"]
    del stats["melodies_set"]

    # Save updated JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return stats
