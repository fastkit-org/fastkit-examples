from typing import Any
from fastkit_core.services import BaseCrudService
# from fastkit_core.services import SlugServiceMixin  # Uncomment if model uses SlugMixin

from .models import Clients
from .repository import ClientsRepository
from .schemas import ClientsCreate, ClientsUpdate, ClientsResponse


class ClientsService(BaseCrudService[
    Clients,
    ClientsCreate,
    ClientsUpdate,
    ClientsResponse
]):
    """
    Service for Clients business logic.

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
        repository = ClientsRepository(session)
        super().__init__(repository, response_schema=ClientsResponse)

    # -------------------------------------------------------------------------
    # Validation hooks
    # -------------------------------------------------------------------------

    def validate_create(self, data: ClientsCreate) -> None:
        pass
        # Example:
        # if self.exists(name=data.name):
        #     raise ValueError(_('validation.clientses.name_taken'))

    def validate_update(self, id: Any, data: ClientsUpdate) -> None:
        pass

    # -------------------------------------------------------------------------
    # Lifecycle hooks
    # -------------------------------------------------------------------------

    def before_create(self, data: dict) -> dict:
        return data
        # Example:
        # data['slug'] = self.generate_slug(data['name'])  # Requires SlugServiceMixin
        # return data

    def after_create(self, instance: Clients) -> None:
        pass
        # Example:
        # send_welcome_email(instance.email)

    def before_update(self, id: Any, data: dict) -> dict:
        return data

    def after_update(self, instance: Clients) -> None:
        pass

    def before_delete(self, id: Any) -> None:
        pass

    def after_delete(self, id: Any) -> None:
        pass
