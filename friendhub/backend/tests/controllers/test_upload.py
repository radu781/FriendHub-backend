import json

import pytest
import requests
import utils.validators.other as validators
from flask_api import status
from tests import UPLOAD_ENDPOINT


@pytest.mark.unit
def test_missing_parameters(auto_login_logout, a):
    res = requests.post(
        UPLOAD_ENDPOINT, headers={"Authorization": f"Bearer {auto_login_logout}"}, timeout=3
    )
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in js
    assert js["reason"] == "missing parameters"
    assert "parameters" in js
    assert js["parameters"] == "text"


@pytest.mark.unit
def test_text_empty(auto_login_logout):
    res = requests.post(
        UPLOAD_ENDPOINT,
        {"text": ""},
        headers={"Authorization": f"Bearer {auto_login_logout}"},
        timeout=3,
    )
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert "reason" in js
    assert js["reason"] == "text missing"


@pytest.mark.unit
def test_text_only_ok(auto_login_logout):
    res = requests.post(
        UPLOAD_ENDPOINT,
        {"text": "Funny post description"},
        headers={"Authorization": f"Bearer {auto_login_logout}"},
        timeout=10,
    )
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_201_CREATED
    assert "id" in js
    assert validators.is_uuid(js["id"])
