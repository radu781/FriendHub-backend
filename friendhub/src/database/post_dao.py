from uuid import UUID

from models.post_model import Post
from models.post_wrapper import PostWrapper
from utils import session

from database.dbmanager import DBManager
from database.user_dao import UserDAO
from database.vote_dao import VoteDAO


class PostDAO:
    @staticmethod
    def create_post(post: Post) -> None:
        DBManager.execute(
            """INSERT INTO
                 posts(id, owner_id, create_time, likes, dislikes, text, image, video, audio)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                str(post.id_),
                str(post.owner_id),
                post.create_time,
                post.likes,
                post.dislikes,
                post.text,
                post.image,
                post.video,
                post.audio,
            ),
        )

    @staticmethod
    def get_visible_posts() -> list[PostWrapper]:
        value = DBManager.execute("SELECT * FROM posts ORDER BY create_time DESC", ())
        out: list[PostWrapper] = []
        for row in value:
            current_post = Post.from_db(row)
            current_post = VoteDAO.get_votes_for_post(current_post)
            author = UserDAO.get_user_by_id(current_post.owner_id)
            if not author:
                continue
            current_user = session.get_user_in_session()
            if not current_user:
                continue
            current_vote = VoteDAO.get_vote(current_post.id_, current_user.id_)
            out.append(PostWrapper(current_post, author, current_vote))
        return out

    @staticmethod
    def get_post_by_id(id_: UUID) -> Post | None:
        value = DBManager.execute("SELECT * FROM posts WHERE id=%s", (str(id_),))
        if value == []:
            return None
        return Post.from_db(value[0])
