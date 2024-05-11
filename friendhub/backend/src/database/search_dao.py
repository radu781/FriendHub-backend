from datetime import datetime

import logger
from database.dbmanager import DBManager
from models.page_group_model import PageGroup
from models.page_model import Page
from models.post_model import Post
from models.user_model import User


class SearchDAO:
    @staticmethod
    def search_name(prompt: str, max_: int) -> list[User]:
        value = DBManager.execute(
            """
        SELECT
          *
        FROM
          users
        ORDER BY
          LEAST(
            levenshtein_distance(%s, first_name),
            levenshtein_distance(%s, middle_name),
            levenshtein_distance(%s, last_name)
          )
        LIMIT %s
        """,
            (prompt, prompt, prompt, max_),
        )
        out: list[User] = []
        for user in value:
            out.append(User.from_db(user))
        return out

    @staticmethod
    def search_profile_description(prompt: str, max_: int) -> list[User]:
        return []

    @staticmethod
    def search_page(prompt: str, max_: int) -> list[Page]:
        value = DBManager.execute(
            """
        SELECT
          *
        FROM
          pages
        ORDER BY
          LEAST(levenshtein_distance (%s, name))
        LIMIT %s
        """,
            (prompt, max_),
        )
        out: list[Page] = []
        for pg in value:
            out.append(Page.from_db(pg))

        logger.debug(str(out))
        return out

    @staticmethod
    def search_page_description(prompt: str, max_: int) -> list[Page]:
        return []

    @staticmethod
    def search_groups(prompt: str, max_: int) -> list[PageGroup]:
        value = DBManager.execute(
            """
        SELECT
          *
        FROM
          pages_groups
        ORDER BY
          LEAST(levenshtein_distance (%s, name))
        LIMIT %s
        """,
            (prompt, max_),
        )
        out: list[PageGroup] = []
        for pg in value:
            out.append(PageGroup.from_db(pg))
        return out

    @staticmethod
    def search_group_description(prompt: str, max_: int) -> list[PageGroup]:
        return []

    @staticmethod
    def search_posts(
        prompt: str,
        max_: int,
        after: datetime,
        before: datetime,
        has_image: bool,
        has_video: bool,
        has_audio: bool,
    ) -> list[Post]:
        value = DBManager.execute(
            """
        SELECT
          *
        FROM
          posts
        WHERE
          create_time >= %s AND create_time <= %s
          AND (posts.image is not null) = %s
          AND (posts.video is not null) = %s
          AND (posts.audio is not null) = %s
        ORDER BY
          LEAST(levenshtein_distance (%s, text))
        LIMIT %s
        """,
            (after, before, has_image, has_video, has_audio, prompt, max_),
        )
        out: list[Post] = []
        for pg in value:
            out.append(Post.from_db(pg))
        return out
