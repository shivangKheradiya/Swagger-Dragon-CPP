import os
import sqlite3
from fastapi.testclient import TestClient
from OPE_DBSQLite.api import app

client = TestClient(app)

DB_DIR = "dbs"
DB_CODE = "TST"

REQUIRED_TABLES = [
    "TreeNodes",
    "TreeNodeAttributes",
    "ElementTypes",
    "ElementTypeAttributes"
]


def test_db_and_tables_created():
    """Verify DB and all required tables are created on first call."""
    client.get(f"/{DB_CODE}/TreeNodes")

    db_path = os.path.join(DB_DIR, f"{DB_CODE}.db")
    assert os.path.exists(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur.fetchall()}

    for t in REQUIRED_TABLES:
        assert t in tables, f"Missing table: {t}"

    conn.close()

test_db_and_tables_created()