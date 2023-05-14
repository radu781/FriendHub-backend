import json

import pytest
import requests
from flask_api import status

from tests import LOGIN_ENDPOINT, USER_EMAIL, USER_PASSWORD


@pytest.mark.unit
def test_correct_details(auto_logout):
    res = requests.post(LOGIN_ENDPOINT, {"email": USER_EMAIL, "password": USER_PASSWORD}, timeout=3)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.unit
def test_incorrect_password(auto_logout):
    res = requests.post(
        LOGIN_ENDPOINT,
        {"email": USER_EMAIL, "password": USER_PASSWORD + "123"},
        timeout=3,
    )
    assert (
        json.loads(res.content)["reason"] == "incorrect password"
        and res.status_code == status.HTTP_401_UNAUTHORIZED
    )


@pytest.mark.unit
def test_user_does_not_exist():
    res = requests.post(LOGIN_ENDPOINT, {"email": "I do not exist", "password": ""}, timeout=3)
    assert (
        json.loads(res.content)["reason"] == "user does not exist"
        and res.status_code == status.HTTP_401_UNAUTHORIZED
    )


@pytest.mark.unit
def test_missing_parameters_some():
    res = requests.post(LOGIN_ENDPOINT, {"email": "mock email"}, timeout=3)
    content = json.loads(res.content)
    assert (
        content["reason"] == "missing parameters"
        and (content["parameters"] == "password")
        and res.status_code == status.HTTP_401_UNAUTHORIZED
    )


@pytest.mark.unit
def test_missing_parameters_all():
    res = requests.post(LOGIN_ENDPOINT, timeout=3)
    content = json.loads(res.content)

    assert "reason" in content
    assert content["reason"] == "missing parameters"
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    assert "parameters" in content
    PARAMETERS = ["password", "email"]
    stripped = [ele.strip() for ele in content["parameters"].split(",")]
    assert sorted(PARAMETERS) == sorted(stripped)
