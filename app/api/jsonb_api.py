from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.jsonb_value import JSONBCreate
from ..crud.jsonb_crud import (
    create_record,
    read_all_records,
    read_record_by_uuid,
    update_record,
    delete_record,
)
from ..registry import DESI_TABLE_REGISTRY


router = APIRouter(prefix="/{code}/jsonb", tags=["JSONB Dynamic Tables"])


# ---------------------------------------------------------
# Helper: validate table name early
# ---------------------------------------------------------
def validate_table(table: str):
    if table not in DESI_TABLE_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table}")


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
@router.post("/{table}", summary="Create a JSONB record")
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

    return create_record(db, table, payload.model_dump())


# ---------------------------------------------------------
# READ ALL
# ---------------------------------------------------------
@router.get("/{table}", summary="Read all records from a JSONB table")
def read_all_jsonb_records(
    code: str,
    table: str,
    db: Session = Depends(get_db),
):
    validate_table(table)
    return read_all_records(db, table)


# ---------------------------------------------------------
# READ ONE
# ---------------------------------------------------------
@router.get("/{table}/{uuid}", summary="Read one JSONB record by UUID")
def read_jsonb_record(
    code: str,
    table: str,
    uuid: UUID,
    db: Session = Depends(get_db),
):
    validate_table(table)
    return read_record_by_uuid(db, table, uuid)


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------
@router.put("/{table}/{uuid}", summary="Update a JSONB record")
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

    return update_record(db, table, uuid, payload.model_dump())


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
@router.delete("/{table}/{uuid}", summary="Delete a JSONB record")
def delete_jsonb_record(
    code: str,
    table: str,
    uuid: UUID,
    db: Session = Depends(get_db),
):
    validate_table(table)
    return delete_record(db, table, uuid)