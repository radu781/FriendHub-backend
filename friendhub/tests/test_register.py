import json
from random import randint

import pytest
import requests
from flask_api import status
from . import *


@pytest.fixture(autouse=True)
def delete_user_fixture():
    print("setup")
    yield
    print("teardown")


def test_missing_parameters():
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL + "+" + str(randint(0, 999)),
            "password": USER_PASSWORD,
            "password-confirm": USER_PASSWORD,
        },
    )
    content = json.loads(res.content)
    assert (
        content["reason"] == "missing parameters"
        and content["parameters"] == "first-name"
        and res.status_code == status.HTTP_401_UNAUTHORIZED
    )


def test_user_exists():
    # register user
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": "",
            "password": "",
            "password-confirm": "",
            "first-name": "",
        },
    )
    content = json.loads(res.content)
    assert (
        content["reason"] == "user already exists"
        and res.status_code == status.HTTP_401_UNAUTHORIZED
    )


def test_passwords_mismatch():
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL + "+" + str(randint(3000, 3999)),
            "password": USER_PASSWORD,
            "password-confirm": USER_PASSWORD + "123",
            "first-name": USER_FIRST_NAME,
        },
    )
    content = json.loads(res.content)
    assert (
        content["reason"] == "passwords mismatch"
        and res.status_code == status.HTTP_401_UNAUTHORIZED
    )


def test_minimal_register():
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL + "+" + str(randint(1000, 1999)),
            "password": USER_PASSWORD,
            "password-confirm": USER_PASSWORD,
            "first-name": USER_FIRST_NAME,
        },
    )
    assert res.status_code == status.HTTP_200_OK


def test_complete_register():
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL + "+" + str(randint(2000, 2999)),
            "password": USER_PASSWORD,
            "password-confirm": USER_PASSWORD,
            "first-name": USER_FIRST_NAME,
            "middle-name": USER_MIDDLE_NAME,
            "last-name": USER_LAST_NAME,
            "country": USER_COUNTRY,
            "city": USER_CITY,
            "education": USER_EDUCATION,
            "extra": USER_EXTRA,
        },
    )
    assert res.status_code == status.HTTP_200_OK
