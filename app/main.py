from fastapi import FastAPI
from app.api.jsonb_api import router as jsonb_router
from app.api.session_api import router as session_router
from app.api.search_api import router as search_router

def create_app() -> FastAPI:
    """
    Application bootstrap.

    IMPORTANT:
    - No global engine
    - No Base.metadata.create_all()
    - DB setup happens inside get_engine(code)
    """
    app = FastAPI(
        title="Dynamic JSONB CRUD API",
        version="1.0.0",
    )

    # Register JSONB dynamic API
    app.include_router(jsonb_router)
    app.include_router(session_router)
    app.include_router(search_router)

    return app


app = create_app()