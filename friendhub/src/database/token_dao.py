from database.dbmanager import DBManager
from models.token_model import Token


class TokenDAO:
    @staticmethod
    def add(token: Token) -> None:
        DBManager.execute(
            """INSERT INTO tokens(id, owner, valid_until, value, purpose, date_created)
             VALUES(%s, %s, %s, %s, %s, %s)""",
            (
                str(token.id_),
                str(token.owner_id),
                token.valid_until,
                token.value,
                token.purpose.value,
                token.date_created,
            ),
        )

    @staticmethod
    def invalidate(token: Token) -> None:
        DBManager.execute("UPDATE tokens SET force_invalid=true WHERE id=%s", (str(token.id_),))

    @staticmethod
    def get_token_by_value(value: str) -> Token | None:
        result = DBManager.execute("SELECT * FROM tokens where value=%s", (value,))
        if not result:
            return None
        return Token.from_db(result[0])
