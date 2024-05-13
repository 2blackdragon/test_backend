from sqlalchemy import select

from database import async_session
from models import BookORM
from schemas import Book_Base, Book_Model


class BookRepository:
    @classmethod
    async def find_all(cls) -> list[Book_Model]:
        async with async_session() as session:
            query = select(BookORM)
            result = await session.execute(query)
            books = result.scalars().all()
            return books

    @classmethod
    async def add_book(cls, model: Book_Base) -> dict:
        async with async_session() as session:
            model = model.model_dump()
            book1 = BookORM(name=model["name"], author=model["author"], year=model["year"])
            session.add(book1)
            await session.commit()
            return model

    @classmethod
    async def find_book_on_name(cls, name: str):
        async with async_session() as session:
            search = "%{}%".format(str(name))
            query = select(BookORM).filter(BookORM.name.like(search))
            data = await session.execute(query)
            data = data.scalars().all()
            return data
