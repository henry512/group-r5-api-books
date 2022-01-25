from abc import ABC, abstractmethod
from typing import List
from src.domains import BookFiltered, BookDTO, BookEntity, SourceEnum
from src.infrastructure import IPostgresContext
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, aliased
from sqlalchemy import or_, delete
from src.domains import Book, Publisher, Author, Category


class IBookRepository(ABC):
    @abstractmethod
    async def get_books(self, filters: BookFiltered) -> BookDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_book(self, id: str):
        raise NotImplementedError
    

class BookRepository(IBookRepository):
    def __init__(self, context: IPostgresContext):
        self._context = context

    async def get_books(self, filters: BookFiltered) -> BookDTO:
        books = BookDTO(books=list(), source=SourceEnum.internal)
        alias_author: Author = aliased(Author)
        alias_category: Category = aliased(Category)
        alias_publisher: Publisher = aliased(Publisher)
        query = (
            select(Book)
            .options(selectinload(Book.publisher))
            .options(selectinload(Book.authors))
            .options(selectinload(Book.categories))
            .join(alias_author, Book.authors)
            .join(alias_category, Book.categories)
            .join(alias_publisher, Book.publisher)
            .distinct(Book.id)
        )
        
        # TODO: La aplicación de los siguientes filtros en una primera etapa de implementación
        # sera con el criterio/operador de busqueda [contains]. Se descarta el resto
        # ver enumerador OperatorEnum src/domains/operator_enum.py
        any_criterian = list()
        
        if filters.id:
            any_criterian.append(Book.id.like(f"%{filters.id}%"))
            
        if filters.title:
            any_criterian.append(Book.title.like(f"%{filters.title}%"))
            
        if filters.subtitle:
            any_criterian.append(Book.subtitle.like(f"%{filters.subtitle}%"))
            
        if filters.description:
            any_criterian.append(Book.description.like(f"%{filters.description}%"))
            
        if filters.datetime_publication:
            any_criterian.append(Book.publisher_date == filters.datetime_publication)
            
        if filters.author:
            any_criterian.append(alias_author.name.like(f"%{filters.author}%"))
            
        if filters.category:
            any_criterian.append(alias_category.name.like(f"%{filters.category}%"))
            
        if filters.editor:
            any_criterian.append(alias_publisher.name.like(f"%{filters.editor}%"))
            
        if not any_criterian:
            return books
        
        query = query.where(or_(*any_criterian))

        try:
            async with self._context.create_session() as session:
                data = await session.execute(query)
                result = data.all()
        except Exception as error:
            print(error) # changed to logger please
            return books
        
        if result:
            book_list: List[BookEntity] = list()
            for row in result:
                _book: Book = row[0]
                book = BookEntity(
                    id = _book.id,
                    title = _book.title,
                    subtitle = _book.subtitle,
                    description = _book.description,
                    datetime_publication = _book.publisher_date,
                    image_link = _book.image,
                )
                if _book.publisher:
                    book.editor = _book.publisher.name
                    
                if _book.authors:
                    book.authors = set([author.name for author in _book.authors])
                    
                if _book.categories:
                    book.categories = set([category.name for category in _book.categories])
                book_list.append(book)
            books.books = book_list
        
        return books
    
    async def delete_book(self, id: str):
        query = delete(Book).where(Book.id == id)
        try:
            async with self._context.get_session() as session:
                async with session.begin():
                    await session.execute(query)
                    await session.commit()
        except Exception as error:
            print(error) # changed to logger please
            return
