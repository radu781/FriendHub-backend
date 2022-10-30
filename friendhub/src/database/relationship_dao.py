from uuid import UUID
from models.relationship_model import Relationship
from database.dbmanager import DBManager


class RelationshipDAO:
    @staticmethod
    def insert_or_update(rel: Relationship) -> None:
        if RelationshipDAO.get_relationship(rel.id_) is None:
            DBManager.execute(
                """INSERT INTO relationships(id, user_id1, user_id2, type, change_time)
                VALUES(%s, %s, %s, %s, %s)""",
                (str(rel.id_), str(rel.user_id1), str(rel.user_id2), rel.type, rel.change_time),
            )
        else:
            DBManager.execute(
                "UPDATE relationships SET type=%s, change_time=%s WHERE id=%s",
                (rel.type, rel.change_time, str(rel.id_)),
            )

    @staticmethod
    def get_relationship(id_: UUID) -> Relationship | None:
        # TODO: should use both user ids, not the relationship id
        value = DBManager.execute("SELECT * FROM relationships WHERE id=%s", (str(id_),))
        if value == []:
            return None
        return Relationship.from_db(value[0])
