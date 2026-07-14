"""Import metrics and melodies from the CTP metrics markdown file."""

import re
from pathlib import Path


def import_metrics(metrics_path: str | Path) -> dict[int, dict]:
    """Import metrics and melodies from the CTP metrics markdown file.

    Args:
        metrics_path: Path to the HinarioCTP_metricas.md file

    Returns:
        dict: Dictionary mapping hymn number to {metric, melody}
    """
    with open(metrics_path, "r", encoding="utf-8") as f:
        content = f.read()

    hymn_data: dict[int, dict] = {}
    current_metric = None

    lines = content.split("\n")

    for line in lines:
        line = line.strip()

        # Check for metric header (## metric)
        if line.startswith("## "):
            metric_candidate = line[3:].strip()
            # Skip non-metric headers
            if metric_candidate and not metric_candidate.startswith("Indice") and not metric_candidate.startswith("Métrica"):
                current_metric = metric_candidate
            continue

        # Skip empty lines and image lines
        if not line or line.startswith("!["):
            continue

        # Skip lines that are just metric patterns (not melody entries)
        if re.match(r"^[\d\.\(\)\[\],\s\-]+$", line):
            continue

        # Try to extract melody name and hymn number
        # Pattern: MELODY_NAME .... NUMBER or MELODY_NAME NUMBER
        match = re.match(r"^(.+?)\s*\.+\s*(\d+[A-Za-z]?)\s*$", line)
        if not match:
            # Try pattern without dots: MELODY_NAME NUMBER
            match = re.match(r"^(.+?)\s+(\d+[A-Za-z]?)\s*$", line)

        if match:
            melody_name = match.group(1).strip()
            hymn_number_str = match.group(2).strip()

            # Extract numeric part of hymn number
            num_match = re.match(r"(\d+)", hymn_number_str)
            if num_match:
                hymn_number = int(num_match.group(1))

                if hymn_number not in hymn_data:
                    hymn_data[hymn_number] = {"metric": None, "melody": None}

                # Set metric if not already set
                if current_metric and hymn_data[hymn_number]["metric"] is None:
                    hymn_data[hymn_number]["metric"] = current_metric

                # Set melody if not already set
                if melody_name and hymn_data[hymn_number]["melody"] is None:
                    hymn_data[hymn_number]["melody"] = melody_name

    return hymn_data
