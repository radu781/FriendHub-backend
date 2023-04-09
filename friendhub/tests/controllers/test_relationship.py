import json
from random import randint

import pytest
import requests
from flask_api import status
from tests import (
    RELATIONSHIP_ENDPOINT,
)
from tests.conftest import create_random_user, delete_user

# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_post_missing_parameters(auto_login_logout):
    res = requests.post(RELATIONSHIP_ENDPOINT, timeout=3)
    content = json.loads(res.content)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in content
    assert content["reason"] == "missing parameters"
    assert "parameters" in content
    PARAMETERS = ["userId", "type"]
    stripped = [ele.strip() for ele in content["parameters"].split(",")]
    assert sorted(PARAMETERS) == sorted(stripped)

# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_post_invalid_uuid(auto_login_logout):
    res = requests.post(RELATIONSHIP_ENDPOINT, {"userId": "123", "type": "friend"}, timeout=3)
    content = json.loads(res.content)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in content
    assert content["reason"] == "given id is not a UUID"
    assert "id" in content
    assert content["id"] == "123"

# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_post_user_not_found(auto_login_logout):
    res = requests.post(
        RELATIONSHIP_ENDPOINT,
        {"userId": "00000000-0000-0000-0000-000000000000", "type": "friend"},
        timeout=3,
    )
    content = json.loads(res.content)

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert "reason" in content
    assert content["reason"] == "user does not exist"

# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_post_unknown_type(auto_login_logout):
    res = requests.post(
        RELATIONSHIP_ENDPOINT,
        {"userId": "00000000-0000-0000-0000-000000000000", "type": "does not exist"},
        timeout=3,
    )
    content = json.loads(res.content)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in content
    assert content["reason"] == "'type' does not exist"
    assert "supportedTypes" in content
    assert content["supportedTypes"] == []

# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_post_ok(auto_login_logout):
    id_ = create_random_user()
    res = requests.post(
        RELATIONSHIP_ENDPOINT,
        {"userId": str(id_), "type": "friend"},
        timeout=3,
    )
    delete_user(id_)
    content = json.loads(res.content)

    assert res.status_code == status.HTTP_201_CREATED
    assert "relationship" in content

# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_get_missing_parameters(auto_login_logout):
    res = requests.post(RELATIONSHIP_ENDPOINT, timeout=3)
    content = json.loads(res.content)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in content
    assert content["reason"] == "missing parameters"
    assert "parameters" in content
    assert content["parameters"] == "userId"

# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_get_invalid_uuid(auto_login_logout):
    res = requests.post(RELATIONSHIP_ENDPOINT, {"userId": "123"}, timeout=3)
    content = json.loads(res.content)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in content
    assert content["error"] == "given id is not a UUID"
    assert "id" in content
    assert content["id"] == "123"

# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_get_user_not_found(auto_login_logout):
    res = requests.post(
        RELATIONSHIP_ENDPOINT, {"userId": "00000000-0000-0000-0000-000000000000"}, timeout=3
    )
    content = json.loads(res.content)

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert "reason" in content
    assert content["reason"] == "user does not exist"

# TODO: fix when adding JWT
@pytest.mark.xfail
@pytest.mark.unit
def test_get_ok(auto_login_logout):
    id_ = create_random_user()
    res = requests.post(RELATIONSHIP_ENDPOINT, {"userId": str(id_)}, timeout=3)
    delete_user(id_)
    content = json.loads(res.content)

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert "data" in content
    assert "from" in content["data"]
    assert "to" in content["data"]
