from dataclasses import dataclass
from random import randint

from faker import Faker
fake = Faker()


@dataclass
class User:
    name: str = ''
    surname: str = ''
    middle_name: str = ''
    username: str = ''
    password: str = ''
    email: str = ''
    access: int = None


class Builder:

    @staticmethod
    def user(name=None, surname=None, middle_name=None, username=None, password=None, email=None, access=1,
             name_length=10, surname_length=10, middle_name_length=10, username_length=10, password_length=10,
             email_length=10, special_chars=False
             ):

        if name is None:
            name = fake.password(length=name_length, special_chars=special_chars)
        if surname is None:
            surname = fake.password(length=surname_length, special_chars=special_chars)
        if middle_name is None:
            middle_name = fake.password(length=middle_name_length, special_chars=special_chars)
        if username is None:
            username = fake.password(length=username_length, special_chars=special_chars)
        if password is None:
            password = fake.password(length=password_length, special_chars=special_chars)
        if email is None:
            email = fake.password(length=email_length-5, special_chars=special_chars) + "@r.ru"

        return User(name=name, surname=surname, middle_name=middle_name, username=username, password=password,
                    email=email, access=access)
