from fastapi import FastAPI
from modules.clients.router import router as clients_router
from modules.products.router import router as products_router
from modules.invoices.router import router as invoices_router

from fastkit_core.database import init_async_database
from fastkit_core.cache import setup_cache
from fastkit_core.config import ConfigManager

configuration = ConfigManager(modules=['app', 'database', 'cache'])
init_async_database(configuration)
setup_cache(configuration)

app = FastAPI()

app.include_router(clients_router)
app.include_router(products_router)
app.include_router(invoices_router)