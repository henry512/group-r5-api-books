from dependency_injector import containers, providers
from logging.config import fileConfig
from src.services import BookService
from src.infrastructure import PostgresContext
from src.repositories import BookRepository


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
    book_repository = providers.Singleton(
        BookRepository,
        context=postgres_context
    )
    book_service = providers.Singleton(
        BookService,
        repository=book_repository
    )
    