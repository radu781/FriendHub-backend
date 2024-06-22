from uuid import UUID
from models.relationship_model import Relationship
from database.dbmanager import DBManager
from models.user_model import User
from database.user_dao import UserDAO


class RelationshipDAO:
    @staticmethod
    def upsert(rel: Relationship) -> None:
        if RelationshipDAO.get_relationship_by_id(rel.from_, rel.to_) is None:
            DBManager.execute(
                """INSERT INTO relationships(id, "from", "to", type, change_time)
                VALUES(%s, %s, %s, %s, %s)""",
                (str(rel.id_), str(rel.from_), str(rel.to_), rel.type_, rel.change_time),
            )
        else:
            DBManager.execute(
                """UPDATE relationships SET type=%s, change_time=%s WHERE "from"=%s AND "to"=%s""",
                (rel.type_, rel.change_time, str(rel.from_), str(rel.to_)),
            )

    @staticmethod
    def get_relationship_by_id(from_id: UUID, to_id: UUID) -> Relationship | None:
        value = DBManager.execute(
            """SELECT * FROM relationships WHERE "from"=%s and "to"=%s""",
            (str(from_id), str(to_id)),
        )
        if value == []:
            return None
        return Relationship.from_db(value[0])

    @staticmethod
    def get_relationship(id1: UUID, id2: UUID) -> dict[str, Relationship]:
        out: dict[str, Relationship] = {}
        value = DBManager.execute(
            """SELECT * FROM relationships WHERE "from"=%s AND "to"=%s""",
            (str(id1), str(id2)),
        )
        if value == []:
            return {}
        out["from"] = Relationship.from_db(value[0])
        value = DBManager.execute(
            """SELECT * FROM relationships WHERE "to"=%s AND "from"=%s""",
            (str(id1), str(id2)),
        )
        if value == []:
            return out
        out["to"] = Relationship.from_db(value[0])
        return out

    @staticmethod
    def get_relationship_count(user_id: UUID, type: Relationship.Type) -> int:
        value = DBManager.execute(
            'SELECT COUNT(*) FROM relationships WHERE "from"=%s AND "type"=%s',
            (str(user_id), type.value),
        )
        return value[0][0]

    @staticmethod
    def get_friends(user_id: UUID) -> list[User]:
        value = DBManager.execute(
            """SELECT * FROM relationships WHERE "from"=%s AND "type"=%s""",
            (str(user_id), Relationship.Type.FRIEND.value),
        )
        print(f"{value=}")
        out = []
        for v in value:
            user = UserDAO.get_user_by_id(v[2])
            if user is not None:
                out.append(user.sanitize())
        return out
