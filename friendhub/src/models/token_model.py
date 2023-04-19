from __future__ import annotations

import random
import string
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import jwt
from config_keys import JWT_ALGORITHM, JWT_KEY
from database.token_dao import TokenDAO


@dataclass(kw_only=True)
class JwtToken:
    @staticmethod
    def __random_data() -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=5))

    owner_id: uuid.UUID
    date_created: datetime = field(default_factory=datetime.now)
    valid_until: datetime
    purpose: Purpose
    rnd: str = field(init=False, default_factory=__random_data)

    class Purpose(str, Enum):
        DELETE_PROFILE = "delete_profile"
        USER_LOGIN = "user_login"

    def build(self) -> str:
        return jwt.encode(
            {
                "sub": str(self.owner_id),
                "iat": int(self.date_created.timestamp()),
                "exp": int(self.valid_until.timestamp()),
                "purpose": self.purpose.value,
                "entropy": self.rnd,
            },
            JWT_KEY,
            JWT_ALGORITHM,
        )

    @classmethod
    def from_str(cls, string_: str) -> JwtToken:
        result = jwt.decode(string_, JWT_KEY, [JWT_ALGORITHM])
        return JwtToken(
            owner_id=uuid.UUID(result["sub"]),
            date_created=datetime.fromtimestamp(result["iat"]),
            valid_until=datetime.fromtimestamp(result["exp"]),
            purpose=JwtToken.Purpose(result["purpose"]),
        )

    @property
    def is_valid(self) -> bool:
        return datetime.now().replace(tzinfo=None) < self.valid_until.replace(
            tzinfo=None
        ) and TokenDAO.is_valid(self.build())
