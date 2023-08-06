from __future__ import annotations

from dataclasses import dataclass, field
import uuid
from datetime import date


@dataclass(kw_only=True)
class Activity:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID = field(default_factory=uuid.uuid4)
    score: int = field(default=0)
    date: date

    @classmethod
    def from_db(cls, row: tuple) -> Activity:
        return Activity(
            id_=uuid.UUID(row[0]),
            user_id=uuid.UUID(row[1]),
            score=int(row[2]),
            date=date(row[3].year, row[3].month, row[3].day),
        )
