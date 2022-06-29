from fastapi.testclient import TestClient
from fastapi import status
from h11 import Response

from main import app
from app.tests.core.faker_provider import get_faker

faker = get_faker()
client = TestClient(app)


def get_test_signup_data() -> dict:
    return {
        "email": f"{faker.first_name_male()}.{faker.last_name()}@{faker.domain_name()}",
        "name": faker.name(),
        "nickname": faker.last_name(),
        "password": "test1234!",
        "phone_number": "01012345678",
    }


def request_signup(data: dict) -> Response:
    return client.post("/api/v1/users/signup", json=data)


def test_signup_user():
    data = get_test_signup_data()
    sut = request_signup(data)
    res_data = sut.json()

    assert sut.status_code is status.HTTP_201_CREATED
    assert res_data["email"] == data["email"]


def test_signup_duplicated_email_user_case():
    data = get_test_signup_data()
    request_signup(data)
    sut = request_signup(data)

    assert sut.status_code == status.HTTP_400_BAD_REQUEST
