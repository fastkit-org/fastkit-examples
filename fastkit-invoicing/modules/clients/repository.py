from sqlalchemy.ext.asyncio import AsyncSession
from fastkit_core.database import AsyncRepository

from .models import Clients


class ClientsRepository(AsyncRepository[Clients]):
    """
    Repository for Clients database operations.

    Inherits all CRUD operations from AsyncRepository:
        - create(data) / create_many(data_list)
        - get(id) / get_or_404(id) / get_all()
        - filter(**kwargs) / paginate(page, per_page)
        - update(id, data) / update_many(filters, data)
        - delete(id) / delete_many(filters)
    """

    def __init__(self, session: AsyncSession):
        super().__init__(Clients, session)
