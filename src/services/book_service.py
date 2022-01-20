from abc import ABC, abstractmethod
from typing import List
from src.domains import BookFiltered, BookDTO


class IBookService(ABC):
    @abstractmethod
    def get_books(self, filters: BookFiltered) -> BookDTO:
        raise NotImplementedError
    
    @abstractmethod
    def group_delete_books(self, ids: List[str]):
        raise NotImplementedError
    

class BookService(IBookService):
    def __init__(self):
        pass
    
    def get_books(self, filters: BookFiltered) -> BookDTO:
        return BookDTO(books=[])
    
    def group_delete_books(self, ids: List[str]):
        return
