from fastapi.testclient import TestClient
from fastapi import status
from h11 import Response

from app.services.user_service import UserService
from app.tests.services.test_user_service import get_test_create_user_data
from main import app
from app.tests.core.faker_provider import get_faker

faker = get_faker()
client = TestClient(app)
service = UserService()


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


def test_login():
    data = get_test_create_user_data()
    password = data.password
    service.create(data)

    sut = client.post(
        "/api/v1/users/signin", json={"email": data.email, "password": password}
    )
    result = sut.json()

    assert sut.status_code == status.HTTP_200_OK
    assert result["access_token"] is not None


def test_get_my_data():
    data = get_test_create_user_data()
    password = data.password
    service.create(data)
    access_token = login(data, password)

    sut = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    me = sut.json()

    assert sut.status_code == status.HTTP_200_OK
    assert me["email"] == data.email


def login(data, password):
    return client.post(
        "/api/v1/users/signin", json={"email": data.email, "password": password}
    ).json()["access_token"]


def test_change_password():
    data = get_test_create_user_data()
    password = data.password
    service.create(data)
    next_password = "change1234!"

    client.patch(
        "/api/v1/users/me/change-pwd",
        json={"current_password": password, "change_password": next_password},
        headers={"Authorization": f"Bearer {login(data, password)}"},
    )

    sut = login(data, next_password)

    assert isinstance(sut, str)


def test_send_auth_sns_message():
    sut = client.post(
        "/api/v1/users/request-auth-phone-number", json={"phone_number": "01012345678"}
    )

    assert sut.status_code == status.HTTP_200_OK
