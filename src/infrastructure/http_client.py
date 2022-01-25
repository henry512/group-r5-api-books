from abc import ABC, abstractmethod
from typing import Optional, Any, ByteString, Tuple
from aiohttp import ClientSession
import logging


class IHttpClient(ABC):
    @abstractmethod
    async def get(self, url: str) -> Tuple[Optional[ByteString], int]:
        raise NotImplementedError

    @abstractmethod
    async def post(self, url: str, data: Any) -> Tuple[Optional[ByteString], int]:
        raise NotImplementedError
    
    @abstractmethod
    async def put(self, url: str, data: Any) -> Tuple[Optional[ByteString], int]:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, url: str) -> Tuple[Optional[ByteString], int]:
        raise NotImplementedError
    
    
class HttpClient(IHttpClient):
    def __init__(self):
        self._client_session: Optional[ClientSession] = None
        self._log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        
    async def get(self, url: str) -> Tuple[Optional[ByteString], int]:
        async with self._get_session_connection().get(url) as res:
            try:
                return tuple([await res.read(), res.status])
            except Exception as error:
                self._log.exception(
                    f"Http Client Exception has occurred: URL: {url}",
                    exc_info=error
                )
                raise
    
    async def post(self, url: str, data: Any) -> Tuple[Optional[ByteString], int]:
        raise NotImplementedError
    
    async def put(self, url: str, data: Any) -> Tuple[Optional[ByteString], int]:
        raise NotImplementedError
    
    async def delete(self, url: str) -> Tuple[Optional[ByteString], int]:
        raise NotImplementedError

    def _get_session_connection(self) -> ClientSession:
        if self._client_session is None:
            self._client_session = ClientSession()
        return self._client_session
    
    async def __del__(self):
        if self._client_session:
            await self._client_session.close()
