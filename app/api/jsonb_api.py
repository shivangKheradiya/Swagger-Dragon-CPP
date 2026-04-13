from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.jsonb_value import JSONBCreate
from ..registry import LIVE_TABLE_REGISTRY

# ✅ NEW: session-overlay CRUD (to be implemented next)
from ..crud.session_overlay_crud import (
    push_create,
    push_update,
    push_delete,
)

from ..crud.session_read_crud import (
    read_all_with_overlay,
    read_one_with_overlay,
)

router = APIRouter(prefix="/{code}", tags=["JSONB Dynamic Tables"])


# ---------------------------------------------------------
# Helper: validate table name early
# ---------------------------------------------------------
def validate_table(table: str):
    if table not in LIVE_TABLE_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table}")


# ---------------------------------------------------------
# CREATE → SESSION OVERLAY
# ---------------------------------------------------------
@router.post("/{table}", summary="Create a JSONB record (session overlay)")
def create_jsonb_record(
    code: str,
    table: str,
    payload: JSONBCreate,
    db: Session = Depends(get_db),
):
    validate_table(table)

    # ✅ Re-validate with table context
    JSONBCreate.model_validate(
        payload.model_dump(),
        context={"table": table},
    )

    return push_create(db, table, payload)


# ---------------------------------------------------------
# READ ALL (LIVE ONLY FOR NOW)
# ---------------------------------------------------------
@router.get("/{table}", summary="Read all records from a JSONB table")
def read_all_jsonb_records(
    code: str,
    table: str,
    db: Session = Depends(get_db),
):
    validate_table(table)
    LiveModel = LIVE_TABLE_REGISTRY[table]
    return db.query(LiveModel).all()


# ---------------------------------------------------------
# READ ONE (LIVE ONLY FOR NOW)
# ---------------------------------------------------------
@router.get("/{table}/{uuid}", summary="Read one JSONB record by UUID")
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
@router.put("/{table}/{uuid}", summary="Update a JSONB record (session overlay)")
def update_jsonb_record(
    code: str,
    table: str,
    uuid: UUID,
    payload: JSONBCreate,
    db: Session = Depends(get_db),
):
    validate_table(table)

    JSONBCreate.model_validate(
        payload.model_dump(),
        context={"table": table},
    )

    return push_update(db, table, uuid, payload)


# ---------------------------------------------------------
# DELETE → SESSION OVERLAY
# ---------------------------------------------------------
@router.delete("/{table}/{uuid}", summary="Delete a JSONB record (session overlay)")
def delete_jsonb_record(
    code: str,
    table: str,
    uuid: UUID,
    session_uuid: UUID,
    db: Session = Depends(get_db),
):
    validate_table(table)
    return push_delete(db, table, uuid, session_uuid)


# ---------------------------------------------------------
# READ ALL (SESSION VIEW)
# ---------------------------------------------------------
@router.get(
    "/{table}/session/{session_uuid}",
    summary="Read all records with session overlay",
)
def read_all_with_session(
    code: str,
    table: str,
    session_uuid: UUID,
    db: Session = Depends(get_db),
):
    validate_table(table)
    return read_all_with_overlay(db, table, session_uuid)


# ---------------------------------------------------------
# READ ONE (SESSION VIEW)
# ---------------------------------------------------------
@router.get(
    "/{table}/{uuid}/session/{session_uuid}",
    summary="Read one record with session overlay",
)
def read_one_with_session(
    code: str,
    table: str,
    uuid: UUID,
    session_uuid: UUID,
    db: Session = Depends(get_db),
):
    validate_table(table)

    result = read_one_with_overlay(
        db=db,
        table_name=table,
        uuid=uuid,
        session_uuid=session_uuid,
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Record not found")

    return result