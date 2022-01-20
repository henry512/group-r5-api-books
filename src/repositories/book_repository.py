from abc import ABC, abstractmethod
from typing import List
from src.domains import BookFiltered, BookDTO
from src.infrastructure import IPostgresContext


class IBookRepository(ABC):
    @abstractmethod
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def group_delete_books(self, ids: List[str]):
        raise NotImplementedError
    

class BookRepository(IBookRepository):
    def __init__(self, context: IPostgresContext):
        self.context = context
    
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        return BookDTO(books=[])
    
    async def group_delete_books(self, ids: List[str]):
        return
