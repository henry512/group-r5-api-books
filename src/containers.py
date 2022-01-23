from dependency_injector import containers, providers
from logging.config import fileConfig
from src.services import BookService
from src.infrastructure import PostgresContext, HttpClient
from src.repositories import BookRepository, BookExternalRepository
from fastapi import BackgroundTasks


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[".controllers"])
    config = providers.Configuration(yaml_files=["config.yml"])
    logging = providers.Resource(
        fileConfig,
        fname="logging.ini",
    )
    
    postgres_context = providers.Singleton(
        PostgresContext,
        configuration=config
    )
    http_client = providers.Singleton(
        HttpClient
    )
    book_repository = providers.Singleton(
        BookRepository,
        context=postgres_context,
        configuration=config
    )
    book_external_repository = providers.Singleton(
        BookExternalRepository,
        http_client=http_client,
        configuration=config
    )
    background_task = providers.Singleton(
        BackgroundTasks
    )
    book_service = providers.Singleton(
        BookService,
        book_repository=book_repository,
        book_external_repository=book_external_repository,
        background_task=background_task
    )
    