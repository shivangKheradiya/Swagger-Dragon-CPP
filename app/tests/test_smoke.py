import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_smoke():
    """
    Basic sanity check:
    - App starts
    - Root returns 404 instead of crash
    """
    response = client.get("/")
    assert response.status_code in (200, 404)


def test_create_attribute_smoke():
    """
    Smoke test for:
    - POST /design/attributes
    - Attribute row created
    - UUID returned
    """

    payload = {
        "tree_node_uuid": str(uuid.uuid4()),
        "element_type_attribute_id": 1,
        "value_type": 1,        # STRING
        "value": "RootNode"
    }

    response = client.post("/design/attributes/", json=payload)

    assert response.status_code == 200

    body = response.json()

    assert "UUID" in body
    assert body["TreeNodeUUID"] == payload["tree_node_uuid"]
    assert body["ElementTypeAttributeID"] == payload["element_type_attribute_id"]
    assert body["ValueType"] == payload["value_type"]
    assert body["ValueString"] == payload["value"]


def test_history_written_smoke():
    """
    Ensures:
    - History entry exists for a created attribute
    """

    payload = {
        "tree_node_uuid": str(uuid.uuid4()),
        "element_type_attribute_id": 1,
        "value_type": 1,
        "value": "HistorySmoke"
    }

    create_resp = client.post("/design/attributes/", json=payload)
    assert create_resp.status_code == 200

    attr_uuid = create_resp.json()["UUID"]

    history_resp = client.get(f"/design/history/{attr_uuid}")
    assert history_resp.status_code == 200

    history = history_resp.json()

    assert len(history) >= 1
    assert history[0]["OperationType"] == 1  # CREATE
    assert history[0]["NewValue"]["Value"] == "HistorySmoke"