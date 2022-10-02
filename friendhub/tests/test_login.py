import json

import pytest
import requests
from flask_api import status

from . import *


@pytest.mark.unit
def test_correct_details():
    res = requests.post(
        LOGIN_ENDPOINT, {"email": USER_EMAIL, "password": USER_PASSWORD}
    )
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.unit
def test_incorrect_password():
    res = requests.post(
        LOGIN_ENDPOINT, {"email": USER_EMAIL, "password": USER_PASSWORD + "123"}
    )
    assert (
        json.loads(res.content)["reason"] == "incorrect password"
        and res.status_code == status.HTTP_401_UNAUTHORIZED
    )


@pytest.mark.unit
def test_user_does_not_exist():
    res = requests.post(
        LOGIN_ENDPOINT,
        {"email": "I do not exist", "password": ""},
    )
    assert (
        json.loads(res.content)["reason"] == "user does not exist"
        and res.status_code == status.HTTP_401_UNAUTHORIZED
    )


@pytest.mark.unit
def test_missing_parameters():
    res = requests.post(LOGIN_ENDPOINT)
    content = json.loads(res.content)
    assert (
        content["reason"] == "missing parameters"
        and (
            content["parameters"] == "password, email"
            or content["parameters"] == "email, password"
        )
        and res.status_code == status.HTTP_401_UNAUTHORIZED
    )
