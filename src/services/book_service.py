from abc import ABC, abstractmethod
from src.domains import BookFiltered, BookDTO, BookEntity
from src.repositories import IBookRepository, IBookExternalRepository
from typing import List
from src.utils import Utils


class IBookService(ABC):
    @abstractmethod
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_book(self, id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def save_books_external(self, books: List[BookEntity]):
        raise NotImplementedError
    

class BookService(IBookService):
    def __init__(
        self, 
        book_repository: IBookRepository, 
        book_external_repository: IBookExternalRepository
    ):
        self._book_repository = book_repository
        self._book_external_repository = book_external_repository
    
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        books_internal = await self._book_repository.get_books(filters)
        if books_internal.books:
            return books_internal
        
        books_external = await self._book_external_repository.get_books(filters)
        if books_external.books:
            return books_external
        
        return BookDTO(books=list(), source=None)
    
    async def delete_book(self, id: str):
        if not id:
            return
        await self._book_repository.delete_book(id)
        
    async def save_books_external(self, books: List[BookEntity]):
        print("tarea de persistencia...")
        chunk_sections = Utils.chunk(books)
        print(len(chunk_sections))
        
        
