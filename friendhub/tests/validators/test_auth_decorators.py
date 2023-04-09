import json

import pytest
import requests
from flask_api import status
from tests import LOGIN_ENDPOINT, UPLOAD_ENDPOINT, USER_EMAIL, USER_PASSWORD
from tests.conftest import logout


@pytest.mark.unit
def test_needs_login():
    logout()
    res = requests.post(UPLOAD_ENDPOINT, timeout=3)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert "error" in js
    assert js["error"] == "not logged in"


# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_needs_logout():
    requests.post(LOGIN_ENDPOINT, {"email": USER_EMAIL, "password": USER_PASSWORD}, timeout=3)
    res = requests.post(LOGIN_ENDPOINT, {"email": USER_EMAIL, "password": USER_PASSWORD}, timeout=3)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert "error" in js
    assert js["error"] == "not logged out"


@pytest.mark.unit
def test_uuid_path():
    ...
