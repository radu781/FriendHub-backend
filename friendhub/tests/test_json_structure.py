import json

import pytest
import requests
import utils.validators.other as validators
from models.relationship_model import Relationship
from tests.conftest import create_random_user, delete_user

from . import (
    LOGIN_ENDPOINT,
    POST_ENDPOINT,
    PROFILE_ENDPOINT,
    RELATIONSHIP_ENDPOINT,
    UPLOAD_ENDPOINT,
    USER_EMAIL,
    USER_PASSWORD,
)


@pytest.mark.unit
def test_token_structure(auto_logout):  # pylint: disable=unused-argument, redefined-outer-name
    res = requests.post(LOGIN_ENDPOINT, {"email": USER_EMAIL, "password": USER_PASSWORD}, timeout=3)
    content = json.loads(res.content)

    assert "token" in content
    assert content["token"].count(".") == 2


@pytest.mark.unit
def test_user_structure(auto_login_logout):  # pylint: disable=unused-argument
    id_ = create_random_user()
    res = requests.get(PROFILE_ENDPOINT + f"/{id_}", timeout=3)
    delete_user(id_)
    js = json.loads(res.text)["user"]

    assert "banner_picture" in js
    assert "city" in js
    assert "country" in js
    assert "education" in js
    assert "email" in js
    assert "extra" in js
    assert "first_name" in js
    assert "id_" in js
    assert "join_time" in js
    assert "last_name" in js
    assert "middle_name" in js
    assert "password" in js
    assert "permissions" in js
    assert "profile_picture" in js

    assert js["password"] is None
    assert js["permissions"] is None
    assert js["email"] is None

    assert js["banner_picture"] is None or validators.is_image_path(js["banner_picture"])
    assert validators.is_uuid(js["id_"])
    assert validators.is_datetime(js["join_time"])
    assert js["profile_picture"] is None or validators.is_image_path(js["profile_picture"])


@pytest.mark.unit
def test_post_structure(auto_login_logout):  # pylint: disable=unused-argument
    res = requests.post(
        UPLOAD_ENDPOINT,
        {"text": "testing text"},
        headers={"Authorization": f"Bearer {auto_login_logout}"},
        timeout=3,
    )
    id_ = json.loads(res.text)["post"]["id_"]
    res = requests.get(
        POST_ENDPOINT + f"/{id_}",
        headers={"Authorization": f"Bearer {auto_login_logout}"},
        timeout=3,
    )
    js = json.loads(res.text)["post"]

    assert "audio" in js
    assert "create_time" in js
    assert "dislikes" in js
    assert "id_" in js
    assert "image" in js
    assert "likes" in js
    assert "owner_id" in js
    assert "text" in js
    assert "video" in js

    assert js["audio"] is None or validators.is_audio_path(js["audio"])
    assert validators.is_datetime(js["create_time"])
    assert isinstance(js["dislikes"], int) and js["dislikes"] >= 0
    assert validators.is_uuid(js["id_"])
    assert js["image"] is None or validators.is_image_path(js["image"])
    assert isinstance(js["likes"], int) and js["likes"] >= 0
    assert validators.is_uuid(js["owner_id"])
    assert isinstance(js["text"], str)
    assert js["video"] is None or validators.is_video_path(js[["video"]])


@pytest.mark.unit
def test_vote_structure(auto_login_logout):  # pylint: disable=unused-argument
    res = requests.get(POST_ENDPOINT, timeout=3)
    js = json.loads(res.text)["vote"]

    assert "author_id" in js
    assert "create_time" in js
    assert "id_" in js
    assert "parent_id" in js
    assert "value" in js

    assert validators.is_uuid(js["author_id"])
    assert validators.is_datetime(js["create_time"])
    assert validators.is_uuid(js["id_"])
    assert validators.is_uuid(js["parent_id"])
    assert isinstance(str, js["value"])


@pytest.mark.unit
def test_relationship_structure(auto_login_logout):  # pylint: disable=unused-argument
    id_ = create_random_user()
    res = requests.post(RELATIONSHIP_ENDPOINT, {"userId": str(id_)}, timeout=3)
    delete_user(id_)
    content = json.loads(res.content)["data"]["from"]

    assert "change_time" in content
    assert "from_" in content
    assert "id_" in content
    assert "to_" in content
    assert "type_" in content

    assert validators.is_datetime(content["change_time"])
    assert validators.is_uuid(content["from_"])
    assert validators.is_uuid(content["id_"])
    assert validators.is_uuid(content["to_"])
    assert content["type_"] in Relationship.Type.values()
