from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.jsonb_value import JSONBCreate
from app.registry import LIVE_TABLE_REGISTRY

from app.crud.session_overlay_crud import (
    push_create,
    push_update,
    push_delete,
)

from app.crud.session_read_crud import (
    read_session_overlay,
    read_session_overlay_one,
)

router = APIRouter(
    prefix="/{code}",
    tags=["JSONB Dynamic Tables"],
)


# ---------------------------------------------------------
# Helper: validate domain/table code
# ---------------------------------------------------------
def validate_table(table: str):
    if table not in LIVE_TABLE_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Invalid table code: {table}")


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
# READ ALL (LIVE TABLE ONLY)
# ---------------------------------------------------------
@router.get(
    "/{table}",
    summary="Read all JSONB records (live)",
)
def read_all_jsonb_records(
    code: str,
    table: str,
    db: Session = Depends(get_db),
):
    validate_table(table)

    LiveModel = LIVE_TABLE_REGISTRY[table]
    return db.query(LiveModel).all()


# ---------------------------------------------------------
# READ ONE (LIVE TABLE ONLY)
# ---------------------------------------------------------
@router.get(
    "/{table}/{uuid}",
    summary="Read one JSONB record by UUID (live)",
)
def read_jsonb_record(
    code: str,
    table: str,
    uuid: UUID,
    db: Session = Depends(get_db),
):
    validate_table(table)

    LiveModel = LIVE_TABLE_REGISTRY[table]
    obj = db.query(LiveModel).filter(LiveModel.uuid == uuid).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Record not found")

    return obj


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