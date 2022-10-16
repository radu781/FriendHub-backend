from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class Post:
    id_: uuid.UUID = field(default=uuid.uuid4())
    owner_id: uuid.UUID = field(default=uuid.uuid4())
    create_time: datetime = field(default=datetime.now())
    likes: int
    dislikes: int
    text: str
    image: str
    video: str
    audio: str

    @staticmethod
    def from_db(row: tuple) -> Post:
        return Post(
            id_=row[0],
            owner_id=row[1],
            create_time=row[2],
            text=row[3],
            image=row[4],
            video=row[5],
            audio=row[6],
            likes=0,
            dislikes=0,
        )
