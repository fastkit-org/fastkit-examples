from sqlalchemy.ext.asyncio import AsyncSession
from fastkit_core.database import AsyncRepository

from .models import Product


class ProductAsyncRepository(AsyncRepository[Product]):
    """
    Async repository for Product database operations.

    Inherits all async CRUD operations from AsyncRepository:
        - await create(data) / await create_many(data_list)
        - await get(id) / await get_or_404(id) / await get_all()
        - await filter(**kwargs) / await paginate(page, per_page)
        - await update(id, data) / await update_many(filters, data)
        - await delete(id) / await delete_many(filters)

    Example:
        repo = ProductAsyncRepository(session)
        instance = await repo.create({'field': 'value'})
        instances = await repo.filter(field='value', _order_by='-created_at')
        instances, meta = await repo.paginate(page=1, per_page=20)
    """

    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    # Define custom async query methods here
    # Example:
    # async def find_by_name(self, name: str) -> Product | None:
    #     results = await self.filter(name=name)
    #     return results[0] if results else None
