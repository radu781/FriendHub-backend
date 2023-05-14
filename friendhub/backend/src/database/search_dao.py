from database.dbmanager import DBManager
from models.user_model import User
from models.page_model import Page


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
    def search_page(prompt: str, max_: int) -> list[Page]:
        return []
