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
    permissions: int = field(default=0)

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
            permissions=row[13],
        )

    @staticmethod
    def from_dict(d: dict) -> User:
        return User(
            id_=d["id_"],
            first_name=d["first_name"],
            middle_name=d["middle_name"],
            last_name=d["last_name"],
            join_time=d["join_time"],
            country=d["country"],
            city=d["city"],
            education=d["education"],
            extra=d["extra"],
            profile_picture=d["profile_picture"],
            banner_picture=d["banner_picture"],
            password=d["password"],
            email=d["email"],
            permissions=d["permissions"],
        )

    @property
    def ok(self) -> bool:
        return not not self.email and not not self.first_name

    @property
    def is_admin(self) -> bool:
        return self.permissions & 1 == 1
