from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.jsonb_value import JSONBCreate
from app.registry import LIVE_TABLE_REGISTRY

from app.schemas.jsonb_bulk import JSONBBulkRequest, JSONBBulkResponse
from app.crud.session_bulk_crud import bulk_stage_operations

from app.crud.session_overlay_crud import (
    push_create,
    push_update,
    push_delete,
)

from app.crud.session_read_crud import (
    read_session_overlay,
    read_session_overlay_one,
)

from app.api.helper import validate_table

router = APIRouter(
    prefix="/{code}",
    tags=["JSON Dynamic Tables Management"],
)


# ---------------------------------------------------------
# CREATE → SESSION OVERLAY
# ---------------------------------------------------------
@router.post(
    "/{table}",
    summary="Stage creation of a JSONB record (session overlay)",
)
def create_jsonb_record(
    code: str,
    table: str,
    payload: JSONBCreate,
    db: Session = Depends(get_db),
):
    validate_table(table)

    return push_create(
        db=db,
        table_code=table,
        payload=payload,
    )


# ---------------------------------------------------------
# UPDATE → SESSION OVERLAY
# ---------------------------------------------------------
@router.put(
    "/{table}/{uuid}",
    summary="Stage update of a JSONB record (session overlay)",
)
def update_jsonb_record(
    code: str,
    table: str,
    uuid: UUID,
    payload: JSONBCreate,
    db: Session = Depends(get_db),
):
    validate_table(table)

    return push_update(
        db=db,
        table_code=table,
        attribute_uuid=uuid,
        payload=payload,
    )


# ---------------------------------------------------------
# DELETE → SESSION OVERLAY
# ---------------------------------------------------------
@router.delete(
    "/{table}/{uuid}",
    summary="Stage deletion of a JSONB record (session overlay)",
)
def delete_jsonb_record(
    code: str,
    table: str,
    uuid: UUID,
    session_uuid: UUID,
    db: Session = Depends(get_db),
):
    validate_table(table)

    return push_delete(
        db=db,
        table_code=table,
        attribute_uuid=uuid,
        session_uuid=session_uuid,
    )

# ---------------------------------------------------------
# READ SESSION OVERLAY (ALL)
# ---------------------------------------------------------
@router.get(
    "/{table}/session/{session_uuid}",
    summary="Read staged changes for a session (overlay only)",
)
def read_session_overlay_api(
    code: str,
    table: str,
    session_uuid: UUID,
    db: Session = Depends(get_db),
):
    validate_table(table)

    return read_session_overlay(
        db=db,
        table_code=table,
        session_uuid=session_uuid,
    )


# ---------------------------------------------------------
# READ SESSION OVERLAY (ONE)
# ---------------------------------------------------------
@router.get(
    "/{table}/{uuid}/session/{session_uuid}",
    summary="Read staged change for one attribute in a session",
)
def read_session_overlay_one_api(
    code: str,
    table: str,
    uuid: UUID,
    session_uuid: UUID,
    db: Session = Depends(get_db),
):
    validate_table(table)

    return read_session_overlay_one(
        db=db,
        table_code=table,
        session_uuid=session_uuid,
        attribute_uuid=uuid,
    )


# ---------------------------------------------------------
# BULK STAGE OPERATIONS (SESSION OVERLAY)
# ---------------------------------------------------------
@router.post(
    "/{table}/bulk",
    response_model=JSONBBulkResponse,
    summary="Stage bulk JSONB operations (CREATE → UPDATE → DELETE)",
)
def bulk_jsonb_operations(
    code: str,
    table: str,
    payload: JSONBBulkRequest,
    db: Session = Depends(get_db),
):
    """
    Stage a bulk set of operations inside a session.

    - Operations are executed in strict order:
        CREATE → UPDATE → DELETE
    - Each item is committed independently
    - Failures do not stop the batch
    - Failed indices are returned for tool-level retry
    """

    validate_table(table)

    return bulk_stage_operations(
        db=db,
        table_code=table,
        payload=payload,
    )
