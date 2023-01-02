from configparser import ConfigParser
from dataclasses import dataclass, field
from datetime import datetime

import config_keys
import psycopg2
import psycopg2.extensions


@dataclass
class __DBManager:
    NO_COMMIT_OPERATIONS = ["SELECT", "DESC"]
    NO_FETCH_OPERATIONS = ["INSERT", "DELETE"]
    cursor: psycopg2.extensions.cursor = field(init=False)

    def __post_init__(self) -> None:
        ini_file = ConfigParser()
        ini_file.read("config/data.ini")
        self.__restart_connection()

    def __restart_connection(self) -> None:
        if hasattr(self, "cursor") and not self.cursor:
            self.cursor.close()
        self.connector = psycopg2.connect(
            database=config_keys.DB_SCHEMA,
            user=config_keys.DB_USERNAME,
            password=config_keys.DB_PASSWORD,
            host=config_keys.DB_HOST,
            port=config_keys.DB_PORT,
        )
        self.cursor = self.connector.cursor()

    def execute(
        self, statement: str, values: tuple[int | str | datetime | None, ...]
    ) -> list[tuple]:
        statement = statement.replace("\n", " ").replace("  ", " ")
        try:
            self.cursor.execute(statement, values)
            if not statement.split(" ")[0].upper() in self.NO_COMMIT_OPERATIONS:
                self.connector.commit()
            if statement.split(" ")[0].upper() in self.NO_FETCH_OPERATIONS:
                return []
            return self.cursor.fetchall()
        except psycopg2.Error as ex:
            print(
                f"PostgreSQL error: {ex}, statement: {statement.replace('  ', ' ')}, "
                f"args: {[str(val).strip() for val in values]}"
            )
            if isinstance(ex, psycopg2.OperationalError):
                print("Restarting PostgreSQL connection")
                self.__restart_connection()
            return []

    def execute_multiple(
        self, statement: str, values: list[tuple[int | str | datetime | None, ...]]
    ) -> list[list[tuple[int | str]]]:
        out: list[list[tuple[int | str]]] = []

        for value in values:
            out.append(self.execute(statement, value))

        return out


DBManager = __DBManager()
