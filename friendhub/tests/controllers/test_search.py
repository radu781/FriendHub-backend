import json

import pytest
import requests
from flask_api import status
import utils.validators.other as validators
from tests.conftest import create_random_user, delete_user
from models.relationship_model import Relationship
from tests import SEARCH_ENDPOINT


@pytest.mark.unit
def test_missing_parameters():
    res = requests.get(SEARCH_ENDPOINT, timeout=3)
    content = json.loads(res.text)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in content
    assert content["reason"] == "missing parameters"
    assert "parameters" in content
    assert content["parameters"] == "query"


@pytest.mark.unit
def test_wrong_body():
    res = requests.get(SEARCH_ENDPOINT, {"query": "test"}, data="{'key':'error}", timeout=3)
    content = json.loads(res.text)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in content
    assert content["error"] == "json body decode error"
    assert "reason" in content


@pytest.mark.unit
def test_type_missing():
    res = requests.get(SEARCH_ENDPOINT, {"query": "test"}, data='{"notType":1}', timeout=3)
    content = json.loads(res.text)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in content
    assert content["reason"] == "expected 'type' in request body"


@pytest.mark.unit
def test_type_zero_len():
    res = requests.get(SEARCH_ENDPOINT, {"query": "test"}, data='{"type":[]}', timeout=3)
    content = json.loads(res.text)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "reason" in content
    assert content["reason"] == "'type' is either not an array or has length 0"


@pytest.mark.unit
def test_type_unknown():
    res = requests.get(SEARCH_ENDPOINT, {"query": "test"}, data='{"type":["unknown"]}', timeout=3)
    content = json.loads(res.text)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "allowedTypes" in content
    assert content["allowedTypes"] == ["user", "page"]
    assert "reason" in content
    assert content["reason"] == "found unknown filter types"
    assert "unknown" in content


# TODO: investigate json creation
@pytest.mark.xfail
@pytest.mark.unit
def test_search_ok():
    TYPES = ["user", "page"]
    for type_ in TYPES:
        res = requests.get(
            SEARCH_ENDPOINT,
            {"query": "test", "max": 5},
            data={"type": type_},
            timeout=3,
        )
        content = json.loads(res.text)

        assert res.status_code == status.HTTP_200_OK
        assert type_ in content
        assert "count" in content[f"{type_}s"]
        assert isinstance(int, content[f"{type_}s"]["count"])
        assert content[f"{type_}s"]["count"] <= 5
        assert "data" in content[f"{type_}s"]
        assert content[f"{type_}s"]["count"] == len(content[f"{type_}s"]["data"])

    res = requests.get(
        SEARCH_ENDPOINT, {"query": "test", "max": 5}, data={"type": TYPES}, timeout=3
    )
    content = json.loads(res.text)

    assert res.status_code == status.HTTP_200_OK
    for type_ in TYPES:
        assert type_ in content
        assert "count" in content[f"{type_}s"]
        assert isinstance(int, content[f"{type_}s"]["count"])
        assert content[f"{type_}s"]["count"] <= 5
        assert "data" in content[f"{type_}s"]
        assert content[f"{type_}s"]["count"] == len(content[f"{type_}s"]["data"])
