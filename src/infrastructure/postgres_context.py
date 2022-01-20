from abc import ABC, abstractmethod
from asyncpg import create_pool, Pool, PostgresConnectionError
from typing import Optional
from retry import retry
from pandas import DataFrame
from dependency_injector.providers import Configuration


class IPostgresContext(ABC):
    @abstractmethod
    async def find(self, query: str) -> DataFrame:
        raise NotImplementedError

    @abstractmethod
    async def execute_query(self, query: str) -> None:
        raise NotImplementedError


class PostgresContext(IPostgresContext):
    def __init__(self, configuration: Configuration):
        self._connectionstring: str = configuration["database"]["connection"]
        self._pool_connection: Optional[Pool] = None

    async def find(self, query: str) -> DataFrame:
        pool = await self._get_pool_connection()
        async with pool.acquire() as connection:
            async with connection.transaction():
                try:
                    result = await connection.fetch(query)
                    if result:
                        return DataFrame([dict(row) for row in result]) 
                    return DataFrame()
                except Exception as error:
                    print(f"Postgres Exception has occurred: \n Error: {error} \n Query: {query} \n")
                    raise

    async def execute_query(self, query: str) -> None:
        pool = await self._get_pool_connection()
        async with pool.acquire() as connection:
            async with connection.transaction():
                try:
                    await connection.execute(query)
                except Exception as error:
                    print(f"Postgres Exception has occurred: \n Error: {error} \n Query: {query} \n")
                    raise

    async def _get_pool_connection(self) -> Pool:
        if self._pool_connection is None or self._pool_connection._closed:
            await self._open_connection()
        return self._pool_connection

    @retry((PostgresConnectionError), tries=3)
    async def _open_connection(self):
        try:
            self._pool_connection = await create_pool(self._connectionstring)
        except PostgresConnectionError:
            raise