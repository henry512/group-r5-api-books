from src.domains import OperatorEnum, BaseResponseDTO
from typing import List, Optional
from fastapi import APIRouter, status


router = APIRouter()


@router.get("/", response_model=BaseResponseDTO, status_code=status.HTTP_200_OK)
async def get(
    operator: Optional[OperatorEnum]=OperatorEnum.contains,
    id: Optional[str]=None,
    title: Optional[str]=None, 
    subtitle: Optional[str]=None,
    author: Optional[str]=None,
    category: Optional[str]=None,
    datetime_publication: Optional[str]=None,
    editor: Optional[str]=None,
    description: Optional[str]=None
):
    return BaseResponseDTO(api_version="1.0.0", method=f"{__name__}.get")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def group_deleted(
    ids: List[str],
):
    return "group_deleted books"
