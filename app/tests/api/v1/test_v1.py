from fastapi.testclient import TestClient
from fastapi import status
from main import app
from app.tests.core.faker_provider import get_faker

faker = get_faker()
client = TestClient(app)


def test_healthcheck():
    sut = client.get("/api/v1/healthcheck")
    data = sut.json()

    assert sut.status_code is status.HTTP_200_OK
    assert data["is_ok"] == True
