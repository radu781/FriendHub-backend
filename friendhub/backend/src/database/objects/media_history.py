from __future__ import annotations

from dataclasses import dataclass, field
import uuid
from datetime import datetime
from enum import Enum


@dataclass(kw_only=True)
class MediaHistory:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    owner_id: uuid.UUID = field(default_factory=uuid.uuid4)
    type_: Type
    create_time: datetime = field(default_factory=datetime.now)
    location: str

    class Type(str, Enum):
        PROFILE = "profile"
        BANNER = "banner"
