from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class Post:
    id_: uuid.UUID = field(default=uuid.uuid4())
    owner_id: uuid.UUID = field(default=uuid.uuid4())
    create_time: datetime = field(default=datetime.now())
    likes: int = field(default=0)
    dislikes: int = field(default=0)
    text: str = field(default="")
    image: str = field(default="")
    video: str = field(default="")
    audio: str = field(default="")

    @staticmethod
    def from_db(row: tuple) -> Post:
        return Post(
            id_=row[0],
            owner_id=row[1],
            create_time=row[2],
            likes=row[3],
            dislikes=row[4],
            text=row[5],
            image=row[6],
            video=row[7],
            audio=row[8]
        )
