"""Import themes from the CTP index markdown file."""

import re
from pathlib import Path


def import_themes(index_path: str | Path) -> dict[int, list[str]]:
    """Import themes from the CTP index markdown file.

    Args:
        index_path: Path to the markdown_índice_ctp.md file

    Returns:
        dict: Dictionary mapping hymn number to list of themes
    """
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    hymn_themes: dict[int, list[str]] = {}
    current_theme = None

    lines = content.split("\n")

    for line in lines:
        line = line.strip()

        # Check for theme header (## Theme Name)
        if line.startswith("## "):
            current_theme = line[3:].strip()
            continue

        # Skip empty lines and non-hymn lines
        if not current_theme or not line:
            continue

        # Match hymn number pattern: number at the start of line
        # Handle various formats:
        # - 30 .....
        # - 228A .....
        # - $30^{\mathrm{A}}$ .....
        # - $30^{\\mathrm{A}}$ .....
        # - 314 $^{A}$ .....
        # - 314 ^ .....
        # - 39 $^{(1*)}$ .....
        # - 39 $^{(2^{a})}$ .....
        match = re.match(r"^(?:\$)?(\d+)", line)
        if match:
            hymn_number = int(match.group(1))
            if hymn_number not in hymn_themes:
                hymn_themes[hymn_number] = []
            if current_theme not in hymn_themes[hymn_number]:
                hymn_themes[hymn_number].append(current_theme)

    return hymn_themes
