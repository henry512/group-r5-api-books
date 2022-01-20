from src.domains import OperatorEnum, BaseResponseDTO, BookFiltered
from typing import List, Optional
from fastapi import APIRouter, status, Depends
from dependency_injector.wiring import inject, Provide
from src.containers import Container
from src.services import IBookService


router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=BaseResponseDTO, status_code=status.HTTP_200_OK)
@inject
async def get(
    operator: Optional[OperatorEnum]=OperatorEnum.contains,
    id: Optional[str]=None,
    title: Optional[str]=None, 
    subtitle: Optional[str]=None,
    author: Optional[str]=None,
    category: Optional[str]=None,
    datetime_publication: Optional[str]=None,
    editor: Optional[str]=None,
    description: Optional[str]=None,
    service: IBookService=Depends(Provide[Container.book_service])
):
    books = await service.get_books(
        BookFiltered(
            operator=operator,
            id=id,
            title=title,
            subtitle=subtitle,
            author=author,
            category=category,
            datetime_publication=datetime_publication,
            editor=editor,
            description=description,
        )
    )
    return BaseResponseDTO(
        api_version="1.0.0", 
        method=f"{__name__}.get", 
        data=books
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def group_deleted(
    ids: List[str],
):
    return "group_deleted books"
