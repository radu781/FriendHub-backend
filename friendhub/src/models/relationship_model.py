from __future__ import annotations

from datetime import datetime
from enum import Enum
import uuid
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Relationship:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id1: uuid.UUID
    user_id2: uuid.UUID
    type: Type
    change_time: datetime

    class Type(str, Enum):
        NONE = "none"
        REQUEST_PENDING = "request_pending"
        REQUEST_SENT = "request_sent"
        FRIEND = "friend"
        BLOCKED = "blocked"
        HIDDEN = "hidden"

        @classmethod
        def values(cls) -> set[str]:
            return set(map(lambda e: e.value, cls))

    @staticmethod
    def from_db(row: tuple) -> Relationship:
        return Relationship(
            id_=row[0], user_id1=row[1], user_id2=row[2], type=row[3], change_time=row[4]
        )
