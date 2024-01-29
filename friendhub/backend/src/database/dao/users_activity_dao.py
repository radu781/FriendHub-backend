from datetime import datetime
from database.objects.users_activity import UsersActivity
from database.dbmanager import DBManager
from uuid import UUID


class UsersActivityDAO:
    @staticmethod
    def create(activity: UsersActivity) -> None:
        DBManager.execute(
            """INSERT INTO users_activity(id, activity_status, user_agent, device_ip, change_time)
            VALUES(%s, %s, %s, %s, %s)""",
            (
                str(activity.id_),
                activity.activity_status.value,
                activity.user_agent,
                activity.device_ip,
                activity.change_time,
            ),
        )

    @staticmethod
    def get(user_id: UUID) -> UsersActivity | None:
        value = DBManager.execute("SELECT * FROM users_activity WHERE user_id=%s", (str(user_id),))
        if value == []:
            return None
        return UsersActivity.from_db(value[0])

    @staticmethod
    def update(user_id: UUID, status: UsersActivity.Activity, user_agent: str, ip: str) -> None:
        DBManager.execute(
            """UPDATE users_activity SET activity_status=%s, change_time=%s, user_agent=%s,
            device_ip=%s WHERE user_id=%s""",
            (
                status.value,
                datetime.now(),
                user_agent,
                ip,
                str(user_id),
            ),
        )
