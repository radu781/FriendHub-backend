from database.dbmanager import DBManager


class TokenDAO:
    @staticmethod
    def insert(jwt: str) -> None:
        DBManager.execute(
            """
            INSERT INTO tokens(value) VALUES(%s)""",
            (jwt,),
        )

    @staticmethod
    def is_valid(jwt: str) -> bool:
        result = DBManager.execute(
            """
            SELECT inactive FROM tokens WHERE value=%s""",
            (jwt,),
        )
        if result == []:
            return False
        return bool(result[0])

    @staticmethod
    def invalidate(jwt: str) -> None:
        DBManager.execute(
            """
            UPDATE tokens SET inactive=true WHERE value=%s""",
            (jwt,),
        )
