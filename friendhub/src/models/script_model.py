from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from config_keys import FERNET_KEY
from cryptography.fernet import Fernet


@dataclass(kw_only=True)
class Script:
    id_: uuid.UUID = field(default_factory=uuid.uuid4)
    author_id: uuid.UUID = field(default_factory=uuid.uuid4)
    code: str = field()
    fernet: Fernet = field(default=Fernet(FERNET_KEY), init=False)

    def encrypt(self) -> None:
        self.code = Script.fernet.encrypt(self.code.encode("utf-8")).decode("utf-8")

    @staticmethod
    def from_db(row: tuple) -> Script:
        return Script(
            id_=row[0],
            author_id=row[1],
            code=Script.fernet.decrypt(row[2]).decode("utf-8"),
        )
