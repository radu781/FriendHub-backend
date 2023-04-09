from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from models.token_model import Token


@pytest.mark.unit
def test_create_invalid_token():
    token = Token(
        owner_id=uuid4(),
        valid_until=datetime.now(),
        purpose=Token.Purpose.DELETE_PROFILE,
        force_invalid=False,
    )
    assert not token.is_valid

    token = Token(
        owner_id=uuid4(),
        valid_until=datetime.now() + timedelta(days=1),
        purpose=Token.Purpose.DELETE_PROFILE,
        force_invalid=True,
    )
    assert not token.is_valid


@pytest.mark.unit
def test_create_valid_token():
    token = Token(
        owner_id=uuid4(),
        valid_until=datetime.now() + timedelta(days=1),
        purpose=Token.Purpose.DELETE_PROFILE,
        force_invalid=False,
    )
    assert token.is_valid
