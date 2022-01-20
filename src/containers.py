from operator import contains
from dependency_injector import containers, providers
from logging.config import fileConfig
from src.services import BookService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[".controllers"])
    config = providers.Configuration(yaml_files=["config.yml"])
    logging = providers.Resource(
        fileConfig,
        fname="logging.ini",
    )
    
    book_service = providers.Singleton(
        BookService
    )
    