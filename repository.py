from sqlalchemy import select

from database import async_session
from models import BookORM
from schemas import Book_Base, Book_Model

from time import sleep


class BookRepository:
    @classmethod
    async def find_all_for_user(cls, user_id) -> list[Book_Model]:
        async with async_session() as session:
            query = select(BookORM).filter(BookORM.user_id == user_id)
            data = await session.execute(query)
            data = data.scalars().all()
            return data

    @classmethod
    async def add_book(cls, model: Book_Base) -> dict:
        async with async_session() as session:
            model = model.model_dump()
            book1 = BookORM(name=model["name"], author=model["author"], year=model["year"], user_id=model["user_id"])
            session.add(book1)
            await session.commit()
            return model

    @classmethod
    async def find_book_on_name_for_user(cls, user_id: int, name: str):
        async with async_session() as session:
            search = "%{}%".format(str(name))
            query = select(BookORM).filter(BookORM.user_id == user_id and BookORM.name.like(search))
            data = await session.execute(query)
            data = data.scalars().all()
            return data
