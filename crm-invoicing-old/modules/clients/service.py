from fastkit_core.services import AsyncBaseCrudService
from fastkit_core.database import AsyncRepository
from sqlalchemy.orm import Session
from modules.clients.models import Client
from modules.clients.schemas import ClientCreate, ClientUpdate, ClientResponse

class ClientService(AsyncBaseCrudService[Client, ClientCreate, ClientUpdate, ClientResponse]):
    def __init__(self, session: Session):
        repository = AsyncRepository(Client, session)
        super().__init__(repository, response_schema=ClientResponse)