"""CTP parser implementation for Cantai Todos os Povos hymnal."""

import re

import pymupdf

from src.cantai.models import Hymn
from src.cantai.parser.base import HymnParser


class CTPParser(HymnParser):
    """Parser for extracting hymns from the Cantai Todos os Povos PDF.

    Responsibilities:
        - Extract hymn data from the CTP PDF file
        - Return a list of Hymn objects

    Non-responsibilities:
        - Classifying themes or topics
        - Calculating metrics or melodies
        - Accessing database
        - Exporting JSON or HTML
        - Modifying Hymn objects
        - Removing or sorting hymns

    Input:
        - source (str): Path to the CTP PDF file

    Output:
        - list[Hymn]: List of Hymn objects extracted from the PDF

    Exceptions:
        - FileNotFoundError: If the source file does not exist
        - ValueError: If the file is not a valid PDF
    """

    HYMN_TITLE_PATTERN = re.compile(
        r"^\s*(\d+)(?:[.\s]*[a-z]?)\s*[-–]{1,2}\s*([A-ZÀ-Ü][A-ZÀ-Ü\s,'\u2019!?-]+)$"
    )

    def parse(self, source: str) -> list[Hymn]:
        """Parse a CTP PDF file and extract all hymns.

        Args:
            source: Path to the CTP PDF file

        Returns:
            list[Hymn]: List of all Hymn objects extracted from the PDF

        Raises:
            FileNotFoundError: If the source file does not exist
            ValueError: If the file is not a valid PDF
        """
        doc = pymupdf.open(source)

        hymn_positions = self._find_all_hymns(doc)
        hymns = []
        for page_idx, line_idx, number in hymn_positions:
            hymn = self._extract_hymn(doc, page_idx, line_idx, number)
            hymns.append(hymn)

        doc.close()

        return hymns

    def _find_all_hymns(self, doc: pymupdf.Document) -> list[tuple[int, int, int]]:
        """Locate all hymn start positions in the PDF document.

        Returns:
            list[tuple]: List of (page_index, line_index, hymn_number)
        """
        positions = []

        for page_idx in range(doc.page_count):
            page = doc[page_idx]
            text = page.get_text()
            lines = text.split("\n")

            for line_idx, line in enumerate(lines):
                match = self.HYMN_TITLE_PATTERN.match(line)
                if match:
                    hymn_number = int(match.group(1))
                    positions.append((page_idx, line_idx, hymn_number))

        return positions

    def _extract_hymn(
        self,
        doc: pymupdf.Document,
        page_idx: int,
        line_idx: int,
        number: int,
    ) -> Hymn:
        """Extract a single hymn from the PDF document.

        Args:
            doc: Opened PDF document
            page_idx: 0-based page index
            line_idx: Line index within the page
            number: Hymn number

        Returns:
            Hymn: Extracted hymn object
        """
        page = doc[page_idx]
        text = page.get_text()
        lines = text.split("\n")

        # Extract title from the hymn start line
        first_line = lines[line_idx]
        title_match = re.search(r"[-–]{1,2}\s*(.+)$", first_line)
        title = title_match.group(1).strip() if title_match else ""

        # Skip title and author lines, get lyrics
        lyrics_lines = []
        for line in lines[line_idx + 2 :]:
            stripped = line.strip()
            # Stop at copyright notice or next hymn title
            if stripped.startswith("©") or self.HYMN_TITLE_PATTERN.match(stripped):
                break
            if stripped:
                lyrics_lines.append(stripped)

        lyrics = "\n".join(lyrics_lines)
        first_line_text = lyrics_lines[0] if lyrics_lines else ""

        return Hymn(
            number=number,
            title=title,
            first_line=first_line_text,
            lyrics=lyrics,
        )
