from controllers.healthchecks import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_app_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "alive"}
