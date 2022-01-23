from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Coroutine
from src.domains import BookFiltered, BookDTO, BookEntity, SourceEnum
from dependency_injector.providers import Configuration
from src.infrastructure import IHttpClient
from asyncio import gather
from json import loads
from uuid import uuid4


class IBookExternalRepository(ABC):
    @abstractmethod
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        raise NotImplementedError
    

class BookExternalRepository(IBookExternalRepository):
    def __init__(self, http_client: IHttpClient, configuration: Configuration):
        self._http_client = http_client
        self._base_url_google_books = (
            configuration["open_api"]["google_books"]["base_url"]
        )
        self._base_url_open_libra = (
            configuration["open_api"]["open_libra"]["base_url"]
        )
    
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        async_calls: List[Coroutine[Any, Any, List[BookEntity]]] = list()
        async_calls.append(self._get_books_of_google_books(filters))
        async_calls.append(self._get_books_of_open_libra(filters))
        all_results = await gather(*async_calls)
        
        books = [book for books in all_results for book in books]
        return BookDTO(books=books)
    
    async def _get_books_of_google_books(self, filters: BookFiltered) -> List[BookEntity]:
        """[summary]
            filtered:
                intitle
                inauthor
                inpublisher

            Example:
                https://www.googleapis.com/books/v1/volumes?q=intitle:flower&fields=items(volumeInfo)
                https://www.googleapis.com/books/v1/volumes?q=inauthor:gomez&fields=items(volumeInfo)
                https://www.googleapis.com/books/v1/volumes?q=inpublisher:Createspace&fields=items(volumeInfo)
                
        Args:
            filters (BookFiltered): [description]

        Returns:
            List[BookEntity]: [description]
        """
        books: List[BookEntity] = list()
        filtered_mappers = list()
        
        if filters.title:
            filtered_mappers.append(f"intitle:{filters.title}")
            
        if filters.author:
            filtered_mappers.append(f"inauthor:{filters.author}")
            
        if filters.editor:
            filtered_mappers.append(f"inpublisher:{filters.editor}")
            
        if not filtered_mappers:
            return books
            
        url_filtered = f"?fields=items(volumeInfo)&q={'+'.join(filtered_mappers).replace(' ', '%20')}"
        try:
            http_data, http_status = (
                await self._http_client.get(f"{self._base_url_google_books}{url_filtered}")
            )
        except Exception:
            return books
        
        if http_status == 200:
            result = loads(http_data)
            for book in result.get("items", []):
                entity = BookEntity(
                    id = str(uuid4()),
                    title = book["volumeInfo"].get("title"),
                    subtitle = book["volumeInfo"].get("subtitle"),
                    description = book["volumeInfo"].get("description"),
                    editor = book["volumeInfo"].get("publisher"),
                    authors = set(book["volumeInfo"].get("authors", set())),
                    categories = set(book["volumeInfo"].get("categories", set())),
                    source = SourceEnum.exteral
                )
                datetime_publication = book["volumeInfo"].get("publishedDate")
                entity.datetime_publication = (
                    None
                    if not datetime_publication
                    else str(datetime_publication[0:4]) # Obtiene el año
                )
                image_link: Optional[Dict[str, str]] = book["volumeInfo"].get("imageLinks")
                entity.image_link = (
                    None
                    if not image_link
                    else str(list(image_link.values())[-1]) # Obtiene la imagen de mayor calidad
                )
                books.append(entity)

        return books
        
    async def _get_books_of_open_libra(self, filters: BookFiltered) -> List[BookEntity]:
        """[summary]
            filtered:
                book_title
                book_author
                publisher
                category
                publisher_date

            Example:
                https://www.etnassoft.com/api/v1/get?book_title=javascript
                https://www.etnassoft.com/api/v1/get?book_author=paenza
                https://www.etnassoft.com/api/v1/get?publisher=UOC
                https://www.etnassoft.com/api/v1/get?publisher_date=2011
                https://www.etnassoft.com/api/v1/get?category=programacion
                
        Args:
            filters (BookFiltered): [description]

        Returns:
            List[BookEntity]: [description]
        """
        books: List[BookEntity] = []
        filtered_mappers = list()
        
        if filters.title:
            filtered_mappers.append(f"book_title={filters.title}")
            
        if filters.author:
            filtered_mappers.append(f"book_author={filters.author}")
            
        if filters.editor:
            filtered_mappers.append(f"publisher={filters.editor}")
            
        if filters.category:
            filtered_mappers.append(f"category={filters.category}")
            
        if filters.datetime_publication:
            filtered_mappers.append(f"publisher_date={filters.datetime_publication}")
            
        if not filtered_mappers:
            return books
            
        url_filtered = f"{self._base_url_open_libra}?{'&'.join(filtered_mappers).replace(' ', '%20')}"
        try:
            http_data, http_status = (
                await self._http_client.get(url_filtered)
            )
        except Exception:
            return books
        
        if http_status == 200:
            result = loads(http_data)
            for book in result:
                entity = BookEntity(
                    id = str(uuid4()),
                    title = book.get("title"),
                    subtitle = book.get("subtitle"),
                    description = book.get("content_short"),
                    editor = book.get("publisher"),
                    image_link = book.get("thumbnail"),
                    source = SourceEnum.exteral
                )
                datetime_publication = book.get("publisher_date")
                entity.datetime_publication = (
                    None
                    if not datetime_publication
                    else str(datetime_publication[0:4]) # Obtiene el año
                )
                categories = book.get("categories", set())
                entity.categories = (
                    set()
                    if not categories
                    else set([category["name"] for category in categories])
                )
                authors = book.get("author")
                entity.authors = (
                    set()
                    if not authors
                    else set([authors])
                )
                books.append(entity)

        return books
