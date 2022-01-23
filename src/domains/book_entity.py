from typing import Optional, Set
from pydantic import BaseModel
from src.domains.source_enum import SourceEnum


class BookEntity(BaseModel):
    id: str
    title: str 
    subtitle: Optional[str]
    authors: Optional[Set[str]]
    categories: Optional[Set[str]]
    datetime_publication: Optional[str]
    editor: Optional[str]
    description: Optional[str]
    source: Optional[SourceEnum]
    image_link: Optional[str]
