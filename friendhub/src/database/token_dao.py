from database.dbmanager import DBManager
from models.token_model import Token


class TokenDAO:
    @staticmethod
    def add(token: Token) -> None:
        DBManager.execute(
            "INSERT INTO tokens(id, owner, valid_until, value, purpose) VALUES(%s, %s, %s, %s, %s)",
            (
                str(token.id_),
                str(token.owner_id),
                token.valid_until,
                token.value,
                token.purpose._value_,
            ),
        )

    @staticmethod
    def get_token_by_value(value: str) -> Token:
        result = DBManager.execute("SELECT * FROM tokens where value=%s", (value,))
        return Token.from_db(result[0])
