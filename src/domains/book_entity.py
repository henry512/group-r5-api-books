from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BookEntity(BaseModel):
    id: str
    title: str 
    subtitle: Optional[str]
    author: str
    category: str
    datetime_publication: datetime
    editor: str
    description: Optional[str]
    original_source: Optional[str]