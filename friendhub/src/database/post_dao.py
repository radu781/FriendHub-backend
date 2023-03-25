from uuid import UUID

from database.dbmanager import DBManager
from database.user_dao import UserDAO
from database.vote_dao import VoteDAO
from models.post_model import Post
from models.post_wrapper import PostWrapper
from models.user_model import User


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
        value = DBManager.execute(
            f"SELECT * FROM posts ORDER BY create_time DESC LIMIT {end-start} OFFSET {start}", ()
        )
        out: list[PostWrapper] = []
        for row in value:
            current_post = Post.from_db(row)
            current_post = VoteDAO.get_votes_for_post(current_post)
            author = UserDAO.get_user_by_id(current_post.owner_id)
            if not author:
                continue
            if not user:
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
