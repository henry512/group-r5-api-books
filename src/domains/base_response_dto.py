from typing import Any, Optional
from pydantic import BaseModel


class BaseResponseDTO(BaseModel):
    api_version : str
    method: str
    data: Optional[Any]
