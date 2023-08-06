from database.objects.media_history import MediaHistory
from database.dbmanager import DBManager


class MediaHistoryDAO:
    @staticmethod
    def insert(media: MediaHistory) -> None:
        DBManager.execute(
            """INSERT INTO media_history(
                id, owner_id, "type", change_time, location),
            VALUES(%s, %s, %s, %s, %s)""",
            (
                str(media.id_),
                str(media.owner_id),
                media.type_.value,
                str(media.create_time),
                media.location,
            ),
        )
