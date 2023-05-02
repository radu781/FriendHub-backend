from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class Post:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    owner_id: uuid.UUID = field(default_factory=uuid.uuid4)
    create_time: datetime = field(default_factory=datetime.now)
    likes: int
    dislikes: int
    text: str
    image: str | None
    video: str | None
    audio: str | None

    @classmethod
    def from_db(cls, row: tuple) -> Post:
        return Post(
            id_=uuid.UUID(row[0]),
            owner_id=uuid.UUID(row[1]),
            create_time=row[2],
            text=row[5],
            image=row[6],
            video=row[7],
            audio=row[8],
            likes=0,
            dislikes=0,
        )
