from fastapi import FastAPI
from modules.clients.router import router as clients_router

from fastkit_core.database import init_async_database
from fastkit_core.config import ConfigManager
configuration = ConfigManager(modules=['app', 'database'])
init_async_database(configuration)

app = FastAPI()

app.include_router(clients_router)