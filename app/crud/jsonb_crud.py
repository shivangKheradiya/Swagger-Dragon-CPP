from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..registry import get_desi_model


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def create_record(
    db: Session,
    table_name: str,
    data: dict,
):
    """
    Create a new record in a JSONB dynamic table.
    """
    try:
        Model = get_desi_model(table_name)
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    obj = Model(**data)

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ---------------------------------------------------------
# READ (ALL)
# ---------------------------------------------------------
def read_all_records(
    db: Session,
    table_name: str,
):
    """
    Read all records from a JSONB dynamic table.
    """
    try:
        Model = get_desi_model(table_name)
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    return db.query(Model).all()


# ---------------------------------------------------------
# READ (ONE)
# ---------------------------------------------------------
def read_record_by_uuid(
    db: Session,
    table_name: str,
    uuid,
):
    """
    Read a single record by UUID.
    """
    try:
        Model = get_desi_model(table_name)
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    obj = db.query(Model).filter(Model.uuid == uuid).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Record not found")

    return obj


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------
def update_record(
    db: Session,
    table_name: str,
    uuid,
    data: dict,
):
    """
    Update an existing record by UUID.
    """
    try:
        Model = get_desi_model(table_name)
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    obj = db.query(Model).filter(Model.uuid == uuid).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Record not found")

    for key, value in data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)

    return obj


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
def delete_record(
    db: Session,
    table_name: str,
    uuid,
):
    """
    Delete a record by UUID.
    """
    try:
        Model = get_desi_model(table_name)
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    obj = db.query(Model).filter(Model.uuid == uuid).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(obj)
    db.commit()

    return {"status": "deleted"}
