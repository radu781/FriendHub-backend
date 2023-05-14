import json

import pytest
import requests
from flask_api import status

from tests import PROFILE_ENDPOINT

from tests.conftest import create_random_user, delete_user


@pytest.mark.unit
def test_user_not_found():
    res = requests.get(PROFILE_ENDPOINT + "/00000000-0000-0000-0000-000000000000", timeout=3)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert "reason" in js
    assert js["reason"] == "user not found"


@pytest.mark.unit
def test_user_exists():
    id_ = create_random_user()
    res = requests.get(PROFILE_ENDPOINT + f"/{id_}", timeout=3)
    delete_user(id_)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_200_OK
    assert "user" in js
