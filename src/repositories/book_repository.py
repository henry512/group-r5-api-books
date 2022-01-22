from abc import ABC, abstractmethod
from typing import List
from src.domains import BookFiltered, BookDTO, BookEntity, SourceEnum
from src.infrastructure import IPostgresContext
from pypika.queries import QueryBuilder
from pypika import PostgreSQLQuery as Query, Table, Criterion, functions as fn
from pypika.enums import JoinType
from dependency_injector.providers import Configuration
from datetime import datetime


class IBookRepository(ABC):
    @abstractmethod
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_book(self, id: str):
        raise NotImplementedError
    

class BookRepository(IBookRepository):
    def __init__(self, context: IPostgresContext, configuration: Configuration):
        self._context = context
        self._schema = configuration["database"]["schema"]
        self._table_books = Table(
            configuration["database"]["tables"]["books"], self._schema
        )
        self._table_authors = Table(
            configuration["database"]["tables"]["authors"], self._schema
        )
        self._table_categories = Table(
            configuration["database"]["tables"]["categories"], self._schema
        )
        self._table_publishing = Table(
            configuration["database"]["tables"]["publishing"], self._schema
        )
        self._table_books_authors = Table(
            configuration["database"]["tables"]["books_authors"], self._schema
        )
        self._table_books_categories = Table(
            configuration["database"]["tables"]["books_categories"], self._schema
        )
    
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        query: QueryBuilder = (
            Query.from_(self._table_books)
            .select(
                self._table_books.id,                
                self._table_books.title,                
                self._table_books.subtitle,                
                self._table_books.description,                
                self._table_books.image,                
                self._table_books.datetime_publications,                
                self._table_authors.name.as_("authors"),
                self._table_categories.name.as_("categories"),
                self._table_publishing.name.as_("publishing"),
            )
            .join(self._table_books_authors, JoinType.inner)
            .on(self._table_books.id == self._table_books_authors.book_id)
            
            .join(self._table_authors, JoinType.inner)
            .on(self._table_books_authors.author_id == self._table_authors.id)
            
            .join(self._table_books_categories, JoinType.inner)
            .on(self._table_books.id == self._table_books_categories.book_id)
            
            .join(self._table_categories, JoinType.inner)
            .on(self._table_books_categories.category_id == self._table_categories.id)
            
            .join(self._table_publishing, JoinType.inner)
            .on(self._table_books.publishing_id == self._table_publishing.id)
        )
        
        # TODO: La aplicación de los siguientes filtros en una primera etapa de implementación
        # sera con el criterio/operador de busqueda [contains]. Se descarta el resto
        # ver enumerador OperatorEnum src/domains/operator_enum.py
        any_criterian = list()
        
        if filters.id:
            any_criterian.append(self._table_books.id.like(f'%{str(filters.id)}%'))
            
        if filters.title:
            any_criterian.append(self._table_books.title.like(f'%{str(filters.title)}%'))
            
        if filters.subtitle:
            any_criterian.append(self._table_books.subtitle.like(f'%{str(filters.subtitle)}%'))
            
        if filters.description:
            any_criterian.append(self._table_books.description.like(f'%{str(filters.description)}%'))
            
        if filters.datetime_publication:
            any_criterian.append(self._table_books.datetime_publication == filters.datetime_publication)
            
        if filters.author:
            any_criterian.append(self._table_authors.name.like(f'%{str(filters.author)}%'))
            
        if filters.category:
            any_criterian.append(self._table_categories.name.like(f'%{str(filters.category)}%'))
            
        if filters.editor:
            any_criterian.append(self._table_publishing.name.like(f'%{str(filters.editor)}%'))
        
        query = query.where(Criterion.any(any_criterian))
        result = await self._context.find(query.get_sql())
        
        if not result.empty:
            books_group = [groups for _, groups in result.groupby("id")]
            books: List[BookEntity] = []
            for item in books_group:
                books.append(
                    BookEntity(
                        id = item["id"][0],
                        title = item["title"][0],
                        subtitle = item["subtitle"][0],
                        description = item["description"][0],
                        datetime_publication = datetime.strptime(
                            str(item["datetime_publications"][0]), '%Y-%m-%d'
                        ).date(),
                        editor = item["publishing"][0],
                        image_link = item["image"][0],
                        authors = set(item["authors"].to_list()),
                        categories = set(item["categories"].to_list()),
                        source = SourceEnum.internal
                    )
                )
            return BookDTO(books=books)
        
        return BookDTO(books=[])
    
    async def delete_book(self, id: str):
        return
