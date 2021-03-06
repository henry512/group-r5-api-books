from abc import ABC, abstractmethod
from typing import Optional
from retry import retry
from dependency_injector.providers import Configuration
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
import logging


class IPostgresContext(ABC):
    @abstractmethod
    def get_engine(self) -> AsyncEngine:
        raise NotImplementedError

    @abstractmethod
    def create_session(self) -> AsyncSession:
        raise NotImplementedError
    

class PostgresContext(IPostgresContext):
    def __init__(self, configuration: Configuration):
        self._connectionstring: str = configuration["database"]["connection"]
        self._engine: Optional[AsyncEngine] = None
        self._log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def get_engine(self) -> AsyncEngine:
        if self._engine is None:
            self._open_connection()
        return self._engine
    
    def create_session(self) -> AsyncSession:
        return AsyncSession(self.get_engine(), expire_on_commit=False)

    @retry((Exception), tries=3)
    def _open_connection(self):
        try:
            self._engine = create_async_engine(
                self._connectionstring, 
                future=True, 
                pool_size=10,
                max_overflow=0,
            )
        except Exception as error:
            self._log.exception(
                "An error occurred while trying to connect to database",
                exc_info=error
            )
            raise
        
    async def __del__(self):
        if self._engine:
            await self._engine.dispose()
