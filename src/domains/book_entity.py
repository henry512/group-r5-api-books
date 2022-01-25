from typing import Optional, Set
from pydantic import BaseModel


class BookEntity(BaseModel):
    id: Optional[str]
    title: Optional[str] 
    subtitle: Optional[str]
    authors: Optional[Set[str]]
    categories: Optional[Set[str]]
    datetime_publication: Optional[str]
    editor: Optional[str]
    description: Optional[str]
    image_link: Optional[str]
