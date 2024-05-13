from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from schemas import Book_Base
from database import create_tables, delete_tables

from repository import BookRepository

from redis import asyncio as aioredis




@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await delete_tables()
    await create_tables()
    print("created tables")
    yield
    print("OFF")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://62.113.118.150:3000",
    "http://88.210.3.106:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@cache()
async def get_cache():
    return 1


@app.get("/{user_id}")
@cache(expire=60)
async def print_books(user_id: int):
    books = await BookRepository.find_all_for_user(user_id)
    return books


@app.post("/")
async def save_book(model: Book_Base):
    book = await BookRepository.add_book(model)

@app.get("/find_book_on_name/{user_id}&{name}")
@cache(expire=60)
async def find_book(user_id: int, name: str):
    books = await BookRepository.find_book_on_name_for_user(user_id, name)
    return books


# TODO: разобраться с pydantic
# TODO: check pymongo
# TODO: потестить фронт бэк вместе дебажить
# TODO: подумать как переделать под микросервисы

