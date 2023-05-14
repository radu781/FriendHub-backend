import json

import pytest
import requests
from flask_api import status

from tests import DELETE_USER_ENDPOINT
from tests.conftest import create_random_user, delete_user


@pytest.mark.unit
def test_user_not_found():
    res = requests.delete(DELETE_USER_ENDPOINT + "/00000000-0000-0000-0000-000000000000", timeout=3)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert "reason" in js
    assert js["reason"] == "user not found"


@pytest.mark.unit
def test_missing_parameters():
    id_ = create_random_user()
    res = requests.delete(DELETE_USER_ENDPOINT + f"/{id_}", timeout=3)
    delete_user(id_)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert "reason" in js
    assert js["reason"] == "missing parameters"
    assert "parameters" in js
    assert js["parameters"] == "key"


@pytest.mark.unit
def test_incorrect_key():
    id_ = create_random_user()
    res = requests.delete(DELETE_USER_ENDPOINT + f"/{id_}", data={"key": "wrong key"}, timeout=3)
    delete_user(id_)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_403_FORBIDDEN
    assert "reason" in js
    assert js["reason"] == "incorrect profile deletion key"


@pytest.mark.xfail
@pytest.mark.unit
def test_delete_ok():
    id_ = create_random_user()
    res = requests.delete(DELETE_USER_ENDPOINT + f"/{id_}", data={"key": "ok key"}, timeout=3)
    delete_user(id_)

    assert res.status_code == status.HTTP_200_OK
