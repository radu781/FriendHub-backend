from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class LoginLocation:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    country: str
    city: str
    region: str
    isp: str
    allowed: bool = field(default=False)
    timestamp: datetime = field(default_factory=datetime.now)
    ip_address: str

    @classmethod
    def from_db(cls, row: tuple) -> LoginLocation:
        return LoginLocation(
            id_=uuid.UUID(row[0]),
            user_id=uuid.UUID(row[1]),
            country=row[2],
            city=row[3],
            region=row[4],
            isp=row[5],
            allowed=bool(row[6]),
            timestamp=row[7],
            ip_address=row[8],
        )
