from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "DevOps Deploy Platform API is running"


def test_get_applications():
    response = client.get("/applications")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_application_not_found():
    response = client.get("/applications/99999")

    assert response.status_code == 404