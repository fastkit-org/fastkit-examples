from sqlalchemy.ext.asyncio import AsyncSession
from fastkit_core.database import AsyncRepository

from .models import InvoiceItem


class InvoiceItemRepository(AsyncRepository[InvoiceItem]):
    def __init__(self, session: AsyncSession):
        super().__init__(InvoiceItem, session)
