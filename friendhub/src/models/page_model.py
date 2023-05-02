from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class Page:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = field(default="")
    join_time: datetime = field(default_factory=datetime.now)
    profile_picture: str = field(default="")
    banner_picture: str = field(default="")

    @classmethod
    def from_db(cls, row: tuple) -> Page:
        return Page(
            id_=uuid.UUID(row[0]),
            name=row[1],
            join_time=row[2],
            profile_picture=row[3],
            banner_picture=row[4],
        )

    @staticmethod
    def from_dict(d: dict) -> Page:  # pylint: disable=invalid-name
        raise NotImplementedError()
