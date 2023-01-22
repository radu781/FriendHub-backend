import pytest
from database.dbmanager import DBManager


@pytest.mark.unit
@pytest.mark.db
def test_connection():
    assert DBManager.execute("SELECT 1", ()) == [(1,)], "No connection"


@pytest.mark.unit
@pytest.mark.db
def test_structure_comments():
    EXPECTED = ["id", "parent_id", "body", "likes", "dislikes"]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC comments", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_im_group_members():
    EXPECTED = ["id", "group_id", "user_or_page_id", "permissions", "join_time"]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC im_group_members", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_im_groups():
    EXPECTED = ["id", "name", "profile_picture"]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC im_groups", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_message():
    EXPECTED = ["id", "from", "to", "time"]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC message", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_p_group_members():
    EXPECTED = ["id", "group_id", "user_or_page_id", "permissions", "join_time"]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC p_group_members", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_pages():
    EXPECTED = ["id", "name", "join_time", "profile_picture", "banner_picture"]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC pages", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_pages_groups():
    EXPECTED = ["id", "name", "profile_picture"]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC pages_groups", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_posts():
    EXPECTED = [
        "id",
        "owner_id",
        "create_time",
        "text",
        "image",
        "video",
        "audio",
    ]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC posts", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_relationships():
    EXPECTED = [
        "id",
        "from",
        "to",
        "type",
        "change_time",
    ]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC relationships", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_tokens():
    EXPECTED = ["id", "owner", "valid_until", "value", "purpose", "date_created", "force_invalid"]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC tokens", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_replies():
    EXPECTED = [
        "id",
        "parent_id",
        "body",
        "likes",
        "dislikes",
    ]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC replies", ())):
        assert expect == line[0], "Table format changed"


@pytest.mark.unit
@pytest.mark.db
def test_structure_users():
    EXPECTED = [
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "join_time",
        "country",
        "city",
        "education",
        "extra",
        "profile_picture",
        "banner_picture",
        "password",
        "email",
    ]
    for expect, line in zip(EXPECTED, DBManager.execute("DESC users", ())):
        assert expect == line[0], "Table format changed"
