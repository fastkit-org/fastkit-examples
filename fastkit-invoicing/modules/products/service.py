from typing import Any
from fastkit_core.services import AsyncBaseCrudService
from fastkit_core.services import SlugServiceMixin
from fastkit_core.cache import cache
from fastkit_core.cache.decorators import cached

from .models import Product
from .repository import ProductAsyncRepository
from .schemas import ProductCreate, ProductUpdate, ProductResponse

CACHE_PREFIX = "products"
CACHE_TTL = 300  # 5 minutes


class ProductService(SlugServiceMixin, AsyncBaseCrudService[
    Product,
    ProductCreate,
    ProductUpdate,
    ProductResponse
]):
    def __init__(self, session):
        repository = ProductAsyncRepository(session)
        super().__init__(repository, response_schema=ProductResponse)

    # -------------------------------------------------------------------------
    # Cache key helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _page_cache_key(page: int, per_page: int) -> str:
        return f"{CACHE_PREFIX}:page:{page}:per_page:{per_page}"

    @staticmethod
    def _item_cache_key(product_id: int) -> str:
        return f"{CACHE_PREFIX}:item:{product_id}"

    # -------------------------------------------------------------------------
    # Cached reads
    # -------------------------------------------------------------------------

    @cached(
        ttl=CACHE_TTL,
        key=lambda self, page=1, per_page=10: ProductService._page_cache_key(page, per_page)
    )
    async def paginate(self, page: int = 1, per_page: int = 10):
        return await super().paginate(page=page, per_page=per_page)

    @cached(
        ttl=CACHE_TTL,
        key=lambda self, product_id: ProductService._item_cache_key(product_id)
    )
    async def find(self, product_id: int):
        return await super().find(product_id)

    # -------------------------------------------------------------------------
    # Cache invalidation
    # -------------------------------------------------------------------------

    async def _invalidate_product_cache(self) -> None:
        """Invalidate all product cache entries."""
        await cache.invalidate(f"{CACHE_PREFIX}:*")

    async def after_create(self, instance: Product) -> None:
        await self._invalidate_product_cache()

    async def after_update(self, instance: Product) -> None:
        await self._invalidate_product_cache()

    async def after_delete(self, id: Any) -> None:
        await self._invalidate_product_cache()

    # -------------------------------------------------------------------------
    # Business logic
    # -------------------------------------------------------------------------

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
