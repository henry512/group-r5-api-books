from typing import Optional
from src.domains import OperatorEnum
from pydantic import BaseModel


class BookFiltered(BaseModel):
    operator: Optional[OperatorEnum]
    id: Optional[str]
    title: Optional[str] 
    subtitle: Optional[str]
    author: Optional[str]
    category: Optional[str]
    datetime_publication: Optional[str]
    editor: Optional[str]
    description: Optional[str]
