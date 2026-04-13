from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.registry import LIVE_TABLE_REGISTRY, HISTORY_TABLE_REGISTRY


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
        LiveModel = LIVE_TABLE_REGISTRY[table_name]
        HistoryModel = HISTORY_TABLE_REGISTRY[table_name]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    obj = LiveModel(**data)
    db.add(obj)
    db.flush()  # get obj.uuid
    
    if HistoryModel:
        history = HistoryModel(
            TNAUUID=obj.uuid,
            OperationType=1,  # CREATE
            OldValue=None,
            NewValue=obj.value,
        )
        db.add(history)

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
        LiveModel = LIVE_TABLE_REGISTRY[table_name]
        HistoryModel = HISTORY_TABLE_REGISTRY[table_name]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    return db.query(LiveModel).all()


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
        LiveModel = LIVE_TABLE_REGISTRY[table_name]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    obj = db.query(LiveModel).filter(LiveModel.uuid == uuid).first()

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
        LiveModel = LIVE_TABLE_REGISTRY[table_name]
        HistoryModel = HISTORY_TABLE_REGISTRY[table_name]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    obj = db.query(LiveModel).filter(LiveModel.uuid == uuid).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Record not found")

    old_value = obj.value

    for key, value in data.items():
        setattr(obj, key, value)

    if HistoryModel:
        history = HistoryModel(
            TNAUUID=obj.uuid,
            OperationType=2,  # UPDATE
            OldValue=old_value,
            NewValue=obj.value,
        )
        db.add(history)

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
        LiveModel = LIVE_TABLE_REGISTRY[table_name]
        HistoryModel = HISTORY_TABLE_REGISTRY[table_name]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    obj = db.query(LiveModel).filter(LiveModel.uuid == uuid).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Record not found")

    if HistoryModel:
        history = HistoryModel(
            TNAUUID=obj.uuid,
            OperationType=3,  # DELETE
            OldValue=obj.value,
            NewValue=None,
        )
        db.add(history)

    db.delete(obj)
    db.commit()

    return {"status": "deleted"}
