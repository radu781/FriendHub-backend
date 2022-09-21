from datetime import datetime
import uuid

from models.user_model import User

from database.dbmanager import DBManager


class UserDAO:
    @staticmethod
    def get_user_by_id(id: uuid.UUID) -> User:
        value = DBManager.execute("SELECT * FROM users WHERE id=%s", (str(id),))
        if value == []:
            return User()
        return User.from_db(value[0])

    @staticmethod
    def register_user(user: User) -> None:
        DBManager.execute(
            "INSERT INTO users(id, email, password, join_time) VALUES(%s, %s, %s, %s)",
            (
                str(user.id_),
                user.email,
                user.password,
                str(datetime.now()),
            ),
        )

    @staticmethod
    def user_exists(email: str) -> bool:
        value = DBManager.execute("SELECT COUNT(*) FROM users WHERE email=%s", (email,))
        return value[0][0] != 0

    @staticmethod
    def correct_password(email: str, password: str) -> bool:
        value = DBManager.execute(
            "SELECT COUNT(*) FROM users WHERE email=%s AND password=%s",
            (email, password),
        )
        return value[0][0] == 1
