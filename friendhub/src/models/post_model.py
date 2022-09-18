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
