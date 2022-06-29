from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate
from app.tests.core.faker_provider import get_faker

faker = get_faker()


def test_create_user():
    data = UserCreate(
        email=f"{faker.first_name_male()}.{faker.last_name()}@{faker.domain_name()}",
        name=faker.name(),
        nickname=faker.last_name(),
        password="test1234!",
        phone_number="01012345678",
    )
    sut = crud_user.create(data)

    assert sut.email == data.email
