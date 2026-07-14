"""Apply themes to hymns and export updated JSON."""

from src.cantai.importers.index import import_themes
from src.cantai.parser.ctp import CTPParser
from src.cantai.exporters.json import export_json


def main():
    # Parse hymns
    parser = CTPParser()
    hymns = parser.parse("data/input/Hinário Cantai Todos os Povos.pdf")

    # Import themes
    hymn_themes = import_themes("data/input/markdown_índice_ctp.md")

    # Apply themes to hymns
    for hymn in hymns:
        if hymn.number in hymn_themes:
            hymn.topics = hymn_themes[hymn.number]

    # Export updated JSON
    export_json(hymns, "data/output/cantai.json")

    # Print statistics
    hymns_with_topics = sum(1 for h in hymns if h.topics)
    hymns_without_topics = sum(1 for h in hymns if not h.topics)

    print(f"Quantidade de hinos: {len(hymns)}")
    print(f"Quantidade de hinos com temas: {hymns_with_topics}")
    print(f"Quantidade de hinos sem temas: {hymns_without_topics}")

    # Get all unique themes
    all_themes = set()
    for themes in hymn_themes.values():
        all_themes.update(themes)

    print(f"\nQuantidade de temas: {len(all_themes)}")
    print("\nTemas em ordem alfabética:")
    for theme in sorted(all_themes):
        print(f"  - {theme}")


if __name__ == "__main__":
    main()
