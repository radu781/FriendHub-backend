from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class PageGroup:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = field(default="")
    profile_picture: str = field(default="")

    @classmethod
    def from_db(cls, row: tuple) -> PageGroup:
        return PageGroup(
            id_=uuid.UUID(row[0]),
            name=row[1],
            profile_picture=row[2],
        )

    @staticmethod
    def from_dict(d: dict) -> PageGroup:
        raise NotImplementedError()
