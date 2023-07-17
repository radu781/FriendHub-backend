from uuid import UUID

from database.dbmanager import DBManager
from database.user_dao import UserDAO
from database.vote_dao import VoteDAO
from models.post_model import Post
from models.post_wrapper import PostWrapper
from models.user_model import User
from models.vote_model import Vote


class PostDAO:
    @staticmethod
    def create_post(post: Post) -> None:
        DBManager.execute(
            """INSERT INTO
                 posts(id, owner_id, create_time, text, image, video, audio, likes, dislikes)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                str(post.id_),
                str(post.owner_id),
                post.create_time,
                post.text,
                post.image,
                post.video,
                post.audio,
                0,
                0,
            ),
        )

    @staticmethod
    def get_visible_posts(user: User | None, start: int, end: int) -> list[PostWrapper]:
        if not user:
            return []
        value = DBManager.execute(
            "SELECT * FROM posts ORDER BY create_time DESC LIMIT %s OFFSET %s", (end - start, start)
        )
        out: list[PostWrapper] = []
        for row in value:
            current_post = Post.from_db(row)
            # current_post = VoteDAO.update_votes_for_post(current_post)
            author = UserDAO.get_user_by_id(current_post.owner_id)
            if not author:
                continue
            current_vote = VoteDAO.get_vote(current_post.id_, user.id_)
            out.append(PostWrapper(current_post, author, current_vote))
        return out

    @staticmethod
    def get_post_by_id(id_: UUID) -> Post | None:
        value = DBManager.execute("SELECT * FROM posts WHERE id=%s", (str(id_),))
        if value == []:
            return None
        return Post.from_db(value[0])

    @staticmethod
    def add_vote(post_id: UUID, vote: Vote.Value) -> None:
        DBManager.execute(
            f"UPDATE posts SET {vote.db_name} = {vote.db_name} + 1 WHERE id = %s",
            (str(post_id),),
        )

    @staticmethod
    def remove_vote(post_id: UUID, vote: Vote.Value) -> None:
        DBManager.execute(
            f"UPDATE posts SET {vote.db_name} = {vote.db_name} - 1 WHERE id = %s",
            (str(post_id),),
        )

    @staticmethod
    def get_post_count_by_user(user_id: UUID) -> int:
        value = DBManager.execute("SELECT COUNT(*) FROM posts WHERE owner_id = %s", (str(user_id),))
        if value == []:
            return 0
        return int(value[0][0])

    @staticmethod
    def get_score_by_user(user_id: UUID) -> int:
        value = DBManager.execute(
            "SELECT SUM(likes)-SUM(dislikes) FROM posts WHERE owner_id = %s", (str(user_id),)
        )
        # return list(PostWrapper(Post.from_db(v[0]), User(), Vote()) for v in value)
        return value[0][0]
