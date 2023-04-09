import json
from random import randint

import pytest
import requests
from flask_api import status
from tests import (
    REGISTER_ENDPOINT,
    USER_CITY,
    USER_COUNTRY,
    USER_EDUCATION,
    USER_EMAIL,
    USER_EXTRA,
    USER_FIRST_NAME,
    USER_LAST_NAME,
    USER_MIDDLE_NAME,
    USER_PASSWORD,
)
from tests.conftest import create_random_user, delete_user

@pytest.mark.unit
def test_missing_parameters(auto_logout):
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL + "+" + str(randint(0, 999)),
            "password": USER_PASSWORD,
            "password-confirm": USER_PASSWORD,
        },
        timeout=3,
    )
    content = json.loads(res.content)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in content
    assert content["reason"] == "missing parameters"
    assert "parameters" in content
    assert content["parameters"] == "first-name"


@pytest.mark.unit
def test_user_exists(auto_logout):
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL,
            "password": USER_PASSWORD,
            "password-confirm": "",
            "first-name": "",
        },
        timeout=3,
    )
    content = json.loads(res.content)
    assert "reason" in content
    assert content["reason"] == "user already exists"
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
def test_passwords_mismatch(auto_logout):
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL + "+" + str(randint(3000, 3999)),
            "password": USER_PASSWORD,
            "password-confirm": USER_PASSWORD + "123",
            "first-name": USER_FIRST_NAME,
        },
        timeout=3,
    )
    content = json.loads(res.content)
    assert "reason" in content
    assert content["reason"] == "passwords mismatch"
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
def test_minimal_register(auto_logout):
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL + "+" + str(randint(1000, 1999)),
            "password": USER_PASSWORD,
            "password-confirm": USER_PASSWORD,
            "first-name": USER_FIRST_NAME,
        },
        timeout=3,
    )
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_201_CREATED
    assert "user" in js


@pytest.mark.unit
def test_complete_register(auto_logout):
    res = requests.post(
        REGISTER_ENDPOINT,
        {
            "email": USER_EMAIL + "+" + str(randint(1000, 9999)),
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
        timeout=3,
    )
    js = json.loads(res.text)
    delete_user(js["user"]["id_"])
    assert res.status_code == status.HTTP_201_CREATED
    assert "user" in js
