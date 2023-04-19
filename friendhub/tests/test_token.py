from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from models.token_model import JwtToken


@pytest.mark.unit
def test_create():
    owner_id = uuid4()
    date_created = datetime.now()
    valid_until = datetime.now() + timedelta(days=1)
    purpose = JwtToken.Purpose.USER_LOGIN
    token_str = JwtToken(
        owner_id=owner_id,
        date_created=date_created,
        valid_until=valid_until,
        purpose=purpose,
    ).build()
    token_obj = JwtToken.from_str(token_str)

    assert token_obj.owner_id == owner_id
    assert token_obj.date_created.timestamp() == pytest.approx(date_created.timestamp(), abs=1)
    assert token_obj.valid_until.timestamp() == pytest.approx(valid_until.timestamp(), abs=1)
    assert token_obj.purpose == purpose


@pytest.mark.unit
def test_is_valid():
    token = JwtToken(
        owner_id=uuid4(),
        date_created=datetime.now(),
        valid_until=datetime.now(),
        purpose=JwtToken.Purpose.USER_LOGIN,
    )
    assert not token.is_valid

    token = JwtToken(
        owner_id=uuid4(),
        date_created=datetime.now(),
        valid_until=datetime.now() - timedelta(days=3),
        purpose=JwtToken.Purpose.USER_LOGIN,
    )
    assert not token.is_valid

    token = JwtToken(
        owner_id=uuid4(),
        date_created=datetime.now(),
        valid_until=datetime.now() + timedelta(days=3),
        purpose=JwtToken.Purpose.USER_LOGIN,
    )
    assert token.is_valid

    token = JwtToken(
        owner_id=uuid4(),
        date_created=datetime.now(),
        valid_until=datetime.now() + timedelta(days=3),
        purpose=JwtToken.Purpose.USER_LOGIN,
    )
    assert not token.is_valid
