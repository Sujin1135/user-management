from fastapi.testclient import TestClient
from fastapi import status

from app.schemas.user import UserCreate
from main import app
from app.tests.core.faker_provider import get_faker

faker = get_faker()
client = TestClient(app)


def test_create_user():
    data = {
        "email": f"{faker.first_name_male()}.{faker.last_name()}@{faker.domain_name()}",
        "name": faker.name(),
        "nickname": faker.last_name(),
        "password": "test1234!",
        "phone_number": "01012345678",
    }
    sut = client.post("/api/v1/users", json=data)
    res_data = sut.json()

    assert sut.status_code is status.HTTP_201_CREATED
    assert res_data["email"] is data.email
