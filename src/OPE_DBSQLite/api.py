from fastapi import FastAPI, HTTPException
from .crud import (
    create_record,
    read_record,
    read_all_records,
    update_record,
    delete_record
)

ALLOWED_TABLES = {
    "TreeNodes",
    "TreeNodeAttributes",
    "ElementTypes",
    "ElementTypeAttributes",
}

app = FastAPI(title="OPE-DBSQLite Multi-DB API")


def validate_table(table: str):
    if table not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail=f"Invalid table '{table}'")


@app.post("/{code}/{table}")
def api_create(code: str, table: str, payload: dict):
    validate_table(table)
    return create_record(code, table, payload)


@app.get("/{code}/{table}")
def api_get_all(code: str, table: str):
    validate_table(table)
    return read_all_records(code, table)


@app.get("/{code}/{table}/{key}")
def api_get_one(code: str, table: str, key: str):
    validate_table(table)
    row = read_record(code, table, key)
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return row


@app.put("/{code}/{table}/{key}")
def api_update(code: str, table: str, key: str, payload: dict):
    validate_table(table)
    return update_record(code, table, key, payload)


@app.delete("/{code}/{table}/{key}")
def api_delete(code: str, table: str, key: str):
    validate_table(table)
    return delete_record(code, table, key)