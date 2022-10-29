from __future__ import annotations

import base64
import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


def random_b64() -> str:
    return base64.b64encode(str(random.getrandbits(160)).encode("utf-8")).decode()[:-2]


@dataclass(kw_only=True)
class Token:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    value: str = field(default_factory=random_b64)
    owner_id: uuid.UUID
    date_created: datetime = field(default_factory=datetime.now)
    valid_until: datetime
    purpose: Purpose
    force_invalid: bool

    class Purpose(str, Enum):
        DELETE_PROFILE = "delete_profile"
        USER_LOGIN = "user_login"

    @staticmethod
    def from_db(row: tuple) -> Token:
        return Token(
            id_=row[0],
            owner_id=row[1],
            valid_until=row[2],
            value=row[3],
            purpose=row[4],
            date_created=row[5],
            force_invalid=row[6],
        )

    @property
    def is_valid(self) -> bool:
        return datetime.now() < self.valid_until and not self.force_invalid

    @property
    def is_delete_profile(self) -> bool:
        return self.purpose == Token.Purpose.DELETE_PROFILE
