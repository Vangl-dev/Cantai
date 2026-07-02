"""Modelos de dados do Cantai Builder."""

from __future__ import annotations

from sqlmodel import Field, SQLModel


class HymnModel(SQLModel, table=True):
    """Modelo de hino persistido no banco."""

    id: int | None = Field(default=None, primary_key=True)
    hymnal: str = Field(index=True)
    number: str
    title: str
    category: str | None = None
    topics: str = "[]"
    first_line: str = ""
    lyrics: str = ""
    slide_count: int = 0
    source_file: str = ""

    class Config:
        unique_together = ("hymnal", "number")
