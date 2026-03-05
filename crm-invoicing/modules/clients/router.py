from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.infrastructure.auth import current_active_user
from fastkit_core.database import get_db
from fastkit_core.http import success_response, paginated_response
from fastkit_core.i18n import _
from .service import ClientService
from .schemas import ClientCreate, ClientUpdate

router = APIRouter(
    prefix="/clients",
    tags=["Client"],
    dependencies=[Depends(current_active_user)]
)


def get_service(session: Session = Depends(get_db)) -> ClientService:
    return ClientService(session)


@router.get('', name='api.clients.index')
async def index(
        page: int = 1,
        per_page: int = 10,
        service: ClientService = Depends(get_service)
) -> JSONResponse:
    clients, meta = await service.paginate(page=page, per_page=per_page)
    return paginated_response(items=[client.model_dump() for client in clients], pagination=meta)

@router.post('', name='api.clients.store')
async def store(client: ClientCreate, service: ClientService = Depends(get_service)) -> JSONResponse:
    data = await service.create(client.model_dump())
    return success_response(
        data= data.model_dump(),
        message=_('clients.create'),
        status_code=201
    )

@router.put('{id}', name='api.clients.update')
async def update(id: int, client: ClientUpdate, service: ClientService = Depends(get_service)) -> JSONResponse:
    data = await service.update(id, client)
    return success_response(
        data=data.model_dump(),
        message=_('clients.update')
    )

@router.delete('{id}', name='api.client.delete', status_code=204)
async def delete(id: int, service: ClientService = Depends(get_service)):
   await service.delete(id)
