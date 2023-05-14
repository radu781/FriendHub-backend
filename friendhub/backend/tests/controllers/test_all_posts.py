import json

import pytest
import requests
from flask_api import status

from tests import ALL_POSTS_ENDPOINT


@pytest.mark.unit
def test_no_params(auto_login_logout):
    res = requests.get(
        ALL_POSTS_ENDPOINT, headers={"Authorization": f"Bearer {auto_login_logout}"}, timeout=10
    )
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_200_OK
    assert "count" in js
    assert int(js["count"]) <= 20
    assert "data" in js
    assert len(js["data"]) == js["count"]

    for sub_item in js["data"]:
        assert "author" in sub_item
        assert "post" in sub_item
        assert "vote" in sub_item


@pytest.mark.unit
def test_all_params(auto_login_logout):
    res = requests.get(
        ALL_POSTS_ENDPOINT,
        {"from": 1, "to": 5},
        headers={"Authorization": f"Bearer {auto_login_logout}"},
        timeout=3,
    )
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_200_OK
    assert "count" in js
    assert int(js["count"]) <= 5 - 1
    assert "data" in js
    assert len(js["data"]) == js["count"]

    for sub_item in js["data"]:
        assert "author" in sub_item
        assert "post" in sub_item
        assert "vote" in sub_item
