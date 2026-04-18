from sqlalchemy.orm import Session
from fastkit_core.database import Repository

from .models import Clients


class ClientsRepository(Repository[Clients]):
    """
    Repository for Clients database operations.

    Inherits all CRUD operations from Repository:
        - create(data) / create_many(data_list)
        - get(id) / get_or_404(id) / get_all()
        - filter(**kwargs) / paginate(page, per_page)
        - update(id, data) / update_many(filters, data)
        - delete(id) / delete_many(filters)

    Example:
        repo = ClientsRepository(Clients, session)
        instance = repo.create({'field': 'value'})
        instances = repo.filter(field='value', _order_by='-created_at')
        instances, meta = repo.paginate(page=1, per_page=20)
    """

    def __init__(self, session: Session):
        super().__init__(Clients, session)

    # Define custom query methods here
    # Example:
    # def find_by_name(self, name: str) -> Clients | None:
    #     results = self.filter(name=name)
    #     return results[0] if results else None
