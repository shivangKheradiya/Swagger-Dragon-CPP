import sqlite3
import os

BASE_DIR = os.path.abspath("dbs")  # All DB files stored here
os.makedirs(BASE_DIR, exist_ok=True)

REQUIRED_TABLES = {
    "TreeNodes": """
        CREATE TABLE IF NOT EXISTS TreeNodes (
            UUID TEXT PRIMARY KEY,
            Parent TEXT DEFAULT NULL,
            IsDeleted BOOLEAN DEFAULT 0
        );
    """,

    "TreeNodeAttributes": """
        CREATE TABLE IF NOT EXISTS TreeNodeAttributes (
            UUID TEXT PRIMARY KEY,
            TreeNodeUUID TEXT,
            ElementTypeAttributeID INTEGER,
            Value TEXT DEFAULT NULL,
            ChangedFrom TEXT DEFAULT NULL,
            IsDeleted BOOLEAN DEFAULT 0
        );
    """,

    "ElementTypes": """
        CREATE TABLE IF NOT EXISTS ElementTypes (
            IDNo INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT DEFAULT NULL
        );
    """,

    "ElementTypeAttributes": """
        CREATE TABLE IF NOT EXISTS ElementTypeAttributes (
            IDNo INTEGER PRIMARY KEY AUTOINCREMENT,
            ElementTypeID INTEGER,
            Name TEXT,
            DataType TEXT,
            DefaultValue TEXT
        );
    """
}


def get_db(code: str):
    """Return DB connection based on 3-letter prefix."""
    if len(code) != 3:
        raise ValueError("DB code must be exactly 3 letters, e.g., 'ABC'")

    db_path = os.path.join(BASE_DIR, f"{code.upper()}.db")
    first_time = not os.path.exists(db_path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    if first_time:
        create_required_tables(conn)

    return conn


def create_required_tables(conn):
    cursor = conn.cursor()
    for sql in REQUIRED_TABLES.values():
        cursor.execute(sql)
    conn.commit()