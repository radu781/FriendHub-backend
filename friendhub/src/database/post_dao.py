from models.post_model import Post
from models.post_wrapper import PostWrapper

from database.dbmanager import DBManager
from database.user_dao import UserDAO


class PostDAO:
    @staticmethod
    def create_post(post: Post) -> None:
        DBManager.execute(
            "INSERT INTO posts(id, owner_id, create_time, likes, dislikes, text, image, video, audio) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
            current_user = UserDAO.get_user_by_id(current_post.owner_id)
            if not current_user:
                continue
            out.append(PostWrapper(current_post, current_user))
        return out
