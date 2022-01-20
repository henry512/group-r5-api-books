from abc import ABC, abstractmethod
from typing import List
from src.domains import BookFiltered, BookDTO
from src.repositories import IBookRepository


class IBookService(ABC):
    @abstractmethod
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def group_delete_books(self, ids: List[str]):
        raise NotImplementedError
    

class BookService(IBookService):
    def __init__(self, repository: IBookRepository):
        self.repository = repository
    
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        return BookDTO(books=[])
    
    async def group_delete_books(self, ids: List[str]):
        return