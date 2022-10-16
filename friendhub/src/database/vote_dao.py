import uuid
from models.post_model import Post
from models.vote_model import Vote
from database.dbmanager import DBManager


class VoteDAO:
    @staticmethod
    def add(vote: Vote) -> None:
        DBManager.execute(
            "INSERT INTO votes(id, parent_id, author_id, value) VALUES(%s, %s, %s, %s)",
            (str(vote.id_), str(vote.parent_id), str(vote.author_id), vote.value),
        )

    @staticmethod
    def get_vote(parent: uuid.UUID, author: uuid.UUID) -> Vote | None:
        value = DBManager.execute(
            "SELECT * FROM votes WHERE parent_id=%s AND author_id=%s",
            (str(parent), str(author)),
        )
        if value == []:
            return None
        return Vote.from_db(value[0])

    @staticmethod
    def get_vote_by_id(id_: uuid.UUID) -> Vote | None:
        value = DBManager.execute("SELECT * FROM votes WHERE id=%s", (str(id_),))
        if value == []:
            return None
        return Vote.from_db(value[0])

    @staticmethod
    def delete(vote_id: uuid.UUID) -> None:
        DBManager.execute("DELETE FROM votes WHERE id=%s", (str(vote_id),))

    @staticmethod
    def get_votes_for_post(post: Post) -> Post:
        value = DBManager.execute(
            "SELECT * FROM votes WHERE parent_id=%s", (str(post.id_),)
        )
        votes: list[Vote] = []
        for val in value:
            votes.append(Vote.from_db(val))

        for vote in votes:
            post.likes += vote.value == Vote.Value.UPVOTE
            post.dislikes += vote.value == Vote.Value.DOWNVOTE

        return post
