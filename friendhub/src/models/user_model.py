from __future__ import annotations
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
    join_time: datetime = field(default=datetime.now())
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

    @staticmethod
    def from_db(row: tuple) -> User:
        return User(
            id_=row[0],
            first_name=row[1],
            middle_name=row[2],
            last_name=row[3],
            join_time=row[4],
            country=row[5],
            city=row[6],
            education=row[7],
            extra=row[8],
            profile_picture=row[9],
            banner_picture=row[10],
            password=row[11],
            email=row[12],
        )
