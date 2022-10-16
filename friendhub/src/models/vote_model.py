from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


@dataclass(kw_only=True)
class Vote:
    id_: uuid.UUID = field(default=uuid.uuid4())
    parent_id: uuid.UUID
    author_id: uuid.UUID
    value: Value
    create_time: datetime = field(default=datetime.now())

    class Value(str, Enum):
        UPVOTE = "upvote"
        DOWNVOTE = "downvote"
        CLEAR = "clear"

    @staticmethod
    def from_db(row: tuple) -> Vote:
        return Vote(id_=row[0], parent_id=row[1], author_id=row[2], value=row[3])
