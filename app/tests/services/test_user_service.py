from app.core.auth import convert_user_model_to_schema
from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate, UserPwdChange
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

    assert isinstance(sut.access_token, str)


def test_change_current_user_password():
    data = get_test_create_user_data()
    password = data.password
    service.create(data)
    next_password = "change1234!"
    cur_user = convert_user_model_to_schema(crud_user.get_by_email(data.email))

    service.change_pwd(
        cur_user,
        UserPwdChange(current_password=password, change_password=next_password),
    )

    sut = service.login(cur_user.email, next_password)

    assert isinstance(sut.access_token, str)
