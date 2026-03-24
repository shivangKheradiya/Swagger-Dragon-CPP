import os, sys
import sqlite3
import pytest
from fastapi.testclient import TestClient

ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_PATH = os.path.join(ROOT, "src")
sys.path.append(SRC_PATH)

from OPE_DBSQLite.api import app
client = TestClient(app)

DB_DIR = r"E:/SKGitRepo/Swagger-Dragon-CPP/dbs"
TEST_DB_CODE = "TST"   # 3‑letter DB code for isolated testing


# -----------------------------------------
# 1. Smoke Test — API Should Boot
# -----------------------------------------
def test_api_starts():
    response = client.get(f"/{TEST_DB_CODE}/TreeNodes")
    assert response.status_code in (200, 204) or response.status_code == 200


# -----------------------------------------
# 2. Database Creation Test
# -----------------------------------------
def test_database_file_created():
    # Trigger database creation via any API call
    client.get(f"/{TEST_DB_CODE}/TreeNodes")

    db_path = os.path.join(DB_DIR, f"{TEST_DB_CODE}.db")
    assert os.path.exists(db_path), f"Database {db_path} was not created"


# -----------------------------------------
# 3. Required Tables Test
# -----------------------------------------
def test_required_tables_exist():
    db_path = os.path.join(DB_DIR, f"{TEST_DB_CODE}.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur.fetchall()}

    required = {
        "TreeNodes",
        "TreeNodeAttributes",
        "ElementTypes",
        "ElementTypeAttributes",
    }

    for t in required:
        assert t in tables, f"Missing required table: {t}"

    conn.close()


# -----------------------------------------
# 4. CRUD Tests for TreeNodes
# -----------------------------------------
def test_create_treenode():
    payload = {
        "UUID": "NODE1",
        "Parent": None,
        "IsDeleted": False
    }
    res = client.post(f"/{TEST_DB_CODE}/TreeNodes", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["UUID"] == "NODE1"


def test_read_treenode():
    res = client.get(f"/{TEST_DB_CODE}/TreeNodes/NODE1")
    assert res.status_code == 200
    data = res.json()
    assert data["UUID"] == "NODE1"
    assert data["IsDeleted"] is False or data["IsDeleted"] == 0


def test_update_treenode():
    payload = {"IsDeleted": True}
    res = client.put(f"/{TEST_DB_CODE}/TreeNodes/NODE1", json=payload)
    assert res.status_code == 200

    res2 = client.get(f"/{TEST_DB_CODE}/TreeNodes/NODE1")
    assert res2.status_code == 200
    assert res2.json()["IsDeleted"] is True or res2.json()["IsDeleted"] == 1


def test_delete_treenode():
    res = client.delete(f"/{TEST_DB_CODE}/TreeNodes/NODE1")
    assert res.status_code == 200

    res2 = client.get(f"/{TEST_DB_CODE}/TreeNodes/NODE1")
    assert res2.status_code == 404


# -----------------------------------------
# 5. CRUD Tests for ElementTypes
# -----------------------------------------
def test_create_element_type():
    payload = {"Name": "Pipe"}
    res = client.post(f"/{TEST_DB_CODE}/ElementTypes", json=payload)
    assert res.status_code == 200
    assert res.json()["Name"] == "Pipe"


def test_read_element_types():
    res = client.get(f"/{TEST_DB_CODE}/ElementTypes")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


# -----------------------------------------
# 6. CRUD Tests for ElementTypeAttributes
# -----------------------------------------
def test_create_element_type_attribute():
    payload = {
        "ElementTypeID": 1,
        "Name": "Diameter",
        "DataType": "float",
        "DefaultValue": "0.0"
    }
    res = client.post(f"/{TEST_DB_CODE}/ElementTypeAttributes", json=payload)
    assert res.status_code == 200
    assert res.json()["Name"] == "Diameter"


def test_read_element_type_attributes():
    res = client.get(f"/{TEST_DB_CODE}/ElementTypeAttributes")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


# -----------------------------------------
# 7. CRUD Tests for TreeNodeAttributes
# -----------------------------------------
def test_create_treenode_attribute():
    payload = {
        "UUID": "ATTR1",
        "TreeNodeUUID": None,
        "ElementTypeAttributeID": 1,
        "Value": "100",
        "ChangedFrom": None,
        "IsDeleted": False
    }
    res = client.post(f"/{TEST_DB_CODE}/TreeNodeAttributes", json=payload)
    assert res.status_code == 200
    assert res.json()["UUID"] == "ATTR1"


def test_read_treenode_attributes():
    res = client.get(f"/{TEST_DB_CODE}/TreeNodeAttributes")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


test_api_starts()
test_database_file_created()
test_required_tables_exist()
test_create_treenode()
test_read_treenode()
test_update_treenode()
test_delete_treenode()
test_create_element_type()
test_read_element_types()
test_create_element_type_attribute()
test_read_element_type_attributes()
test_create_treenode_attribute()
test_read_treenode_attributes()