import uuid

from database.dbmanager import DBManager
from database.objects.activity import Activity
from datetime import date


class ActivityDAO:
    @staticmethod
    def create_activity(post: Activity) -> None:
        DBManager.execute(
            "INSERT INTO activities(id, user_id, score, date) VALUES(%s, %s, %s, %s)",
            (str(post.id_), str(post.user_id), post.score, str(post.date)),
        )

    @staticmethod
    def get_activities(user_id: uuid.UUID, from_: date, to: date) -> list[Activity]:
        value = DBManager.execute("SELECT * FROM activities WHERE user_id=%s", (str(user_id),))
        activities = list(Activity.from_db(row) for row in value)
        return activities
