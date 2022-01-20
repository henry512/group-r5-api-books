from typing import List, Optional
from src.domains import BookEntity
from pydantic import BaseModel


class BookDTO(BaseModel):
    books: List[BookEntity]
