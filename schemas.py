from pydantic import BaseModel

class Book_Base(BaseModel):
    name: str
    author: str
    year: int


class Book_Model(Book_Base):
    id: int
