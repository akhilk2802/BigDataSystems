from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_healthcheck():
    response = client.get(url="/api/v1/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"message":"Ok"}

def test_fetch_all_data():
    response = client.get(url="/api/v1/fetch_all_data")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_fetch_by_state_ma():
    response = client.post(
        url="/api/v1/fetch_by_state",
        json={
            "state": "ma"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

