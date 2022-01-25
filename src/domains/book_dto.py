from typing import List, Optional
from src.domains.book_entity import BookEntity
from src.domains.source_enum import SourceEnum
from pydantic import BaseModel


class BookDTO(BaseModel):
    books: List[BookEntity]
    source: Optional[SourceEnum]
