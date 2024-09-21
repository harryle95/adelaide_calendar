# import engine
from db.engine import engine
from db.models.course import Base

__all__ = (
    "create_database",
    "delete_database",
    "reset_database",
)


def create_database() -> None:
    Base.metadata.create_all(engine)


def delete_database() -> None:
    Base.metadata.drop_all(engine)


def reset_database() -> None:
    delete_database()
    create_database()
