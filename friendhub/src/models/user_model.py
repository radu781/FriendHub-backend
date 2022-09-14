import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class User:
    id_: uuid.UUID = field(default=uuid.uuid4())
    first_name: str = field(default="")
    profile_picture: str = field(default="")
    middle_name: str = field(default="")
    last_name: str = field(default="")
    join_time: datetime = field(default=datetime.fromtimestamp(0))
    country: str = field(default="")
    city: str = field(default="")
    education: str = field(default="")
    extra: str = field(default="")
    banner_picture: str = field(default="")
    email: str = field(default="")
    password: str = field(default="")

    def __post_init__(self) -> None:
        if self.password != None:
            self.password = hashlib.sha256(bytes(self.password, "utf-8")).digest().hex()
