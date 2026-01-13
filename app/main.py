from fastapi import FastAPI
from .api.router import router
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Deribit Monitor")
app.include_router(router, prefix="/api/v1")