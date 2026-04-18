from fastapi import FastAPI
from modules.clients.router import router as clients_router

app = FastAPI()

app.include_router(clients_router)