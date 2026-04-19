from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from starlette.responses import JSONResponse

from fastkit_core.database import get_async_db
from fastkit_core.http import success_response, error_response, paginated_response
from fastkit_core.validation.errors import format_validation_errors
from fastkit_core.i18n import _
from .service import ProductService
from .schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Product"],
)


def get_service(session: AsyncSession = Depends(get_async_db)) -> ProductService:
    return ProductService(session)


@router.get('', name='api.products.index')
async def index(page: int = 1, per_page: int = 10, service: ProductService = Depends(get_service)) -> JSONResponse:
    products, meta = await service.paginate(page=page, per_page=per_page)
    return paginated_response(items=[product.model_dump() for product in products], pagination=meta)

@router.post('', name='api.products.store')
async def store(product: ProductCreate, service: ProductService = Depends(get_service)) -> JSONResponse:
    data = await service.create(product.model_dump())
    return success_response(data= data.model_dump(), message=_('products.create'), status_code=201)

@router.put('{id}', name='api.products.update')
async def update(id: int, product: ProductUpdate, service: ProductService = Depends(get_service)) -> JSONResponse:
    data = await service.update(id, product)
    return success_response(data=data.model_dump(), message=_('products.update'))

@router.delete('{id}', name='api.products.delete', status_code=204)
async def delete(id: int, service: ProductService = Depends(get_service)):
   await service.delete(id)
