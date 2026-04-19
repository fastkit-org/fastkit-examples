from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.responses import JSONResponse
from fastkit_core.database import get_async_db
from fastkit_core.http import success_response, paginated_response
from fastkit_core.i18n import _
from .service import InvoiceService
from .schemas import InvoiceCreate, InvoiceUpdate
from .models import Invoice
from modules.invoice_items.models import InvoiceItem

router = APIRouter(
    prefix="/invoices",
    tags=["Invoice"],
)


def get_service(session: AsyncSession = Depends(get_async_db)) -> InvoiceService:
    return InvoiceService(session)

@router.get('', name='api.invoices.index')
async def index(page: int = 1, per_page: int = 10, service: InvoiceService = Depends(get_service)) -> JSONResponse:
    invoices, meta = await service.paginate(
        page= page,
        per_page=per_page,
        _load_relations=[
            selectinload(Invoice.client),
            selectinload(Invoice.items).selectinload(InvoiceItem.product)
        ]
    )
    return paginated_response(items=[invoice.model_dump() for invoice in invoices], pagination=meta)

@router.post('', name='api.invoices.store')
async def store(invoice: InvoiceCreate, service: InvoiceService = Depends(get_service)) -> JSONResponse:
    data = await service.create_with_items(invoice)
    return success_response(data=data.model_dump(), message=_('invoices.create'), status_code=201)

@router.put('{id}', name='api.invoices.update')
async def update(id: int, invoice: InvoiceUpdate, service: InvoiceService = Depends(get_service)) -> JSONResponse:
    data = await service.update(id, invoice)
    return success_response(data=data.model_dump(), message=_('invoices.update'))

@router.delete('{id}', name='api.invoices.delete', status_code=204)
async def destroy(id: int, service: InvoiceService = Depends(get_service)):
    await service.delete(id)
