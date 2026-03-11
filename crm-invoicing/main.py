from fastapi import FastAPI
from app.routers.auth import router as auth_router
from modules.clients.router import router as client_router
from modules.products.router import router as product_router
from modules.invoices.router import router as invoice_router
from fastkit_core.database import init_async_database
from fastkit_core.config import ConfigManager
configuration = ConfigManager(modules=['app', 'database', 'auth'])
init_async_database(configuration)

app = FastAPI()
app.include_router(auth_router)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(invoice_router)
