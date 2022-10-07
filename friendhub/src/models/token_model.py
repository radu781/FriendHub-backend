from __future__ import annotations

import base64
import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass(kw_only=True)
class Token:
    id_: uuid.UUID = field(default=uuid.uuid4())
    value: str = base64.b64encode(str(random.getrandbits(160)).encode("utf-8")).decode()[:-2]
    owner_id: uuid.UUID
    date_created: datetime=field(default=datetime.now())
    valid_until: datetime
    purpose: Purpose

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
            date_created=row[5]
        )

    @property
    def is_valid(self) -> bool:
        return datetime.now() < self.valid_until

    @property
    def is_delete_profile(self) -> bool:
        return self.purpose == Token.Purpose.DELETE_PROFILE
