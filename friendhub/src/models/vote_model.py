from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass(kw_only=True)
class Vote:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    parent_id: uuid.UUID
    author_id: uuid.UUID
    value: Value
    create_time: datetime = field(default_factory=datetime.now)

    class Value(str, Enum):
        UPVOTE = "upvote"
        DOWNVOTE = "downvote"
        CLEAR = "clear"

        @property
        def is_clear(self) -> bool:
            return self.value == Vote.Value.CLEAR

        @classmethod
        def values(cls) -> set[str]:
            return set(map(lambda e: e.value, cls))

    @staticmethod
    def from_db(row: tuple) -> Vote:
        return Vote(id_=row[0], parent_id=row[1], author_id=row[2], value=row[3])
