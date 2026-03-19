from typing import Dict, Any, List
from .database import get_db, TABLE_NAME


def create_item(data: Dict[str, Any]):
    conn = get_db()
    cursor = conn.cursor()

    # TODO: implement insert
    # cursor.execute("INSERT INTO ...")

    conn.commit()
    conn.close()
    return {"status": "created"}


def read_items() -> List[dict]:
    conn = get_db()
    cursor = conn.cursor()

    # TODO: implement select all
    # cursor.execute("SELECT * FROM ...")

    results = []  # placeholder
    conn.close()
    return results


def read_item(item_id: int):
    conn = get_db()
    cursor = conn.cursor()

    # TODO: implement select one
    # cursor.execute("SELECT * FROM ... WHERE id=?", (item_id,))

    row = None  # placeholder
    conn.close()
    return row


def update_item(item_id: int, data: Dict[str, Any]):
    conn = get_db()
    cursor = conn.cursor()

    # TODO: implement update
    # cursor.execute("UPDATE ... WHERE id=?", (item_id,))

    conn.commit()
    conn.close()
    return {"status": "updated"}


def delete_item(item_id: int):
    conn = get_db()
    cursor = conn.cursor()

    # TODO: implement delete
    # cursor.execute("DELETE FROM ... WHERE id=?", (item_id,))

    conn.commit()
    conn.close()
    return {"status": "deleted"}