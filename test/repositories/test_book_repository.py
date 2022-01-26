from unittest.mock import MagicMock, Mock
import uuid
from src.repositories import BookRepository
from src.infrastructure import IPostgresContext
from src.domains import *
from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    AsyncResult
)


async def test_get_books(monkeypatch):
    async def mock_get_all_books_by_session(self, query):
        return [
            [
                Book(
                    id = str(uuid.uuid4()), 
                    title = "title",
                    subtitle = "subtitle",
                    description = "description",
                    publisher_date = "2022",
                    image = "image", 
                    publisher=Publisher(id=1, name="publisher1"),
                    authors=[Author(id=1, name="autor1"), Author(id=2, name="autor2")],
                    categories=[Category(id=1, name="categoria1"), Category(id=2, name="categoria2")]
                )
            ]
        ]
    monkeypatch.setattr(BookRepository, "_get_all_books_by_session", mock_get_all_books_by_session)
    
    context = mock_context()
    repository = BookRepository(context)
    filters = BookFiltered(
        id="id",
        title="title",
        subtitle="subtitle",
        author="author",
        category="category",
        datetime_publication="2022",
        editor="editor",
        description="description"
    )
    result = await repository.get_books(filters)
    assert len(result.books)
    assert result.source is SourceEnum.internal
    

async def test_get_books_return_none(monkeypatch):
    async def mock_get_all_books_by_session(self, query):
        raise Exception("mock exception")
    
    monkeypatch.setattr(BookRepository, "_get_all_books_by_session", mock_get_all_books_by_session)
    
    context = mock_context()
    repository = BookRepository(context)
    filters = BookFiltered(
        id="id",
        title="title",
        subtitle="subtitle",
        author="author",
        category="category",
        datetime_publication="2022",
        editor="editor",
        description="description"
    )
    result = await repository.get_books(filters)
    assert not len(result.books)
    
    
async def test_get_books_none_filters():
    context = mock_context()
    repository = BookRepository(context)
    filters = BookFiltered(
        id=None,
        title=None,
        subtitle=None,
        author=None,
        category=None,
        datetime_publication=None,
        editor=None,
        description=None
    )
    result = await repository.get_books(filters)
    assert not len(result.books) 
    assert result.source is SourceEnum.internal
    

# Factories Dependencies
def mock_context(side_effect=None):
    mock_session = MagicMock(AsyncSession)
    mock_session.execute = MagicMock(AsyncResult)
    
    mock = MagicMock(IPostgresContext)
    async def async_create_session():
        return mock_session
    mock.create_session = Mock(side_effect=async_create_session)

    return mock
