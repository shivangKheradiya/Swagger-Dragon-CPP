from fastapi import FastAPI, Depends, HTTPException
from .crud import (
    create_record,
    read_record,
    read_all_records,
    update_record,
    delete_record,
    run_bulk_operations
)
from .database import get_db

app = FastAPI(title="OPE-DBSQLite (SQLAlchemy Version)")

ALLOWED_TABLES = {
    "TreeNodes",
    "TreeNodeAttributes",
    "ElementTypes",
    "ElementTypeAttributes",
}


@app.post("/{code}/bulk")
def api_bulk(code: str, payload: dict, db=Depends(get_db)):
    # Validate tables
    for section in ["insert", "update", "delete"]:
        if section in payload:
            for table in payload[section].keys():
                if table not in ALLOWED_TABLES:
                    raise HTTPException(status_code=400, detail=f"Invalid table: {table}")

    return run_bulk_operations(db, payload)


def validate_table(table: str):
    if table not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail=f"Invalid table: {table}")


@app.post("/{code}/{table}")
def api_create(code: str, table: str, payload: dict, db=Depends(get_db)):
    validate_table(table)
    return create_record(db, table, payload)


@app.get("/{code}/{table}")
def api_read_all(code: str, table: str, db=Depends(get_db)):
    validate_table(table)
    return read_all_records(db, table)


@app.get("/{code}/{table}/{key}")
def api_read_one(code: str, table: str, key: str, db=Depends(get_db)):
    validate_table(table)
    record = read_record(db, table, key)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@app.put("/{code}/{table}/{key}")
def api_update(code: str, table: str, key: str, payload: dict, db=Depends(get_db)):
    validate_table(table)
    return update_record(db, table, key, payload)


@app.delete("/{code}/{table}/{key}")
def api_delete(code: str, table: str, key: str, db=Depends(get_db)):
    validate_table(table)
    return delete_record(db, table, key)