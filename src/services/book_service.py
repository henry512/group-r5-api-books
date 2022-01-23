from abc import ABC, abstractmethod
from fastapi import BackgroundTasks
from async_timeout import asyncio
from src.domains import BookFiltered, BookDTO
from src.repositories import IBookRepository, IBookExternalRepository


class IBookService(ABC):
    @abstractmethod
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_book(self, id: str):
        raise NotImplementedError
    

class BookService(IBookService):
    def __init__(
        self, 
        book_repository: IBookRepository, 
        book_external_repository: IBookExternalRepository,
        background_task: BackgroundTasks
    ):
        self._book_repository = book_repository
        self._book_external_repository = book_external_repository
        self._background_task = background_task
    
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        books_internal = await self._book_repository.get_books(filters)
        if books_internal.books:
            return books_internal
        
        books_external = await self._book_external_repository.get_books(filters)
        if books_external.books:
            # iniciar Background Task para persistir lo obtenido
            return books_external
        
        return BookDTO(books=[])
    
    async def delete_book(self, id: str):
        await self._book_repository.delete_book(id)
