from fastapi import FastAPI
from app.routers.attributes_design import router as attributes_router
from app.routers.history_design import router as history_router
from app.db import engine
from app.models.base import Base

app = FastAPI(title="Attribute-Driven Tree API")

Base.metadata.create_all(bind=engine)

app.include_router(attributes_router)
app.include_router(history_router)