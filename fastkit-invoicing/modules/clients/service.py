from typing import Any
from fastkit_core.services import AsyncBaseCrudService

from .models import Clients
from .repository import ClientsRepository
from .schemas import ClientsCreate, ClientsUpdate, ClientsResponse


class ClientsService(AsyncBaseCrudService[
    Clients,
    ClientsCreate,
    ClientsUpdate,
    ClientsResponse
]):
    """
    Service for Clients business logic.
    """

    def __init__(self, session):
        repository = ClientsRepository(session)
        super().__init__(repository, response_schema=ClientsResponse)

    # -------------------------------------------------------------------------
    # Validation hooks
    # -------------------------------------------------------------------------

    async def validate_create(self, data: ClientsCreate) -> None:
        pass

    async def validate_update(self, id: Any, data: ClientsUpdate) -> None:
        pass

    # -------------------------------------------------------------------------
    # Lifecycle hooks
    # -------------------------------------------------------------------------

    async def before_create(self, data: dict) -> dict:
        return data

    async def after_create(self, instance: Clients) -> None:
        pass

    async def before_update(self, id: Any, data: dict) -> dict:
        return data

    async def after_update(self, instance: Clients) -> None:
        pass

    async def before_delete(self, id: Any) -> None:
        pass

    async def after_delete(self, id: Any) -> None:
        pass
