from fastkit_core.services import AsyncBaseCrudService, SlugServiceMixin
from fastkit_core.database import AsyncRepository
from sqlalchemy.orm import Session
from .models import Product
from .schemas import ProductCreate, ProductUpdate, ProductResponse


class ProductService(SlugServiceMixin, AsyncBaseCrudService[Product, ProductCreate, ProductUpdate, ProductResponse]):
    def __init__(self, session: Session):
        self.repository = AsyncRepository(Product, session)
        super().__init__(self.repository, response_schema=ProductResponse)

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
