"""Base parser interface for hymn extraction."""

from abc import ABC, abstractmethod

from src.cantai.models import Hymn


class HymnParser(ABC):
    """Interface for parsing hymns from a source file.

    Responsibilities:
        - Extract hymn data from a PDF file
        - Return a list of Hymn objects

    Non-responsibilities:
        - Interpreting or classifying hymns
        - Calculating themes or topics
        - Calculating metrics or melodies
        - Storing data to database
        - Exporting data to JSON

    Input:
        - Path to a PDF file (provided via constructor or parse method)

    Output:
        - list[Hymn]: List of Hymn objects extracted from the PDF

    Exceptions:
        - FileNotFoundError: If the source file does not exist
        - ValueError: If the file is not a valid PDF
        - RuntimeError: If extraction fails due to PDF corruption
    """

    @abstractmethod
    def parse(self, source: str) -> list[Hymn]:
        """Parse a source file and extract hymns.

        Args:
            source: Path to the source file (PDF)

        Returns:
            list[Hymn]: List of Hymn objects extracted from the source

        Raises:
            FileNotFoundError: If the source file does not exist
            ValueError: If the file is not a valid format
            RuntimeError: If extraction fails
        """
