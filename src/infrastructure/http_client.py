from abc import ABC, abstractmethod
from typing import Optional, Any
from aiohttp import ClientSession


class IHttpClient(ABC):
    @abstractmethod
    async def get(self, url: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def post(self, url: str, data: Any) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def put(self, url: str, data: Any) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, url: str) -> Any:
        raise NotImplementedError
    
    
class HttpClient(IHttpClient):
    def __init__(self):
        self._client_session: Optional[ClientSession] = None
        
    def __del__(self):
        if self._client_session:
            self._client_session.close()
        
    async def get(self, url: str) -> Any:
        async with self._get_session_connection().get(url) as res:
            try:
                return await res.read()
            except Exception as error:
                print(f"Http Client Exception has occurred: \n Error: {error} \n URL: {url} \n")
                raise
    
    async def post(self, url: str, data: Any) -> Any:
        async with self._get_session_connection().post(url, data=bytes(data)) as res:
            try:
                return await res.read()
            except Exception as error:
                print(f"Http Client Exception has occurred: \n Error: {error} \n URL: {url} \n")
                raise
    
    async def put(self, url: str, data: Any) -> Any:
        raise NotImplementedError
    
    async def delete(self, url: str) -> Any:
        raise NotImplementedError

    def _get_session_connection(self) -> ClientSession:
        if self._client_session is None:
            self._client_session = ClientSession()
        return self._client_session
