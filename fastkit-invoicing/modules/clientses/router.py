from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import ValidationError
from starlette.responses import JSONResponse

from fastkit_core.database import get_db
from fastkit_core.http import success_response, error_response, paginated_response
from fastkit_core.validation.errors import format_validation_errors
from fastkit_core.i18n import _
from .service import ClientsService
from .schemas import ClientsCreate, ClientsUpdate, ClientsResponse

router = APIRouter(
    prefix="/clientses",
    tags=["Clients"],
)


def get_service(session: Session = Depends(get_db)) -> ClientsService:
    return ClientsService(session)


@router.get("/", response_model=list[ClientsResponse])
def index(
    page: int = 1,
    per_page: int = 20,
    service: ClientsService = Depends(get_service),
) -> JSONResponse:
    items, meta = service.paginate(page=page, per_page=per_page)
    return paginated_response(items=items, pagination=meta)


@router.get("/{id}", response_model=ClientsResponse)
def show(
    id: int,
    service: ClientsService = Depends(get_service),
) -> JSONResponse:
    item = service.find_or_fail(id)
    return success_response(data=item.model_dump())


@router.post("/", response_model=ClientsResponse, status_code=status.HTTP_201_CREATED)
def store(
    data: ClientsCreate,
    service: ClientsService = Depends(get_service),
) -> JSONResponse:
    try:
        item = service.create(data)
        return success_response(data=item.model_dump(), status_code=status.HTTP_201_CREATED)
    except ValidationError as e:
        errors = format_validation_errors(e.errors())
        return error_response(message=_('validation.failed'), errors=errors, status_code=422)


@router.put("/{id}", response_model=ClientsResponse)
def update(
    id: int,
    data: ClientsUpdate,
    service: ClientsService = Depends(get_service),
) -> JSONResponse:
    try:
        item = service.update(id, data)
        return success_response(data=item.model_dump())
    except ValidationError as e:
        errors = format_validation_errors(e.errors())
        return error_response(message=_('validation.failed'), errors=errors, status_code=422)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id: int,
    service: ClientsService = Depends(get_service),
) -> None:
    service.delete(id)
