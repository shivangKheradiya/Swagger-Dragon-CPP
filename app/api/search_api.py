from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from app.database import get_db
from app.schemas.search import SearchRequest
from app.crud.search_crud import execute_search

from app.api.helper import validate_table

router = APIRouter(
    prefix="/{code}",
    tags=["Search Query on Table"],
)

@router.post(
    "/search",
    summary="Generic cascading search (AND / OR)",
)
def search_jsonb(
    code: str,
    payload: SearchRequest,
    db: Session = Depends(get_db),
):
    validate_table(payload.table)
    return execute_search(db, payload)