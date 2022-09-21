from uuid import UUID
from models.post_model import Post

from database.dbmanager import DBManager


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
    def get_visible_posts(uuid: UUID) -> list[Post]:
        value = DBManager.execute("SELECT * FROM posts", ())
        return [Post.from_db(row) for row in value]
