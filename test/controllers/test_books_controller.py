import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.services import book_service
from src.domains import BookDTO, BookFiltered, BookEntity, SourceEnum
from fastapi import status

    
client = TestClient(app)


def test_get_books_none_filters(monkeypatch):
    async def mock_get_books(self, filters):
        return BookDTO(
            books=list(), source=None
        )
    monkeypatch.setattr(book_service.BookService, "get_books", mock_get_books)
    
    async def mock_save_books(self, filters):
        return
    monkeypatch.setattr(book_service.BookService, "save_books_external", mock_save_books)
    
    response = client.get("/books/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"]["books"] == list()
    assert data["data"]["source"] is None
    

def test_get_books_internal_full_filters(monkeypatch):
    async def mock_get_books(self, filters):
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
    monkeypatch.setattr(book_service.BookService, "get_books", mock_get_books)
    
    async def mock_save_books(self, books):
        return
    monkeypatch.setattr(book_service.BookService, "save_books_external", mock_save_books)
    
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
    
    url = f"/books/?id={filters.id}&title={filters.title}&subtitle={filters.subtitle}&author={filters.author}&category={filters.category}&datetime_publication={filters.datetime_publication}&editor={filters.editor}&description={filters.description}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert len(data["data"]["books"]) > 0
    assert data["data"]["source"] == SourceEnum.internal
    

def test_get_books_external_full_filters(monkeypatch):
    async def mock_get_books(self, filters):
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
    monkeypatch.setattr(book_service.BookService, "get_books", mock_get_books)
    
    async def mock_save_books(self, books):
        return
    monkeypatch.setattr(book_service.BookService, "save_books_external", mock_save_books)
    
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
    
    url = f"/books/?id={filters.id}&title={filters.title}&subtitle={filters.subtitle}&author={filters.author}&category={filters.category}&datetime_publication={filters.datetime_publication}&editor={filters.editor}&description={filters.description}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert len(data["data"]["books"]) > 0
    assert data["data"]["source"] == SourceEnum.external
    

def test_delete_book(monkeypatch):
    async def mock_delete_book(self, id):
        return
    monkeypatch.setattr(book_service.BookService, "delete_book", mock_delete_book)
    
    identified = "id"
    response = client.delete(f"/books/?id={identified}")
    assert response.status_code == status.HTTP_204_NO_CONTENT