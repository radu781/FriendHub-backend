import uuid

from database.dbmanager import DBManager
from models.script_model import Script


class ScriptDAO:
    @staticmethod
    def add(script: Script) -> None:
        DBManager.execute(
            "INSERT INTO scripts(id, author, script) VALUES(%s, %s,%s)",
            (str(script.id_), str(script.author_id), script.code),
        )

    @staticmethod
    def get(id_: uuid.UUID) -> Script | None:
        value = DBManager.execute("SELECT * FROM scripts WHERE id=%s", (str(id_),))
        if value == []:
            return None
        return Script.from_db(value[0])
