from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    published_year: int
    genre: Optional[str] = None
    available: bool = True

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True 