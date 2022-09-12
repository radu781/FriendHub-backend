from datetime import datetime

from models.user_model import User

from database.dbmanager import DBManager


class UserDAO:
    @staticmethod
    def register_user(user: User) -> None:
        DBManager().execute(
            "INSERT INTO users(id, email, password, join_time) VALUES(:id, :email, :password, :date)",
            {
                "id": str(user.id_),
                "email": user.email,
                "password": user.password,
                "date": str(datetime.now()),
            },
        )
