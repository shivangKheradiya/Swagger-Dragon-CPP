from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import (
    TreeNodes,
    TreeNodeAttributes,
    ElementTypes,
    ElementTypeAttributes
)

TABLE_MAP = {
    "TreeNodes": TreeNodes,
    "TreeNodeAttributes": TreeNodeAttributes,
    "ElementTypes": ElementTypes,
    "ElementTypeAttributes": ElementTypeAttributes,
}

PRIMARY_KEYS = {
    "TreeNodes": "UUID",
    "TreeNodeAttributes": "UUID",
    "ElementTypes": "IDNo",
    "ElementTypeAttributes": "IDNo",
}


def create_record(db: Session, table: str, data: dict):
    Model = TABLE_MAP[table]
    record = Model(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def read_all_records(db: Session, table: str):
    Model = TABLE_MAP[table]
    return db.query(Model).all()


def read_record(db: Session, table: str, key: str):
    Model = TABLE_MAP[table]
    pk = PRIMARY_KEYS[table]
    record = db.query(Model).filter(getattr(Model, pk) == key).first()
    return record


def update_record(db: Session, table: str, key: str, data: dict):
    Model = TABLE_MAP[table]
    pk = PRIMARY_KEYS[table]

    record = db.query(Model).filter(getattr(Model, pk) == key).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    for k, v in data.items():
        setattr(record, k, v)

    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, table: str, key: str):
    Model = TABLE_MAP[table]
    pk = PRIMARY_KEYS[table]

    record = db.query(Model).filter(getattr(Model, pk) == key).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()
    return {"status": "deleted"}