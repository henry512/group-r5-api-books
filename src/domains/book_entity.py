from datetime import date
from typing import Optional, Set
from pydantic import BaseModel
from src.domains.source_enum import SourceEnum


class BookEntity(BaseModel):
    id: str
    title: str 
    subtitle: Optional[str]
    authors: Set[str]
    categories: Set[str]
    datetime_publication: date
    editor: str
    description: Optional[str]
    source: Optional[SourceEnum]
    image_link: Optional[str]
