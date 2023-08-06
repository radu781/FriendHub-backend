from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass(kw_only=True)
class UsersActivity:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    activity_status: Activity
    user_agent: str
    device_ip: str
    change_time: datetime = field(default_factory=datetime.now)
    user_id: uuid.UUID

    class Activity(str, Enum):
        ACTIVE = "active"
        AWAY = "away"
        DO_NOT_DISTURB = "do_not_disturb"
        OFFLINE = "offline"

        @classmethod
        def values(cls) -> set[str]:
            return set(map(lambda e: e.value, cls))


    @classmethod
    def from_db(cls, row: tuple) -> UsersActivity:
        return UsersActivity(
            id_=uuid.UUID(row[0]),
            activity_status=UsersActivity.Activity(row[1]),
            user_agent=row[2],
            device_ip=row[3],
            change_time=datetime(
                row[4].year, row[4].month, row[4].day, row[4].hour, row[4].minute, row[4].second
            ),
            user_id=uuid.UUID(row[5])
        )
