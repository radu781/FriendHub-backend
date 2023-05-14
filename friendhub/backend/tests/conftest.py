import json
import uuid
from random import randint

import pytest
import requests
from database.user_dao import UserDAO

from . import (
    LOGIN_ENDPOINT,
    LOGOUT_ENDPOINT,
    REGISTER_ENDPOINT,
    USER_EMAIL,
    USER_FIRST_NAME,
    USER_PASSWORD,
)


@pytest.fixture(scope="function")
def auto_login_logout(request):
    jwt = login()
    yield jwt
    logout()


@pytest.fixture(scope="function")
def auto_login(request):
    jwt = login()
    yield jwt


@pytest.fixture(scope="function")
def auto_logout(request):
    logout()
    yield request
    logout()


def delete_user(user_id: uuid.UUID) -> None:
    UserDAO.delete_user(user_id)


def logout() -> None:
    requests.post(LOGOUT_ENDPOINT, timeout=3)


def login() -> str:
    data = requests.post(
        LOGIN_ENDPOINT, {"email": USER_EMAIL, "password": USER_PASSWORD}, timeout=3
    )
    return json.loads(data.text)["token"]


def create_random_user() -> uuid.UUID:
    logout()
    random_int = str(randint(1000, 9999))
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL + "+" + random_int,
            "password": USER_PASSWORD,
            "password-confirm": USER_PASSWORD,
            "first-name": USER_FIRST_NAME,
        },
        timeout=3,
    )
    return uuid.UUID(json.loads(res.text)["user"]["id_"])
