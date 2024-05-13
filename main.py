from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import Book_Base
from database import create_tables, delete_tables

from repository import BookRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    print("created tables")
    yield
    print("OFF")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def print_books():
    books = await BookRepository.find_all()
    return books


@app.post("/")
async def save_book(model: Book_Base):
    book = await BookRepository.add_book(model)


@app.get("/find_book_on_name/{name}")
async def find_book(name: str):
    books = await BookRepository.find_book_on_name(name)
    return books


# TODO: разобраться с pydantic
# TODO: check pymongo
# TODO: потестить фронт бэк вместе дебажить
# TODO: подумать как переделать под микросервисы

