from typing import List
from src.domains.book_entity import BookEntity
from pydantic import BaseModel


class BookDTO(BaseModel):
    books: List[BookEntity]
