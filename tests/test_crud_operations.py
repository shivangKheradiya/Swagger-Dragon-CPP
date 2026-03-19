from fastapi.testclient import TestClient
from OPE_DBSQLite.api import app

client = TestClient(app)

DB = "CRD"  # test DB code


def test_create_treenode():
    payload = {
        "UUID": "abc123",
        "Parent": None,
        "IsDeleted": False
    }

    res = client.post(f"/{DB}/TreeNodes", json=payload)
    assert res.status_code == 200
    assert res.json()["status"] == "created"


def test_read_treenode():
    res = client.get(f"/{DB}/TreeNodes/abc123")
    assert res.status_code == 200
    data = res.json()
    assert data["UUID"] == "abc123"
    assert data["IsDeleted"] == 0


def test_update_treenode():
    payload = {"IsDeleted": True}

    res = client.put(f"/{DB}/TreeNodes/abc123", json=payload)
    assert res.status_code == 200
    assert res.json()["status"] == "updated"

    res2 = client.get(f"/{DB}/TreeNodes/abc123")
    assert res2.status_code == 200
    assert res2.json()["IsDeleted"] == 1


def test_delete_treenode():
    res = client.delete(f"/{DB}/TreeNodes/abc123")
    assert res.status_code == 200

    res2 = client.get(f"/{DB}/TreeNodes/abc123")
    assert res2.status_code == 404

#test_create_treenode()
test_read_treenode()
test_update_treenode()
test_delete_treenode()