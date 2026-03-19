from fastapi.testclient import TestClient
from OPE_DBSQLite.api import app

client = TestClient(app)

def test_api_starts():
    """Ensures API starts and responds."""
    res = client.get("/ABC/TreeNodes")
    assert res.status_code in (200, 204, 400)

print(test_api_starts())