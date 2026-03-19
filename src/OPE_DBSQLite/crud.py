from typing import Dict, Any
from .database import get_db

PRIMARY_KEY_COL = {
    "TreeNodes": "UUID",
    "TreeNodeAttributes": "UUID",
    "ElementTypes": "IDNo",
    "ElementTypeAttributes": "IDNo",
}


def create_record(code: str, table: str, data: Dict[str, Any]):
    conn = get_db(code)
    cursor = conn.cursor()

    cols = ", ".join(data.keys())
    placeholders = ", ".join("?" for _ in data)
    values = list(data.values())

    cursor.execute(
        f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
        values
    )
    conn.commit()
    conn.close()
    return {"status": "created"}


def read_all_records(code: str, table: str):
    conn = get_db(code)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


def read_record(code: str, table: str, key: str):
    conn = get_db(code)
    cursor = conn.cursor()

    key_col = PRIMARY_KEY_COL[table]

    cursor.execute(
        f"SELECT * FROM {table} WHERE {key_col} = ?",
        (key,)
    )
    row = cursor.fetchone()

    conn.close()
    return dict(row) if row else None


def update_record(code: str, table: str, key: str, data: Dict[str, Any]):
    conn = get_db(code)
    cursor = conn.cursor()

    key_col = PRIMARY_KEY_COL[table]
    sets = ", ".join(f"{k}=?" for k in data)
    values = list(data.values()) + [key]

    cursor.execute(
        f"UPDATE {table} SET {sets} WHERE {key_col} = ?",
        values
    )

    conn.commit()
    conn.close()
    return {"status": "updated"}


def delete_record(code: str, table: str, key: str):
    conn = get_db(code)
    cursor = conn.cursor()

    key_col = PRIMARY_KEY_COL[table]

    cursor.execute(f"DELETE FROM {table} WHERE {key_col} = ?", (key,))
    conn.commit()
    conn.close()

    return {"status": "deleted"}