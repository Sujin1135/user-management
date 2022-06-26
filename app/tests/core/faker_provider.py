from faker import Faker
from random import randrange


def _gen_random_seed():
    return randrange(10000)


def get_faker():
    Faker.seed(_gen_random_seed())
    return Faker()
