from datetime import datetime
import uuid

from models.user_model import User

from database.dbmanager import DBManager


class UserDAO:
    @staticmethod
    def get_user_by_id(id_: uuid.UUID) -> User | None:
        value = DBManager.execute("SELECT * FROM users WHERE id=%s", (str(id_),))
        if value == []:
            return None
        return User.from_db(value[0])

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        value = DBManager.execute("SELECT * FROM users WHERE email=%s", (email,))
        if value == []:
            return None
        return User.from_db(value[0])

    @staticmethod
    def register_user(user: User) -> None:
        DBManager.execute(
            "INSERT INTO users(id, first_name, middle_name, last_name, join_time, country, city, education, extra, profile_picture, banner_picture, password, email, permissions) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                str(user.id_),
                user.first_name,
                user.middle_name,
                user.last_name,
                str(datetime.now()),
                user.country,
                user.city,
                user.education,
                user.extra,
                user.profile_picture,
                user.banner_picture,
                user.password,
                user.email,
                user.permissions,
            ),
        )

    @staticmethod
    def user_exists(email: str) -> bool:
        return UserDAO.get_user_by_email(email) is not None

    @staticmethod
    def correct_password(email: str, password: str) -> bool:
        value = DBManager.execute(
            "SELECT COUNT(*) FROM users WHERE email=%s AND password=%s",
            (email, password),
        )
        return value[0][0] == 1
