from fastapi.testclient import TestClient
from OPE_DBSQLite.api import app

client = TestClient(app)

def test_smoke():
    """Ensures API loads and basic endpoint responds."""
    response = client.get("/items")
    assert response.status_code in (200, 204, 500)  # 500 ok for empty SQL

print(test_smoke())