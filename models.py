from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class BookORM(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    author: Mapped[Optional[str]]
    year: Mapped[Optional[int]]
    user_id: Mapped[int]
