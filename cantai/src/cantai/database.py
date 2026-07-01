"""Camada de persistência SQLite com SQLModel."""

import json
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select

from cantai.models import HymnModel
from cantai.schemas import Hymn

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "database" / "cantai.db"

engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)


def create_database() -> None:
    """Cria o banco de dados e as tabelas."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)


def save_hymns(hymns: list[Hymn]) -> tuple[int, int]:
    """Persiste hinos no banco, evitando duplicidade por (hymnal, number).

    Retorna (novos, atualizados).
    """
    novos = 0
    atualizados = 0

    with Session(engine) as session:
        for hymn in hymns:
            stmt = select(HymnModel).where(
                HymnModel.hymnal == hymn.hymnal,
                HymnModel.number == hymn.number,
            )
            existing = session.exec(stmt).first()

            if existing:
                existing.title = hymn.title
                existing.category = hymn.category
                existing.first_line = hymn.first_line
                existing.lyrics = hymn.lyrics
                existing.slide_count = hymn.slide_count
                existing.source_file = str(hymn.source_file)
                session.add(existing)
                atualizados += 1
            else:
                model = HymnModel(
                    hymnal=hymn.hymnal,
                    number=hymn.number,
                    title=hymn.title,
                    category=hymn.category,
                    first_line=hymn.first_line,
                    lyrics=hymn.lyrics,
                    slide_count=hymn.slide_count,
                    source_file=str(hymn.source_file),
                )
                session.add(model)
                novos += 1

        session.commit()

    return novos, atualizados


def count_hymns() -> int:
    """Retorna o total de hinos no banco."""
    with Session(engine) as session:
        return len(session.exec(select(HymnModel)).all())


def load_hymns() -> list[Hymn]:
    """Carrega todos os hinos do banco como objetos Hymn."""
    from pathlib import Path as _Path

    with Session(engine) as session:
        models = session.exec(select(HymnModel)).all()

    return [
        Hymn(
            hymnal=m.hymnal,
            number=m.number,
            title=m.title,
            category=m.category,
            first_line=m.first_line,
            lyrics=m.lyrics,
            slide_count=m.slide_count,
            source_file=_Path(m.source_file),
            topics=json.loads(m.topics) if m.topics else [],
        )
        for m in models
    ]


def update_hymn_categories(updates: dict[str, dict], hymnal: str = "CTP") -> tuple[int, int]:
    """Atualiza category e topics dos hinos.

    updates: {number: {"category": str, "topics": list[str]}}
    hymnal: identificador do hinário (CTP, HARPA, CC).
    Retorna (atualizados, nao_encontrados).
    """
    atualizados = 0
    nao_encontrados = 0

    with Session(engine) as session:
        for number, data in updates.items():
            stmt = select(HymnModel).where(
                HymnModel.hymnal == hymnal,
                HymnModel.number == number,
            )
            model = session.exec(stmt).first()

            if model:
                if data.get("category"):
                    model.category = data["category"]
                if data.get("topics"):
                    model.topics = json.dumps(data["topics"], ensure_ascii=False)
                session.add(model)
                atualizados += 1
            else:
                nao_encontrados += 1

        session.commit()

    return atualizados, nao_encontrados
