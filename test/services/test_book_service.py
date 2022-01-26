from unittest.mock import MagicMock, Mock
import uuid
from src.repositories import IBookRepository, IBookExternalRepository
from src.services import BookService
from src.domains import *


async def test_get_books_internal():
    async def mock_get_books_internal(filtered):
        return BookDTO(
            books=[
                BookEntity(
                    id="id",
                    title="title",
                    subtitle="subtitle",
                    description="description",
                    datetime_publication="2022"
                )
            ], 
            source=SourceEnum.internal
        )
    async def mock_get_books_external(filtered):
        return BookDTO(
            books=list(), 
            source=None
        )
    
    book_repository = mock_repository(mock_get_books_internal)
    book_repository_external = mock_repository_external(mock_get_books_external)
    service = BookService(book_repository, book_repository_external)
    filters = BookFiltered(
        id="id",
        title="title",
        subtitle="subtitle",
        author="author",
        category="category",
        datetime_publication="2022",
        editor="editor",
        description="description",
    )
    result = await service.get_books(filters)
    
    assert len(result.books)
    assert result.source is SourceEnum.internal
    
    
async def test_get_books_external():
    async def mock_get_books_internal(filtered):
        return BookDTO(
            books=list(), 
            source=None
        )
    async def mock_get_books_external(filtered):
        return BookDTO(
            books=[
                BookEntity(
                    id="id",
                    title="title",
                    subtitle="subtitle",
                    description="description",
                    datetime_publication="2022"
                )
            ], 
            source=SourceEnum.external
        )
    
    book_repository = mock_repository(mock_get_books_internal)
    book_repository_external = mock_repository_external(mock_get_books_external)
    service = BookService(book_repository, book_repository_external)
    filters = BookFiltered(
        id="id",
        title="title",
        subtitle="subtitle",
        author="author",
        category="category",
        datetime_publication="2022",
        editor="editor",
        description="description",
    )
    result = await service.get_books(filters)
    
    assert len(result.books)
    assert result.source is SourceEnum.external


async def test_get_books_none():
    async def mock_get_books_internal(filtered):
        return BookDTO(
            books=list(), 
            source=None
        )
    async def mock_get_books_external(filtered):
        return BookDTO(
            books=list(), 
            source=None
        )
    
    book_repository = mock_repository(mock_get_books_internal)
    book_repository_external = mock_repository_external(mock_get_books_external)
    service = BookService(book_repository, book_repository_external)
    filters = BookFiltered(
        id="id",
        title="title",
        subtitle="subtitle",
        author="author",
        category="category",
        datetime_publication="2022",
        editor="editor",
        description="description",
    )
    result = await service.get_books(filters)
    
    assert not len(result.books)
    assert result.source is None
    
    
async def test_delete_book():
    async def mock_delete_book(id):
        return
        
    book_repository = mock_repository(mock_delete_book)
    book_repository_external = mock_repository_external()
    service = BookService(book_repository, book_repository_external)
    await service.delete_book(str(uuid.uuid4()))
    

async def test_delete_book_none():
    async def mock_delete_book(id):
        return
        
    book_repository = mock_repository(mock_delete_book)
    book_repository_external = mock_repository_external()
    service = BookService(book_repository, book_repository_external)
    await service.delete_book(None)
    
    
async def test_save_book():
    async def mock_save_book(book):
        return
        
    book_repository = mock_repository(mock_save_book)
    book_repository_external = mock_repository_external()
    service = BookService(book_repository, book_repository_external)
    
    books = [
        BookEntity(
            id="id",
            title="title1",
            subtitle="subtitle1",
            description="description1",
            datetime_publication="2022",
            authors= set(["autor1"]),
            categories= set(["categoria1"]),
            editor= "publisher1",
            image_link= None
        ),
        BookEntity(
            id="id2",
            title="title2",
            subtitle="subtitle2",
            description="description2",
            datetime_publication="2022",
            authors= set(["autor2"]),
            categories= set(["categoria2"]),
            editor= "publisher2",
            image_link= None
        ),
        BookEntity(
            id="i3",
            title="title3",
            subtitle="subtitle3",
            description="description3",
            datetime_publication="2022",
            authors= set(["autor3"]),
            categories= set(["categoria3"]),
            editor= "publisher3",
            image_link= None
        )
    ]
    
    await service.save_books_external(books)
    

async def test_save_book_none():
    async def mock_save_book(book):
        return
        
    book_repository = mock_repository(mock_save_book)
    book_repository_external = mock_repository_external()
    service = BookService(book_repository, book_repository_external)
    
    books = list()
    await service.save_books_external(books)
    

# Factories Dependencies
def mock_repository(side_effect=None):
    mock = MagicMock(IBookRepository)
    mock.get_books = Mock(side_effect=side_effect)
    mock.delete_book = Mock(side_effect=side_effect)
    mock.save_book = Mock(side_effect=side_effect)

    return mock


def mock_repository_external(side_effect=None):
    mock = MagicMock(IBookExternalRepository)
    mock.get_books = Mock(side_effect=side_effect)

    return mock