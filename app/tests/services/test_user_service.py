from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.tests.core.faker_provider import get_faker

faker = get_faker()

service = UserService()


def get_test_create_user_data():
    return UserCreate(
        email=f"{faker.first_name_male()}.{faker.last_name()}@{faker.domain_name()}",
        name=faker.name(),
        nickname=faker.last_name(),
        password="test1234!",
        phone_number="01012345678",
    )


def test_create_user():
    data = get_test_create_user_data()
    sut = service.create(data)

    assert sut.email == data.email


def test_verify_password():
    data = get_test_create_user_data()
    password = data.password
    service.create(data)

    assert service.verify_password(data.email, password)


def test_login():
    data = get_test_create_user_data()
    password = data.password
    service.create(data)

    sut = service.login(data.email, password)

    assert isinstance(sut["access_token"], str)
    assert isinstance(sut["refresh_token"], str)
