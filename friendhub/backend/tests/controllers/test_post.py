import json

import pytest
import requests
from flask_api import status
from tests import POST_ENDPOINT, UPLOAD_ENDPOINT


@pytest.mark.xfail
@pytest.mark.unit
def test_get_not_found(auto_login_logout):
    res = requests.get(POST_ENDPOINT + "/00000000-0000-0000-0000-000000000000", timeout=3)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert "reason" in js
    assert js["reason"] == "post not found"


# TODO: create random post and delete after
@pytest.mark.xfail
@pytest.mark.unit
def test_get_found(auto_login_logout):
    requests.post(
        UPLOAD_ENDPOINT,
        {"text": "testing text"},
        headers={"Authorization": f"Bearer {auto_login_logout}"},
        timeout=3,
    )
    res = requests.get(POST_ENDPOINT + "/f2cccc42-df1e-4145-ad57-298b949c141a", timeout=3)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_200_OK
    assert "data" in js
    assert "author" in js["data"]
    assert "post" in js["data"]
    assert "vote" in js["data"]


# TODO: create random post and delete after
@pytest.mark.xfail
@pytest.mark.unit
def test_put_missing_parameters(auto_login_logout):
    res = requests.put(POST_ENDPOINT + "/f2cccc42-df1e-4145-ad57-298b949c141a", timeout=3)
    js = json.loads(res.text)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in js
    assert js["reason"] == "missing parameters"
    assert "parameters" in js
    assert js["parameters"] == "vote"


# TODO: create random post and delete after
@pytest.mark.xfail
@pytest.mark.unit
def test_put_no_db_clear_intent(auto_login_logout):
    res = requests.put(
        POST_ENDPOINT + "/f2cccc42-df1e-4145-ad57-298b949c141a", {"vote": "clear"}, timeout=3
    )

    assert res.status_code == status.HTTP_202_ACCEPTED


# TODO: create random post and delete after
@pytest.mark.xfail
@pytest.mark.unit
def test_put_no_db_no_clear_intent(auto_login_logout):
    res = requests.put(
        POST_ENDPOINT + "/f2cccc42-df1e-4145-ad57-298b949c141a", {"vote": "upvote"}, timeout=3
    )

    assert res.status_code == status.HTTP_201_CREATED


# TODO: create random post and delete after
@pytest.mark.xfail
@pytest.mark.unit
def test_put_db_clear_intent(auto_login_logout):
    res = requests.put(
        POST_ENDPOINT + "/f2cccc42-df1e-4145-ad57-298b949c141a", {"vote": "clear"}, timeout=3
    )

    assert res.status_code == status.HTTP_205_RESET_CONTENT


# TODO: create random post and delete after
@pytest.mark.xfail
@pytest.mark.unit
def test_put_db_same_intent(auto_login_logout):
    res = requests.put(
        POST_ENDPOINT + "/f2cccc42-df1e-4145-ad57-298b949c141a", {"vote": "upvote"}, timeout=3
    )

    assert res.status_code == status.HTTP_202_ACCEPTED


# TODO: create random post and delete after
@pytest.mark.xfail
@pytest.mark.unit
def test_put_db_diff_intent(auto_login_logout):
    res = requests.put(
        POST_ENDPOINT + "/f2cccc42-df1e-4145-ad57-298b949c141a", {"vote": "upvote"}, timeout=3
    )

    assert res.status_code == status.HTTP_201_CREATED


# TODO: create random post and delete after
@pytest.mark.xfail
@pytest.mark.unit
def test_unknown(auto_login_logout):
    res = requests.put(
        POST_ENDPOINT + "/f2cccc42-df1e-4145-ad57-298b949c141a",
        {"vote": "does not exist"},
        timeout=3,
    )

    assert res.text == ""
    assert res.status_code == status.HTTP_201_CREATED
