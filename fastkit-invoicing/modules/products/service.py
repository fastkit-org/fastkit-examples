from typing import Any
from fastkit_core.services import BaseCrudService
from fastkit_core.services import SlugServiceMixin  # Uncomment if model uses SlugMixin

from .models import Product
from .repository import ProductRepository
from .schemas import ProductCreate, ProductUpdate, ProductResponse


class ProductService(SlugServiceMixin, BaseCrudService[
    Product,
    ProductCreate,
    ProductUpdate,
    ProductResponse
]):
    """
    Service for Product business logic.

    Inherits all CRUD operations from BaseCrudService:
        - find(id) / find_or_fail(id) / get_all() / filter(**kwargs)
        - paginate(page, per_page) / exists(**kwargs) / count(**kwargs)
        - create(data) / create_many(data_list)
        - update(id, data) / update_many(filters, data)
        - delete(id) / delete_many(filters)

    Lifecycle hooks available to override:
        - validate_create(data) / validate_update(id, data)
        - before_create(data) / after_create(instance)
        - before_update(id, data) / after_update(instance)
        - before_delete(id) / after_delete(id)
    """

    def __init__(self, session):
        repository = ProductRepository(session)
        super().__init__(repository, response_schema=ProductResponse)

    async def before_create(self, data: dict) -> dict:
        data['slug'] = await self.async_generate_slug(data['name'])
        return data

    def find_active(self) -> list[Product]:
        """Get all active products."""
        return self.filter(is_active=True, _order_by='name')

    def deactivate(self, product_id: int) -> Product:
        """Deactivate product (soft disable without deleting)."""
        return self.update(product_id, {'is_active': False})

    def activate(self, product_id: int) -> Product:
        """Activate product."""
        return self.update(product_id, {'is_active': True})

    def find_by_sku(self, sku: str) -> Product | None:
        """Find product by SKU."""
        return self.filter_one(sku=sku)
