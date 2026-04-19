from typing import Any
from fastkit_core.services import AsyncBaseCrudService
from fastkit_core.services import SlugServiceMixin  # Uncomment if model uses SlugMixin

from .models import Product
from .repository import ProductAsyncRepository
from .schemas import ProductCreate, ProductUpdate, ProductResponse


class ProductService(SlugServiceMixin, AsyncBaseCrudService[
    Product,
    ProductCreate,
    ProductUpdate,
    ProductResponse
]):
    """
    Async service for Product business logic.

    Inherits all async CRUD operations from AsyncBaseCrudService:
        - await find(id) / await find_or_fail(id) / await get_all() / await filter(**kwargs)
        - await paginate(page, per_page) / await exists(**kwargs) / await count(**kwargs)
        - await create(data) / await create_many(data_list)
        - await update(id, data) / await update_many(filters, data)
        - await delete(id) / await delete_many(filters)

    Lifecycle hooks available to override:
        - async validate_create(data) / async validate_update(id, data)
        - async before_create(data) / async after_create(instance)
        - async before_update(id, data) / async after_update(instance)
        - async before_delete(id) / async after_delete(id)
    """

    def __init__(self, session):
        repository = ProductAsyncRepository(session)
        super().__init__(repository, response_schema=ProductResponse)

    async def before_create(self, data: dict) -> dict:
        name = data['name']
        slug_source = name.get('en') or next(iter(name.values()), '') if isinstance(name, dict) else str(name)
        data['slug'] = await self.async_generate_slug(slug_source)
        return data

    async def find_active(self) -> list[Product]:
        """Get all active products."""
        return await self.filter(is_active=True, _order_by='name')

    async def deactivate(self, product_id: int) -> Product:
        """Deactivate product (soft disable without deleting)."""
        return await self.update(product_id, {'is_active': False})

    async def activate(self, product_id: int) -> Product:
        """Activate product."""
        return await self.update(product_id, {'is_active': True})

    async def find_by_sku(self, sku: str) -> Product | None:
        """Find product by SKU."""
        return await self.filter_one(sku=sku)
